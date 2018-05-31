# Python 3.6.4
# author: Kim Do Hyeon
# date: 2018.5.28

import folderHider
import Manage_Crypt
import os
import pickle

class Controlinform:
    def __init__(self):                     # key is hashed sha256
        self.set_file = "setting.set"
        self.encrypted_set_file = "setting.set.encrypt"
        self.pass_file = "password.set"
        self.encrypted_pass_file = "password.set.encrypt"
        self.key = 0
        self.md5_key = 0
        self.isFirst = False
        if not os.path.exists(self.encrypted_pass_file):
            self.isFirst = True

    def setkey(self, key):
        self.key = key
        self.md5_key = Manage_Crypt.make_md5_key(key)

    def iscorrect(self):
        crypt = Manage_Crypt.AESmanager(self.md5_key)
        crypt.dec_file(self.encrypted_pass_file)
        correct = False
        with open(self.pass_file, 'rb') as inputFile:
            read = inputFile.readline()
            if bytes(self.key,'utf-8') != read:
                correct = False
            else:
                correct = True
        os.remove(self.pass_file)
        if correct:
            return True
        else:
            return False

    def make_pass_file(self):
        with open(self.pass_file, 'w') as outputFile:
            outputFile.write(self.key)
        crypt = Manage_Crypt.AESmanager(self.md5_key)
        crypt.enc_file(self.pass_file)
        os.remove(self.pass_file)

    def getinform(self):
        if not os.path.exists(self.encrypted_set_file):
            return []
        crypt = Manage_Crypt.AESmanager(self.md5_key)
        crypt.dec_file(self.encrypted_set_file)
        os.remove(self.encrypted_set_file)
        with open(self.set_file, 'rb') as inputFile:
            data = pickle.load(inputFile)
        return data

    def make_setfile(self, data):
        with open(self.set_file, 'wb') as outputFile:
            pickle.dump(data, outputFile)
        crypt = Manage_Crypt.AESmanager(self.md5_key)
        crypt.enc_file(self.set_file)
        os.remove(self.set_file)



def test():
    con = Controlinform()
    key = 'password'
    if con.isFirst:
        con.setkey(Manage_Crypt.make_sha_key(key))
        con.make_pass_file()
    else:
        con.setkey(Manage_Crypt.make_sha_key(key))
        if con.iscorrect():
            print("correct")
        else:
            print("uncorrect")

    print(con.getinform())
    a=[1,2,3]
    b=[34,2434,34]
    c=[a,b]
    con.make_setfile(c)


if __name__ == '__main__':
    test()