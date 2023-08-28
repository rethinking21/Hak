from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver


class SimpleDriver:
    def __init__(
            self,
            options: Optional[Options] = None,
            service: Optional[Service] = None,
            keep_alive: bool = True,
            wait_time: int = 1):

        self.driver: Optional[WebDriver] = None

        self.options: Optional[Options] = options
        self.service: Optional[Service] = service
        self.keep_alive: bool = keep_alive

        self.wait_time: int = wait_time

    def run(self):
        """
        Start the WebDriver instance.
        """
        if self.driver is not None:
            return
        self.driver = webdriver.Chrome(options=self.options, service=self.service, keep_alive=self.keep_alive)

    def quit(self):
        """
        Quit the WebDriver instance.
        """
        if self.driver is None:
            return
        else:
            self.driver.quit()
            self.driver = None

    def refresh_driver(self, debug: bool = False):
        """
        Refresh the WebDriver instance.

        Parameters
        ----------
        debug : bool, optional
            Flag to print debug information.
        """
        if debug:
            print("refresh driver..")
        self.quit()
        self.run()

    def set_headless(self):
        """
        Set the WebDriver instance to run in headless mode.
        """
        self.options.add_argument("headless")
