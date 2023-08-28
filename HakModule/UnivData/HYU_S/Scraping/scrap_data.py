import os
import time
import datetime
from collections import OrderedDict
from typing import Optional, Union

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as WebEC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class HYUSeoulClassUrl:
    """
    This class provides methods to generate URLs and file names for Hanyang University's Seoul campus class information page.

    Attributes
    ----------
    MAIN_URL : str
        The main URL of the class information page.

    Parameters
    ----------
    year : int, optional
        Academic year (default is 2023).
    class_no : int, optional
        Class number (default is 10001).
    term : int, optional
        Term number (default is 0).
    langauge : str, optional
        Language for the URL (default is 'ko').
    """
    MAIN_URL: str = r"https://portal.hanyang.ac.kr/openPop.do?header=hidden&url=/haksa/SughAct/findSuupPlanDocHyIn.do"

    def __init__(self, year: int = 2023, class_no: int = 10001, term: int = 0, langauge: str = 'ko'):
        """
        Initialize the HYUSeoulClassUrl instance with parameters.

        Parameters
        ----------
        year : int, optional
            Academic year (default is 2023).
        class_no : int, optional
            Class number (default is 10001).
        term : int, optional
            Term number (default is 0).
        langauge : str, optional
            Language for the URL (default is 'ko').
        """
        self.year: int = year
        self.class_no: int = class_no
        self.term: int = 10 + 5 * term  # thinking
        self.langauge: str = langauge  # ko or en

    def set_current_year(self) -> None:
        """
        Set the current year based on the system date.
        """
        self.year = datetime.datetime.today().year

    def get_url(self) -> str:
        """
        Generate and return the URL for the HYUSeoulClass page.

        Returns
        -------
        str
            The generated URL as a string.
        """
        return f"{HYUSeoulClassUrl.MAIN_URL}&flag=DN&year={self.year}&term={self.term}&suup={self.class_no}&language={self.langauge}"

    def get_file_name(self) -> str:
        """
        Generate and return a file name based on instance parameters.

        Returns
        -------
        str
            The generated file name as a string.
        """
        term = ['none', 'none', 'first', 'summer', 'second', 'winter'][self.term//5]
        return f"hyu_class_{self.year}_{term}_{self.langauge}"


class HYUSeoulClassData:
    """
    This class represents data extracted from Hanyang University's Seoul campus class information page.

    Attributes
    ----------
    full_web_element : WebElement, optional
        The full web element containing class data.
    datas : OrderedDict
        Ordered dictionary to store class data.

    Methods
    -------
    clear_web_element()
        Clear the web element.
    convert_data(check_course_info=True, check_instructor=True, ...)
        Convert class data based on given flags.
    check_valid_class_data()
        Check if the class data is valid.
    find_element_safe(by=By.ID, value=None, target=None)
        Find a single web element safely.
    find_elements_safe(by=By.ID, value=None, target=None)
        Find a list of web elements safely.
    find_text_data(by=By.ID, value=None, target=None, return_type=str)
        Find and return text data from a web element.
    find_readonly_text_data(by=By.ID, value=None, target=None, return_type=str)
        Find and return readonly text data from a web element.
    convert_course_info_data()
        Convert course information data to an ordered dictionary.
    convert_course_info_schedule()
        Convert course information schedule data to a list.
    convert_instructor_data()
        Convert instructor data to an ordered dictionary.
    convert_outline()
        Convert outline data to an ordered dictionary.
    convert_books()
        Convert books data to an ordered dictionary.
    convert_element_to_book(target=None)
        Convert an element to book data and return an ordered dictionary.
    convert_evaluation()
        Convert evaluation data to an ordered dictionary.
    convert_weekly_course()
        Convert weekly course data to a list.
    convert_element_to_course(target=None)
        Convert an element to course data and return an ordered dictionary.
    """
    def __init__(self, full_data: WebElement = None):
        """
        Initialize the HYUSeoulClassData instance.

        Parameters
        ----------
        full_data : WebElement, optional
            Full web element containing class data.
        """
        self.full_web_element: WebElement = full_data
        self.datas: OrderedDict = OrderedDict([])

    def clear_web_element(self) -> None:
        """
        Clear the web element.
        """
        self.full_web_element = None

    def convert_data(self,
                     check_course_info: bool = True,
                     check_instructor: bool = True,
                     check_outline: bool = True,
                     check_books: bool = True,
                     check_eval: bool = True,
                     check_weekly_course: bool = True,
                     ) -> None:
        """
        Convert class data based on given flags.

        Parameters
        ----------
        check_course_info : bool, optional
            Flag to check course information data.
        check_instructor : bool, optional
            Flag to check instructor data.
        check_outline : bool, optional
            Flag to check outline data.
        check_books : bool, optional
            Flag to check books data.
        check_eval : bool, optional
            Flag to check evaluation data.
        check_weekly_course : bool, optional
            Flag to check weekly course data.
        """
        if self.check_valid_class_data():
            self.datas['valid']: bool = True
        else:
            self.datas['valid']: bool = False
            return

        if self.find_element_safe(By.ID, "gdLecture") is None:
            self.datas['course_info'] = None
        else:
            # TODO: catch exception
            if check_course_info:
                self.datas['course_info'] = self.convert_course_info_data()
            if check_instructor:
                self.datas['instructor'] = self.convert_instructor_data()
            if check_outline:
                self.datas['outline'] = self.convert_outline()
            if check_books:
                self.datas['books'] = self.convert_books()
            if check_eval:
                self.datas['eval'] = self.convert_evaluation()
            if check_weekly_course:
                self.datas['weekly_course'] = self.convert_weekly_course()

    def check_valid_class_data(self) -> bool:
        """
        Check if the class data is valid.

        Returns
        -------
        bool
            True if class data is valid, False otherwise.
        """
        return self.find_element_safe(By.ID, "messageBox") is None

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
        try:
            if target is None:
                result = self.full_web_element.find_element(by, value)
            else:
                result = target.find_element(by, value)
        except NoSuchElementException:
            return None
        else:
            return result

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
        try:
            if target is None:
                result = self.full_web_element.find_elements(by, value)
            else:
                result = target.find_elements(by, value)
        except NoSuchElementException:
            return []
        else:
            return result

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
        result = self.find_element_safe(by, value, target).text
        if result == "":
            return None
        else:
            return return_type(result)

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
        result_element = self.find_element_safe(by, value, target)
        if result_element is None:
            return None

        result = self.find_element_safe(by, value, target).get_attribute('value')
        if result == "" or result is None:
            return None
        else:
            return return_type(result)

    def convert_course_info_data(self) -> OrderedDict:
        """
        Convert course information data to an ordered dictionary.

        Returns
        -------
        OrderedDict
            Ordered dictionary containing course information data.
        """
        course_info = OrderedDict([])
        course_info['year']: int = self.find_text_data(By.ID, "suupYear", return_type=int)

        course_info_semester: str = self.find_text_data(By.ID, "suupTermNm")
        if course_info_semester is None:
            course_info['semester'] = None
        elif '1' in course_info_semester or 'first' in course_info_semester:
            course_info['semester'] = 'first'
        elif '여름' in course_info_semester or 'summer' in course_info_semester:
            course_info['semester'] = 'summer'
        elif '2' in course_info_semester or 'second' in course_info_semester:
            course_info['semester'] = 'second'
        elif '겨울' in course_info_semester or 'winter' in course_info_semester:
            course_info['semester'] = 'winter'
        else:
            course_info['semester'] = None

        course_info['number']: str = self.find_text_data(By.ID, "haksuNo")
        course_info['code']: int = self.find_text_data(By.ID, "suupNo", return_type=int)

        course_info['type']: str = self.find_text_data(By.ID, "courseTypeNm")
        course_info['name_kr']: str = self.find_text_data(By.ID, "gwamokNm")
        course_info['name_en']: str = self.find_text_data(By.ID, "gwamokEnm")
        course_info['unit']: int = self.find_text_data(By.ID, "isuUnitCd", return_type=int)
        course_info['c_hy']: str = self.find_text_data(By.ID, "yrGbNm")

        course_info['credit']: int = self.find_text_data(By.ID, "hakjeom", return_type=int)
        course_info['time_theory']: int = self.find_text_data(By.ID, "ironSigan", return_type=int)
        course_info['time_pratice']: int = self.find_text_data(By.ID, "silsSigan", return_type=int)

        course_info['department_lecture']: str = self.find_text_data(By.ID, "slgSosokNm")
        course_info['department_charge']: str = self.find_text_data(By.ID, "gnjSosokNm")

        course_info['schedule']: list = self.convert_course_info_schedule()
        return course_info

    def convert_course_info_schedule(self) -> list:
        """
        Convert course information schedule data to a list.

        Returns
        -------
        list
            List of course information schedule data.
        """
        course_info_schedule_text: str = self.find_text_data(By.ID, "suupTimeStr")
        if course_info_schedule_text is None:
            return []
        course_info_schedule: list = []
        # TODO: get detailed Lecture schedule
        for schedule_text in course_info_schedule_text.split(','):
            course_info_schedule.append(schedule_text.split())
        return course_info_schedule

    def convert_instructor_data(self) -> OrderedDict:
        """
        Convert instructor data to an ordered dictionary.

        Returns
        -------
        OrderedDict
            Ordered dictionary containing instructor data.
        """
        instructor = OrderedDict([])
        instructor['department']: str = self.find_text_data(By.ID, "deptNm")
        instructor['name']: str = self.find_text_data(By.ID, "pName")
        instructor['contact']: str = self.find_readonly_text_data(By.NAME, "gyosuHpNo")
        instructor['email']: str = self.find_readonly_text_data(By.NAME, "gyosuEmail")
        instructor['homepage']: str = self.find_readonly_text_data(By.NAME, "gyosuHomepage")
        return instructor

    def convert_outline(self) -> OrderedDict:
        """
        Convert outline data to an ordered dictionary.

        Returns
        -------
        OrderedDict
            Ordered dictionary containing outline data.
        """
        outline = OrderedDict([])
        outline['outline']: str = self.find_readonly_text_data(By.ID, "gwamokYoyak")
        outline['guide']: str = self.find_readonly_text_data(By.ID, "gwamokMokpyo")
        outline['last_eval']: str = self.find_readonly_text_data(By.ID, "lastGupgCmt")
        outline_detail: list[str] = [self.find_readonly_text_data(By.ID, "detailGoal1"),
                                     self.find_readonly_text_data(By.ID, "detailGoal2"),
                                     self.find_readonly_text_data(By.ID, "detailGoal3")]
        outline['details']: list[str] = [detail
                                         for detail in outline_detail
                                         if detail is not None]
        # add detail 1 2 3
        outline['main_subject']: str = self.find_readonly_text_data(By.ID, "gwamokGaeyo")
        outline['prerequisites']: str = self.find_readonly_text_data(By.ID, "seonsuGwamok")
        return outline

    def convert_books(self) -> OrderedDict:
        """
        Convert books data to an ordered dictionary.

        Returns
        -------
        OrderedDict
            Ordered dictionary containing books data.
        """
        books = OrderedDict([])
        textbooks: list[OrderedDict] = []
        textbooks_element = self.find_element_safe(By.ID, 'gdText')
        if textbooks_element is None:
            return books
        for book_element in self.find_elements_safe(By.XPATH, './tbody/tr', target=textbooks_element):
            if self.find_element_safe(By.CLASS_NAME, 'emptyDataList', target=book_element) is not None:
                break
            textbooks.append(self.convert_element_to_book(book_element))
        books['first'] = textbooks

        second_textbooks: list[OrderedDict] = []
        second_textbooks_element = self.find_element_safe(By.ID, 'gdTextAn')
        if second_textbooks_element is None:
            return books
        for book_element in self.find_elements_safe(By.XPATH, './tbody/tr', target=second_textbooks_element):
            if self.find_element_safe(By.CLASS_NAME, 'emptyDataList', target=book_element) is not None:
                break
            textbooks.append(self.convert_element_to_book(book_element))
        books['second'] = second_textbooks
        return books

    def convert_element_to_book(self, target: WebElement = None) -> OrderedDict:
        """
        Convert an element to book data and return an ordered dictionary.

        Parameters
        ----------
        target : WebElement, optional
            Web element to convert.

        Returns
        -------
        OrderedDict
            Ordered dictionary containing book data.
        """
        book = OrderedDict([])
        if target is None:
            return book
        book['name']: str = self.find_readonly_text_data(By.NAME, 'textNm', target=target)
        book['author']: str = self.find_readonly_text_data(By.NAME, 'textJeoja', target=target)
        book['publish']: str = self.find_readonly_text_data(By.NAME, 'textPublisher', target=target)
        book['isbn']: str = self.find_readonly_text_data(By.NAME, 'textIsbn', target=target)
        book['price']: str = self.find_readonly_text_data(By.NAME, 'textPrice', target=target)
        return book

    def convert_evaluation(self) -> OrderedDict:
        """
        Convert evaluation data to an ordered dictionary.

        Returns
        -------
        OrderedDict
            Ordered dictionary containing evaluation data.
        """
        evaluation = OrderedDict([])
        evaluation['attendance']: int = self.find_readonly_text_data(By.NAME, "attendRatio", return_type=int)
        evaluation['quiz']: int = self.find_readonly_text_data(By.NAME, "quizRatio", return_type=int)
        evaluation['report']: int = self.find_readonly_text_data(By.NAME, "reportRatio", return_type=int)
        evaluation['exam_mid']: int = self.find_readonly_text_data(By.NAME, "midexamRatio", return_type=int)
        evaluation['debate']: int = self.find_readonly_text_data(By.NAME, "discussRatio", return_type=int)
        evaluation['exam_final']: int = self.find_readonly_text_data(By.NAME, "finalexamRatio", return_type=int)
        evaluation['team']: int = self.find_readonly_text_data(By.NAME, "teamprojectRatio", return_type=int)
        evaluation['participation']: int = self.find_readonly_text_data(By.NAME, "studyactivityRatio", return_type=int)
        # TODO: get 'gdEtc' id data (ex) 2023, 10003)
        return evaluation

    def convert_weekly_course(self) -> list:
        """
        Convert weekly course data to a list.

        Returns
        -------
        list
            List of weekly course data.
        """
        weekly_course = []
        weekly_course_element = self.find_element_safe(By.ID, 'gdWeek')
        for course_element in self.find_elements_safe(By.XPATH, './tbody/tr', target=weekly_course_element):
            weekly_course.append(self.convert_element_to_course(course_element))
        return weekly_course

    def convert_element_to_course(self, target: WebElement = None) -> OrderedDict:
        """
        Convert an element to course data and return an ordered dictionary.

        Parameters
        ----------
        target : WebElement, optional
            Web element to convert.

        Returns
        -------
        OrderedDict
            Ordered dictionary containing course data.
        """
        course = OrderedDict([])
        if target is None or self.find_element_safe(By.CLASS_NAME, 'emptyDataList', target=target) is not None:
            return course
        course['number']: str = self.find_text_data(By.ID, 'jucha', target=target)
        if self.find_text_data(By.ID, 'hyuilNm', target=target) is not None:
            course['holiday']: bool = True
            course['holiday_name']: str = self.find_text_data(By.ID, 'hyuilNm', target=target)
            course['holiday_notice']: str = self.find_text_data(By.ID, 'hyuilNotice', target=target)
        else:
            course['holiday']: bool = False

        course['subject']: str = self.find_readonly_text_data(By.NAME, 'subject', target=target)
        course['career']: str = self.find_readonly_text_data(By.NAME, 'hwaldong', target=target)
        view_type_list = ['선택', '대면강의', '실시간화상강의', '온라인녹화강의',
                          '대면+실시간', '시험및평가', '녹화+실시간', '녹화+대면']
        if self.find_element_safe(By.NAME, 'suupViewtype') is None:
            course['view_type']: str = ''
        else:
            view_type_index = self.find_element_safe(By.NAME, 'suupViewtype').get_attribute('selectedIndex')
            if view_type_index is None or int(view_type_index) == 0:
                course['view_type']: str = ''
            else:
                course['view_type']: str = view_type_list[int(view_type_index)]
        return course


class HYUSeoulClassScraper:
    """
    Class for scraping class data from Hanyang University's Seoul campus class information page.

    Attributes
    ----------
    hyu_url : HYUSeoulClassUrl
        Instance of HYUSeoulClassUrl containing the base URL.
    driver : WebDriver, optional
        WebDriver instance for handling browser interaction.

    options : Options, optional
        WebDriver options for browser configuration.
    service : Service, optional
        WebDriver service.
    keep_alive : bool
        Flag to keep the WebDriver instance alive.
    wait_time : int
        Wait time in seconds.

    Methods
    -------
    run()
        Start the WebDriver instance.
    quit()
        Quit the WebDriver instance.
    refresh_driver(debug=False)
        Refresh the WebDriver instance.
    set_headless()
        Set the WebDriver instance to run in headless mode.
    get_data(class_no, show_debug=False, ...)
        Get class data for a specific class number.
    get_datas(ranges, check_course_info=True, ...)
        Get class data for a list of class numbers or ranges.
    """
    def __init__(self, hyu_url: HYUSeoulClassUrl,
                 options: Optional[Options] = None,
                 service: Optional[Service] = None,
                 keep_alive: bool = True,
                 wait_time: int = 1):
        """
        Initialize the HYUSeoulClassScraper instance.

        Parameters
        ----------
        hyu_url : HYUSeoulClassUrl
            Instance of HYUSeoulClassUrl containing the base URL.
        options : Options, optional
            WebDriver options for browser configuration.
        service : Service, optional
            WebDriver service.
        keep_alive : bool, optional
            Flag to keep the WebDriver instance alive.
        wait_time : int, optional
            Wait time in seconds.
        """
        self.hyu_url: HYUSeoulClassUrl = hyu_url
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
            pass
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

    def get_data(self, class_no: int,
                 show_debug: bool = False,
                 check_course_info: bool = True,
                 check_instructor: bool = True,
                 check_outline: bool = True,
                 check_books: bool = True,
                 check_eval: bool = True,
                 check_weekly_course: bool = True, ) -> Optional[HYUSeoulClassData]:
        """
        Get class data for a specific class number.

        Parameters
        ----------
        class_no : int
            Class number.
        show_debug : bool, optional
            Flag to print debug information.
        check_course_info : bool, optional
            Flag to check course information data.
        check_instructor : bool, optional
            Flag to check instructor data.
        check_outline : bool, optional
            Flag to check outline data.
        check_books : bool, optional
            Flag to check books data.
        check_eval : bool, optional
            Flag to check evaluation data.
        check_weekly_course : bool, optional
            Flag to check weekly course data.

        Returns
        -------
        Optional[HYUSeoulClassData]
            Instance of HYUSeoulClassData or None.
        """
        if show_debug:
            print(f"getting data.. : {class_no}")
        self.hyu_url.class_no = class_no
        self.driver.get(self.hyu_url.get_url())
        try:
            WebDriverWait(self.driver, 1).until(
                WebEC.presence_of_element_located((By.ID, "messageBox"))  # thinking
            )
        except TimeoutException:
            time.sleep(0.1)

        hyu_data = HYUSeoulClassData(self.driver.find_element(By.XPATH, '/html/body'))
        hyu_data.convert_data(
            check_course_info=check_course_info,
            check_instructor=check_instructor,
            check_outline=check_outline,
            check_books=check_books,
            check_eval=check_eval,
            check_weekly_course=check_weekly_course
        )
        hyu_data.clear_web_element()
        if hyu_data.datas['valid']:
            return hyu_data
        else:
            return None

    def get_datas(self,
                  ranges: list[Union[int, tuple[int, int]]],
                  check_course_info: bool = True,
                  check_instructor: bool = True,
                  check_outline: bool = True,
                  check_books: bool = True,
                  check_eval: bool = True,
                  check_weekly_course: bool = True,
                  debug: bool = False,
                  refresh_driver_rate: int = 50
                  ) -> list[Optional[HYUSeoulClassData]]:
        """
        Get class data for a list of class numbers or ranges.

        Parameters
        ----------
        ranges : list[Union[int, tuple[int, int]]]
            List of class numbers or ranges.
        check_course_info : bool, optional
            Flag to check course information data.
        check_instructor : bool, optional
            Flag to check instructor data.
        check_outline : bool, optional
            Flag to check outline data.
        check_books : bool, optional
            Flag to check books data.
        check_eval : bool, optional
            Flag to check evaluation data.
        check_weekly_course : bool, optional
            Flag to check weekly course data.
        debug : bool, optional
            Flag to print debug information.
        refresh_driver_rate : int, optional
            Refresh driver after every 'refresh_driver_rate' number of requests.

        Returns
        -------
        list[Optional[HYUSeoulClassData]]
            List of HYUSeoulClassData instances or None.
        """
        refresh_driver_counter: int = 0
        result = []
        for data_range in ranges:
            if type(data_range) is int:
                refresh_driver_counter += 1
                if refresh_driver_counter > refresh_driver_rate:
                    self.refresh_driver(debug=debug)
                    refresh_driver_counter = 0
                if debug:
                    print(f"get HYU Seoul data {data_range}")
                result.append(self.get_data(
                    class_no=data_range,
                    check_course_info=check_course_info,
                    check_instructor=check_instructor,
                    check_outline=check_outline,
                    check_books=check_books,
                    check_eval=check_eval,
                    check_weekly_course=check_weekly_course
                ))
            elif type(data_range) is tuple:
                first, last = data_range
                for number in range(first, last):
                    refresh_driver_counter += 1
                    if refresh_driver_counter > refresh_driver_rate:
                        self.refresh_driver(debug=debug)
                        refresh_driver_counter = 0
                    if debug:
                        print(f"info : get HYU Seoul data {number}")
                    result.append(self.get_data(
                        class_no=number,
                        check_course_info=check_course_info,
                        check_instructor=check_instructor,
                        check_outline=check_outline,
                        check_books=check_books,
                        check_eval=check_eval,
                        check_weekly_course=check_weekly_course
                    ))

        return [data
                for data in result
                if data is not None]


if __name__ == '__main__':
    print(__file__)
# https://portal.hanyang.ac.kr/openPop.do?header=hidden&url=/haksa/SughAct/findSuupPlanDocHyIn.do&flag=DN&year=2023&term=20&suup=10001&language=ko

# 2023 (10001 ~ 15485)
