import os

class TmpFileCleanup(object):
    """ Used to clean up tmp files.
    """

    def __enter__(self):
        # Keep local copy of the tmp files.
        self.tmp_files = []
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Delete all tmp files.
        for file_path in self.tmp_files:
            try:
                os.remove(file_path)
            except OSError:
                pass
