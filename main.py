import paramiko
import shutil
from configparser import ConfigParser

config = ConfigParser()
config.read("sensitive.ini")
server = config["SERVER"]
file = config["FILE"]

host = server["host"]
user = server["user"]
password = server["password"]

path = file["path"]
dirName = path.split("/")[-1]


shutil.copytree(path, "tmp/_" + dirName)
shutil.make_archive("tmp/_" + dirName, "zip", path)

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=host, username=user, password=password)

ssh_client.exec_command("rm -rf /var/www/" + dirName)

sftp_client = ssh_client.open_sftp()
sftp_client.put("tmp/_" + dirName + ".zip", "/var/www/_" + dirName)
sftp_client.close()


ssh_client.exec_command("mkdir /var/www/" + dirName)
ssh_client.exec_command("unzip /var/www/_" + dirName + " -d /var/www/" + dirName)
ssh_client.exec_command("rm /var/www/_" + dirName)


shutil.rmtree("tmp")