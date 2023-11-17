# vim:tw=0:ts=4:sw=4:et:norl
# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/config-decorator#🎀
# License: MIT
# Copyright © 2019-2020 Landon Bouma. All rights reserved.

import os
from collections import OrderedDict

import pytest

from config_decorator import section
from config_decorator.config_decorator import ConfigDecorator
from config_decorator.key_chained_val import KeyChainedValue

KeyChainedValue._envvar_prefix = "TEST_"

REAL_OPTION_NAME_VALUE = "Test train-case setting and snake_case default fcn"


def generate_config_root():
    @section(None)
    class RootSection(object):
        def inner_function(self):
            return "foo"

    # ***

    @RootSection.section(None)
    class RootSectionOverlay(object):
        def __init__(self):
            pass

        # ***

        @property
        @RootSection.setting(
            "Hidden test.",
            hidden=True,
        )
        def inner_function(self):
            return RootSection._innerobj.inner_function()

        # ***

        @property
        @RootSection.setting(
            "Hidden test, too.",
            hidden=lambda x: True,
        )
        def callable_hidden_test(self):
            return ""

        # ***

        @property
        @RootSection.setting(
            "Choices test.",
            choices=["", "one", "two", "three"],
        )
        def choices_test(self):
            return ""

        # ***

        @property
        @RootSection.setting(
            "Different Name test.",
            name="real-option-name",
        )
        def real_option_name(self):
            return REAL_OPTION_NAME_VALUE

        # ***

        def some_value_conversation(value):
            if isinstance(value, int):
                return value
            return int(value) + 100

        @property
        @RootSection.setting(
            "Value Type test.",
            conform=some_value_conversation,
        )
        def conform_test(self):
            return "1"

        # ***

        @property
        @RootSection.setting(
            "Allow None test.",
            value_type=bool,
            allow_none=True,
        )
        def allow_none_test(self):
            return None

        # ***

        @property
        @RootSection.setting(
            "Default value None test.",
        )
        def default_value_none_test(self):
            return None

        # ***

        @property
        @RootSection.setting(
            "Default value bool test.",
        )
        def default_value_bool_test(self):
            return True

        # ***

        @property
        @RootSection.setting(
            "Default value int test.",
        )
        def default_value_int_test(self):
            return 123

        # ***

        @property
        @RootSection.setting(
            "Default value list test, implicit.",
        )
        def default_value_list_test_implicit(self):
            return [1, "foo"]

        @property
        @RootSection.setting(
            "Default value list test, explicit.",
            allow_none=True,
            value_type=list,
        )
        def default_value_list_test_explicit(self):
            return None

        # ***

        @property
        @RootSection.setting(
            "Default value are test.",
        )
        def default_value_str_test(self):
            return ""

        # ***

        @property
        @RootSection.setting(
            "Ephemeral test.",
            ephemeral=True,
        )
        def ephemeral_test(self):
            return "This will not be saved!"

        # ***

        @property
        @RootSection.setting(
            "Callable Ephemeral test.",
            ephemeral=lambda x: True,
        )
        def callable_ephemeral_test(self):
            return "Neither will this be saved."

        # ***

        def must_validate_foo(some_value):
            return some_value

        @property
        @RootSection.setting(
            "Validate pass test.",
            validate=must_validate_foo,
        )
        def pass_validate_test(self):
            return "This will be validated!"

        # ***

        def validate_true(some_value):
            return True

        @property
        @RootSection.setting(
            "Validate okay test.",
            validate=validate_true,
        )
        def validate_okay_test(self):
            return None

        # ***

        @property
        @RootSection.setting(
            "Validate bool string test, false.",
            value_type=bool,
        )
        def validate_bool_string_false_test(self):
            return "False"

        @property
        @RootSection.setting(
            "Validate bool string test, true.",
            value_type=bool,
        )
        def validate_bool_string_true_test(self):
            return "True"

    # ***

    @RootSection.section("level1")
    class RootSectionLevel1(object):
        def __init__(self):
            pass

        @property
        @RootSection.setting(
            "Test sub config setting, level1.foo",
        )
        def foo(self):
            return "baz"

        @property
        @RootSection.setting(
            "Test same-named settings in separate sections",
        )
        def conflict(self):
            return "level1"

    # ***

    @RootSectionLevel1.section("level2")
    class RootSectionLevel2(object):
        def __init__(self):
            pass

        @property
        @RootSectionLevel1.setting(
            "Test sub sub config setting, level1.level2.bar",
        )
        def baz(self):
            return "bat"

        @property
        @RootSectionLevel1.setting(
            "Test same-named settings in separate sections",
        )
        def conflict(self):
            return "level2"

    # ***

    @RootSection.section("level1.2")
    class RootSectionLevel1dot2TestsDownloadToDictDelConfigSection(object):
        def __init__(self):
            pass

    # ***

    @RootSection.section("unstructured")
    class RootSectionUnstructured(object):
        def __init__(self, *args, **kwargs):
            pass

    # SAVVY: Dot-notation won't work here, because Python keyword, e.g.,
    #   (Pdbr) rootcfg.asobj.unstructured.None
    #   *** SyntaxError: invalid syntax
    # Whereas dictionary lookup still works, e.g.,:
    #   (Pdbr) self.rootcfg['unstructured']['None'].as_dict()
    #   {...}
    # Just FYI re: section names and dot-notation limitations.
    @RootSectionUnstructured.section("None", default_value_type=None)
    class RootSectionUnstructuredNone(object):
        def __init__(self, *args, **kwargs):
            pass

    @RootSectionUnstructured.section("bool", default_value_type=bool)
    class RootSectionUnstructuredBool(object):
        def __init__(self, *args, **kwargs):
            pass

    @RootSectionUnstructured.section("int", default_value_type=int)
    class RootSectionUnstructuredInt(object):
        def __init__(self, *args, **kwargs):
            pass

    @RootSectionUnstructured.section("list", default_value_type=list)
    class RootSectionUnstructuredList(object):
        def __init__(self, *args, **kwargs):
            pass

    @RootSectionUnstructured.section("str", default_value_type=str)
    class RootSectionUnstructuredStr(object):
        def __init__(self, *args, **kwargs):
            pass

    @RootSectionUnstructured.section("object", default_value_type=object)
    class RootSectionUnstructuredObject(object):
        def __init__(self, *args, **kwargs):
            pass

    @RootSectionUnstructured.section("identity", default_value_type=lambda x: x)
    class RootSectionUnstructuredIdentity(object):
        def __init__(self, *args, **kwargs):
            pass

    # ***

    @RootSectionUnstructured.section(
        "boolOrNone",
        default_value_type=bool,
        default_allow_none=True,
    )
    class RootSectionUnstructuredBoolOrNone(object):
        def __init__(self, *args, **kwargs):
            pass

    # ***

    @RootSection.section("train-case")
    class RootSectionTrainCase(object):
        def __init__(self):
            pass

        @property
        @RootSection.setting(
            "Test train-case/snake_case setting",
        )
        def foo_bar(self):
            return "foo_bar"

        @property
        @RootSection.setting(
            "Test train-case/snake_case setting",
            name="baz-bat",
        )
        def baz_bat(self):
            return "baz_bat"

    # ***

    return RootSection


# ***


class TestConfigDecoratorAsDict:
    def test_something(self):
        rootcfg = generate_config_root()
        assert isinstance(rootcfg, ConfigDecorator)
        assert isinstance(rootcfg._innerobj, object)
        _settings = rootcfg.as_dict()  # noqa: F841: var never used


# ***


class TestConfigDecoratorSetDefault:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.setdefault("totally-unknown-key", 123)
        rootcfg.setdefault("totally-unknown-key.subsection.too", False)
        rootcfg.setdefault("level1.foo", "exercise different branch on known sub key")
        with pytest.raises(TypeError):
            rootcfg.setdefault("missing.value")


# ***


class TestConfigDecoratorKeysValuesItems:
    def test_config_decorator_keys(self):
        rootcfg = generate_config_root()
        _keys = rootcfg.keys()  # noqa: F841: var never used
        # sorted(list(keys)) is the names of the settings tests above, e.g.,
        #   ['allow_none_test', 'choices_test', 'ephemeral_test', etc.]

    def test_config_decorator_values(self):
        rootcfg = generate_config_root()
        _values = rootcfg.values()  # noqa: F841: var never used
        # values is the default values of the settings tests above, e.g.,
        #   ['foo', '', '', 101, None, 'This will not be saved!', etc.]

    def test_config_decorator_items(self):
        rootcfg = generate_config_root()
        _items = rootcfg.items()  # noqa: F841: var never used


# ***


class TestConfigDecoratorAttributeMagic:
    def test_something(self):
        rootcfg = generate_config_root()
        assert rootcfg.asobj.level1.level2.baz.value == "bat"


class TestConfigDecoratorSubscriptability:
    def test_something(self):
        rootcfg = generate_config_root()
        assert rootcfg["level1"]["level2"]["baz"] == "bat"


# ***


class TestConfigDecoratorFindAllManyParts:
    def test_something(self):
        rootcfg = generate_config_root()
        settings = rootcfg.find_all(["level1", "level2", "baz"])
        assert settings[0].value == "bat"


class TestConfigDecoratorFindAllNoPartsSelf:
    def test_something(self):
        rootcfg = generate_config_root()
        settings = rootcfg.find_all(parts=[])
        assert settings == [rootcfg]


class TestConfigDecoratorFindSection:
    def test_something(self):
        rootcfg = generate_config_root()
        settings = rootcfg.find_all(parts=["level1", "level2"])
        assert len(settings) == 1
        assert settings[0] is rootcfg["level1"]["level2"]


# ***


class TestConfigDecoratorFindRoot:
    def test_something(self):
        rootcfg = generate_config_root()
        assert rootcfg["level1"].find_root() is rootcfg
        rootcfg = generate_config_root()
        assert rootcfg["level1"].asobj.foo.find_root() is rootcfg


# ***


class TestConfigDecoratorSectionPath:
    def test_something(self):
        rootcfg = generate_config_root()
        assert rootcfg.asobj.level1.level2._.section_path() == "level1.level2"
        assert rootcfg.asobj.level1.level2._.section_path("_") == "level1_level2"


# ***


class TestConfigDecoratorForgetfulWalk:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.forget_config_values()


# ***


class TestConfigDecoratorSetAttributeValueBool:
    def test_one_way(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.validate_bool_string_false_test.value = True

    def test_or_the_other(self):
        rootcfg = generate_config_root()
        rootcfg["validate_bool_string_false_test"] = False


# ***


class TestConfigDecoratorSetAttributeValueString:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg["level1.foo"] = "zab"


# ***


class TestConfigDecoratorSetAttributeValueList:
    def test_default_value_list_test_implicit(self):
        rootcfg = generate_config_root()
        rootcfg["default_value_list_test_implicit"] = 123
        assert rootcfg["default_value_list_test_implicit"] == [
            123,
        ]

    def test_default_value_list_test_explicit(self):
        rootcfg = generate_config_root()
        rootcfg["default_value_list_test_explicit"] = "abc123"
        assert rootcfg["default_value_list_test_explicit"] == [
            "abc123",
        ]


# ***


class TestConfigDecoratorSetSubscriptableVague:
    def test_something(self):
        rootcfg = generate_config_root()
        # KeyError: 'More than one config object named: “conflict”'
        with pytest.raises(KeyError):
            rootcfg["conflict"] = "zab"


# ***


class TestConfigDecoratorGetAttributeError:
    def test_something(self):
        rootcfg = generate_config_root()
        with pytest.raises(AttributeError):
            # AttributeError: 'More than one config object named: “conflict”'
            rootcfg.conflict
        # However, setting an unknown key works just fine.
        rootcfg.conflict = "zab"
        # FIXME/2019-12-23: (lb): Remove attribute magic, or maybe gait
        # through an intermediate attribute, e.g.,, rootcfg.settings.conflict.


# ***


class TestConfigDecoratorDownloadToDict:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.level1.level2.baz.value_from_config = (
            "test: return ckv.value_from_config"
        )
        cfgdict = {}
        rootcfg.apply_items(cfgdict)
        assert cfgdict == rootcfg.as_dict(unmutated=True)


# ***


class TestConfigDecoratorUpdateKnown:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.level1.level2.baz.value_from_config = (
            "test: return ckv.value_from_config"
        )
        cfgdict = {
            "level1": {
                "level2": {"baz": "zab"},
                "unknown": "unconsumed",
            }
        }

        _unconsumed, _errs = rootcfg.update_known(cfgdict)  # noqa: F841: var never used

        assert rootcfg.asobj.level1.level2.baz.value == "zab"
        assert rootcfg["level1"]["level2"]["baz"] == "zab"
        with pytest.raises(AttributeError):
            rootcfg["level1"]["unknown"]
        assert _unconsumed["level1"]["unknown"] == "unconsumed"


# ***


class TestConfigDecoratorUpdateGrossAkaUnstructured:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.level1.level2.baz.value_from_config = (
            "test: return ckv.value_from_config"
        )
        cfgdict = {
            "level1.level2.baz": "zab",
            "level1.level2.unknown": "consumed",
        }

        # Call update(), which calls update_gross(), for more coverage.
        # - update_gross is a more inclusive update_known.
        rootcfg.update(cfgdict)

        assert rootcfg.asobj.level1.level2.baz.value == "zab"
        assert rootcfg["level1"]["level2"]["baz"] == "zab"
        assert rootcfg.asobj.level1.level2.unknown.value == "consumed"
        assert rootcfg["level1"]["level2"]["unknown"] == "consumed"


# ***


class TestConfigDecoratorUnstructuredDefaultValueTypes:
    rootcfg = generate_config_root()

    def test_unstructured_default_value_type_None(self):
        none_at_all = "None treats values as str"
        cfgdict = {"unstructured.None.my_key_None": none_at_all}
        self.rootcfg.update(cfgdict)
        assert self.rootcfg["unstructured"]["None"]["my_key_None"] == none_at_all

        nothing = None
        cfgdict = {"unstructured.None.my_key_None": nothing}
        with pytest.raises(ValueError):
            self.rootcfg.update(cfgdict)

    def test_unstructured_default_value_type_bool(self):
        cfgdict = {"unstructured.bool.my_key_bool": "this_is_not_a_bool"}
        with pytest.raises(ValueError):
            self.rootcfg.update(cfgdict)

        cfgdict = {"unstructured.bool.my_key_bool": "True"}
        self.rootcfg.update(cfgdict)
        assert self.rootcfg["unstructured"]["bool"]["my_key_bool"] is True

    def test_unstructured_default_value_type_int(self):
        cfgdict = {"unstructured.int.my_key_int": "this_is_not_a_int"}
        with pytest.raises(ValueError):
            self.rootcfg.update(cfgdict)

        cfgdict = {"unstructured.int.my_key_int": "123"}
        self.rootcfg.update(cfgdict)
        assert self.rootcfg["unstructured"]["int"]["my_key_int"] == 123

    def test_unstructured_default_value_type_list_single_item_int(self):
        cfgdict = {"unstructured.list.my_key_list": 123}
        self.rootcfg.update(cfgdict)
        assert self.rootcfg["unstructured"]["list"]["my_key_list"] == [123]

    def test_unstructured_default_value_type_list_single_item_str(self):
        just_the_one = "this is a single item list"
        cfgdict = {"unstructured.list.my_key_list": just_the_one}
        self.rootcfg.update(cfgdict)
        assert self.rootcfg["unstructured"]["list"]["my_key_list"] == [just_the_one]

    def test_unstructured_default_value_type_list_actual_list(self):
        four_on_the_floor = ["this", "list", "has four", "comma-separated items"]
        cfgdict = {"unstructured.list.my_key_list": four_on_the_floor}
        self.rootcfg.update(cfgdict)
        assert self.rootcfg["unstructured"]["list"]["my_key_list"] == four_on_the_floor

    def test_unstructured_default_value_type_str(self):
        its_true = "everything's a string"
        cfgdict = {"unstructured.str.my_key_str": its_true}
        self.rootcfg.update(cfgdict)
        assert self.rootcfg["unstructured"]["str"]["my_key_str"] == its_true

    def test_unstructured_default_value_type_str_level2(self):
        its_true = "everything's a string"
        cfgdict = {"unstructured.str.level2.my_key_str_level2": its_true}
        self.rootcfg.update(cfgdict)
        assert (
            self.rootcfg["unstructured"]["str"]["level2"]["my_key_str_level2"]
            == its_true
        )

    # These 2 tests are not how people would use the class, but demonstrate
    # its (absurd?) flexibility, also tests "unexpected" usage.

    def test_unstructured_default_value_type_object(self):
        some_obj = object()
        cfgdict = {"unstructured.object.my_key_object": some_obj}
        with pytest.raises(ValueError):
            self.rootcfg.update(cfgdict)

    def test_unstructured_default_value_type_object_level2(self):
        some_obj = object()
        cfgdict = {"unstructured.object.level2.my_key_object": some_obj}
        self.rootcfg.update(cfgdict)
        assert self.rootcfg["unstructured"]["object"]["level2"]["my_key_object"] == str(
            some_obj
        )

    # Allow None, without a default_f (rare, but completes coverage).

    def test_unstructured_default_value_type_bool_or_none(self):
        cfgdict = {
            "unstructured.boolOrNone.my_key_bool_none": None,
            "unstructured.boolOrNone.my_key_bool_true": True,
        }
        self.rootcfg.update(cfgdict)
        assert self.rootcfg["unstructured"]["boolOrNone"]["my_key_bool_none"] is None
        assert self.rootcfg["unstructured"]["boolOrNone"]["my_key_bool_true"] is True


# ***


class TestConfigDecoratorKeyChainedValueSource:
    def test_something(self):
        rootcfg = generate_config_root()
        assert rootcfg.asobj.level1.foo.source == "default"
        assert rootcfg.asobj.level1.foo.value == "baz"

        cfgdict = {"level1": {"foo": "qux"}}
        _unconsumed, _errs = rootcfg.update_known(cfgdict)  # noqa: F841: var never used
        assert rootcfg.asobj.level1.foo.source == "config"
        assert rootcfg.asobj.level1.foo.value == "qux"

        environame = "TEST_LEVEL1_FOO"
        os.environ[environame] = "quux"
        assert rootcfg.asobj.level1.foo.source == "envvar"
        assert rootcfg.asobj.level1.foo.value == "quux"
        del os.environ[environame]

        rootcfg.asobj.level1.foo.value_from_cliarg = "quuz"
        assert rootcfg.asobj.level1.foo.source == "cliarg"
        assert rootcfg.asobj.level1.foo.value == "quuz"

        rootcfg.asobj.level1.foo.value_from_forced = "corge"
        assert rootcfg.asobj.level1.foo.source == "forced"
        assert rootcfg.asobj.level1.foo.value == "corge"


# ***


class TestConfigDecoratorYouveBeenWarned:
    def test_something(self, capsys):
        rootcfg = generate_config_root()
        cfgdict = {"level1": {"foo": "oof"}}

        _unconsumed, _errs = rootcfg.update_known(cfgdict)  # noqa: F841: var never used

        KeyChainedValue._envvar_prefix = ""

        assert rootcfg.asobj.level1.foo.value == "oof"
        out, err = capsys.readouterr()
        assert err == "WARNING: You should set KeyChainedValue._envvar_prefix\n"

        assert rootcfg.asobj.level1.foo.value == "oof"
        out, err = capsys.readouterr()
        assert err == ""

        KeyChainedValue._envvar_prefix = "TEST_"


# ***


class TestConfigDecoratorKeyChainedValueToStr:
    def test_something(self):
        rootcfg = generate_config_root()

        assert (
            str(rootcfg.asobj.real_option_name)
            == f".real-option-name: {REAL_OPTION_NAME_VALUE}"
        )


# ***


class TestConfigDecoratorKeyChainedValueNormalizesCase:
    def test_something(self):
        rootcfg = generate_config_root()

        assert rootcfg["real-option-name"] == REAL_OPTION_NAME_VALUE

        # Because dashes are replaced for dot-notation to work, e.g.,:
        assert rootcfg.asobj.real_option_name.value == REAL_OPTION_NAME_VALUE
        # You can also do similar via dict lookup:
        assert rootcfg["real_option_name"] == REAL_OPTION_NAME_VALUE


# ***


class TestConfigDecoratorConfigDecoratorNormalizesCase:
    def test_something(self):
        rootcfg = generate_config_root()
        assert rootcfg.asobj.train_case.foo_bar.value == "foo_bar"

        cfgdict = {
            "train-case": {
                # Opposite cases of definitions.
                "foo-bar": "baz",  # Defined in config above as foo_bar
                "baz_bat": "quux",  # Defined in config above as baz-bat
            },
        }

        _unconsumed, _errs = rootcfg.update_known(cfgdict)  # noqa: F841: var never used

        assert rootcfg.asobj.train_case.foo_bar.value == "baz"
        assert rootcfg["train-case"]["foo-bar"] == "baz"
        assert rootcfg["train-case"]["foo_bar"] == "baz"

        assert rootcfg.asobj.train_case.baz_bat.value == "quux"
        assert rootcfg["train-case"]["baz-bat"] == "quux"
        assert rootcfg["train-case"]["baz_bat"] == "quux"


# ***


class TestConfigDecoratorConfigDecoratorNormalizesConflicts:
    def test_something(self):
        rootcfg = generate_config_root()
        assert rootcfg.asobj.train_case.foo_bar.value == "foo_bar"

        # Note that same-name different-casing conflicts handled silently.
        sub_cfg_1 = OrderedDict()
        sub_cfg_1["foo-bar"] = "baz_1"
        sub_cfg_1["foo_bar"] = "baz_2"
        sub_cfg_2 = OrderedDict()
        sub_cfg_2["foo-bar"] = "baz_3"
        sub_cfg_2["foo_bar"] = "baz_4"
        cfgdict = OrderedDict()
        cfgdict["train-case"] = sub_cfg_1
        cfgdict["train_case"] = sub_cfg_2

        _unconsumed, _errs = rootcfg.update_known(cfgdict)  # noqa: F841: var never used

        assert rootcfg.asobj.train_case.foo_bar.value == "baz_4"
        assert rootcfg["train-case"]["foo-bar"] == "baz_4"
        assert rootcfg["train-case"]["foo_bar"] == "baz_4"
        assert rootcfg["train_case"]["foo-bar"] == "baz_4"
        assert rootcfg["train_case"]["foo_bar"] == "baz_4"


# ***


class TestConfigDecoratorFindSettingOkay:
    def test_something(self):
        rootcfg = generate_config_root()
        setting = rootcfg.find_setting(["level1", "level2", "baz"])
        assert setting.value == "bat"


class TestConfigDecoratorFindSettingFailOnePart:
    def test_something(self):
        rootcfg = generate_config_root()
        with pytest.raises(KeyError):
            rootcfg.find_setting(["unknown setting"])


class TestConfigDecoratorFindSettingFailManyParts:
    def test_something(self):
        rootcfg = generate_config_root()
        with pytest.raises(KeyError):
            rootcfg.find_setting(["unknown setting", "foo"])


class TestConfigDecoratorFindSettingOnePart:
    def test_something(self):
        rootcfg = generate_config_root()
        setting = rootcfg.find_setting(["conflict"])
        assert setting.value == "level1"


# ***


class TestConfigDecoratorAsobjOkay:
    def test_something(self):
        rootcfg = generate_config_root()
        assert (
            "Test sub sub config setting, level1.level2.bar"
            == rootcfg.asobj.level1.level2.baz.doc
        )


# ***


class TestConfigDecoratorSettingWalk:
    def test_something(self):
        def visitor(section, setting):
            assert section is rootcfg.asobj.level1.level2._

        rootcfg = generate_config_root()
        rootcfg.asobj.level1.level2.baz.walk(visitor)


# ***


class TestConfigDecoratorSettingSetForced:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.level1.level2.baz.value_from_forced = 123


# ***


class TestConfigDecoratorSettingSetCliarg:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.level1.level2.baz.value_from_cliarg = 123


# ***


class TestSectionSettingValidationOkay:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.validate_okay_test.value = 123


# ***


class TestSectionSettingChoicesOkay:
    def test_something(self):
        rootcfg = generate_config_root()
        rootcfg.asobj.choices_test.value = "one"


class TestSectionSettingChoicesFail:
    def test_something(self):
        rootcfg = generate_config_root()
        with pytest.raises(ValueError):
            rootcfg.asobj.choices_test.value = "foo"


# ***


class TestSectionSettingFromEnvvar:
    def test_something(self):
        rootcfg = generate_config_root()

        environame = "TEST_LEVEL1_FOO"
        os.environ[environame] = "zab"
        assert rootcfg.asobj.level1.foo.value == "zab"
        del os.environ[environame]


# ***


class TestSectionSettingPrecedence:
    def test_something(self):
        rootcfg = generate_config_root()
        assert rootcfg.asobj.level1.foo.value == "baz"
        # Note that setting value assumes from config.
        rootcfg.asobj.level1.foo.value = "bat"
        assert rootcfg.asobj.level1.foo.value_from_config == "bat"
        assert rootcfg.asobj.level1.foo.value == "bat"

        environame = "TEST_LEVEL1_FOO"
        os.environ[environame] = "zab"
        assert rootcfg.asobj.level1.foo.value == "zab"
        # Note that int will be converted to setting type, which is string.
        rootcfg.asobj.level1.foo.value_from_cliarg = 123
        assert rootcfg.asobj.level1.foo.value == "123"
        #
        rootcfg.asobj.level1.foo.value_from_forced = "perfect!"
        assert rootcfg.asobj.level1.foo.value == "perfect!"
