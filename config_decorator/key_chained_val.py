# -*- coding: utf-8 -*-

# Part of project: https://github.com/hotoffthehamster/config-decorator
# Copyright © 2019 Landon Bouma. All rights reserved.
#
# This program is free software:  you can redistribute it and/or modify
# it  under  the  terms  of  the  GNU Affero General Public License  as
# published by the  Free Software Foundation, either  version 3  of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY;  without even the implied warranty of
# MERCHANTABILITY or  FITNESS FOR A PARTICULAR PURPOSE.  See  the
# GNU   Affero   General   Public   License   for   more  details.
#
# If you lost the GNU Affero General Public License that ships with
# this code (the 'LICENSE' file), see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, unicode_literals

from gettext import gettext as _

import os

__all__ = (
    'KeyChainedValue',
)


class KeyChainedValue(object):
    _envvar_prefix = ''

    def __init__(
        self,
        section=None,
        name='',
        default_f=None,
        value_type=None,
        allow_none=False,
        # Optional.
        choices='',
        doc='',
        ephemeral=False,
        hidden=False,
        validate=None,
    ):
        self._section = section
        self._name = name
        self._default_f = default_f
        self._choices = choices
        self._doc = doc
        self._ephemeral = ephemeral
        self._hidden = hidden
        self._validate_f = validate

        self._value_type = self.deduce_value_type(value_type)
        self._value_allow_none = allow_none

        # These attributes will only be set if some particular
        # source specifies a value:
        #  self._val_forced
        #  self._val_cliarg
        #  self._val_envvar
        #  self._val_config

    @property
    def name(self):
        return self._name

    @property
    def default(self):
        return self._default_f(self._section)

    def deduce_value_type(self, value_type=None):
        if value_type is not None:
            return value_type
        elif self.ephemeral:
            return lambda val: val
        return self.deduce_default_type()

    def deduce_default_type(self):
        default_value = self.default
        if default_value is None:
            return lambda val: val
        elif isinstance(default_value, bool):
            return bool
        elif isinstance(default_value, int):
            return int
        elif isinstance(default_value, list):
            # Because ConfigObj auto-detects list-like values,
            # we might get a string value in a list-type setting,
            # which we don't want to ['s', 'p', 'l', 'i', 't'].
            # So rather than a blind:
            #   return list
            # we gotta be smarter.
            return self._typify_list
        elif isinstance(default_value, str):
            return str
        # We could default to, say, str, or we could nag user to either
        # add another `elif` here, or to fix their default return value.
        raise NotImplementedError

    @property
    def doc(self):
        return self._doc

    @property
    def ephemeral(self):
        if callable(self._ephemeral):
            if self._section is None:
                return False
            return self._ephemeral(self)
        return self._ephemeral

    def _find_root(self):
        return self._section._find_root()

    @property
    def hidden(self):
        if callable(self._hidden):
            if self._section is None:
                # FIXME/2019-12-23: (lb): I think this is unreachable,
                # because self._section is only None when config is
                # being built, but hidden not called during that time.
                return False
            return self._hidden(self)
        return self._hidden

    @property
    def persisted(self):
        return hasattr(self, '_val_config')

    def _typify(self, value):
        if self._value_allow_none and value is None:
            return value
        if self._value_type is bool:
            if isinstance(value, bool):
                return value
            elif value == 'True':
                return True
            elif value == 'False':
                return False
            else:
                raise ValueError(
                    _("Unrecognized string for bool setting ‘{}’: “{}”").format(
                        self._name, value,
                    ),
                )
        return self._value_type(value)

    def _typify_list(self, value):
        # Handle ConfigObj parsing a string without finding commas to
        # split on, but the @setting indicating it's a list; or a
        # default method returning [] so we avoid calling list([]).
        if isinstance(value, list):
            return value
        return [value]

    def _walk(self, visitor):
        visitor(self._section, self)

    # ***

    @property
    def value(self):
        # Honor forced values foremost.
        try:
            return self.value_from_forced
        except AttributeError:
            pass
        # Honor CLI-specific values secondmost.
        try:
            return self.value_from_cliarg
        except AttributeError:
            pass
        # Check the environment third.
        try:
            return self.value_from_envvar
        except KeyError:
            pass
        # See if the config value was specified by the config that was read.
        try:
            return self.value_from_config
        except AttributeError:
            pass
        # Nothing found so far! Finally just return the default value.
        return self._typify(self.default)

    @value.setter
    def value(self, value):
        value = self.value_cast_and_validate(value)
        # Using the `value =` shortcut, or using `section['key'] = `,
        # is provided as a convenient way to inject values from the
        # config file, or that the user wishes to set in the file.
        # If the caller wants to just override the value, consider
        # setting self.value_from_forced instead.
        self.value_from_config = value

    def value_cast_and_validate(self, value):
        value = self._typify(value)
        invalid = False
        addendum = ''
        if self._validate_f:
            if not self._validate_f(value):
                invalid = True
        elif self._choices:
            if value not in self._choices:
                invalid = True
                addendum = _(' (Choose from: ‘{}’)').format('’, ‘'.join(self._choices))
        if invalid:
            raise ValueError(
                _("Unrecognized value for setting ‘{}’: “{}”{}").format(
                    self._name, value, addendum,
                ),
            )
        return value

    # ***

    @property
    def value_from_forced(self):
        return self._val_forced

    @value_from_forced.setter
    def value_from_forced(self, value_from_forced):
        self._val_forced = self._typify(value_from_forced)

    # ***

    @property
    def value_from_cliarg(self):
        return self._val_cliarg

    @value_from_cliarg.setter
    def value_from_cliarg(self, value_from_cliarg):
        self._val_cliarg = self._typify(value_from_cliarg)

    # ***

    @property
    def value_from_envvar(self):
        environame = '{}{}_{}'.format(
            KeyChainedValue._envvar_prefix,
            self._section._section_path(sep='_').upper(),
            self._name.upper(),
        )
        envval = os.environ[environame]
        envval = self.value_cast_and_validate(envval)
        return envval

    # ***

    @property
    def value_from_config(self):
        return self._val_config

    @value_from_config.setter
    def value_from_config(self, value_from_config):
        self._val_config = self._typify(value_from_config)

    def forget_config_value(self):
        try:
            del self._val_config
        except AttributeError:
            pass


