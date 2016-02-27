import configparser
from cleaner import *
from log_conf import Logger
from ftplib import FTP

config = configparser.ConfigParser()
config.read('config.cfg')

host = config.get('FTP-Credentials','host')
port = str(config.get('FTP-Credentials','port'))
user = config.get('FTP-Credentials','user')
password = config.get('FTP-Credentials','pass')

ftp = FTP()
ftp.set_pasv(0)
ftp.connect(host, port)
ftp.login(user, password)

clean = Cleaner(ftp)
directorieList, aviFilesPWD = clean.walkDir()

for path in aviFilesPWD:
	if clean.isValidVideo(path):
		Logger.logr.info("Valid: " + str(path[0] + '/' + path[1]))
		clean.download(path)
	else:
		Logger.logr.info("Not Valid: " + str(path[0] + '/' + path[1]))

Logger.logr.info("Done")
