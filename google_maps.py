import time
from multiprocessing import Pool, freeze_support

from loguru import logger

from config import create_driver

driver = create_driver()


def clear_fuel_price(price: str):
    try:
        price = price.replace('US', '')
        price = price.replace('$', '')
        price = price.replace('*', '')
        price = price.replace('-', '')
    except Exception as ex:
        logger.error(f'[GMB]: {str(ex)}')
    return price.strip()


def create_comp_list(data_dict: dict):
    url_list = []
    for company_id, url in data_dict.items():
        url_list.append(url)
    return url_list


def get_data_data(url):
    prices_dict = {}
    driver.get(url)
    time.sleep(2)
    data_id = url.split('/data=')[-1].split('?hl=')[0]
    prices_dict.update({data_id: {}})
    price = str(driver.page_source).split('class="Fnmwje" jsan="7.Fnmwje">Diesel</div>')[-1]
    price = price.split('</span>')[0].split('>')[-1].replace('$', '')
    if price.replace('.', '', 1).isdigit():
        prices_dict[data_id]['diesel'] = price
    else:
        logger.warning(f'[GOOGLE_MAPS]: NO FUEL PRICE\nURL: {url}')
    return prices_dict


def result_gmb(db_data: dict, brand_name: str):
    main_dict = {}
    fuel_price_dict = {}
    count = 0
    try:
        url_list = create_comp_list(db_data)
        with Pool(processes=10) as pool:
            for i in pool.imap_unordered(get_data_data, url_list, ):
                count += len(i)
                fuel_price_dict.update(i)
                logger.info(f'[{brand_name.upper()}]: Progress: {count}/{len(url_list)}')

        for company_id, url in db_data.items():
            main_dict.update({company_id: {}})
            data_id_db = url.split('/data=')[-1].split('?hl=')[0]
            for data_id_gmb, fuel_price in fuel_price_dict.items():
                if data_id_gmb in data_id_db:
                    main_dict[company_id]['Diesel'] = fuel_price.get('diesel')
    except Exception as ex:
        logger.info(f'[{brand_name.upper()}]: {str(ex)}')
    return main_dict
