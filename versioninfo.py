from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Union


class ReleaseLevel(Enum):
    alpha = "alpha"
    beta = "beta"
    release = "release"


@dataclass
class VersionInfo:
    major: int
    minor: int = field(default=0)
    micro: int = field(default=0)
    releaselevel: ReleaseLevel = field(
        default=ReleaseLevel.release, init=False)
    serial: Union[int, None] = field(default=None, init=False)
    name: Union[str, None] = field(default=None, init=False)

    def __repr__(self) -> str:
        if self.releaselevel == ReleaseLevel.release:
            return f"""<{self.__class__.__name__}{"" if not self.name else f" of '{self.name}'"} major={self.major}, minor={self.minor}, micro={self.micro}>"""
        elif self.releaselevel == ReleaseLevel.beta:
            if self.serial:
                return f"""<{self.__class__.__name__}{"" if not self.name else f" of '{self.name}'"} major={self.major}, minor={self.minor}, micro={self.micro}, releaselevel=beta, serial={self.serial}>"""
            else:
                return f"""<{self.__class__.__name__}{"" if not self.name else f" of '{self.name}'"} major={self.major}, minor={self.minor}, micro={self.micro}, releaselevel=beta>"""
        elif self.releaselevel == ReleaseLevel.alpha:
            if self.serial:
                return f"""<{self.__class__.__name__}{"" if not self.name else f" of '{self.name}'"} major={self.major}, minor={self.minor}, micro={self.micro}, releaselevel=alpha, serial={self.serial}>"""
            else:
                return f"""<{self.__class__.__name__}{"" if not self.name else f" of '{self.name}'"} major={self.major}, minor={self.minor}, micro={self.micro}, releaselevel=alpha>"""

    def __getitem__(self, __name: str):
        "x.__getitem__(y) <==> x[y]"
        return self.__dict__.__getitem__(__name)

    def to_tuple(self) -> tuple[Union[str, None], int, int, int, ReleaseLevel, Union[int, None]]:
        return (self.name, self.major, self.minor, self.micro, self.releaselevel.value, self.serial)

    def to_dict(self) -> dict[str, Any]:
        return dict(name=self.name, major=self.major, minor=self.minor, micro=self.micro, releaselevel=self.releaselevel.value, serial=self.serial)

    def set_releaselevel(self, releaselevel: ReleaseLevel, serial: Union[int, None] = None):
        "Set a release level for the package/library/class"
        if not isinstance(releaselevel, ReleaseLevel):
            raise TypeError(
                f"'releaselevel' must be an instance of 'ReleaseLevel' not of '{type(releaselevel).__name__}'")
        if not isinstance(serial, int) and not isinstance(serial, type(None)):
            raise TypeError("'serial' may only be an int or None")
        self.releaselevel = releaselevel
        self.serial = serial
        return self

    def set_name(self, __name: str):
        "Set the name of the package/library/class"
        if not isinstance(__name, str):
            raise TypeError("'name' may only be of type 'str'")
        if __name == "":
            raise ValueError("'name' can't be an empty string")
        self.name = __name
        return self