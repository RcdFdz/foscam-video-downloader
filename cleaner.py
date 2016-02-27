import os
import re
from log_conf import Logger
from datetime import datetime
from datetime import date

class Cleaner:

	def __init__(self, ftpConnection):
		self.ftp = ftpConnection
		self.directories = self.ftp.nlst()
		self.path = self.ftp.pwd()

	directorieList = []
	aviFilesPWD = []

	def getCurrentDirs(self, directories, path):
		directoriesInDir = [bool(re.search('^[^\.]*$', files)) for files in directories]
		directory = [index for index, directory in enumerate(directoriesInDir) if directory == True]
		return [path + '/' + directories[values] + '/' for values in directory]

	def getAVIFiles(self, filesList, path):
		aviFilesInDir = [bool(re.search('.avi', files)) for files in filesList]
		aviIndexs = [index for index, aviFiles in enumerate(aviFilesInDir) if aviFiles == True]

		if any(aviFilesInDir):
			[self.aviFilesPWD.append([path, filesList[values]]) for values in aviIndexs]

	def walkDir(self):
		currentAviFidles = self.getAVIFiles(self.directories, self.path)
		currentDirs = self.getCurrentDirs(self.directories, self.path)
		for dirs in currentDirs:
			self.directorieList.append(dirs)
			try:
				self.directories = self.ftp.nlst()
				self.path = self.ftp.pwd()
				self.ftp.cwd(dirs)
				self.walkDir()
			except:
				self.directorieList.pop()
				self.ftp.cwd('..')
				self.walkDir()
		return self.directorieList, self.aviFilesPWD

	def setTime(self, dateDecimal, timeDecimal):
		return datetime.strptime(dateDecimal + ' ' + timeDecimal, '%Y%m%d %H%M%S')

	def isValidVideo(self, path):
		_, dateFile, timeFile = path[-1].replace('.avi','').split('_')
		dateTime = self.setTime(dateFile, timeFile)

		startTime1 = self.setTime(dateFile, '100000')
		endTime1 = self.setTime(dateFile, '144500')

		startTime2 = self.setTime(dateFile, '163000')
		endTime2 = self.setTime(dateFile, '181500')

		if date.isoweekday(dateTime) <= 5:
			if (startTime1 <= dateTime <= endTime1) or (startTime2 <= dateTime <= endTime2):
				return True
			else:
				return False
		else:
			return True

	def download(self, path):
		filePath = path[0] + '/' + path[1]
		file = path[1]
		try:
		    self.ftp.retrbinary('RETR %s' % filePath, open(file, 'wb').write)
		except:
		    Logger.logr.warning('ERROR: cannot read file "%s"' % file)
		    os.unlink(file)
		else:
		    Logger.logr.info('*** Downloaded "%s" to CWD' % file)
