import sys
import os
import paramiko
import shutil
from configparser import ConfigParser

user_input = input("What shloud be pushed to your server? Leave blank to open config.\n")

if not user_input:
    os.system("open config.ini")
    sys.exit()
else:
    try:
        config = ConfigParser()
        config.read("config.ini")
        server = config["SERVER"]
        con = config[user_input]
    except:
        print("SERVER or PATH not found in config.ini!")
        sys.exit()

try:
    print("Starting to push to your Server...")

    host = server["host"]
    user = server["user"]
    password = server["password"]

    path = con["path_to_directory"]
    dirName = path.split("/")[-1]
    server_path = con["path_to_server_directory"]

    shutil.copytree(path, "tmp/_" + dirName)
    shutil.make_archive("tmp/_" + dirName, "zip", path)

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=user, password=password)

    ssh_client.exec_command("rm -rf " + server_path + dirName)

    sftp_client = ssh_client.open_sftp()
    sftp_client.put("tmp/_" + dirName + ".zip", server_path + "_" + dirName)
    sftp_client.close()


    ssh_client.exec_command("mkdir " + server_path + dirName)
    ssh_client.exec_command("unzip " + server_path + "_" + dirName + " -d " + server_path + dirName)
    ssh_client.exec_command("rm "+ server_path + "_" + dirName)


    shutil.rmtree("tmp")

    print("FINISHED ;)")

except:
    print("Something went wrong!")