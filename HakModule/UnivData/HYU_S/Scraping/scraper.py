from HakModule.UnivData.HYU_S.Scraping.scrap_data import *
from selenium.common.exceptions import WebDriverException
import json
import os
import time
'''
Scraper Sample
'''
# 2023: (10001~13430, 15001~15485)
if __name__ == "__main__":

    FILE_PATH: str = os.path.join('.', "HakFile", "UnivData", "HYU_S")  # need to change
    file_name: str = "test"
    ranges = [

    ]

    HYU_Url = HYUSeoulClassUrl(year=2023, class_no=10002, term=2)

    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    hyu = HYUSeoulClassScraper(HYU_Url, service=service, options=options)

    full_start = time.time()
    for start_index, end_index in ranges:
        print(f"start scraping ({start_index} ~ {end_index})")
        start = time.time()
        hyu.run()
        while True:  # dangerous
            try:
                full_dict = [data.datas for data in hyu.get_datas([(start_index, end_index)], debug=True)]
            except AttributeError:
                print("error AttributeError : refreshing driver")
                full_dict = []
                hyu.refresh_driver()
                time.sleep(20)
            except WebDriverException:
                print("error WebDriverException : refreshing driver")
                full_dict = []
                hyu.refresh_driver()
                time.sleep(20)
            else:
                break
        print(HYU_Url.get_file_name())
        print(f"scraping complete in{start-time.time()}s")

        with open(os.path.join(
                FILE_PATH,
                f"{file_name}_{HYU_Url.get_file_name()}_{start_index}_{end_index}.json"),
                "w", encoding='UTF-8') as file:
            json.dump({'data': full_dict}, file, indent='\t', ensure_ascii=False)

        print(f"save ({start_index} ~ {end_index}) complete in{start-time.time()}s")
        hyu.quit()
    print(f"{full_start-time.time()}")
    print("done")
