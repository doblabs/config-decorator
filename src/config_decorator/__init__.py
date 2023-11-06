# vim:tw=0:ts=4:sw=4:et:norl
# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/config-decorator#🎀
# License: MIT
# Copyright © 2019-2020 Landon Bouma. All rights reserved.

"""Root module package-level alias to :func:`config_decorator.config_decorator.section`.

- So you can call, e.g.,

  .. code-block:: python

      from config_decorator import section

  instead of

  .. code-block:: python

      from config_decorator.config_decorator import section
"""

from .config_decorator import section, ConfigDecorator
from .key_chained_val import KeyChainedValue

__all__ = (
    'section',
    'ConfigDecorator',
    'KeyChainedValue',
)
