"""Version Info Helper

Example:
>>> version_info = VersionInfo('str', 1, 2, 3)
>>> print(version_info)
<VersionInfo of 'str' major=1 minor=2 micro=3>"""


from .versioninfo import VersionInfo, ReleaseLevel


__version__ = "2.0.0"
__author__ = "waifusempire"
version_info = VersionInfo("versioninfo", 2, 0, 0)


__all__ = ["VersionInfo", "ReleaseLevel"]