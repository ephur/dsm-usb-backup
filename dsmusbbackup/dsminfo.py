import os

from dsmusbbackup import util

DSM_VERSION_FILE = "/etc.defaults/VERSION"


def get_version_info(info_file=DSM_VERSION_FILE):
    """
    Get version info from DSM

    Returns a dict containing all of the version related info that DSM provides
    """
    info_dict = dict()
    try:
        with open(info_file, 'r') as ifile:
            for line in ifile:
                (key, val) = line.rstrip("\n").split("=")
                info_dict[key] = val.strip('\"')
    except FileNotFoundError:
        return None
    return info_dict


def get_fs_info(target):
    """
    Returns the filesystem type of the provided file (or directory)

    While this could be done using internal methods, portability is not a concern
    since this is DSM specific, keeping it simple.
    """
    (exit_code, output, error) = util.pipe_exec(
        ["/bin/df -Tk {}".format(target)])
    output = output.decode("utf-8")
    error = error.decode("utf-8")
    if exit_code != 0:
        raise ValueError("df error:EXIT: {}\nSTDOUT:\n{}\nSTDERR:\n{}\n".format(
            exit_code, output, error))

    # Parse output based on columns
    # Filesystem     Type 1M-blocks  Used Available Use% Mounted on
    try:
        (_, fsinfo) = output.splitlines()
    except ValueError as e:
        raise ValueError(
            "Value Error: {} when attempting to parse output:\n{}".format(e, output))

    ri = dict()
    (ri["filesystem"], ri["type"], ri["kb_total"], ri["kb_used"], ri["kb_available"],
     ri["percent"], ri["mountpoint"]) = fsinfo.rstrip("\n").split()
    return ri
