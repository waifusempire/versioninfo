from __future__ import annotations
import attrs
from enum import Enum
from typing import Any, TypedDict


class VersionInfoDict(TypedDict):
    name: str
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int


def handle_attr(__cls: VersionInfo, __attr: attrs.Attribute, __value: object):
    raise attrs.exceptions.FrozenAttributeError(
        f"Unable modify frozen attribute '{__attr.name}'")


class ReleaseLevel(Enum):
    alpha = "alpha"
    beta = "beta"
    final = "final"
    release = "release"


@attrs.define(repr=False, slots=True, str=False, init=True)
class VersionInfo:
    name: str = attrs.field(converter=str, on_setattr=handle_attr, init=True)
    major: int = attrs.field(converter=int, on_setattr=handle_attr, init=True)
    minor: int = attrs.field(default=0, converter=int,
                             on_setattr=handle_attr, init=True)
    micro: int = attrs.field(default=0, converter=int,
                             on_setattr=handle_attr, init=True)
    releaselevel: ReleaseLevel = attrs.field(
        default=ReleaseLevel.final, validator=attrs.validators.instance_of(ReleaseLevel), on_setattr=handle_attr, init=True)
    serial: int = attrs.field(default=0, converter=int,
                              on_setattr=handle_attr, init=True)

    def __repr__(self) -> str:
        name = self.name
        major = self.major
        minor = self.minor
        micro = self.micro
        releaselevel = self.releaselevel
        serial = self.serial
        repr_str = f"VersionInfo({name=}, {major=}, {minor=}, {micro=}, releaselevel={str(releaselevel)}, {serial=})"
        return repr_str

    def to_dict(self) -> VersionInfoDict:
        return VersionInfoDict(name=self.name, major=self.major, minor=self.minor, micro=self.micro, releaselevel=self.releaselevel.value, serial=self.serial)

    def to_version_string(self):
        "name==A.B.CXY"
        if self.releaselevel == ReleaseLevel.final:
            s = f"{self.name}=={self.major}.{self.minor}.{self.micro}"
        elif self.releaselevel == ReleaseLevel.beta:
            s = f"{self.name}=={self.major}.{self.minor}.{self.micro}b{'' if not self.serial else self.serial}"
        elif self.releaselevel == ReleaseLevel.alpha:
            s = f"{self.name}=={self.major}.{self.minor}.{self.micro}a{'' if not self.serial else self.serial}"
        elif self.releaselevel == ReleaseLevel.release:
            s = f"{self.name}=={self.major}.{self.minor}.{self.micro}rc{'' if not self.serial else self.serial}"
        else:
            s = ""
        return s

    def to_vstring(self):
        "vA.B.CXY"
        s = f"v{self.major}.{self.minor}.{self.micro}"
        if self.releaselevel == ReleaseLevel.final:
            pass
        elif self.releaselevel == ReleaseLevel.release:
            s += "rc{s}".format(s=self.serial) if self.serial else "rc"
        elif self.releaselevel == ReleaseLevel.beta:
            s += "b{s}".format(s=self.serial) if self.serial else "b"
        elif self.releaselevel == ReleaseLevel.alpha:
            s += "a{s}".format(s=self.serial) if self.serial else "a"
        else:
            pass
        return s


__all__ = ["ReleaseLevel", "VersionInfo"]