### DO NOT EDIT THIS PART ###
import os
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
                               '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
### DO NOT EDIT THIS PART ###

# Site's name
SITE_NAME = "bunkerch-based textboard"

#Change this to something hard to guess, just use a random generator or something
SECRET_KEY = 'Secret Key'

#Auth for mod page, !CHANGE THIS!
#(This will be implemented better later)
ADMIN = 'ADMIN'
PASSWORD = 'PASSWORD'

#Python dictionary so edit it as so
#The keys are the board's letters, the values are their full names
#If you don't know that means just think of it like this:
#Format: "[board letter]": "[board name]", each board seperated by commas 
#For example 
#boards = { 
#   "a": "Anime and Manga",
#   "b": "Random"
#   } 
#and so on 
#They can be on one line too obviously but I did it this way for easier readability
#By default you have /b/, if you don't want it remove it
#You will have to manually run db_migrate.py if you edit this from here and not the mod interface
BOARDS = {
    "b": "Random"
}

#Wordfilters
#Dictionary just like the boards
#Leave it empty if you aren't using it
FILTERS = {}

#Set this to True if you are using a reverse proxy with nginx
#Set nginx to listen to listen to sofich on 8080 otherwise you are 
#going to have to be changing it manually in run.py to your port of choice
REVPROX = False 

#If you type 'noko' (or prefix any other options like 'sage' with 'noko', like 'nokosage') in the options field on a thread,
#You will stay in the thread instead of returning to the board index/catalog
#If this is set to True, users will not have to type 'noko' to stay in the thread,
#But can type 'nonoko' to be returned to the index/catalog like normal
ALWAYS_NOKO = True 
