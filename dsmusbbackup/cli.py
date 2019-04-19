import pprint
import sys
import textwrap

import click

import dsmusbbackup.dsminfo as dsminfo


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
    return


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

ACCEPT ALL VIA ENV_VARS!

source (multiple sources, unique named)
target (path to output directory)
patterns to ignore (rsync compatible ignore patterns)
maximum copies to keep (how many copies of unit duration to keep in target dir)
unit durations (days, hours, etc.)
skipversioncheck

"""
@click.command()
@click.option("-s", "--source", "source", multiple=True, envvar="DSM_USB_BACKUP_SOURCE",
              type=click.Path(exists=True), required=True,
              help="Source path, can be provided multiple times")
@click.option("-t", "--target", "target", envvar="DSM_USB_BACKUP_TARGET",
              type=click.Path(exists=True), required=True, callback=validate_target,
              help="Target path (must be on ext4 file system)")
@click.option("--skip-version-check/--no-skip-version-check", envvar="DSM_USB_BACKUP_SKIP_VERSION_CHECK",
              default=False, help="skip DSM version compatibility check", callback=validate_version)
def main(args=None, **kwargs):
    pass


if __name__ == "__main__":
    main()
