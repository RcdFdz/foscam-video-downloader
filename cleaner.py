import os
import configparser
import re
from log_conf import Logger
from ftplib import FTP
from datetime import datetime
from datetime import date

def getCurrentDirs(directories, path):
	directoriesInDir = [bool(re.search('^[^\.]*$', files)) for files in directories]	
	directory = [index for index, directory in enumerate(directoriesInDir) if directory == True]
	return [path + '/' + directories[values] + '/' for values in directory]

def getAVIFiles(filesList, path):
	aviFilesInDir = [bool(re.search('.avi', files)) for files in filesList]	
	aviIndexs = [index for index, aviFiles in enumerate(aviFilesInDir) if aviFiles == True]

	if any(aviFilesInDir):
		 [ aviFilesPWD.append([path, filesList[values]]) for values in aviIndexs]

def walkDir(directories, path, ftp):
	currentAviFiles = getAVIFiles(directories, path) 
	currentDirs = getCurrentDirs(directories, path)
	for dirs in currentDirs:
		directorieList.append(dirs)
		try:
			ftp.cwd(dirs)
			walkDir(ftp.nlst(), ftp.pwd(), ftp)
		except:
			directorieList.pop()
			ftp.cwd('..')
			walkDir(ftp.nlst(), ftp.pwd(), ftp)

def isValidVideo(path):
	_, dateFile, timeFile = path[-1].replace('.avi','').split('_')
	dateTime = datetime.strptime(dateFile + ' ' + timeFile,'%Y%m%d %H%M%S')
	
	startTime1 = datetime.strptime(dateFile + ' 100000','%Y%m%d %H%M%S')
	endTime1 = datetime.strptime(dateFile + ' 144500','%Y%m%d %H%M%S')

	startTime2 = datetime.strptime(dateFile + ' 163000','%Y%m%d %H%M%S')
	endTime2 = datetime.strptime(dateFile + ' 181500','%Y%m%d %H%M%S')

	if date.isoweekday(dateTime) <= 5:
		if (startTime1 <= dateTime <= endTime1) or (startTime2 <= dateTime <= endTime2):
			return True
		else:
			return False
	else:
		return True

def download(path, ftp):
	filePath = path[0] + '/' + path[1]
	file = path[1]
	try:
	    ftp.retrbinary('RETR %s' % filePath, open(file, 'wb').write)
	except:
	    logging.warning('ERROR: cannot read file "%s"' % file)
	    os.unlink(file)
	else:
	    Logger.logr.info('*** Downloaded "%s" to CWD' % file)

## configuration

directorieList = []
aviFilesPWD = []

config = configparser.ConfigParser()
config.read('config.cfg')

host = config.get('FTP-Credentials','host')
port = str(config.get('FTP-Credentials','port'))
user = config.get('FTP-Credentials','user')
password = config.get('FTP-Credentials','pass')

## conect and move to the correct directorie
ftp = FTP()
ftp.set_pasv(0)
ftp.connect(host, port)
ftp.login(user, password)
ftp.cwd('.')
walkDir(ftp.nlst(), ftp.pwd(), ftp)

for path in aviFilesPWD:
	if isValidVideo(path):
		Logger.logr.info("Valid: " + str(path[0] + '/' + path[1]))
		download(path, ftp)
	else:
		Logger.logr.info("Not Valid: " + str(path[0] + '/' + path[1]))
		
Logger.logr.info("Done")







