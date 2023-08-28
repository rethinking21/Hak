from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class SimpleElementFinder:
    def __init__(self, full_data: WebElement = None):
        """
        Initialize the SimpleElement instance.

        Parameters
        ----------
        full_data : WebElement, optional
            Full web element containing class data.
        """
        self.full_web_element: WebElement = full_data

    def find_element_safe(self, by: By = By.ID, value=None, target: WebElement = None) -> Optional[WebElement]:
        """
        Find a single web element safely.

        Parameters
        ----------
        by : str or By, optional
            Search method (default is By.ID).
        value : str, optional
            Search value.
        target : WebElement, optional
            Web element to search within.

        Returns
        -------
        WebElement or None
            Found web element or None.
        """
        if target is None:
            return find_element_safe(by=by, value=value, target=self.full_web_element)
        else:
            return find_element_safe(by=by, value=value, target=target)

    def find_elements_safe(self, by: By = By.ID, value=None, target: WebElement = None) -> list[WebElement]:
        """
        Find a list of web elements safely.

        Parameters
        ----------
        by : str or By, optional
            Search method (default is By.ID).
        value : str, optional
            Search value.
        target : WebElement, optional
            Web element to search within.

        Returns
        -------
        list[WebElement]
            List of found web elements.
        """
        if target is None:
            return find_elements_safe(by=by, value=value, target=self.full_web_element)
        else:
            return find_elements_safe(by=by, value=value, target=target)

    def find_text_data(self, by: By = By.ID, value=None, target: WebElement = None, return_type: type = str):
        """
        Find and return text data from a web element.

        Parameters
        ----------
        by : str or By, optional
            Search method (default is By.ID).
        value : str, optional
            Search value.
        target : WebElement, optional
            Web element to search within.
        return_type : type, optional
            Data type to return (default is str).
        """
        if target is None:
            return find_text_data(by=by, value=value, return_type=return_type, target=self.full_web_element)
        else:
            return find_text_data(by=by, value=value, return_type=return_type, target=target)

    def find_readonly_text_data(self, by: By = By.ID, value=None, target: WebElement = None, return_type: type = str):
        """
        Find and return readonly text data from a web element.

        Parameters
        ----------
        by : str or By, optional
            Search method (default is By.ID).
        value : str, optional
            Search value.
        target : WebElement, optional
            Web element to search within.
        return_type : type, optional
            Data type to return (default is str).
        """
        if target is None:
            return find_readonly_text_data(by=by, value=value, return_type=return_type, target=self.full_web_element)
        else:
            return find_readonly_text_data(by=by, value=value, return_type=return_type, target=target)


def find_element_safe(target: WebElement = None, by: By = By.ID, value=None) -> Optional[WebElement]:
    """
    Find a single web element safely.

    Parameters
    ----------
    by : str or By, optional
        Search method (default is By.ID).
    value : str, optional
        Search value.
    target : WebElement, optional
        Web element to search within.

    Returns
    -------
    WebElement or None
        Found web element or None.
    """
    try:
        if target is None:
            return None
        else:
            result = target.find_element(by, value)
    except NoSuchElementException:
        return None
    else:
        return result


def find_elements_safe(target: WebElement = None, by: By = By.ID, value=None) -> list[WebElement]:
    """
    Find a list of web elements safely.

    Parameters
    ----------
    by : str or By, optional
        Search method (default is By.ID).
    value : str, optional
        Search value.
    target : WebElement, optional
        Web element to search within.

    Returns
    -------
    list[WebElement]
        List of found web elements.
    """
    try:
        if target is None:
            return []
        else:
            result = target.find_elements(by=by, value=value)
    except NoSuchElementException:
        return []
    else:
        return result


def find_text_data(target: WebElement = None, by: By = By.ID, value=None, return_type: type = str):
    """
    Find and return text data from a web element.

    Parameters
    ----------
    by : str or By, optional
        Search method (default is By.ID).
    value : str, optional
        Search value.
    target : WebElement, optional
        Web element to search within.
    return_type : type, optional
        Data type to return (default is str).
    """
    result = find_element_safe(by=by, value=value, target=target).text
    if result == "":
        return None
    else:
        return return_type(result)


def find_readonly_text_data(target: WebElement = None, by: By = By.ID, value=None, return_type: type = str):
    """
    Find and return readonly text data from a web element.

    Parameters
    ----------
    by : str or By, optional
        Search method (default is By.ID).
    value : str, optional
        Search value.
    target : WebElement, optional
        Web element to search within.
    return_type : type, optional
        Data type to return (default is str).
    """
    result_element = find_element_safe(by=by, value=value, target=target)
    if result_element is None:
        return None

    result = find_element_safe(by=by, value=value, target=target).get_attribute('value')
    if result == "" or result is None:
        return None
    else:
        return return_type(result)
