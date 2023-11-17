# vim:tw=0:ts=4:sw=4:et:norl
# Author: Landon Bouma <https://tallybark.com/>
# Project: https://github.com/doblabs/config-decorator#🎀
# License: MIT
# Copyright © 2019-2023 Landon Bouma. All rights reserved.

"""Real powerful stuff."""

__all__ = ("train2snakecase",)


def train2snakecase(name):
    return name.replace("-", "_")
