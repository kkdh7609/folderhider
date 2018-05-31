#-*- coding: utf-8 -*-

# Python 3.6.4
# author: Kim Do Hyeon
# date: 2018.5.30

import folder_inform
import folderHider
import Manage_Crypt
import client_socket
import sys
import os

con = folder_inform.Controlinform()
pw = 0
if con.isFirst:
    pw = input("Setting Password: ")
    con.setkey(Manage_Crypt.make_sha_key(pw))
    con.make_pass_file()
else:
    pw = input("Input Password: ")
    con.setkey(Manage_Crypt.make_sha_key(pw))
    if con.iscorrect():
        print("Login Success!")
    else:
        print("Login Failed")
        want = input("Do you want to find password? yes or no: ")
        if want.upper() == "YES":
            email = input("Input your mail: ")
            net = client_socket.Netclient()
            if not net.checkserver():
                print("Wrong Server")
                sys.exit(0)
            if not net.getAESkey():
                print("Connecting Failed")
                sys.exit(0)
            net.getpw(email)
            print("Please restart the program")
            sys.exit(0)
        else:
            sys.exit(0)

data = con.getinform()
while True:
    con.make_setfile(data)
    if len(data) != 0:
        print("Encrypted Folders".center(110))
        for i in data:
            print("path:" + i[0].center(100) + "mode: "+ str(i[2]).center(20))
    for i in range(2):
        print()
    path = input("Input Target Folder. If you want to back up your password to the server, input 1: ")
    if path == "1":
        email = input("Input your Email: ")
        net = client_socket.Netclient()
        if not net.checkserver():
            print("Wrong Server")
            continue
        if not net.getAESkey():
            print("Connecting Failed")
            continue
        net.sendpw(email, pw)
        continue
    index = -1
    if len(data) != 0:
        for i in range(0,len(data)):
            if path == data[i][0]:
                index = i
                break
    if index != -1:
        if input("unlock the folder? yes or no: ").upper() == "YES":
            locker = folderHider.FolderLocker(data[index][1], pw, data[index][2], islocked=True)
            locker.exe_lock()
            del data[index]
    elif not os.path.exists(path):
        print("Wrong Path")
        continue
    else:
        mode = input("Input mode( 1 : Just hide folder   2 : make Encrypted Zip file   3: Encrypt Folder  4: Encrypt Folder(with wiper)) : ")
        mode = int(mode)
        locker = folderHider.FolderLocker(path, pw, mode)
        if input("File recovery can fail. Do you want to do that? yes or no: ").upper() == "YES":
            locker.exe_lock()
            data.append(locker.save_inform())
    for i in range(10):
        print()







