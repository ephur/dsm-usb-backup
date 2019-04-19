import pprint
import sys
import textwrap

import click

import dsmusbbackup.dsminfo as dsminfo
import dsmusbbackup.backup as dsmbackup


def validate_target(ctx, param, target):
    """
    ensures operations only continue for known ext4 targets

    I don't have a target btrfs drive to test this with, so limiting target drives to ext4.
    """
    try:
        if dsminfo.get_fs_info(target)["type"] != "ext4":
            click.secho(
                "{} does not appear to be an ext4 filesystem, unable to continue".format(
                    target), err=True, fg="red")
            sys.exit(2)
    except ValueError as e:
        click.secho("Got exception while trying to validate target filesystem:\n{}".format(
            textwrap.indent(str(e), '    ')), err=True, fg="red")
        sys.exit(2)
    return target


def validate_version(ctx, param, skip_check):
    tested_versions = [
        "6.2.1"
    ]
    if skip_check is True:
        return None
    version_info = dsminfo.get_version_info()
    if version_info is None:
        click.secho(
            "Unable to get version info! Not continuing without force.", err=True, fg="red")
        sys.exit(2)

    if version_info["productversion"] not in tested_versions:
        click.secho("Not validated with version {} of DSM! Not continuing without force.".format(
            version_info["productversion"]), err=True, fg="red")
        sys.exit(2)


"""
Options:


patterns to ignore (rsync compatible ignore patterns)

"""
@click.command()
@click.option("-s", "--source", "source", multiple=True, envvar="DUB_SOURCE",
              type=click.Path(exists=True), required=True,
              help="Source path, can be provided multiple times")
@click.option("-t", "--target", "target", envvar="DUB_TARGET",
              type=click.Path(exists=True), required=True, callback=validate_target,
              help="Target path (must be on ext4 file system)")
@click.option("-r", "--retain", default=7, help="number of backup copies to retain", envvar="DUB_RETAIN")
@click.option("--skip-version-check/--no-skip-version-check", envvar="DUB_SKIP_VERSION_CHECK",
              default=False, help="skip DSM version compatibility check", callback=validate_version)
def main(source, target, retain, skip_version_check):
    backup = dsmbackup.Backup(target)
    for s in source:
        backup.sync(s)
