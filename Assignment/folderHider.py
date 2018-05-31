# Python 3.6.4
# author: Kim Do Hyeon
# date: 2018.5.28

import os
import pyminizip
import Manage_Crypt
import shutil
import zipfile

class FolderLocker:
    def __init__(self, path, key, mode=1, islocked=False):  # mode 1:simple lock 2:lock compressed folder 3:Ransomeware 4:Ransomeware 2
        self.path = path
        self.changed_path = path
        self.key = Manage_Crypt.make_md5_key(key)
        self.mode = mode
        self.islocked = islocked

    def exe_lock(self):
        if self.islocked:
            if self.mode == 1:
                self.solve()
            elif self.mode == 2:
                self.unzip_folder()
            elif self.mode == 3 or self.mode == 4:
                self.dec_folder()
        else:
            if self.mode == 1:
                self.lock()
            elif self.mode == 2:
                self.zip_folder()
            elif self.mode == 3 or self.mode == 4:
                self.enc_folder()

    def save_inform(self):
        return [self.path, self.changed_path, self.mode]

    def lock(self):
        adder = ".{2559a1f2-21d7-11d4-bdaf-00c04f60b9f0}"
        folder_name = self.path + adder
        os.rename(self.path, folder_name)
        comd = "attrib +h +s +r " + folder_name
        os.system(comd)
        self.changed_path = folder_name

    def solve(self):
        folder_name = ".".join(self.path.split('.')[:-1])
        os.rename(self.path, folder_name)
        comd = "attrib -h -s -r " + folder_name
        os.system(comd)
        self.changed_path = folder_name

    def enc_folder(self):
        file_list = self.get_filelist()
        crypt = Manage_Crypt.AESmanager(self.key)
        for file in file_list:
            crypt.enc_file(file)
            if self.mode == 4:
                file_wiper(file)
            else:
                os.remove(file)
            print("Encrypted " + file)

    def dec_folder(self):
        file_list = self.get_filelist()
        crypt = Manage_Crypt.AESmanager(self.key)
        for file in file_list:
            crypt.dec_file(file)
            os.remove(file)
            print("Decrypted " + file)

    def get_filelist(self):
        file_list = []
        for (path, dirs, files) in os.walk(self.path):
            for filename in files:
                file_list.append(path + '\\' + filename)
        return file_list

    def zip_folder(self):
        compression_level = 5
        out_file_name = self.path + ".zip"
        file_list = self.get_filelist()
        pyminizip.compress_multiple(file_list, [], out_file_name, self.key, compression_level)
        shutil.rmtree(self.path)
        self.changed_path = out_file_name

    def unzip_folder(self):
        out_file_name = ".".join(self.path.split('.')[:-1])
        zip_key = bytes(self.key, 'utf-8')
        zip_folder = zipfile.ZipFile(self.path)
        zip_folder.extractall(out_file_name, pwd=zip_key)
        zip_folder.close()
        os.remove(self.path)


def file_wiper(file, cycle=7):
    file_size = os.path.getsize(file)
    with open(file, "rb+") as inputFile:
        for i in range(cycle):
            inputFile.seek(0)
            inputFile.write(os.urandom(file_size))
            #print("Wiper " + str(i+1) + " times")
    os.remove(file)


def test():
    file = 'D:\\aaaaaaaa\\akakak.zip'
    key = 'password'
    lock = FolderLocker(file, key)
    lock.unzip_folder()
    #lock.dec_folder()


if __name__ == '__main__':
    test()
