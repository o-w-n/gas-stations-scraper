import requests
from loguru import logger
from bs4 import BeautifulSoup

from config import logger_success, timed


def get_page_data(brand_name: str) -> dict:
    fuels_dict = {}
    url = 'https://www.roadrangerusa.com/fuel/check-fuel-prices'
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for row in soup.find_all('table')[0].tbody.find_all('tr'):
            address = row.find_all('th')[0].contents[1].text
            diesel_price = row.find_all('td')[3].contents[0].replace('$', '')
            fuels_dict[address] = {
                'diesel': diesel_price
            }
    except requests.exceptions.HTTPError as ex:
        logger.error(f'[{brand_name.upper()}]: {str(ex)} | CHECK PROXY')
    return fuels_dict


@timed
def result_roadranger(db_data: dict, brand_name: str) -> dict:
    price_dict = {}
    fuel_dict = get_page_data(brand_name)
    for company_id, values in db_data.items():
        price_dict.update({company_id: {}})
        adr_admin = values.split()[0]
        for adr_site, fuel_prices in fuel_dict.items():
            adr_site = adr_site.split()[0]
            if adr_admin == adr_site:
                price_dict[company_id] = {
                    'Diesel': fuel_prices.get('diesel'),
                    'Brand_name': brand_name
                }
    logger_success(len(db_data), len(price_dict), brand_name)
    return price_dict
