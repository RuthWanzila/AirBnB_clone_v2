#!/usr/bin/python3
# Script to delete out-of-date archives.
import os
from fabric.api import *

env.hosts = ["104.196.168.90", "35.196.46.172"]


def delete_outdated_archives(number=0):
    """
    Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If the number is 0 or 1, it keeps only the most recent archive.
    If the number is 2, it keeps the most and second-most recent archives so on
    """
    number = 1 if int(number) == 0 else int(number)

    # Delete local archives
    local_archives = sorted(os.listdir("versions"))
    [local_archives.pop() for _ in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(archive)) for archive in local_archives]

    # Delete remote archives
    with cd("/data/web_static/releases"):
        r_archs = run("ls -tr").split()
        r_archs = [archive for archive in r_archs if "web_static_" in archive]
        [r_archs.pop() for _ in range(number)]
        [run("rm -rf ./{}".format(archive)) for archive in r_archs]
