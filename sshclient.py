from os.path import splitext
import json
import os
from pathlib import Path
import time
from Client import Client
from Config import Config
from File import File


def get_config_file():
    return "config/Config.json"


def get_config_options(config_path):
    with open(config_path, 'r') as config_options:
        data = json.load(config_options)
    return data


def set_config():
    config_file_name = get_config_file()
    config_file = Path(config_file_name)
    if not config_file.exists():
        print("brak pliku konfiguracyjnego, program zostanie zamkniety")
        exit(1)
    config_options = get_config_options(str(config_file))
    return config_options


def printspace():
    print("------------------------------------")


def files_remote_directory(sftp):
    try:
        sftp.chdir("pliki")
    except Exception:
        pass
    files = sftp.listdir_iter()
    for i in files:
        print(i.filename + "\t" + str(time.ctime(i.st_mtime)))


def files_local_directory(home_dir):
    files = get_local_files(home_dir)
    for i in files:
        mtime = os.path.getmtime(home_dir+"\\"+i.name)
        print(i.name + "\t" + str(time.ctime(mtime)))


def choose_action():
    print("1. Overwrite (Nadpisz wszystkie pliki, dodaj te których nie ma)")
    print("2. Update (Nadpisz starsze pliki w folderze zdalnym)")
    print("3. Add non existing (Wysyla tylko te pliki ktorych nie ma w folderze zdalnym)")
    print("4. Print directories (Wyświetla zawartość folderów lokalny i zdalny)")
    print("0\Q. Exit")


def overwrite(sftp, conf):
    files = get_local_files(conf.home_dir)
    for i in files:
        if not is_ignored(i.name, conf.ignore):
            print("sending " + i.name)
            sftp.put(conf.home_dir+i.name, conf.remote_dir+i.name)


def update(sftp, conf):
    local_files = get_local_files(conf.home_dir)
    remote_files = get_remote_files(sftp)
    for local in local_files:
        for remote in remote_files:
            if local.name == remote.name:
                if not is_ignored(local.name, conf.ignore) and remote.is_older(local):
                    print("sending "+ local.name)
                    sftp.put(conf.home_dir+local.name, conf.remote_dir+remote.name)


def add_non_existing(sftp, conf):
    local_files = get_local_files(conf.home_dir)
    remote_files = get_remote_files(sftp)
    for local in local_files:
        exist = False
        for remote in remote_files:
            if local.name == remote.name:
                exist = True
        if not exist:
            if not is_ignored(local.name, conf.ignore):
                print("sending" + local.name)
                sftp.put(conf.home_dir+local.name, conf.remote_dir+local.name)


def is_ignored(filename, ignore_list):
    name, ext = splitext(filename)
    for extension in ignore_list:
        if ('.'+extension) == ext:
            return True
    return False


def show_files(sftp, conf):
    printspace()
    print("Files in the remote directory " + conf.remote_dir + ":")
    files_remote_directory(sftp)
    printspace()
    print("Files in the local directory " + conf.home_dir + ":")
    files_local_directory(conf.home_dir)
    printspace()


def get_local_files(home_dir):
    file_list = []
    files = os.listdir(home_dir)
    for i in files:
        mtime = os.path.getmtime(home_dir + "\\" + i)
        file_list.append(File(i, mtime))
    return file_list


def get_remote_files(ftp):
    try:
        ftp.chdir("pliki")
    except Exception:
        pass
    file_list = []
    files = ftp.listdir_iter()
    for i in files:
        file_list.append(File(i.filename, i.st_mtime))
    return file_list


def main():
    print("Program synchronizujacy pliki miedzy folderami lokalnym i zdalnym")
    config = Config(set_config())
    client = Client()
    client.connection(config)
    ftp = client.client.open_sftp()
    show_files(ftp, config)
    choose_action()
    while True:
        choose = input("Action: ")
        if choose == "1":
            overwrite(ftp, config)
        elif choose == "2":
            update(ftp, config)
        elif choose == "3":
            add_non_existing(ftp, config)
        elif choose == "4":
            show_files(ftp, config)
        elif choose != "Q" or choose != "0":
            print("Closing application")
            break
        else:
            print("Non action with this option")

    ftp.close()
    client.close()


main()
