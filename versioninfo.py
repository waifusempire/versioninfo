from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ReleaseLevel(Enum):
    alpha = "alpha"
    beta = "beta"
    final = "final"
    release = "release"


@dataclass(frozen=True, slots=True)
class VersionInfo:
    name: str
    major: int
    minor: int = field(default=0)
    micro: int = field(default=0)
    releaselevel: ReleaseLevel = field(
        default=ReleaseLevel.final)
    serial: int = field(default=0)

    def __repr__(self) -> str:
        if self.releaselevel == ReleaseLevel.final:
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
        elif self.releaselevel == ReleaseLevel.release:
            if self.serial:
                return f"""<{self.__class__.__name__}{"" if not self.name else f" of '{self.name}'"} major={self.major}, minor={self.minor}, micro={self.micro}, releaselevel=release, serial={self.serial}>"""
            else:
                return f"""<{self.__class__.__name__}{"" if not self.name else f" of '{self.name}'"} major={self.major}, minor={self.minor}, micro={self.micro}, releaselevel=release>"""

    def to_dict(self) -> dict[str, Any]:
        return dict(name=self.name, major=self.major, minor=self.minor, micro=self.micro, releaselevel=self.releaselevel.value, serial=self.serial)

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
            s+="rc{s}".format(s=self.serial)
        elif self.releaselevel == ReleaseLevel.beta:
            s+="b{s}".format(s=self.serial)
        elif self.releaselevel == ReleaseLevel.alpha:
            s+="a{s}".format(s=self.serial)
        else:
            pass
        return s