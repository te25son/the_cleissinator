import os
import shutil


class DirectoryMaster:

    def __init__(self, homepath, naming_dictionary, download_dir):
        self.homepath = homepath
        self.naming_dictionary = naming_dictionary
        self.download_dir = download_dir.replace('\\', '/')

    def remove_download_directory(self):
        try:
            shutil.rmtree(self.download_dir)
        except:
            pass

    def make_directories_if_they_dont_already_exist(self):
        try:
            os.makedirs(self.download_dir + '/MISC_FILES')
        except:
            pass
        for key in self.naming_dictionary:
            try:
                os.makedirs(self.download_dir + '/' + self.naming_dictionary[key][0])
                os.makedirs(self.download_dir + '/' + self.naming_dictionary[key][1])
            except FileExistsError:
                pass
