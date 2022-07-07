###########################################################
#
# This python script is used for mysql database backup
# using mysqldump and tar utility.
#
# Written by : Rahul Kumar
# Modified by: Gerardo Suárez
# Website: http://tecadmin.net
# Created date: Dec 03, 2013
# Last modified: May 27, 2021
# Tested with : Python 3.8.6
# Script Revision: 1.4.1
#
##########################################################

# Import required python libraries
import ntpath
import os
import time
import datetime
import pipes
import logging
import shutil

# Logging and console
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.

DB_HOST = 'localhost'
DB_USER = 'user database'
DB_USER_PASSWORD = 'Password'
DB_NAME = 'database_name'
BACKUP_PATH = 'path'
XAMPP = 'C:/xampp/mysql/bin/'

# Getting current DateTime to create the separate backup folder like "20180817-123433".
DATETIME = time.strftime('%d%m%Y-%H%M%S')
TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME

# Checking if backup folder already exists or not. If not exists will create it.
try:
    os.stat(TODAYBACKUPPATH)
except:
    os.mkdir(TODAYBACKUPPATH)

# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
logger.debug("checking for databases names file.")
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1
    logger.debug("Databases file found...")
    logger.debug("Starting backup of all dbs listed in file {}".format(DB_NAME))

else:
    logger.debug("Databases file not found...")
    logger.debug("Starting backup of database: {}".format(DB_NAME))
    multi = 0

# Starting actual database backup process.
if multi:
   in_file = open(DB_NAME,"r")
   flength = len(in_file.readlines())
   in_file.close()
   p = 1
   dbfile = open(DB_NAME,"r")

   while p <= flength:
       db = dbfile.readline()   # reading database name from file
       db = db[:-1]         # deletes extra line
       dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + db + ".sql"
       os.system(dumpcmd)
       p = p + 1
   dbfile.close()
else:
   db = DB_NAME
   dumpcmd = XAMPP + "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
   os.system(dumpcmd)
   shutil.make_archive(TODAYBACKUPPATH, 'zip', TODAYBACKUPPATH)

logger.debug("")
logger.debug("Backup script completed")
logger.debug("Your backups have been created in {} directory".format(TODAYBACKUPPATH))
