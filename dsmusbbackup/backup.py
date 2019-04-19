import os
import re

from . import util
from datetime import datetime


class Backup(object):
    def __init__(self, target):
        self.target = target
        self._start_time = datetime.strftime(datetime.now(), '%Y-%m-%d_%H%M%S')
        self._backup_path = "{}/{}".format(self.target, self._start_time)
        self._rsync_args = list()
        self._rsync_args.append("-r")
        self._rsync_args.append("-a")
        self._rsync_args.append("-H")
        self._rsync_args.append("--delete")

        os.mkdir(self._backup_path)

    def get_backups(self):
        """
        Return a sorted list of backups in the target
        """
        print(self.target)
        with os.scandir(path=self.target) as dir_list:
            # Get a list of directories in the target, which match the expected format
            dirs = [
                item.path for item in dir_list if item.is_dir and re.match(r'\d{4}-\d{2}-\d{2}_\d{6}', item.name) is not None]
        try:
            dirs.remove(self._backup_path)
        except ValueError:
            pass

        return sorted(dirs)

    def rsync(self, source):
        """
        Execute the rsync of files from sources to backup location
        """
        print("starting rsync from {} to {}".format(source, self._backup_path))
        return_code, out, outerr = util.pipe_exec(
            "/usr/bin/rsync {} {} {}".format(" ".join(self._rsync_args), source, self._backup_path))
        if return_code != 0:
            raise OSError(outerr)
        print("rsync {} to {} finished".format(source, self._backup_path))
        return None

    def copy(self, source):
        """
        Execute a hardlink copy before rsync
        """
        try:
            last_backup = self.get_backups()[-1]
        except IndexError:
            print("no previous backup, skipping copy")
            return False

        source_in_target = os.path.basename(os.path.normpath(source))
        if os.path.isdir("{}/{}".format(last_backup, source_in_target)):
            print("hardlinking from \"{}/{}\" to \"{}/{}\"".format(last_backup,
                                                                   source_in_target, self._backup_path, source_in_target))
            util.pipe_exec("/bin/cp -al {}/{} {}/{}".format(last_backup,
                                                            source_in_target, self._backup_path, source_in_target))
            return True
        else:
            print("\"{}/{}\" does not exist, skipping hardlink".format(
                last_backup, source_in_target))
        return False

    def sync(self, source):
        """
        A shortcut to do a copy/rsync on a source
        """
        self.copy(source)
        self.rsync(source)
        pass

    def complete(self):
        """
        Mark the backups as done, update links for latest
        """
        pass

    def prune_old(self, copies):
        """
        Prune older backups.
        """
