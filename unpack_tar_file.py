import tarfile, sys

class UnpackTarFile:
    def __init__(self, fname, my_path):
        if (tarfile.is_tarfile(fname)):
            with tarfile.open(fname, 'r') as tfile:
                tfile.extractall(path=my_path, members=self.track_progress(tfile))
            tfile.close()

        else:
            # TODO: Should be throw an exception
            print 'This file is not valid!'

    def track_progress(self, members):
        for member in members:
            # this will be the current file being extracted
            yield member
            print 'Extracting: ', member