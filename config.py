import os
import csv
import time
import json
from datetime import date

import psutil
import requests
from loguru import logger
from selenium import webdriver
from fake_useragent import UserAgent

TODAY = str(date.today())
PROCESS_NAME = 'chromedriver.exe'
CHUNK_SIZE = 15
TIMEOUT = 500
ITTER_TIME = 5
LOAD_PAGE_TIME = 10
logger.add(
    f'{os.getcwd()}\\log\\logs.log - {TODAY}',
    format=' {level} | {time:MM-DD-YY | HH:mm:ss | dddd} | {message} ',
    level='SUCCESS',
    rotation='1 day',
    compression='zip',
    # serialize=True
)


def timed(func):
    """
    records approximate durations of function calls
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = "[{name}]: Time spend: {elapsed:.2f}s".format(
            name=func.__name__.upper(),
            elapsed=time.time() - start
        )
        logger.info(duration)
        return result

    return wrapper


def create_driver():
    useragent = UserAgent()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--lang=en")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument(f"user-agent={useragent.random}")
    chrome_options.add_argument("--disable-site-isolation-trials")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def logger_success(len_db_data: int, len_site_dict: int, file_name: str):
    if len_db_data == len_site_dict:
        logger.success(
            f'[{file_name.upper()}]: DB - {len_db_data} | '
            f'SITE - {len_site_dict} | '
        )
    else:
        logger.success(
            f'[{file_name.upper()}]: CHECK NUMBER OF COMPANIES | '
            f'DB - {len_db_data} | SITE - {len_site_dict} | '
        )


def save_json(data: dict):
    with open(f'fuel_price_json\\fuel_price - {TODAY}.json', 'w', encoding='UTF-8') as json_file:
        json.dump(data, json_file, indent=3)


def save_scv(data_dict: dict):
    with open(f'fuel_price_scv\\fuel_price - {TODAY}.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('ID', 'Name', 'DIESEL', 'DEF'))
        for company_id, values in data_dict.items():
            diesel = values.get('Diesel', '')
            brand_name = values.get('Brand_name', '')
            def_ = values.get('Def', '')
            if diesel:
                writer.writerow((company_id, brand_name, diesel, def_))
            else:
                logger.warning(f'[{company_id}]: NO FUEL PRICE | {brand_name.upper()}')


def open_scv(file_name: str) -> list:
    with open(f'{file_name}', "r") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        return [row for row in reader]


def kill_by_process():
    try:
        for proc in psutil.process_iter():
            if proc.name() == PROCESS_NAME:
                proc.kill()
    except Exception as ex:
        os.system("taskkill /f /im " + PROCESS_NAME)
        # logger.warning('[KILL BY PROCESS SHELL]')
        pass


def create_company_dict(db_file_name: str) -> dict:
    url_dicts = {
        'tapetro': {},
        'loves': {},
        'pilotflyingj': {},
        'kwiktrip': {},
        'sappbros': {},
        'roadranger': {},
        'gmb': {},
        'notes': {},
        # 'no_price': {}
    }
    data_list = open_scv(db_file_name)
    logger.debug(f'[LIST LENGTH]: {len(data_list)} |')
    for company in data_list:
        company_id = company[0]
        company_name = company[2]
        company_city = company[3]
        company_state = company[4]
        company_address = company[6]
        company_web_site = company[21]
        company_gmb = company[8].split('?hl')[0]  # .replace('http:', 'https:')
        company_notes = company[-1].split('?hl')[0]  # .replace('http:', 'https:')
        if 'sappbros.net' in company_web_site:
            url_dicts['sappbros'].update({company_id: company_web_site})
        elif 'Road Ranger' in company_name:
            url_dicts['roadranger'].update({company_id: company_address})
        elif 'ta-petro.com' in company_web_site:
            try:
                office_id = int(company_name.split("#")[-1])
                url_dicts['tapetro'].update({company_id: office_id})
            except ValueError:
                logger.warning(f'[{company_id}]: {company_name} | CHECK NAME IN ADMIN-TG')
        elif 'loves.com' in company_web_site:
            try:
                office_id = int(company_name.split("#")[-1])
                url_dicts['loves'].update({company_id: office_id})
            except ValueError:
                logger.warning(f'[{company_id}]: {company_name} | CHECK NAME IN ADMIN-TG')
        elif 'pilotflyingj.com' in company_web_site:
            try:
                office_id = int(company_name.split("#")[-1])
                url_dicts['pilotflyingj'].update({company_id: office_id})
            except ValueError:
                logger.warning(f'[{company_id}]: {company_name} | CHECK NAME IN ADMIN-TG')
        elif 'kwiktrip.com' in company_web_site:
            try:
                office_id = int(company_name.split("#")[-1])
                url_dicts['kwiktrip'].update({company_id: office_id})
            except ValueError:
                logger.warning(f'[{company_id}]: {company_name} | CHECK NAME IN ADMIN-TG')
        elif 'www.google.com/maps/place/' in company_notes:
            if company_id.isdigit() and company_notes:
                url_dicts['notes'].update({company_id: {}})
                url_dicts['notes'][company_id] = f'{company_notes}?hl=en'
        elif 'www.google.com/maps/place/' not in company_notes:
            if company_id.isdigit() and company_gmb:
                url_dicts['gmb'].update({company_id: {}})
                url_dicts['gmb'][company_id] = f'{company_gmb}?hl=en'
        # elif 'no_price' in company_notes:
        # url_dicts['gmb'][company_id] = f'[NO_PRICE]: {company_name}'
        else:
            logger.warning(f'[{company_id}]: {company_name} | '
                           f'{company_city} | '
                           f'{company_state} | '
                           f'EDIT COMPANY IN ADMIN-TG')
    return url_dicts


def get_ip():
    return requests.get('https://api64.ipify.org?format=json').json()["ip"]


def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    return {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
