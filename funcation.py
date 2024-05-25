import csv
import logging
import os
import re
import shutil
import time
import xml.etree.cElementTree as ET
from datetime import date, datetime, timedelta
from xml.etree import ElementTree
# import htmlmin
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
# import ml.cpv_classifier as classifier
# from gec_common.web_application_properties import *
# from false_cpv import false_cpv
import requests
# import speech_recognition as sr
from os import path
# from pydub import AudioSegment
import uuid
import glob
# from webdriver_manager.chrome import ChromeDriverManager
# import pdfplumber 
import requests
# import PyPDF2
# from PyPDF2 import PdfReader
import pandas as pd
# from csv import DictReader

EPROCUREMENT_SCRAPE_FROM_DAYS_AGO = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s, %(levelname)s: %(message)s")


def today_formatted():
    return date.today().strftime('%Y-%m-%d')


def today_formatted_for_saving_output_xmls():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def get_string_between(extract, start, end):
    extract = ' ' + extract
    try:
        ini = extract.index(start)
    except:
        return ''
    if (ini == 0):
        return ''
    ini += len(start)
    newSrting = extract[ini:]
    end_position = newSrting.index(end)
    output = newSrting[:end_position]
    return output


def get_after(extract, start, length):
    try:
        ini = extract.index(start)
    except:
        return ''

    if (ini == 0):
        return ''
    ini += len(start)
    end = ini + length
    output = extract[ini:end]
    return output


def unique(list1):
    # intilize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    return unique_list


def get_email(text):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    if (len(emails) > 0):
        return emails[0]
    else:
        return ''


def load_page_by_locator(driver: WebDriver, url: str, locator=None, timeout_seconds=5):
    MAX_LOAD_PAGE_ATTEMPTS = 2
    for loop_counter in range(1, MAX_LOAD_PAGE_ATTEMPTS):
        try:
            driver.get(url)
            if locator is not None:
                element_present = expected_conditions.presence_of_element_located(locator)
                WebDriverWait(driver, timeout_seconds).until(element_present)
            else:
                time.sleep(5)
            return
        except TimeoutException as e:
            if loop_counter == MAX_LOAD_PAGE_ATTEMPTS:
                raise e
            else:
                pass


def load_page(driver: WebDriver, url: str, timeout_seconds=5):
    return load_page_by_locator(driver, url, None, timeout_seconds)


def load_page_expect_id(driver: WebDriver, url: str, wait_fo_element_with_id: str, timeout_seconds=5):
    assert wait_fo_element_with_id is not None
    return load_page_by_locator(driver, url, (By.ID, wait_fo_element_with_id), timeout_seconds)


def load_page_expect_xpath(driver: WebDriver, url, wait_of_element_with_xpath: str, timeout_seconds=5):
    assert wait_of_element_with_xpath is not None
    return load_page_by_locator(driver, url, (By.XPATH, wait_of_element_with_xpath), timeout_seconds)


def init_chrome_driver(arguments=[], experimental_options={}):
    MAX_LOAD_DRIVER_ATTEMPTS = 10

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage') 
    for argument in arguments:
        options.add_argument(argument)
    for key, value in experimental_options.items():
        options.add_experimental_option(key, value)

    for loop_counter in range(1, MAX_LOAD_DRIVER_ATTEMPTS + 1):
        try:
            #driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
            driver = webdriver.Chrome(options=options)
            if driver is not None:
                return driver
        except WebDriverException as e:
            if loop_counter == MAX_LOAD_DRIVER_ATTEMPTS:
                raise e
            else:
                pass

def init_chrome_driver_head(arguments=[], experimental_options={}):
    MAX_LOAD_DRIVER_ATTEMPTS = 10

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage') 
    for argument in arguments:
        options.add_argument(argument)
    for key, value in experimental_options.items():
        options.add_experimental_option(key, value)

    for loop_counter in range(1, MAX_LOAD_DRIVER_ATTEMPTS + 1):
        try:
            #driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
            driver = webdriver.Chrome(options=options)
            if driver is not None:
                return driver
        except WebDriverException as e:
            if loop_counter == MAX_LOAD_DRIVER_ATTEMPTS:
                raise e
            else:
                pass

def init_chrome_driver_vpn(arguments=[], experimental_options={}):
    MAX_LOAD_DRIVER_ATTEMPTS = 10

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage') 
    options.add_extension("Urban-Free-VPN-proxy-Unblocker---Best-VPN.crx")
    for argument in arguments:
        options.add_argument(argument)
    for key, value in experimental_options.items():
        options.add_experimental_option(key, value)

    for loop_counter in range(1, MAX_LOAD_DRIVER_ATTEMPTS + 1):
        try:
            #driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
            driver = webdriver.Chrome(options=options)
            time.sleep(20)
            if driver is not None:
                return driver
        except WebDriverException as e:
            if loop_counter == MAX_LOAD_DRIVER_ATTEMPTS:
                raise e
            else:
                pass


def captcha(audio_url):
    doc = requests.get(audio_url)
    file_name = str(uuid.uuid4())
    with open(TMP_DIR + '/' + file_name + '.mp3', 'wb') as f:
        f.write(doc.content)
    time.sleep(10)
    sound = AudioSegment.from_mp3(TMP_DIR + '/' + file_name + '.mp3')
    sound.export(TMP_DIR + '/' + file_name + '.wav', format="wav")
    time.sleep(10)
    r = sr.Recognizer()
    with sr.AudioFile(TMP_DIR + '/' + file_name + '.wav') as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text)
        except:
            pass
    mp3file = TMP_DIR + '/' + file_name + '.mp3'
    wavfile = TMP_DIR + '/' + file_name + '.wav'
    os.remove(mp3file)
    os.remove(wavfile)
    return text


def CPV_mapping(filename,category = None):
    cpvs= []
    if category is not None:
        category = category.lower()
        if ',' in category or '.' in category:
            category = category.replace(',','')
            category = category.replace('.','')
        file_path = ASSETS_PATH+filename
        with open(file_path, 'r',encoding = 'cp437') as f:
            reader = csv.reader(f)
            maps = list(reader)
            CPV_mapping = dict(maps)
        try:
            cpv = CPV_mapping.get(category)
            cpvss = cpv.split('#')
            for cpv in cpvss:
                if cpv == '':
                    pass
                else:
                    cpvs.append(cpv.strip())
        except:
            pass
    return cpvs

    
def bytes_converter(filesize):
    try:
        if 'kb' in filesize.lower() or 'kilobytes' in filesize.lower():
            filesize = filesize.lower().replace('kb','').replace('kilobytes','').replace(',','.').strip()
            filesize_bytes = float(filesize) * 1024
        elif 'mb' in filesize.lower() or 'megabytes' in filesize.lower():
            filesize = filesize.lower().replace('mb','').replace('megabytes','').replace(',','.').strip()
            filesize_bytes = float(filesize) * 1024 * 1024
        elif 'gb' in filesize.lower() or 'gigabytes' in filesize.lower():
            filesize = filesize.lower().replace('gb','').replace('gigabytes','').replace(',','.').strip()
            filesize_bytes = float(filesize) * 1024 * 1024 * 1024
        else:
            filesize_bytes = 0.00
    except:
        filesize_bytes = 0.00
    return filesize_bytes

def procedure_mapping(filename,type_of_procedure_actual = None):
    type_of_procedure = 'Other'
    if type_of_procedure_actual is not None:
        type_of_procedure_actual = type_of_procedure_actual.replace(',','').replace('.','')
        file_path = ASSETS_PATH+filename
        with open(file_path, 'r',encoding = 'utf-8') as f:
            reader = csv.reader(f)
            maps = list(reader)
            procedure_mapping = dict(maps)
        type_of_procedure = procedure_mapping.get(type_of_procedure_actual)
    return type_of_procedure

def url_match(url):
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def valid_email(email):
    email_valid = bool(re.search(r'[\w\.-]+@[\w\.-]+', email))
    return email_valid


def nupco_csv(filepath):    
    with open(filepath, 'r',encoding='latin-1') as f:
        dict_reader = DictReader(f)
        list_of_dict = list(dict_reader)
    return list_of_dict

def date(publish_date):
    date_year = re.findall('\d{4}',publish_date)[0]
    current_year = datetime.now().year

    if int(date_year) > current_year + 100:
        date = publish_date.replace(date_year,'')
        return str(current_year + 1)+date
    else:
        return publish_date
#import sys
# def log(SCRIPT_NAME, log_arguments_list=None):

#     if log_arguments_list is None:

#         log_arguments_list = sys.argv[1:8]

#     logdate = date.today()
#     logdate = logdate.strftime('%d-%m-%Y')
#     filename = LOG_PATH + SCRIPT_NAME + '-' + logdate + '.log'
#     file_handler = logging.FileHandler(filename=filename)
#     stdout_handler = logging.StreamHandler(stream=sys.stdout)
#     handlers = [file_handler, stdout_handler]

#     if log_arguments_list == []:
#         logging.basicConfig(level=logging.INFO, handlers=handlers, encoding='utf-8',
#                             format="%(asctime)s," + SCRIPT_NAME + ',' + "%(levelname)s: %(message)s")
#     else:
#         log_format = "%(asctime)s," + SCRIPT_NAME + ',' + ','.join(log_arguments_list) + ',' + "%(levelname)s: %(message)s"
#         logging.basicConfig(level=logging.INFO, handlers=handlers, encoding='utf-8', format=log_format)
