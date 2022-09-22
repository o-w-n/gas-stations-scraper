import requests
from loguru import logger

from config import logger_success, timed


def get_response(page_number: int, brand_name: str) -> dict:
    response = ''
    headers = {
        'authority': 'www.walmart.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': 'adblocked=false; next-day=1653573600|true|false|1653652800|1653570235; location-data=07014%3AClifton%3ANJ%3A%3A1%3A1|4fs%3B%3B2.94%2C2fr%3B%3B4.18%2C2qy%3B%3B4.68%2C2ps%3B%3B5.24%2C47b%3B%3B5.71%2C2xf%3B%3B6.19%2C4iz%3B%3B11.83%2C2jg%3B%3B13.3%2C2nn%3B%3B14.72%2C3x1%3B%3B15.28||7|1|1xi9%3B16%3B0%3B1.3%2C1xme%3B16%3B1%3B2.11%2C1xk8%3B16%3B8%3B7.46%2C1xyt%3B16%3B9%3B7.65%2C1xph%3B16%3B10%3B8.29; DL=07014%2C%2C%2Cip%2C07014%2C%2C; TB_Latency_Tracker_100=1; TB_Navigation_Preload_01=1; TB_SFOU-100=; vtc=dGrsAQ7MoJ0rMVX_WQb2eo; bstc=dGrsAQ7MoJ0rMVX_WQb2eo; mobileweb=0; xpa=-wnVY|0DSDD|0t4gT|2kBTR|DAwQd|FEyuJ|HF8Yi|HXzAk|IJVMl|V-nnO|VxKe2|_-wfu|_QKU8|_mN9p|bupnU|ccDGr|eJ9VH|eXnIH|esGri|gtEvP|gynZP|ke52M|mD451|nzyw-|obzLE|opVBu|v5uMk|vvTaq|xR8AV|zCylr; exp-ck=0t4gT1DAwQd3FEyuJ2HXzAk1IJVMl1V-nnO1VxKe21_mN9p1ccDGr1eJ9VH2eXnIH1gtEvP1gynZP2mD4511nzyw-1obzLE1v5uMk1vvTaq1; _cvftc=rest; TS01b0be75=01538efd7cf5280a2b81552289df1e2831034a828ffe8f97027369bbc4134d7812968a54d4d5990ddee5b969fd953b5a325fe305b5; TS013ed49a=01538efd7cf5280a2b81552289df1e2831034a828ffe8f97027369bbc4134d7812968a54d4d5990ddee5b969fd953b5a325fe305b5; TBV=7; xpm=1%2B1653570234%2BdGrsAQ7MoJ0rMVX_WQb2eo~%2B0; ndcache=d; bm_mi=D2AE854D160880642F0A9D3BAD83C289~YAAQhHhGaM43Dt2AAQAAOXR3AA+cFfy5qjktIEAuOnpYPcqtAi04/XzflIVCTooCVkg/VyiQndAOddgt8T0bDwXUukv/R75Wgg+c2/WBLpq2y3TpY+q04AiLT/ynQfXB3EPa25cDNZskwle40Oi5r61V0Oq3mDnUS5CMTAJB41Kue5BHufUJY/AoBQjXc38KLLOukTMAWu/fgQjx5SQEKf8JbEt2oe0+L3x+7B2wI9LUzY5F6c6FDn8wPWJ7F6R/EDnDA6EqsUWTOUa+pyuIIjTw16xzZd4SElliaWzuapVLAPAnBMuXCOoaNcRLxklUyGL19t67KUZ+zRzZr0C4Ji7Ieq8w2ouhmGTJMu70aIDksBMVzbo=~1; pxcts=4db89792-dcf4-11ec-93cf-586656486350; _pxvid=4db8842f-dcf4-11ec-93cf-586656486350; _pxff_cfp=1; _gcl_au=1.1.1777202242.1653570238; _px3=b49e113e6e35b4bf115ca41a13d3060d5bb8a0209d341c4803a8303763b9c11b:X2Y6RqP34tOVmifrNw+gko7j2GgYdAzip7a4MFDUGfDxHAiBGR6qSTazY68hRyf/T22bquv5sEO/n1xfscuvyQ==:1000:4a4ruThdMJAZNRtbDGTHpNb9GJdvzJQV58HoFzDyoOq4mJLkZcOOmLPp5zghZnSStf+8K6FQybcH3/CgXqvlCVvVph4BxuVB5NRru1I70QkLZbUpd5IfcS7R2NQi3JS/H6Whcp6+SM3nA1ixCRUvvI/J/io5Fu1KBUtNBy1QVQbqNjwVLwjimAMUfY760i7x0tKpNdo/3cHgyesl2mPc8Q==; _uetsid=4e7bcde0dcf411ecac753fb630b8447e; _uetvid=4e7c08e0dcf411ec82d77f69bb6ac687; xptwg=3571887312:DE007284744228:240A00C:7524A19:B2FE6814:F5C2F462:; ak_bmsc=99C9AF7110005AF78CFD3FE3248B1183~000000000000000000000000000000~YAAQhHhGaJZCDt2AAQAApZB3AA90V/mSLinbyeRdWEAEsioNFoEIq6pnqz6bBI1FcW9XY9yW/TrB2fsMEk2Xqx6dN1euelMWuS465ZQO1SgN2QFgoaxXPPmT2Xro8Vm86a7AeYWXj7o10qZZi+U4r/a2x13J79iR+qwOJhwu3DbL9wVgoQITFA+cIFa2ffxIBPUC/VJnw2ok4goL0jdbge+q4BpJnmu/RcGf5d8OYG41eLdr3MG/LkUVt9Gs8gm0lKNH+u3ABk0r9IfYhDeqIjvYWKX1bFtTy82/zfH4m4wufb9WTW0qotLLTGigV5PMUtgSiCJeUzdYV0qlWqmi+mR4x3C87qYHw/Nl81yluzmyiVsaMERCl/kd+f0+V0K1Pw23GLTCQdvXK1IaA7Sc5KNvJrqfAUd1wy1YeeY+SEKblKQRupUnfqb4ywoJNpe3QhGNSEAZo0MXwCZAbsIAX/6XldjOSwCwKWPKfdF6Llg1ScQ91Ik+huxR5DbCzDCMTqBpo1bUFS4KKjGJPQdOB86ghQNwu2LjqIljNH3Exp8zxQB8SHUN8R7y; bm_sv=62B16D3B29C5B173C413C8F153647859~YAAQhHhGaJdCDt2AAQAApZB3AA/zHDNri3HtgFWHt8q5m3KTgWxHAsxiUYQWW54/D76AdpSKRugfDmh5XrdoBBt92A/rln7Hcibl1pzvpUALsbzLAES3qi+AlUBraam5Znj2QUH2yvmlwcxVhhLnEJshqGE4baLtW0B1ose78WIG9dway7CrPQTrWMMSmBgfqiRt+Z2/pnKnyrjGVxqPBVKWPt6wSWIpqniKWeUov+ASPkx8Fj2KlI3L+ziagV9svA==~1; incap_ses_6522_727601=v8mfVWZqTXMaqweGmcyCWrAMAWMAAAAA5AVFprZ2/7ypWek424cL1A==; nlbi_727601=Mo88CmB6/nCXislsanAwUwAAAADWr28Dqxw9cFBJcOL4sf3e; visid_incap_727601=MeweNVIWSGSoP1lA+sbvQ8z0kWIAAAAAQUIPAAAAAADDCDWU/upbdN810zfoijLY; ADRUM_BT1=R:46|i:3144811|e:104; ADRUM_BTa=R:46|g:d306d669-43a5-4413-a8e6-860cc7c76646|n:lovetravelstops-prod_7aa7954c-af7e-4409-818b-b794767800a0; ARRAffinity=600cad8478501eec864f23c43de2cbc13665e4a00d62bae11875281995134fd3; ARRAffinitySameSite=600cad8478501eec864f23c43de2cbc13665e4a00d62bae11875281995134fd3; ASP.NET_SessionId=zvoubprnkxljh4q4yzs2ycnp; SC_ANALYTICS_GLOBAL_COOKIE=32bb1b7a0c574a009e434cbc02f8345d|False; SameSite=None',
        'referer': 'https://www.walmart.com/store/731-demopolis-al',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
    }
    try:
        url = 'https://www.loves.com/api/sitecore/StoreSearch/SearchStoresWithDetail'
        params = {
            "StoreTypes": "Travel Stop",
            "pageNumber": page_number,
            "top": 30,
            "lat": 38.130353038797594,
            "lng": -97.81370249999999
        }
        response = requests.get(url, headers=headers, params=params)
    except requests.exceptions.HTTPError as ex:
        logger.error(f'[{brand_name.upper()}]: {str(ex)} | CHECK PROXY')
    return response.json()


def get_fuel_price(data, brand_name) -> dict:
    fuel_prices_dict = {}
    try:
        for comp_dict in data:
            office_id = comp_dict['Number']
            prices = comp_dict['FuelPrices']
            fuel_prices_dict.update({office_id: {}})
            for item in prices:
                fuel_type = item['DisplayName']
                fuel_price = item['CashPrice']
                if 'diesel' in fuel_type.lower():
                    fuel_prices_dict[office_id]['diesel'] = str(fuel_price)
                elif 'def' in fuel_type.lower():
                    fuel_prices_dict[office_id]['def'] = str(fuel_price)
    except Exception as ex:
        logger.error(f'[{brand_name.upper()}]: {str(ex)}')
    return fuel_prices_dict


@timed
def result_loves(db_data: dict, brand_name: str) -> dict:
    prices_dict = {}
    fuel_price = {}
    for count in range(18):
        fuel_price.update(get_fuel_price(get_response(count, brand_name), brand_name))
    for company_id, db_office_id in db_data.items():
        prices_dict.update({company_id: {}})
        for web_office_id, fuel_prices in fuel_price.items():
            if int(db_office_id) == int(web_office_id):
                prices_dict[company_id] = {
                    'Diesel': fuel_prices.get('diesel'),
                    'Def': fuel_prices.get('def'),
                    'Brand_name': brand_name
                }
    logger_success(len(db_data), len(fuel_price), brand_name)
    return prices_dict
