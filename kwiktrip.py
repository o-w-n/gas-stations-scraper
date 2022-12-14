import requests
import concurrent.futures

from loguru import logger

from config import logger_success, timed


def create_url_list(db_data: dict) -> list:
    url_list = []
    for company_id, office_id in db_data.items():
        url = f'https://www.kwiktrip.com/ktapi/location/store/information/{office_id}'
        url_list.append(url)
    return url_list


def load_url(url, timeout):
    return requests.get(url, timeout=timeout)


def get_responses(db_data: dict, brand_name: str) -> list:
    responses = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {executor.submit(load_url, url, 10): url for url in create_url_list(db_data)}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                response = future.result()
                responses.append(response)
            except Exception as ex:
                logger.error(f'[{brand_name.upper()}]: {str(ex)}')
    return responses


def get_fuel_price(responses: list, brand_name: str) -> dict:
    fuel_prices_dict = {}
    try:
        for response in responses:
            data = response.json()
            office_id = data['storeNumber']
            prices = data['fuel']
            fuel_prices_dict.update({office_id: {}})
            for item in prices:
                fuel_type = item['type']
                if 'DIESEL #2' == fuel_type:
                    fuel_prices_dict[office_id]['diesel'] = item.get('currentPrice')
                elif 'DIESEL EXHAUST FLUID' == fuel_type:
                    fuel_prices_dict[office_id]['def'] = item.get('currentPrice')
    except Exception as ex:
        logger.error(f'[{brand_name.upper()}]: {str(ex)}')
    return fuel_prices_dict


@timed
def result_kwiktrip(db_data: dict, brand_name: str) -> dict:
    prices_dict = {}
    fuel_price = get_fuel_price(get_responses(db_data, brand_name), brand_name)
    for company_id, db_office_id in db_data.items():
        prices_dict.update({company_id: {}})
        for web_office_id, fuel_prices in fuel_price.items():
            if int(db_office_id) == int(web_office_id):
                prices_dict[company_id] = {
                    'Diesel': fuel_prices.get('diesel', ''),
                    'Def': fuel_prices.get('def', ''),
                    'Brand_name': brand_name
                }
    logger_success(len(db_data), len(fuel_price), brand_name)
    return prices_dict
