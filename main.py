from loguru import logger

from google_maps import result_gmb
from loves import result_loves
from tapetro import result_tapetro
from sappbros import result_sappbros
from kwiktrip import result_kwiktrip
from road_ranger import result_roadranger
from pilotflyingj import result_pilotflyingj
from config import create_company_dict, get_location, save_json, save_scv, logger_success, kill_by_process, timed, TODAY


@timed
def main():
    if get_location()['country'] == 'United States':
        main_dict = {}
        companies_dict_db = create_company_dict("db_ts.csv")
        for company in companies_dict_db.items():
            company_name_dict = company[0]
            company_values_dict = company[1]
            if company_name_dict == 'tapetro':
                logger.debug(f'[{company_name_dict.upper()}] | Collecting data |')
                main_dict.update(result_tapetro(company_values_dict, company_name_dict))
            elif company_name_dict == 'loves':
                logger.debug(f'[{company_name_dict.upper()}] | Collecting data |')
                main_dict.update(result_loves(company_values_dict, company_name_dict))
            elif company_name_dict == 'pilotflyingj':
                logger.debug(f'[{company_name_dict.upper()}] | Collecting data |')
                main_dict.update(result_pilotflyingj(company_values_dict, company_name_dict))
            elif company_name_dict == 'roadranger':
                logger.debug(f'[{company_name_dict.upper()}] | Collecting data |')
                main_dict.update(result_roadranger(company_values_dict, company_name_dict))
            elif company_name_dict == 'sappbros':
                logger.debug(f'[{company_name_dict.upper()}] | Collecting data |')
                main_dict.update(result_sappbros(company_values_dict, company_name_dict))
            elif company_name_dict == 'kwiktrip':
                logger.debug(f'[{company_name_dict.upper()}] | Collecting data |')
                main_dict.update(result_kwiktrip(company_values_dict, company_name_dict))
            elif company_name_dict == 'gmb':
                logger.debug(f'[{company_name_dict.upper()}] | Collecting data |')
                main_dict.update(result_gmb(company_values_dict, company_name_dict))
                kill_by_process()
            elif company_name_dict == 'notes':
                logger.debug(f'[{company_name_dict.upper()}] | Collecting data |')
                main_dict.update(result_gmb(company_values_dict, company_name_dict))
        save_json(main_dict)
        logger.success(f'[SAVE JSON]')
        save_scv(main_dict)
        logger.success(f'[SAVE SCV] - {TODAY}')
        kill_by_process()
        logger_success(sum([len(companies_dict_db[x]) for x in companies_dict_db]),
                       sum(1 for y in main_dict.items() if y[1].get('Diesel')),
                       'main')
    else:
        logger.error(f'[MAIN]: TURN ON VPN')


if __name__ == '__main__':
    main()
