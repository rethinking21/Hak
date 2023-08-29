import pprint
import time
from collections import OrderedDict
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as WebEC
from selenium.webdriver.support.wait import WebDriverWait

from HakModule.Google.Selenium.SimpleDriver import SimpleDriver
from HakModule.Google.Selenium.SimpleElementFinder import *


class EverytimeScheduleData(SimpleElementFinder):
    def __init__(self, table_body_data: WebElement = None):
        """
        Initialize an instance of EverytimeScheduleData.

        Parameters
        ----------
        table_body_data : WebElement, optional
            The web element containing table body data.
        """
        super(EverytimeScheduleData, self).__init__(table_body_data)
        self.classroom_datas = []

    def convert_data(self):
        """
        Convert raw web data into structured classroom data.
        """
        for classroom_element in self.find_elements_safe(by=By.CLASS_NAME, value="subject"):
            self.add_classroom_data(classroom_element)

    def add_classroom_data(self, element: WebElement = None):
        """
        Add classroom data to the list of classroom datas.

        Parameters
        ----------
        element : WebElement, optional
            The web element containing classroom data.
        """
        classroom_data = OrderedDict([])
        if self.find_element_safe(target=element, by=By.CLASS_NAME, value="name") is not None:
            classroom_data['timed']: bool = False
            classroom_data['name']: str = self.find_text_data(target=element, by=By.CLASS_NAME, value="name")
        else:
            classroom_data['timed']: bool = True
            classroom_data['name']: str = self.find_text_data(target=element, by=By.TAG_NAME, value="h3")
            classroom_data['instructor']: str = self.find_text_data(target=element, by=By.TAG_NAME, value="em")
            classroom_data['place']: str = self.find_text_data(target=element, by=By.TAG_NAME, value="span")
        if classroom_data['name'] not in [data['name'] for data in self.classroom_datas]:
            self.classroom_datas.append(classroom_data)


class EverytimeToText(SimpleDriver):
    def __init__(
            self,
            options: Optional[Options] = None,
            service: Optional[Service] = None,
            keep_alive: bool = True,
            wait_time: int = 1):
        """
        Initialize an instance of EverytimeToText.

        Parameters
        ----------
        options : Options, optional
            Custom options for configuring the WebDriver.
        service : Service, optional
            Custom service for the WebDriver.
        keep_alive : bool, optional
            Boolean flag indicating whether to keep the WebDriver alive.
        wait_time : int, optional
            Time to wait between actions, in seconds.
        """
        super(EverytimeToText, self).__init__(
            options=options,
            service=service,
            keep_alive=keep_alive,
            wait_time=wait_time
        )

    def setting_new_headless(self):
        """
        Add the "--headless=new" argument to the WebDriver options.
        """
        self.options.add_argument("--headless=new")

    def code_to_classroom_data(self, code: str = '') -> Optional[EverytimeScheduleData]:
        """
        Convert a code to classroom data.

        Parameters
        ----------
        code : str, optional
            The code to convert.

        Returns
        -------
        EverytimeScheduleData or None
            An instance of EverytimeScheduleData containing classroom data.
        """
        return self.url_to_classroom_data(f"https://everytime.kr/@{code}")

    def url_to_classroom_data(self, url: str = '') -> Optional[EverytimeScheduleData]:
        """
        Convert a URL to classroom data.

        Parameters
        ----------
        url : str, optional
            The URL to convert.

        Returns
        -------
        EverytimeScheduleData or None
            An instance of EverytimeScheduleData containing classroom data.
        """
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 2).until(
                WebEC.presence_of_element_located((By.CLASS_NAME, "tablebody"))  # thinking
            )
        except TimeoutException:
            time.sleep(0.1)
            return None
            # TODO: Thinking raise Exception
        else:
            schedule_data = EverytimeScheduleData(
                self.get_classroom_element()
            )
            schedule_data.convert_data()
            return schedule_data

    def get_classroom_element(self, element: WebElement = None) -> Optional[WebElement]:
        """
        Retrieve the classroom element from the web page.

        Parameters
        ----------
        element : WebElement, optional
            The web element to search from.

        Returns
        -------
        WebElement or None
            The classroom element or None if not found.
        """
        element = self.driver.find_element(By.XPATH, '/html/body')
        if element is None:
            return None

        return find_element_safe(element, by=By.CLASS_NAME, value='tablebody')


if __name__ == "__main__":
    URL = "https://everytime.kr/@example_code"
    service = Service()
    options = webdriver.ChromeOptions()

    everytime = EverytimeToText(options=options, service=service)
    everytime.setting_new_headless()
    everytime.run()
    everytime_data = everytime.code_to_classroom_data("WT0E2D8NrETJDQ5eaF8q")
    pprint.pprint(everytime_data.classroom_datas)
    time.sleep(1)
    everytime.quit()
