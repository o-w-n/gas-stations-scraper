import requests
from loguru import logger
from bs4 import BeautifulSoup
from urllib3 import disable_warnings

from config import logger_success, timed


def get_page_data(band_name: str) -> dict:
    fuels_dict = {}
    prices_list = []
    url = 'https://www.sappbros.net/travel-centers/fuel-prices/'
    try:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        for row in soup.find_all('table')[0].tbody.find_all('tr'):
            prices_list.append([i for i in row.find_all('td')])
        for item in prices_list:
            if item:
                web_site = item[0].find('a').get('href')
                fuels_dict[web_site] = {
                    'diesel': item[1].text,
                    'def': item[5].text,
                }
    except requests.exceptions.HTTPError as ex:
        logger.error(f'[{band_name.upper()}]: {str(ex)} -> CHECK PROXY')
    return fuels_dict


@timed
def result_sappbros(db_data: dict, band_name: str) -> dict:
    disable_warnings()
    prices_dict = {}
    fuel_price = get_page_data(band_name)
    for company_id, values in db_data.items():
        prices_dict.update({company_id: {}})
        web_admin = values
        for web_site, fuel_prices in fuel_price.items():
            if web_site in web_admin:
                prices_dict[company_id] = {
                    'Diesel': fuel_prices.get('diesel'),
                    'Def': fuel_prices.get('def'),
                    'Brand_name': band_name
                }
    logger_success(len(db_data), len(prices_dict), band_name)
    return prices_dict
