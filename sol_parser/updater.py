import urllib
import re
import os
import sys

__version__ = "0"
    
class Updater(object):
    def num(self, s):
        if s.isdigit(): return int(s)
        return s

    def compare_versions(self, vA, vB):
        """
        Compares two version number strings
        @param vA: first version string to compare
        @param vB: second version string to compare
        @author <a href="http_stream://sebthom.de/136-comparing-version-numbers-in-jython-pytho/">Sebastian Thomschke</a>
        @return negative if vA < vB, zero if vA == vB, positive if vA > vB.
        """
        if vA == vB: return 0

        seqA = map(self.num, re.findall('\d+|\w+', vA.replace('-SNAPSHOT', '')))
        seqB = map(self.num, re.findall('\d+|\w+', vB.replace('-SNAPSHOT', '')))

        # this is to ensure that 1.0 == 1.0.0 in cmp(..)
        lenA, lenB = len(seqA), len(seqB)
        for i in range(lenA, lenB): seqA += (0,)
        for i in range(lenB, lenA): seqB += (0,)

        rc = cmp(seqA, seqB)

        if rc == 0:
            if vA.endswith('-SNAPSHOT'): return -1
            if vB.endswith('-SNAPSHOT'): return 1
        return rc

    def __init__(self, dl_url, force_update=False):
        """
        Attempts to download the update url in order to find if an update is needed.
        If an update is needed, the current script is backed up and the update is
        saved in its place.
        """
        self.app_path = os.path.realpath(sys.argv[0])
        self.dl_url = dl_url
        self.force_update = force_update

    def __call__(self):
        if not os.access(self.app_path, os.W_OK):
            print("Cannot update -- unable to write to {}".format(self.app_path))
        else:
            if self.check_version():
                if self.download_update() and self.backup_existing() and self.install_update():
                    print("New version installed as {}".format(self.app_path))
                    print("(previous version backed up to {})".format(self.backup_path))
                else:
                    self.restore_backup()
                    print("Update failed")
                    print("(previous version restored)")    
    
    def check_version(self):
        # dl the first 256 bytes and parse it for version number
        try:
            http_stream = urllib.urlopen(self.dl_url)
            update_file = http_stream.read(256)
            http_stream.close()
        except IOError, (errno, strerror):
            print("Unable to retrieve version data")
            print("Error {}: {}".format(errno, strerror))
            return False

        match_regex = re.search(r'__version__ *= *"(\S+)"', update_file)
        if not match_regex:
            print("No version info could be found")
            return False
        update_version = match_regex.group(1)

        if not update_version:
            print("Unable to parse version data")
            return False
    
        if self.force_update:
            print("Forcing update, downloading version {}...".format(update_version))
            return True
        else:
            cmp_result = self.compare_versions(__version__, update_version)
            if cmp_result < 0:
                print("Newer version {} available, downloading...".format(update_version))
                return True
            elif cmp_result > 0:
                print("Local version {} newer then available {}, not updating.".format(__version__, update_version))
                return False
            else:
                print("You already have the latest version.")
                return False
   
    def download_update(self):
        self.dl_path = self.app_path + ".new"
        self.backup_path = self.app_path + ".old"
        try:
            self.dl_file = open(self.dl_path, 'w')
            http_stream = urllib.urlopen(self.dl_url)
            total_size = None
            bytes_so_far = 0
            chunk_size = 8192
            try:
                total_size = int(http_stream.info().getheader('Content-Length').strip())
            except:
                # The header is improper or missing Content-Length, just download
                self.dl_file.write(http_stream.read())

            while total_size:
                chunk = http_stream.read(chunk_size)
                self.dl_file.write(chunk)
                bytes_so_far += len(chunk)

                if not chunk:
                    break

                percent = float(bytes_so_far) / total_size
                percent = round(percent*100, 2)
                sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" %
                    (bytes_so_far, total_size, percent))

                if bytes_so_far >= total_size:
                    sys.stdout.write('\n')

            http_stream.close()
            self.dl_file.close()
            return True
        except IOError, (errno, strerror):
            print "Download failed"
            print "Error %s: %s" % (errno, strerror)
            return False

    def backup_existing(self):
        try:
            os.rename(self.app_path, self.backup_path)
            return True
        except OSError, (errno, strerror):
            print "Unable to rename %s to %s: (%d) %s" \
                % (self.app_path, self.backup_path, errno, strerror)
            return False

    def install_update(self):
        try:
            os.rename(self.dl_path, self.app_path)
            return True
        except OSError, (errno, strerror):
            print "Unable to rename %s to %s: (%d) %s" \
                % (self.dl_path, self.app_path, errno, strerror)
            return False

    def restore_backup(self):
        try:
            import shutil
            shutil.copymode(self.backup_path, self.app_path)
        except:
            os.chmod(self.app_path, 0755)

up = Updater("https://gist.githubusercontent.com/Haaruun-I/7742df86770cc7c2066b99dca05186e9/raw/6d1c687b311978b71d083ee0914d2e56938b20e5/self-update-script.py")
up()
# update("https://gist.githubusercontent.com/Haaruun-I/7742df86770cc7c2066b99dca05186e9/raw/6d1c687b311978b71d083ee0914d2e56938b20e5/self-update-script.py")
