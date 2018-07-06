import threading
from datetime import date
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import xlrd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
import psycopg2
import configparser
import os
import logging

#
#引用其他的文件
#
#
from logSystem import logger
from test_email import envoyer_email
import re
#
#
# global variable
#
#
#*********************** Data Base**********************************
DATA_BASE_NAME = 'fioul'
DATA_BASE_USER = 'dbuser'
DATA_BASE_PASSWORD = 'password'
DATA_BASE_HOST_ADDRESS = '192.168.192.128'
DATA_BASE_PORT = '5432'
#********************* Email system *********************************
EMAIL_USER =''
EMAIL_PASSWORD = ''
TO_EMAIL_USERS_BON_SIGNE = ''
TO_EMAIL_USERS_REPORT = ''
TO_EMAIL_USERS_URGENT = ''
SMTP_SERVER  ='smtp.gmail.com'
#********************* Log level debug or not************************
LOG_DEBUG = False
#********************** web driver **********************************
DRIVER_EXECUTABLE_PATH = r'C:\Program Files\Mozilla Firefox\geckodriver'
FIREFOX_PROFILE = r'C:\Users\49383\AppData\Roaming\Mozilla\Firefox\Profiles\coa5jxxc.default'
#********************* others ***************************************
TIME_OUT_SET = "17:52:00"
#********************** localisation des elements********************
#
#
#********************** FIOUL MARKET ********************************
FIOUL_MARKET_CP_INPUT = ''
FIOUL_MARKET_BUTTON = ''
FIOUL_MARKET_FIOUL_TYPE =''
FIOUL_MARKET_FIOUL_ORDINAIRE = ''
FIOUL_MARKET_QUANTITE = ''
FIOUL_MARKET_LIVRAISON = ''
FIOUL_MARKET_PRIX = ''
#********************** FIOUL REDUC ********************************
FIOUL_REDUC_CP_INPUT = ''
FIOUL_REDUC_QUANTITE =''
FIOUL_REDUC_EMAIL = ''
FIOUL_REDUC_BUTTON =''
FIOUL_REDUC_LIVRAISON_RAPIDE =''
FIOUL_REDUC_TYPE_ORDINAIRE = ''
FIOUL_REDUC_PRIX = ''
#******************** FIOUL CARREFOUR *****************************
FIOUL_CARREFOUR_CP_INPUT = ''
FIOUL_CARREFOUR_QUANTITE = ''
FIOUL_CARREFOUR_DEVIS_BUTTON = ''
FIOUL_CARREFOUR_PRIX = ''
FIOUL_CARREFOUR_CLOSE_BUTTON = ''

#
#function definition
#


"""

  init_program - init the program when start
 
  To create the category of configuration and the category of log if they are not existed, then configure the programme with the 
  configuration file or/and the configuration information stored in the database.
 
  RETURNS: non

"""
def init_program():
    logger.info("begin to init the program with configuration file")
    cwd = os.getcwd()
    catalogue_base = cwd + "\config"
    catalogue_config_file = cwd + "\config\config.ini"

    if os.path.exists(catalogue_base) == False:
        os.mkdir(catalogue_base)
    if os.path.exists(catalogue_config_file):
        pass
    else:
        file = open(catalogue_config_file,'w')
        file.close()
    config= configparser.ConfigParser()
    config.read(catalogue_config_file)

    global DATA_BASE_NAME
    global DATA_BASE_USER
    global DATA_BASE_PASSWORD
    global DATA_BASE_HOST_ADDRESS
    global DATA_BASE_PORT
    global EMAIL_USER
    global EMAIL_PASSWORD
    global TO_EMAIL_USERS_BON_SIGNE
    global TO_EMAIL_USERS_REPORT
    global SMTP_SERVER
    global LOG_DEBUG
    global DRIVER_EXECUTABLE_PATH
    global FIREFOX_PROFILE
    global TIME_OUT_SET
    global FIOUL_MARKET_CP_INPUT
    global FIOUL_MARKET_BUTTON
    global FIOUL_MARKET_FIOUL_TYPE
    global FIOUL_MARKET_FIOUL_ORDINAIRE
    global FIOUL_MARKET_QUANTITE
    global FIOUL_MARKET_LIVRAISON
    global FIOUL_MARKET_PRIX
    global FIOUL_REDUC_CP_INPUT
    global FIOUL_REDUC_QUANTITE
    global FIOUL_REDUC_EMAIL
    global FIOUL_REDUC_BUTTON
    global FIOUL_REDUC_LIVRAISON_RAPIDE
    global FIOUL_REDUC_TYPE_ORDINAIRE
    global FIOUL_REDUC_PRIX
    global FIOUL_CARREFOUR_CP_INPUT
    global FIOUL_CARREFOUR_QUANTITE
    global FIOUL_CARREFOUR_DEVIS_BUTTON
    global FIOUL_CARREFOUR_PRIX
    global FIOUL_CARREFOUR_CLOSE_BUTTON
#**************************** DataBase configuration **********************
    if len(config.get('database','data_base_name')):
        DATA_BASE_NAME = config.get('database','data_base_name')
    else:
        logger.info("there are no data_base_name value in the config file")
    if len(config.get('database','data_base_user')):
        DATA_BASE_USER = config.get('database','data_base_user')
    else:
        logger.info("there are no data_base_user value in the config file")
    if len(config.get('database','data_base_password')):
        DATA_BASE_PASSWORD = config.get('database','data_base_password')
    else:
        logger.info("there are no data_base_password value in the config file")
    if len(config.get('database','data_base_host_address')):
        DATA_BASE_HOST_ADDRESS = config.get('database','data_base_host_address')
    else:
        logger.info("there are no data_base_host_address value in the config file")
    if len(config.get('database','data_base_port')):
        DATA_BASE_PORT = config.get('database','data_base_port')
    else:
        logger.info("there are no data_base_port value in the config file")

# ******************************** Email configuration**********************
    try:
        conn = psycopg2.connect(database=DATA_BASE_NAME, user=DATA_BASE_USER, password=DATA_BASE_PASSWORD,
                                host=DATA_BASE_HOST_ADDRESS, port=DATA_BASE_PORT)
    except Exception as e:
        logger.error(e)
        logger.error("connect to the database failed")
        exit(0)
    try:
        cur = conn.cursor()
        query = 'SELECT * FROM configuration;'
        cur.execute(query)
        temps_configuration = cur.fetchall()[0]
        EMAIL_USER = temps_configuration[1]
        EMAIL_PASSWORD = temps_configuration[2]
        temps_configuration_2 = temps_configuration[3].split(',')
        temps_configuration_3 = temps_configuration[4].split(',')
        temps_configuration_4 = temps_configuration[5].split(',')
        temps_list = []
        for i in temps_configuration_2:
            temps_list.append(i)
        TO_EMAIL_USERS_BON_SIGNE = temps_list
        temps_list = []
        for i in temps_configuration_3:
            temps_list.append(i)
        temps_list = []
        TO_EMAIL_USERS_REPORT = temps_list
        for i in temps_configuration_4:
            temps_list.append(i)
        TO_EMAIL_USERS_URGENT = temps_list
        SMTP_SERVER = temps_configuration[6]
        TIME_OUT_SET = temps_configuration[7]
        FIOUL_MARKET_CP_INPUT = temps_configuration[8]
        FIOUL_MARKET_BUTTON = temps_configuration[9]
        FIOUL_MARKET_FIOUL_TYPE = temps_configuration[10]
        FIOUL_MARKET_FIOUL_ORDINAIRE = temps_configuration[11]
        FIOUL_MARKET_PRIX = temps_configuration[12]
        FIOUL_REDUC_CP_INPUT = temps_configuration[13]
        FIOUL_REDUC_QUANTITE = temps_configuration[14]
        FIOUL_REDUC_EMAIL = temps_configuration[15]
        FIOUL_REDUC_BUTTON = temps_configuration[16]
        FIOUL_REDUC_LIVRAISON_RAPIDE = temps_configuration[17]
        FIOUL_REDUC_TYPE_ORDINAIRE = temps_configuration[18]
        FIOUL_REDUC_PRIX = temps_configuration[19]
        FIOUL_CARREFOUR_CP_INPUT = temps_configuration[20]
        FIOUL_CARREFOUR_QUANTITE = temps_configuration[21]
        FIOUL_CARREFOUR_DEVIS_BUTTON = temps_configuration[22]
        FIOUL_CARREFOUR_PRIX = temps_configuration[23]
        FIOUL_CARREFOUR_CLOSE_BUTTON = temps_configuration[24]
        conn.close()
        logger.info("get the email configuration succeed")

    except Exception as e:
        logger.error(e)
        logger.error("get the email configuration failed")
        conn.close()
#     if len(config.get('email','email_user')):
#         EMAIL_USER= config.get('email','email_user')
#     else:
#         logger.info("there are no email_user value in the config file")
#
#     if len(config.get('email','email_password')):
#         EMAIL_PASSWORD = config.get('email','email_password')
#     else:
#         logger.info("there are no email_password value in the config file")
#
#     if len(config.get('email','to_email_users_bon_signe')):
#         temp_users = str(config.get('email','to_email_users_bon_signe'))
#         temp_users = temp_users.strip("'").split(',')
#         temp_users_bon_signe = []
#         for i in temp_users:
#             temp_users_bon_signe.append(i)
#         TO_EMAIL_USERS_BON_SIGNE = temp_users_bon_signe
#     else:
#         logger.info("there are no to_email_users_bon_signe value in the config file")
#     if len(config.get('email','to_email_users_report')):
#         temp_users = str(config.get('email', 'to_email_users_report'))
#         temp_users = temp_users.strip("'").split(',')
#         temp_users_report = []
#         for i in temp_users:
#             temp_users_report.append(i)
#         TO_EMAIL_USERS_REPORT = temp_users_report
#     else:
#         logger.info("there are no to_email_users_report value in the config file")
#     if len(config.get('email','smtp_server')):
#         SMTP_SERVER= config.get('email','smtp_server')
#     else:
#         logger.info("there are no smtp_server value in the config file")
#********************************log configuration ********************
    if len(config.get('log','log_debug')):
        LOG_DEBUG = config.get('log','log_debug')
        if LOG_DEBUG == 'True':
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
    else:
        logger.info("there are no log_debug value in the config file")
#****************************** web driver ******************************
    if len(config.get('webdriver','driver_executable_path')):
        DRIVER_EXECUTABLE_PATH = config.get('webdriver','driver_executable_path')
    else:
        logger.info("there are no driver_executable_path value in the config file")
    if len(config.get('webdriver','firefox_profile')):
        FIREFOX_PROFILE = config.get('webdriver','firefox_profile')
    else:
        logger.info("there are no firefox_profile value in the config file")

"""

  etat_init - create a new programme status record in the database

  To insert a new programme status record in the database which indicate the status of this programme:
  status = 0  :The programme is running
  status = 1  :The programme is finished with success 
  status = 2  :The programme is finished with some or all prices failed
  
  RETURNS: non

"""
def etat_init():
    logger.info('etat init')
    try:
        conn = psycopg2.connect(database=DATA_BASE_NAME, user=DATA_BASE_USER, password=DATA_BASE_PASSWORD,
                                host=DATA_BASE_HOST_ADDRESS, port=DATA_BASE_PORT)
    except Exception as e:
        logger.error(e)
        logger.error('connect to the database failed')
        envoyer_bad_signal()
        exit(0)
    runtime = time.strftime("%Y-%m-%d", time.localtime())
    try:
        cur = conn.cursor()
        query = 'SELECT * FROM etat where date = %s;'
        cur.execute(query, (runtime))
        conn.commit()
    except Exception as e:
        logger.error(e)
        logger.error('connect to the database failed')
    try:
        logger.info('try to insert a new etat into the datebase')
        cur = conn.cursor()
        query = 'INSERT INTO etat (etat_code, date) VALUES (%s,%s);'
        cur.execute(query, (0, runtime))
        conn.commit()
        logger.info('etat init succeed')
    except Exception as e:
        logger.error(e)
        logger.error("can't insert a new etat into the datebase")
        conn.close()
    conn.close()

"""

  etat_set - set the status of this programme
  
  Parameter:
  etat_code: The value of the status which you want to set
  status = 1  :The programme is finished with success 
  status = 2  :The programme is finished with some or all prices failed
    
  Set the status of this programme when the programme is finished(status = 1) or The time is out(status = 2).

  RETURNS: non

"""
def etat_set(etat_code):
    logger.info("it going to update the etat to %d", etat_code)
    try:
        conn = psycopg2.connect(database=DATA_BASE_NAME, user=DATA_BASE_USER, password=DATA_BASE_PASSWORD,
                                host=DATA_BASE_HOST_ADDRESS, port=DATA_BASE_PORT)
    except Exception as e:
        logger.error(e)
        logger.error("connect to the database failed")
        exit(0)
    runtime = time.strftime("%Y-%m-%d", time.localtime())
    try:
        cur = conn.cursor()
        query = 'UPDATE etat SET etat_code = %s WHERE date = %s;'
        cur.execute(query, (etat_code, runtime))
        etat_temp = cur.fetchall()
        if len(etat_temp):
            conn.close()
            etat_set(0)
        else:
            query = 'INSERT INTO etat (etat_code, date) VALUES (%s,%s);'
            cur.execute(query, (0, runtime))
            conn.commit()
            logger.info('etat init succeed')
    except Exception as e:
        logger.error(e)
        logger.error("can't update the etat on the database")
    conn.close()

"""

  get_etat - get the status of this programme

  Get the status of this programme in order to decide to send a good signal email or a report.

  RETURNS: non

"""
def get_etat():
    logger.info("it goinug to get the etat from the database")
    try:
        conn = psycopg2.connect(database=DATA_BASE_NAME, user=DATA_BASE_USER, password=DATA_BASE_PASSWORD,
                                host=DATA_BASE_HOST_ADDRESS, port=DATA_BASE_PORT)
    except Exception as e:
        logger.error(e)
        logger.error("connect to the database failed")
        exit(0)
    runtime = time.strftime("%Y-%m-%d", time.localtime())
    try:
        cur = conn.cursor()
        query = 'SELECT etat_code FROM etat WHERE date = %s;'
        cur.execute(query, (runtime,))
        temp_etat = cur.fetchall()[0][0]
        conn.close()
        logger.info("get the stat succeed")
        return temp_etat

    except Exception as e:
        logger.error(e)
        logger.error("get the stat failed")
        conn.close()

"""

  envoyer_bad_signal - Send email to inform the person concerned when the programme stop with serious problem

  When the programme face some problem serious which are unable be solved by the programme itself.

  RETURNS: non

"""
def envoyer_bad_signal():
    try:
        envoyer_email('The programme of collection has stopped due to some serious problems !',sujet="Outil fioul:Le programme a planté ",from_addr=EMAIL_USER, password=EMAIL_PASSWORD, to_addrs=TO_EMAIL_USERS_BON_SIGNE,smtp_server=SMTP_SERVER)
    except Exception as e:
        logger.error(e)
        logger.error("send succeed signal failed")

"""

  envoyer_bon_signal - Send email when all the prices are collected

  When the programme is going to finish, if the programme has collected all the prices, it will going to send a good signal 
  email to the people concerned.

  RETURNS: non

"""
def envoyer_bon_signal():
    try:
        envoyer_email('tout va bien!!!!!!!!!!',from_addr=EMAIL_USER, password=EMAIL_PASSWORD, to_addrs=TO_EMAIL_USERS_BON_SIGNE,smtp_server=SMTP_SERVER)
    except Exception as e:
        logger.error(e)
        logger.error("send succeed signal failed")

"""

  envoyer_rapport - Send report when some of prices aren't collected

  When the time is out and the programme haven't collected all the prices, it will goting to send a report to the person 
  concerned which will contain the information necessary.

  RETURNS: non

"""
def envoyer_rapport():
    try:
        conn = psycopg2.connect(database=DATA_BASE_NAME, user=DATA_BASE_USER, password=DATA_BASE_PASSWORD,
                                host=DATA_BASE_HOST_ADDRESS, port=DATA_BASE_PORT)
    except Exception as e:
        logger.error(e)
        logger.error("connect to the database failed")
        exit(0)
    runtime = time.strftime("%Y-%m-%d", time.localtime())
    codepostals = ''
    sites = ''
    rapport_contenu= []
    try:
        cur = conn.cursor()
        cur.execute('SELECT id, site, code_postal FROM site WHERE active = True;')
        rows = cur.fetchall()
        sites = rows
    except Exception as e:
        logger.error(e)
        logger.error("can't get the sites from database")
        conn.close()
    for site in sites:
        cur = conn.cursor()
        query = "SELECT code_postal.code_postal FROM code_postal,prix WHERE prix.code_postal=code_postal.id AND prix.date = %s AND prix.site = %s;"
        cur.execute(query,(runtime, site[0]))
        codepostals = cur.fetchall()
        temp_codepostals = []
        for codepostal in codepostals:
            temp_codepostals.append(codepostal[0])
        temp_codepostals = set(temp_codepostals)
        temp_codepostals = (set(site[2]) - temp_codepostals)
        if (len(temp_codepostals) == 0):
            continue
        temp_contenu = {'site':'', 'code_postal_loupé':''}
        temp_contenu['site'] = site[1]
        temp_contenu['code_postal_loupé'] = temp_codepostals
        rapport_contenu.append(temp_contenu)
    conn.close()
    contenu = ''
    for i in rapport_contenu:
        text ="Site:" + i['site'] + "\n"
        text = text + "code postal loupé:" + str(i['code_postal_loupé'])+ "\n\n"
        contenu = contenu + text
    try:
        envoyer_email(contenu, sujet="Rapport de récupération de prix ",from_addr=EMAIL_USER, password=EMAIL_PASSWORD, to_addrs=TO_EMAIL_USERS_REPORT,smtp_server=SMTP_SERVER)
        logger.info("send email report succeed")
    except Exception as e:
        logger.error(e)
        logger.error("send email report failed")

"""

  time_out - Verify if it is time out

  The programme should stop when it is time out, this function is used to verify if is time out or not.

  RETURNS:
  True: Time is out
  False: There are still some time to run the programme

"""
def time_out():
    nowtime = datetime.datetime.now().strftime('%H:%M:%S')
    setTime = TIME_OUT_SET
    setTimeArray = time.strptime(setTime, "%H:%M:%S")
    nowTimeArray = time.strptime(nowtime, "%H:%M:%S")
    return nowTimeArray > setTimeArray

"""

  extractPriceForReducMarket - extract the price from the price text collected for the site 

  Extract the price from the price text collected for the site.
  for example: input(785,00€) --> output(785)

  RETURNS:
  it return a string as the price

"""
def extractPriceForSite(strPrice):
    match = re.search('.*,', strPrice)
    return match.group().replace(' ','')[: -1]

"""

  ajouter_nouveaux_cps_dans_site - add new code postal to the site
  
  parameter:
  website:The site which you are going to add some new code postal
  bon_cps:The code postal that you want to add to the site

  Sometimes, some site doesn't offer fioul in some code postal, once the programme find some new code postal offered by the site,
  we should add the code postal to the site. 

  RETURNS:
  None

"""
def ajouter_nouveaux_cps_dans_site(website, bon_cps):
    logger.info("going to add some new code postal to the site" + website[1])
    try:
        conn = psycopg2.connect(database=DATA_BASE_NAME, user=DATA_BASE_USER, password=DATA_BASE_PASSWORD,
                                host=DATA_BASE_HOST_ADDRESS, port=DATA_BASE_PORT)
    except Exception as e:
        logger.error(e)
        logger.error("can't connect to the data base")
    try:
        cur = conn.cursor()
        query = "SELECT code_postal FROM site WHERE site = %s;"
        cur.execute(query, (website[1],))
        code_postal = cur.fetchall()[0][0]
        for cp in bon_cps:
            code_postal.append(cp[1])

        query ='''
UPDATE site set code_postal = %s WHERE site= %s;
'''
        cur.execute(query, (code_postal, website[1]))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(e)
        logger.error("can't selecte or update the data on the data base")
        conn.close()

"""

  add_prix - add new price date to the database

  parameter:
  website:The site which you are going to add  new price data
  code_postals:The code postal that you want to add to the site
  prix_reel:The price final (example:885)
  prix_original:The price original (it is equal to the prix_reel at this time )
  dates:The date of this price data (example:2018-07-04)
  types:The type of the fioul (exemple:standard)
  commentaire: The comment for this price data if necessary 
  
  When the programme collect the price on the site during a iteration of collection, it will call this method to add new price data
  into the database.

  RETURNS:
  None

"""
def add_prix(website, code_postals, prix_reel, prix_original, dates, types, commentaire = []):
    logger.info("site:%s \n info:going to insert date into prix table ", website[1])
    if len(commentaire) == 0 :
        for i in range(len(types)):
            commentaire.append('')
    try:
        conn = psycopg2.connect(database=DATA_BASE_NAME, user=DATA_BASE_USER, password=DATA_BASE_PASSWORD,
                                host=DATA_BASE_HOST_ADDRESS, port=DATA_BASE_PORT)
    except Exception as e:
        logger.error(e)
        logger.error("can't connect to the date base")
        exit(0)
    try:
        cur = conn.cursor()
        j = 0
        for i in code_postals:
            query = "INSERT INTO prix (code_postal,site,prix_reel,prix_original,date,type,commentaire,fournisseur) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
            cur.execute(query,(i[0], website[0], prix_reel[j], prix_original[j], dates[j], types[j],commentaire[j],website[3]))
            conn.commit()
            j = j + 1
        logger.info("site:%s \n info:succeed in inserting the data into the price table ", website[1])
        conn.close()
    except Exception as e:
        logger.error(e)
        logger.error("can't insert the date into the prix table")
        conn.close()

"""

  recuperation_carrefour_essayer - A function try to collect the price in the site carrefour 

  parameter:
  website:The site which you are going to try to collect price
  code_postals:The code postal for which you want to collect price 

  There are some code postal for which the carrefour doesn't offer the fioul, but we still need to try to collect the price in case.

  RETURNS:
  None

"""
def recuperation_carrefour_essayer(website, codepostals):
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    browser = webdriver.Firefox(executable_path=DRIVER_EXECUTABLE_PATH,
                                firefox_options=firefox_options,firefox_profile=FIREFOX_PROFILE)
    except_time = 0
    quantite = 1000
    bon_cps = []
    cps_prix_reel = []
    cps_prix_original = []
    cps_type = []
    cps_date = []
    commentaire = []
    premier_fois = True
    for i in range(5):
        try:
            logger.info("try/retry to open the site:" + website[1])
            browser.get(website[1])
            logger.info("succeed in opening this site:"+ website[1])
            break
        except Exception as e:
            browser.quit()
            logger.error("failed open the site:" + website[1])
            except_time = except_time + 1
        if (except_time == 4):
            logger.warning("After several times try, failed open the site:" + website[1])
            exit()

    for cp in codepostals:
        codepostal = cp
        cp = cp[1]
        except_signal = False
        cookie_signal = True
        popup_signal = True
        reduce_signal = True
        unhanded_error = False
        if (premier_fois == True):
            premier_fois = False
            try:
                elem = WebDriverWait(browser, 2, 0.5).until(
                    EC.presence_of_element_located((By.ID, "alersModalRefuseButton")))
            except Exception as e:
                logger.info(e)
                logger.info("site: %s \n info:The site's pub doesn't appear%s ", website[1],cp)
                reduce_signal = False
            if (reduce_signal):
                elem.click()

            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.NAME, FIOUL_CARREFOUR_CP_INPUT)))
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error: can't load code postal input element \n code postal:%s ", website[1],cp)
                except_signal = True
            if (except_signal):
                browser.refresh()
                continue
            elem.send_keys(cp)

            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.NAME, FIOUL_CARREFOUR_QUANTITE)))
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error: can't load code quantity input element \n code postal:%s ", website[1],cp)
                except_signal = True
            if (except_signal):
                browser.refresh()
                continue
            elem.send_keys(quantite)
            try:
                elem = WebDriverWait(browser, 2, 0.5).until(
                    EC.presence_of_element_located((By.ID, "tc_privacy_close")))
            except Exception as e:
                logger.info(e)
                logger.info("site: %s \n info: The cookie request doesn't appear \n code postal:%s ", website[1],cp)
                cookie_signal = False
            if (cookie_signal):
                elem.click()

            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.ID, FIOUL_CARREFOUR_DEVIS_BUTTON)))
                elem.click()
            except Exception as e:
                logger.info(e)
                logger.info("site: %s \n info:The button doesn't appear \n code postal:%s ", website[1],cp)
                except_signal = True
            if (except_signal):
                browser.refresh()
                continue
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, FIOUL_CARREFOUR_PRIX)))
            except Exception as e:
                logger.info(e)
                logger.info("site: %s \n error: can't load price element \n code postal:%s ", website[1],
                             cp)
                except_signal = True
            if (except_signal):
                continue
            prix = extractPriceForSite(elem.text)
            bon_cps.append(codepostal)
            cps_prix_reel.append(prix)
            cps_prix_original.append(prix)
            cps_type.append('standard')
            cps_date.append(time.strftime("%Y-%m-%d", time.localtime()))
            commentaire.append('')
            logger.info("site: %s\ninfo:the first collection finished in this site code postal:%s\n prix:%s ", website[1], cp, prix)
        else:
            try:
                elem = WebDriverWait(browser, 2, 0.5).until(
                    EC.presence_of_element_located((By.XPATH, FIOUL_CARREFOUR_CLOSE_BUTTON)))
                elem.click()
            except Exception as e:
                logger.info(e)
                logger.info("site: %s \n error: can't load window close element \n code postal:%s ", website[1],cp)
                unhanded_error = True
            if (unhanded_error):
                browser.refresh()

            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.NAME, FIOUL_CARREFOUR_CP_INPUT)))
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error can't load code postal element \n code postal:%s ", website[1], cp)
                except_signal = True
            if (except_signal):
                browser.refresh()
                continue
            elem.clear()
            sleep(0.1)
            elem.send_keys(cp)

            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.NAME, FIOUL_CARREFOUR_QUANTITE)))
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error can't load quantity element \n code postal:%s ", website[1], cp)
                except_signal = True
            if (except_signal):
                browser.refresh()
                continue
            elem.clear()
            sleep(0.1)
            elem.send_keys(quantite)
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.ID, FIOUL_CARREFOUR_DEVIS_BUTTON)))
                elem.click()
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error can't load button element \n code postal:%s ", website[1], cp)
                except_signal = True
            if (except_signal):
                browser.refresh()
                continue
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, FIOUL_CARREFOUR_PRIX)))
            except Exception as e:
                logger.info(e)
                logger.info("site: %s \n error can't load price element \n code postal:%s ", website[1], cp)
                except_signal = True
            if (except_signal):
                continue
            sleep(2)
            prix = extractPriceForSite(elem.text)
            bon_cps.append(codepostal)
            cps_prix_reel.append(prix)
            cps_prix_original.append(prix)
            cps_type.append('standard')
            cps_date.append(time.strftime("%Y-%m-%d", time.localtime()))
            commentaire.append('')
            logger.info("site: %s \n code postal:%s \n prix: %s ", website[1], cp, prix)
            sleep(1)
    browser.quit()
    if len(bon_cps) != 0:
        ajouter_nouveaux_cps_dans_site(website, bon_cps)
        add_prix(website, bon_cps, cps_prix_reel, cps_prix_original, cps_date, cps_type)

"""

  recuperation_carrefour_falloir - A function collect the price for all the code postal passed in the site carrefour 

  parameter:
  website:The site which you are going to collect price
  code_postals:The code postal for which you are going to collect price 

  The code postal passed to this function is supposed to collect the price completely

  RETURNS:
  None

"""
def recuperation_carrefour_falloir(website, codepostals):
    initial_length = len(codepostals)
    succeed_length = 0
    time_out_signal = False
    while True:
        if time_out_signal:
            break
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        browser = webdriver.Firefox(executable_path=DRIVER_EXECUTABLE_PATH,
                                    firefox_options=firefox_options, firefox_profile=FIREFOX_PROFILE)
        except_time = 0
        quantite = 1000
        bon_cps = []
        cps_prix_reel = []
        cps_prix_original = []
        cps_type = []
        cps_date = []
        commentaire = []
        premier_fois = True
        for i in range(5):
            try:
                logger.info("try/retry to open the site:" + website[1])
                browser.get(website[1])
                logger.info("succeed in opening this site:" + website[1])
                break
            except Exception as e:
                browser.quit()
                logger.error("failed open the site:" + website[1])
                except_time = except_time + 1
            if (except_time == 4):
                logger.warning("After several times try, failed open the site:" + website[1])
                exit()
        for cp in codepostals:
            if time_out():
                logger.warning("site:%s \n info:time out, it going to stop the programme" + website[1])
                time_out_signal = True
                break
            codepostal = cp
            cp = cp[1]
            except_signal = False
            cookie_signal = True
            popup_signal = True
            reduce_signal = True
            unhanded_error = False
            if (premier_fois == True):
                premier_fois = False
                try:
                    elem = WebDriverWait(browser, 2, 0.5).until(
                        EC.presence_of_element_located((By.ID, "alersModalRefuseButton")))
                except Exception as e:
                    logger.info(e)
                    logger.info("site: %s \n info:The site's pub doesn't appear%s ", website[1], cp)
                    reduce_signal = False
                if (reduce_signal):
                    elem.click()

                try:
                    elem = WebDriverWait(browser, 5, 0.5).until(
                        EC.presence_of_element_located((By.NAME, FIOUL_CARREFOUR_CP_INPUT)))
                except Exception as e:
                    logger.error(e)
                    logger.error("site: %s \n error: can't load code postal input element \n code postal:%s ",
                                 website[1], cp)
                    except_signal = True
                if (except_signal):
                    browser.refresh()
                    continue
                elem.send_keys(cp)

                try:
                    elem = WebDriverWait(browser, 5, 0.5).until(
                        EC.presence_of_element_located((By.NAME, FIOUL_CARREFOUR_QUANTITE)))
                except Exception as e:
                    logger.error(e)
                    logger.error("site: %s \n error: can't load code quantity input element \n code postal:%s ",
                                 website[1], cp)
                    except_signal = True
                if (except_signal):
                    browser.refresh()
                    continue
                elem.send_keys(quantite)
                try:
                    elem = WebDriverWait(browser, 2, 0.5).until(
                        EC.presence_of_element_located((By.ID, "tc_privacy_close")))
                except Exception as e:
                    logger.info(e)
                    logger.info("site: %s \n info: The cookie request doesn't appear \n code postal:%s ", website[1],cp)
                    cookie_signal = False
                if (cookie_signal):
                    elem.click()

                try:
                    elem = WebDriverWait(browser, 5, 0.5).until(
                        EC.presence_of_element_located((By.ID, FIOUL_CARREFOUR_DEVIS_BUTTON)))
                    elem.click()
                except Exception as e:
                    logger.info(e)
                    logger.info("site: %s \n info:The button doesn't appear \n code postal:%s ", website[1], cp)
                    except_signal = True
                if (except_signal):
                    browser.refresh()
                    continue
                try:
                    elem = WebDriverWait(browser, 5, 0.5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, FIOUL_CARREFOUR_PRIX)))
                except Exception as e:
                    logger.error(e)
                    logger.error("site: %s \n error: can't load price element \n code postal:%s ", website[1],cp)
                    except_signal = True
                if (except_signal):
                    continue
                prix = extractPriceForSite(elem.text)
                bon_cps.append(codepostal)
                cps_prix_reel.append(prix)
                cps_prix_original.append(prix)
                cps_type.append('standard')
                cps_date.append(time.strftime("%Y-%m-%d", time.localtime()))
                commentaire.append('')
                logger.info("site: %s\ninfo:the first collection finished in this site code postal:%s\n prix:%s ",
                            website[1], cp, prix)
            else:
                try:
                    elem = WebDriverWait(browser, 2, 0.5).until(
                        EC.presence_of_element_located((By.XPATH, FIOUL_CARREFOUR_CLOSE_BUTTON)))
                    elem.click()
                except Exception as e:
                    logger.error(e)
                    logger.error("site: %s \n error: can't load window close element \n code postal:%s ", website[1],
                                 cp)
                    unhanded_error = True
                if (unhanded_error):
                    browser.refresh()
                try:
                    elem = WebDriverWait(browser, 5, 0.5).until(
                        EC.presence_of_element_located((By.NAME, FIOUL_CARREFOUR_CP_INPUT)))
                except Exception as e:
                    logger.error(e)
                    logger.error("site: %s \n error can't load code postal element \n code postal:%s ", website[1], cp)
                    except_signal = True
                if (except_signal):
                    browser.refresh()
                    continue
                elem.clear()
                sleep(0.1)
                elem.send_keys(cp)

                try:
                    elem = WebDriverWait(browser, 5, 0.5).until(
                        EC.presence_of_element_located((By.NAME, FIOUL_CARREFOUR_QUANTITE)))
                except Exception as e:
                    logger.error(e)
                    logger.error("site: %s \n error can't load quantity element \n code postal:%s ", website[1], cp)
                    except_signal = True
                if (except_signal):
                    browser.refresh()
                    continue
                elem.clear()
                sleep(0.1)
                elem.send_keys(quantite)

                try:
                    elem = WebDriverWait(browser, 5, 0.5).until(
                        EC.presence_of_element_located((By.ID, FIOUL_CARREFOUR_DEVIS_BUTTON)))
                    elem.click()
                except Exception as e:
                    logger.error(e)
                    logger.error("site: %s \n error can't load button element \n code postal:%s ", website[1], cp)
                    except_signal = True
                if (except_signal):
                    browser.refresh()
                    continue

                try:
                    elem = WebDriverWait(browser, 5, 0.5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, FIOUL_CARREFOUR_PRIX)))
                except Exception as e:
                    logger.error(e)
                    logger.error("site: %s \n error can't load price element \n code postal:%s ", website[1], cp)
                    except_signal = True
                if (except_signal):
                    browser.refresh()
                    continue
                sleep(2)
                prix = extractPriceForSite(elem.text)
                bon_cps.append(codepostal)
                cps_prix_reel.append(prix)
                cps_prix_original.append(prix)
                cps_type.append('standard')
                cps_date.append(time.strftime("%Y-%m-%d", time.localtime()))
                commentaire.append('')
                logger.info("site: %s \n code postal:%s \n prix: %s ", website[1], cp, prix)
                sleep(5)
        browser.quit()
        logger.info("site: %s \n info:one end of the cycle \n", website[1])
        if len(bon_cps) != 0:
            succeed_length = succeed_length + len(bon_cps)
            codepostals = list(set(codepostals) - set(bon_cps))
            add_prix(website, bon_cps, cps_prix_reel, cps_prix_original, cps_date, cps_type,commentaire)
        if succeed_length == initial_length:
            logger.info("site: %s \n info:end of the collection of price, collection succeed \n", website[1])
            break

"""

  recuperation_reduc_essayer - A function try to collect the price in the site reduc 

  parameter:
  website:The site which you are going to try to collect price
  code_postals:The code postal for which you want to collect price 

  There are some code postal for which the reduc doesn't offer the fioul, but we still need to try to collect the price in case.

  RETURNS:
  None

"""
def recuperation_reduc_essayer(website, codepostals):
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    try:
        browser = webdriver.Firefox(executable_path=DRIVER_EXECUTABLE_PATH,
                                    firefox_options=firefox_options, firefox_profile=FIREFOX_PROFILE)
    except Exception as e:
        logger.error(e)
        logger.error("init webdriver failed,due to executable_path or/and firefox_profile")

    except_time = 0
    quantite = 1000
    email = 'toto@gmail.com'
    bon_cps = []
    cps_prix_reel = []
    cps_prix_original = []
    cps_type = []
    cps_date = []
    cps_commentaire = []
    for i in range(5):
        try:
            logger.info("try/retry to open the site:" + website[1])
            browser.get(website[1])
            logger.info("succeed in opening this site:"+ website[1])
            break
        except Exception as e:
            browser.quit()
            logger.error("failed open the site:" + website[1])
            except_time = except_time + 1
        if (except_time == 4):
            logger.warning("After several times try, failed open the site:" + website[1])
            exit()

    for cp in codepostals:
        fioul_type = 'standard'
        codepostal = cp
        cp = cp[1]
        except_signal = False
        livraison = False
        try:
            elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located((By.NAME, FIOUL_REDUC_CP_INPUT)))
        except Exception as e:
            logger.error(e)
            logger.error("site: %s \n error: can't load code postal input element \n code postal:%s ", website[1], cp)
            except_signal = True
        if (except_signal):
            browser.refresh()
            continue
        elem.clear()
        sleep(0.1)
        elem.send_keys(cp)
        try:
            elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located((By.NAME, FIOUL_REDUC_QUANTITE)))
        except Exception as e:
            logger.error(e)
            logger.error("site: %s \n error: can't load quantity input element \n code postal:%s ", website[1], cp)
            except_signal = True
        if (except_signal):
            browser.refresh()
            continue
        elem.clear()
        sleep(0.1)
        elem.send_keys(quantite)
        try:
            elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located((By.NAME, FIOUL_REDUC_EMAIL)))
        except Exception as e:
            logger.error(e)
            logger.error("site: %s \n error: can't load email input element \n code postal:%s ", website[1], cp)
            except_signal = True
        if (except_signal):
            browser.refresh()
            continue
        elem.clear()
        sleep(0.1)
        elem.send_keys(email)
        try:
            elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located((By.ID, FIOUL_REDUC_BUTTON)))
        except Exception as e:
            logger.error(e)
            logger.error("site: %s \n error: can't load click button element \n code postal:%s ", website[1], cp)
            except_signal = True
        if (except_signal):
            browser.refresh()
            continue
        try:
            elem.click()
        except Exception as e:
            logger.error(e)
            logger.error("site: %s \n error: can't click the button,may be il was block by other element \n code postal:%s ", website[1], cp)
            except_signal = True
        if (except_signal):
            browser.refresh()
            continue
        try:
            elem = WebDriverWait(browser, 5, 0.5).until(
                EC.presence_of_element_located(
                    (By.XPATH, FIOUL_REDUC_LIVRAISON_RAPIDE)))
            cps_commentaire.append('')
            elem.click()
        except Exception as e:
            logger.warning("site: %s \n info: can't locate the options of livraison.possibility:\n 1.the site don't supply for this code postal \n 2.the site don't allow chose the type of livraison temporary\n code postal:%s ", website[1], cp)
            try :
                logger.info(
                    "site: %s \n info: try to locate close button \n code postal:%s ",
                    website[1], cp)
                elem = browser.find_element_by_xpath('/html/body/div[3]/div[1]/button')
                logger.info("located the close button")
            except Exception as e:
                logger.info(e)
                logger.info("site: %s \n info:the site don't allow chose the type of livraison temporary \n code postal:%s ", website[1], cp)
                livraison = True
            if livraison:
                elem = browser.find_element_by_xpath('//*[@id="order-block-delivery"]/div[1]/div[2]/div/p[1]')
                cps_commentaire.append(elem.text)
            else:
                elem.click()
                logger.info(
                    "site: %s \n info:the site don't supply for this code postal temporary \n code postal:%s ",
                    website[1], cp)
                continue

        try:
            elem = WebDriverWait(browser, 5, 0.5).until(
                EC.presence_of_element_located(
                    (By.XPATH, FIOUL_REDUC_TYPE_ORDINAIRE)))
        except Exception as e:
            logger.error(e)
            logger.error("site: %s \n error:can't locate the fioul type element \n code postal:%s ",
                    website[1], cp)
            browser.back()
            except_signal = True

        if (except_signal):
            continue
        if 'active' in elem.get_attribute('class'):
            pass
        else:
            elem.click()
            sleep(2)
            elem = browser.find_element_by_xpath(FIOUL_REDUC_TYPE_ORDINAIRE)
            if 'active' in elem.get_attribute('class'):
                pass
            else:
                fioul_type = 'superieur'
        try:
            elem = WebDriverWait(browser, 5, 0.5).until(
                EC.presence_of_element_located((By.ID, FIOUL_REDUC_PRIX)))
        except Exception as e:
            logger.error(e)
            logger.error("site: %s \n error:can't locate the price element \n code postal:%s ",
                    website[1], cp)
            except_signal = True
        if (except_signal):
            browser.back()
            continue
        sleep(1.5)
        prix = elem.text
        if prix == '':
            sleep(2)
            prix = elem.text
            if prix == '':
                sleep(2)
                prix = elem.text
                if prix == '':
                    logger.error("site: %s \n the price element don't contain the price \n code postal:%s ",
                    website[1], cp)
                    browser.back()
                    continue
        prix = extractPriceForSite(prix)
        bon_cps.append(codepostal)
        cps_prix_reel.append(prix)
        cps_prix_original.append(prix)
        cps_type.append(fioul_type)
        cps_date.append(time.strftime("%Y-%m-%d", time.localtime()))
        logger.info("site: %s \n info:succeed in collecting the price  \n code postal:%s \n price:%s",
                     website[1], cp, prix)
        browser.back()
    browser.quit()
    if len(bon_cps)!=0:
        ajouter_nouveaux_cps_dans_site(website, bon_cps)
        add_prix(website, bon_cps, cps_prix_reel, cps_prix_original, cps_date, cps_type, cps_commentaire)

"""

  recuperation_reduc_falloir - A function collect the price for all the code postal passed in the site reduc 

  parameter:
  website:The site which you are going to collect price
  code_postals:The code postal for which you are going to collect price 

  The code postal passed to this function is supposed to collect the price completely

  RETURNS:
  None

"""
def recuperation_reduc_falloir(website, codepostals):
    initial_length = len(codepostals)
    succeed_length = 0
    time_out_signal = False
    while True:
        if time_out_signal:
            break
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        try:
            browser = webdriver.Firefox(executable_path=DRIVER_EXECUTABLE_PATH,
                                        firefox_options=firefox_options, firefox_profile=FIREFOX_PROFILE)
        except Exception as e:
            logger.error(e)
            logger.error("init webdriver failed,due to executable_path or/and firefox_profile")
        except_time = 0
        quantite = 1000
        email = 'toto@gmail.com'
        bon_cps = []
        cps_prix_reel = []
        cps_prix_original = []
        cps_type = []
        cps_date = []
        cps_commentaire = []
        for i in range(5):
            try:
                logger.info("try/retry to open the site:" + website[1])
                browser.get(website[1])
                logger.info("succeed in opening this site:" + website[1])
                break
            except Exception as e:
                browser.quit()
                logger.error("failed open the site:" + website[1])
                except_time = except_time + 1
            if (except_time == 4):
                logger.warning("After several times try, failed open the site:" + website[1])
                exit()

        for cp in codepostals:
            fioul_type = 'standard'
            if time_out():
                logger.warning("site:%s \n info:time out, it going to stop the programme" + website[1])
                time_out_signal = True
                break
            codepostal = cp
            cp = cp[1]
            except_signal = False
            livraison = False
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located((By.NAME, FIOUL_REDUC_CP_INPUT)))
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error: can't load code postal input element \n code postal:%s ", website[1],cp)
                except_signal = True
            if (except_signal):
                browser.refresh()
                continue
            elem.clear()
            sleep(0.1)
            elem.send_keys(cp)
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located((By.NAME, FIOUL_REDUC_QUANTITE)))
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error: can't load quantity input element \n code postal:%s ", website[1], cp)
                except_signal = True
            if (except_signal):
                browser.refresh()
                continue
            elem.clear()
            sleep(0.1)
            elem.send_keys(quantite)
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located((By.NAME, FIOUL_REDUC_EMAIL)))
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error: can't load email input element \n code postal:%s ", website[1], cp)
                except_signal = True
            if (except_signal):
                browser.refresh()
                continue
            elem.clear()
            sleep(0.1)
            elem.send_keys(email)
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.ID, FIOUL_REDUC_BUTTON)))
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error: can't load click button element \n code postal:%s ", website[1], cp)
                except_signal = True
            if (except_signal):
                browser.refresh()
                continue
            try:
                elem.click()
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error: can't click the button,may be il was block by other element \n code postal:%s ",
                    website[1], cp)
                except_signal = True
            if (except_signal):
                browser.refresh()
                continue
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, FIOUL_REDUC_LIVRAISON_RAPIDE)))
                cps_commentaire.append('')
                elem.click()
            except Exception as e:
                logger.warning(
                    "site: %s \n info: can't locate the options of livraison.possibility:\n 1.the site don't supply for this code postal \n 2.the site don't allow chose the type of livraison temporary\n code postal:%s ",
                    website[1], cp)
                try:
                    logger.info(
                        "site: %s \n info: try to locate close button \n code postal:%s ",
                        website[1], cp)
                    elem = browser.find_element_by_xpath('/html/body/div[3]/div[1]/button')
                    logger.info("located the close button")
                except Exception as e:
                    logger.info(e)
                    logger.info(
                        "site: %s \n info:the site don't allow chose the type of livraison temporary \n code postal:%s ",
                        website[1], cp)
                    livraison = True
                if livraison:
                    elem = browser.find_element_by_xpath('//*[@id="order-block-delivery"]/div[1]/div[2]/div/p[1]')
                    cps_commentaire.append(elem.text)
                else:
                    elem.click()
                    logger.info(
                        "site: %s \n info:the site don't supply for this code postal temporary \n code postal:%s ",
                        website[1], cp)
                    continue

            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, FIOUL_REDUC_TYPE_ORDINAIRE)))
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error:can't locate the fioul type element \n code postal:%s ",
                             website[1], cp)
                browser.back()
                except_signal = True

            if (except_signal):
                continue
            if 'active' in elem.get_attribute('class'):
                pass
            else:
                elem.click()
                sleep(2)
                elem = browser.find_element_by_xpath(FIOUL_REDUC_TYPE_ORDINAIRE)
                if 'active' in elem.get_attribute('class'):
                    pass
                else:
                    fioul_type = 'superieur'
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.ID, FIOUL_REDUC_PRIX)))
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error:can't locate the price element \n code postal:%s ",
                             website[1], cp)
                except_signal = True
            if (except_signal):
                browser.back()
                continue
            sleep(1.5)
            prix = elem.text
            if prix == '':
                sleep(2)
                prix = elem.text
                if prix == '':
                    sleep(2)
                    prix = elem.text
                    if prix == '':
                        logger.error("site: %s \n the price element don't contain the price \n code postal:%s ",
                                     website[1], cp)
                        browser.back()
                        continue
            prix = extractPriceForSite(prix)
            bon_cps.append(codepostal)
            cps_prix_reel.append(prix)
            cps_prix_original.append(prix)
            cps_type.append(fioul_type)
            cps_date.append(time.strftime("%Y-%m-%d", time.localtime()))
            logger.info("site: %s \n info:succeed in collecting the price  \n code postal:%s \n price:%s",
                        website[1], cp, prix)
            browser.back()
        browser.quit()
        logger.info("site: %s \n info:one end of the cycle \n",website[1])
        if len(bon_cps) != 0:
            succeed_length = succeed_length + len(bon_cps)
            codepostals = list(set(codepostals)-set(bon_cps))
            add_prix(website, bon_cps, cps_prix_reel, cps_prix_original, cps_date, cps_type,cps_commentaire)
        if succeed_length == initial_length:
            logger.info("site: %s \n info:end of the collection of price, collection succeed \n", website[1])
            break

"""

  recuperation_market_essayer - A function try to collect the price in the site market 

  parameter:
  website:The site which you are going to try to collect price
  code_postals:The code postal for which you want to collect price 

  There are some code postal for which the market doesn't offer the fioul, but we still need to try to collect the price in case.

  RETURNS:
  None

"""
def recuperation_market_essayer(website, codepostals):
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    browser = webdriver.Firefox(executable_path=DRIVER_EXECUTABLE_PATH,
                                firefox_options=firefox_options,firefox_profile=FIREFOX_PROFILE)
    except_time = 0
    bon_cps = []
    cps_prix_reel = []
    cps_prix_original = []
    cps_type = []
    cps_date = []
    commentaire = []
    for i in range(5):
        try:
            logger.info("try/retry to open the site:" + website[1])
            browser.get(website[1])
            logger.info("succeed in opening this site:" + website[1])
            break
        except Exception as e:
            browser.quit()
            logger.error("failed open the site:" + website[1])
            except_time = except_time + 1
        if (except_time == 4):
            logger.warning("After several times try, failed open the site:" + website[1])
            exit()


    for cp in codepostals:
        fioul_type = 'standard'
        codepostal = cp
        cp = cp[1]
        except_signal = False
        try:
            elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located(
                (By.XPATH, "//input[@class='js-PostalCode-input main-postal-code']")))
        except Exception as e:
            logger.info(e)
            logger.info("site: %s \n info:can't load the code postal element %s ", website[1], cp)
            except_signal = True
        if (except_signal):
            continue
        elem.clear()
        elem.send_keys(cp)
        try:
            elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located(
                (By.XPATH, '//form[@class="form-command-fioul decli2 js-PostalCode-form"]/div[2]/button')))
        except Exception as e:
            logger.info(e)
            logger.info("site: %s \n info:The button doesn't appear \n code postal:%s ", website[1], cp)
            except_signal = True
        if (except_signal):
            continue
        elem.click()
        try:
            elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='main']/div[1]/div/aside/div/div[1]/div[1]/div/div[2]/div[2]/span[2]/span")))
        except Exception as e:
            logger.info(e)
            logger.info("site: %s \n info:The fioul type lable doesn't appear \n code postal:%s ", website[1], cp)

        if(len(elem.text)):
            pass
        else:
            sleep(2)
        if 'ordinaire' in elem.text:
            pass
        else:
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located(
                    (By.XPATH, "//form[@id = 'tunnel-step-one']/div[2]/p[2]/label")))
                elem.click()
                sleep(2)
                temps_type = browser.find_element_by_xpath("//*[@id='main']/div[1]/div/aside/div/div[1]/div[1]/div/div[2]/div[2]/span[2]/span")
                if 'ordinaire' in temps_type.text:
                    pass
                else:
                    fioul_type = 'superieur'
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n info:The fioul standard lable doesn't appear \n code postal:%s ", website[1],cp)
                except_signal = True
            if except_signal:
                continue

        try:
            elem = WebDriverWait(browser, 5, 0.5).until(
                EC.presence_of_element_located((By.XPATH, FIOUL_MARKET_LIVRAISON)))
            elem.click()
        except Exception as e:
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.ID, 'title-for-commune')))
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error: can't load livraison element \n code postal:%s ", website[1], cp)
                except_signal = True

        if (except_signal):
            continue
        try:
            elem = WebDriverWait(browser, 5, 0.5).until(
                EC.presence_of_element_located((By.NAME, FIOUL_MARKET_QUANTITE)))
            elem.clear()
            elem.send_keys('1000')
            sleep(5)
        except Exception as e:
            logger.error(e)
            logger.error("site: %s \n error: can't load quantity element \n code postal:%s ", website[1], cp)
            except_signal = True
        if (except_signal):
            continue
        try:
            elem = WebDriverWait(browser, 5, 0.5).until(
                EC.presence_of_element_located((By.XPATH, FIOUL_MARKET_PRIX)))
        except Exception as e:
            logger.error(e)
            logger.error("site: %s \n error: can't load prix element \n code postal:%s ", website[1], cp)
            except_signal = True
        if (except_signal):
            continue
        prix = elem.text
        if prix =='':
            sleep(2)
            prix = elem.text
            if prix =='':
                sleep(2)
                prix = elem.text
                if prix == '':
                    logger.error("site: %s \n the price element don't contain the price \n code postal:%s ",
                                website[1], cp)
                    browser.back()
                    continue
        prix = extractPriceForSite(prix)
        prix = str(int(prix))
        bon_cps.append(codepostal)
        cps_prix_reel.append(prix)
        cps_prix_original.append(prix)
        cps_type.append(fioul_type)
        cps_date.append(time.strftime("%Y-%m-%d", time.localtime()))
        commentaire.append('')
        logger.info("site: %s\ncode postal:%s\n prix:%s ", website[1], cp, prix)
        browser.back()
    browser.quit()
    if len(bon_cps)!=0:
        ajouter_nouveaux_cps_dans_site(website, bon_cps)
        add_prix(website, bon_cps, cps_prix_reel, cps_prix_original, cps_date, cps_type)

"""

  recuperation_market_falloir - A function collect the price for all the code postal passed in the site market 

  parameter:
  website:The site which you are going to collect price
  code_postals:The code postal for which you are going to collect price 

  The code postal passed to this function is supposed to collect the price completely

  RETURNS:
  None

"""
def recuperation_market_falloir(website, codepostals):
    initial_length = len(codepostals)
    succeed_length = 0
    time_out_signal = False
    while True:
        if time_out_signal:
            break
        firefox_options = Options()
        # firefox_options.add_argument("--headless")
        browser = webdriver.Firefox(executable_path=DRIVER_EXECUTABLE_PATH,
                                    firefox_options=firefox_options, firefox_profile=FIREFOX_PROFILE)
        except_time = 0
        bon_cps = []
        cps_prix_reel = []
        cps_prix_original = []
        cps_type = []
        cps_date = []
        commentaire = []
        for i in range(5):
            try:
                logger.info("try/retry to open the site:" + website[1])
                browser.get(website[1])
                logger.info("succeed in opening this site:" + website[1])
                break
            except Exception as e:
                browser.quit()
                logger.error("failed open the site:" + website[1])
                except_time = except_time + 1
            if (except_time == 4):
                logger.warning("After several times try, failed open the site:" + website[1])
                exit()

        for cp in codepostals:
            fioul_type = 'standard'
            if time_out():
                logger.warning("site:%s \n info:time out, it going to stop the programme" + website[1])
                time_out_signal = True
                break
            codepostal = cp
            cp = cp[1]
            except_signal = False
            commune_signal = False
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located(
                    (By.XPATH, FIOUL_MARKET_CP_INPUT)))
            except Exception as e:
                logger.info(e)
                logger.info("site: %s \n info:can't load the code postal element%s ", website[1], cp)
                except_signal = True
            if (except_signal):
                continue
            elem.clear()
            elem.send_keys(cp)
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located(
                    (By.XPATH, FIOUL_MARKET_BUTTON)))
            except Exception as e:
                logger.info(e)
                logger.info("site: %s \n info:The button doesn't appear \n code postal:%s ", website[1], cp)
                except_signal = True
            if (except_signal):
                continue
            elem.click()
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located(
                    (By.XPATH,
                     FIOUL_MARKET_FIOUL_TYPE)))

            except Exception as e:
                logger.info(e)
                logger.info("site: %s \n info:The fioul type lable doesn't appear \n code postal:%s ", website[1], cp)
            if (len(elem.text)):
                pass
            else:
                sleep(2)
            if 'ordinaire' in elem.text:
                pass
            else:
                try:
                    elem = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located(
                        (By.XPATH, FIOUL_MARKET_FIOUL_ORDINAIRE)))
                    elem.click()
                    sleep(2)
                    temps_type = browser.find_element_by_xpath(
                        FIOUL_MARKET_FIOUL_TYPE)
                    if 'ordinaire' in temps_type.text:
                        pass
                    else:
                        fioul_type = 'superieur'
                except Exception as e:
                    logger.error(e)
                    logger.error("site: %s \n info:The fioul standard lable doesn't appear \n code postal:%s ",
                                 website[1], cp)
                    except_signal = True
                if except_signal:
                    continue
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="content-delivery-range"]/table/tbody/tr[2]/td[2]')))
                elem.click()
            except Exception as e:
                try:
                    elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.ID, 'title-for-commune')))
                    commune_signal = True
                except Exception as e:
                    logger.error(e)
                    logger.error("site: %s \n error: can't load livraison element \n code postal:%s ", website[1], cp)
                    except_signal = True

            if (except_signal):
                continue
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.NAME, 'form[volume]')))
                elem.clear()
                elem.send_keys('1000')
                sleep(8)
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error: can't load quantity element \n code postal:%s ", website[1], cp)
                except_signal = True
            if (except_signal):
                continue
            try:
                elem = WebDriverWait(browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.XPATH, FIOUL_MARKET_PRIX)))
            except Exception as e:
                logger.error(e)
                logger.error("site: %s \n error: can't load prix element \n code postal:%s ", website[1], cp)
                except_signal = True
            if (except_signal):
                continue
            prix = elem.text
            if prix == '':
                sleep(2)
                prix = elem.text
                if prix == '':
                    sleep(2)
                    prix = elem.text
                    if prix == '':
                        logger.error("site: %s \n the price element don't contain the price \n code postal:%s ",
                                     website[1], cp)
                        browser.back()
                        continue
            prix = extractPriceForSite(prix)
            if commune_signal:
                prix = str(int(prix) + 30)
            else:
                prix = str(int(prix))
            bon_cps.append(codepostal)
            cps_prix_reel.append(prix)
            cps_prix_original.append(prix)
            cps_type.append(fioul_type)
            cps_date.append(time.strftime("%Y-%m-%d", time.localtime()))
            commentaire.append('')
            logger.info("site: %s\n code postal:%s\n prix:%s ",
                        website[1], cp, prix)
            browser.back()
        browser.quit()
        logger.info("site: %s \n info:one end of the cycle \n", website[1])
        if len(bon_cps) != 0:
            succeed_length = succeed_length + len(bon_cps)
            codepostals = list(set(codepostals) - set(bon_cps))
            add_prix(website, bon_cps, cps_prix_reel, cps_prix_original, cps_date, cps_type,commentaire)
        if succeed_length == initial_length:
            logger.info("site: %s \n info:end of the collection of price, collection succeed \n", website[1])
            break

"""

  comparer_cp - compare the code_postal_site and the code_postals_tout in order to get the code postal for which the programme need 
  to try to collect the price of fioul

  parameter:
  code_postals_site:The code postal for which the site offer the fioul
  code_postals_tout:All the code postal for which auchan want to collect the price of fioul

  Compare the code_postal_site and the code_postals_tout in order to get the code postal for which the programme need 
  to try to collect the price of fioul and the code postal for which the programme is supposed to collect the price of fioul

  RETURNS:
  code_postals_obligatoire:the code postal for which the programme is supposed to collect the price of fioul
  code_postals_essaye:the code postal for which the programme need to try to collect the price of fioul
"""
def comparer_cp(code_postals_site, code_postals_tout):
    code_postals_obligatoire = []
    code_postals_essaye = []
    for i in code_postals_tout:
        if i[1] in code_postals_site[2]:
            code_postals_obligatoire.append(i)
        else:
            code_postals_essaye.append(i)
    return code_postals_obligatoire,code_postals_essaye

"""

  recuperation_market - a function which is used to collect the price of fioul for the site market

  parameter:
  site:It contains all the information necessary for the site(id of site, URL of site, code postal offered by the site etc)
  codepostals:All the code postal for which auchan want to collect the price of fioul and some other information necessary for 
  the code postal (id of code postal)

  a function which is used to collect the price of fioul for the site market, it will call the funtion of comparer_cp, and the return 
  result of the function comparer_cp will be used for recuperation_market_essayer and recuperation_market_falloir
  
  RETURNS:
  None
"""
def recuperation_market(site, codepostals):
    logger.info("Begin to collect the price from %s",site[1])
    code_postals_obligatoire, code_postals_essaye = comparer_cp(site, codepostals)
    logger.info("site:%s \n code postal obligatoire:%s \n code postal essay:%s",site[1], code_postals_obligatoire, code_postals_essaye)
    if len(code_postals_essaye) != 0:
        recuperation_market_essayer(site, code_postals_essaye)
    recuperation_market_falloir(site, code_postals_obligatoire)

"""

  recuperation_market - a function which is used to collect the price of fioul for the site reduc

  parameter:
  site:It contains all the information necessary for the site(id of site, URL of site, code postal offered by the site etc)
  codepostals:All the code postal for which auchan want to collect the price of fioul and some other information necessary for 
  the code postal (id of code postal)

  a function which is used to collect the price of fioul for the site reduc, it will call the funtion of comparer_cp, and the return 
  result of the function comparer_cp will be used for recuperation_reduc_essayer and recuperation_reduc_falloir

  RETURNS:
  None
"""
def recuperation_reduc(site, codepostals):
    logger.info("Begin to collect the price from %s",site[1])
    code_postals_obligatoire, code_postals_essaye = comparer_cp(site, codepostals)
    logger.info("site:%s \n code postal obligatoire:%s \n code postal essay:%s",site[1], code_postals_obligatoire, code_postals_essaye)
    if len(code_postals_essaye) != 0:
        recuperation_reduc_essayer(site, code_postals_essaye)
    recuperation_reduc_falloir(site, code_postals_obligatoire)

"""

  recuperation_market - a function which is used to collect the price of fioul for the site carrefour

  parameter:
  site:It contains all the information necessary for the site(id of site, URL of site, code postal offered by the site etc)
  codepostals:All the code postal for which auchan want to collect the price of fioul and some other information necessary for 
  the code postal (id of code postal)

  a function which is used to collect the price of fioul for the site market, it will call the funtion of comparer_cp, and the return 
  result of the function comparer_cp will be used for recuperation_carrefour_essayer and recuperation_carrefour_falloir

  RETURNS:
  None
"""
def recuperation_carrefour(site, codepostals):
    logger.info("Begin to collect the price from %s",site[1])
    code_postals_obligatoire, code_postals_essaye = comparer_cp(site, codepostals)
    logger.info("site:%s \n code postal obligatoire:%s \n code postal essay:%s",site[1], code_postals_obligatoire, code_postals_essaye)
    if len(code_postals_essaye) != 0:
        recuperation_carrefour_essayer(site, code_postals_essaye)
    recuperation_carrefour_falloir(site, code_postals_obligatoire)

"""

  recuperation_market - a function which is used to collect the price of one site

  parameter:
  site:It contains all the information necessary for the site(id of site, URL of site, code postal offered by the site etc)
  codepostals:All the code postal for which auchan want to collect the price of fioul and some other information necessary for 
  the code postal (id of code postal)

  This function will call the recuperation_xxx according to the site passed to this function

  RETURNS:
  None
"""
def recuperation(site, codepostals):
    if site[1] == 'https://www.fioulmarket.fr/':
        recuperation_market(site, codepostals)
    elif site[1] == 'https://www.fioulreduc.com/':
        recuperation_reduc(site, codepostals)
    elif site[1] == 'http://www.carrefour.fr/services/fioul-domestique/':
        recuperation_carrefour(site, codepostals)
    else:
        logger.warning("There are no function to treat this site:" + site[1])

#
#  连接数据库 获取数据（cp, site）
#
#
if __name__=='__main__':

    init_program()
    begin = time.clock()
    etat_init()

    try:
        logger.info('try to connect to the database in order to get all the code postals')
        conn = psycopg2.connect(database=DATA_BASE_NAME, user=DATA_BASE_USER, password=DATA_BASE_PASSWORD,
                                host=DATA_BASE_HOST_ADDRESS, port=DATA_BASE_PORT)
    except Exception as e:
        logger.error(e)
        logger.error("can't connect to the database")
        exit(0)
    logger.info("connection succeed")
    codepostals = ''
    sites = ''
    try:
        logger.info("try to select code postals and sites from database")
        cur = conn.cursor()
        cur.execute('SELECT id, code_postal FROM code_postal WHERE active = True;')
        rows = cur.fetchall()
        codepostals = rows
        cur.execute('SELECT id, site, code_postal, fournisseur FROM site WHERE active = True;')
        rows = cur.fetchall()
        sites = rows
    except Exception as e:
        logger.error("selection of code postal and sites from database failed")
        logger.error(e)
        conn.close()
    logger.info('selection of code postal and sites from database succeed')
    conn.close()
    date_num = 0
    for site in sites:
        date_num = date_num + len(site[2])
     #
     # 循环开始
     # thread
    try:
        logger.info('begin to lance the thread')
        thread_list = []
        for site in sites:
            t = threading.Thread(target=recuperation,args=(site, codepostals,), name='open_thread')
            thread_list.append(t)
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        logger.info('lance the thread succeed')
    except Exception as e:
        logger.error(e)
        logger.error("lance the thread failed or the theread stop when lancing")

    if time_out():
        logger.warning('Program finished with time out, it going to set the etat as 2')
        etat_set(2)
    else:
        logger.info("Program finish with success, it going to set the etat as 1")
        etat_set(1)

    if(get_etat() == 1):
        logger.info("it going to send a succeed signal")
        envoyer_bon_signal()
    elif(get_etat() == 2):
        logger.info('it going to send a report of this collection')
        envoyer_rapport()

    finish = time.clock()
    logger.info('This program this time spent %d s',finish-begin)

