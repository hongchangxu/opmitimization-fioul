import logging
import  time
from logging.handlers import RotatingFileHandler
import os

cwd = os.getcwd()
catalogue_base = cwd + "\log"
catalogue_log =cwd + "\log\log"
catalogue_log_debug =cwd + "\log\debug"

if os.path.exists(catalogue_base) == False:
    os.mkdir(catalogue_base)
if os.path.exists(catalogue_log) == False:
    os.mkdir(catalogue_log)
if os.path.exists(catalogue_log_debug) == False:
    os.mkdir(catalogue_log_debug)

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
today = time.strftime("%d%m%Y", time.localtime())
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.INFO)
# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo

file_name1 = catalogue_log + "\\" + today + ".log"
file_handler1 = RotatingFileHandler(file_name1, 'a', 1000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler1.setLevel(logging.INFO)
file_handler1.setFormatter(formatter)
logger.addHandler(file_handler1)

file_name2 = catalogue_log_debug + "\\" + today + ".log"
file_handler2 = RotatingFileHandler(file_name2, 'a', 1000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler2.setLevel(logging.DEBUG)
file_handler2.setFormatter(formatter)
logger.addHandler(file_handler2)

# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
logger.addHandler(stream_handler)
