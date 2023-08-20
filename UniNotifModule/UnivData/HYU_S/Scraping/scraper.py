import datetime
from collections import OrderedDict
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class HYUSeoulClassUrl:
    MAIN_URL: str = r"https://portal.hanyang.ac.kr/openPop.do?header=hidden&url=/haksa/SughAct/findSuupPlanDocHyIn.do"

    def __init__(self, year: int = 2023, class_no: int = 10001, term: int = 0, langauge: str = 'ko'):
        self.year: int = year
        self.class_no: int = class_no
        self.term: int = 10 + 5 * term  # thinking
        self.langauge: str = langauge  # ko or en

    def set_current_year(self):
        self.year = datetime.datetime.today().year

    def get_url(self) -> str:
        return f"{HYUSeoulClassUrl.MAIN_URL}&flag=DN&year={self.year}&term={self.term}&suup={self.class_no}&language={self.langauge}"


class HYUSeoulClassData:
    def __init__(self, full_data: WebElement = None):
        self.full_web_element: WebElement = full_data
        self.datas: OrderedDict = OrderedDict([])

    def convert_data(self):
        if self.check_valid_class_data():
            self.datas['valid']: bool = True
        else:
            self.datas['valid']: bool = False
            return

        if self.find_element_safe(By.ID, "gdLecture") is None:
            self.datas['course_info'] = None
        else:
            # TODO: catch exception
            self.datas['course_info'] = self.convert_course_info_data()
            self.datas['instructor'] = self.convert_instructor_data()
            self.datas['outline'] = self.convert_outline()
            self.datas['books'] = self.convert_books()
            self.datas['eval'] = self.convert_evaluation()
            # TODO: weekly_course

    def check_valid_class_data(self) -> bool:
        return self.find_element_safe(By.ID, "messageBox") is None

    def find_element_safe(self, by: By = By.ID, value=None, target: WebElement = None):
        try:
            if target is None:
                result = self.full_web_element.find_element(by, value)
            else:
                result = target.find_element(by, value)
        except NoSuchElementException:
            return None
        else:
            return result

    def find_elements_safe(self, by: By = By.ID, value=None, target: WebElement = None) -> list:
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
        result = self.find_element_safe(by, value, target).text
        if result == "":
            return None
        else:
            return return_type(result)

    def find_readonly_text_data(self, by: By = By.ID, value=None, target: WebElement = None, return_type: type = str):
        result_element = self.find_element_safe(by, value, target)
        if result_element is None:
            return None

        result = self.find_element_safe(by, value, target).get_attribute('value')
        if result == "" or result is None:
            return None
        else:
            return return_type(result)

    def convert_course_info_data(self) -> OrderedDict:
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
        course_info_schedule_text: str = self.find_text_data(By.ID, "suupTimeStr")
        if course_info_schedule_text is None:
            return []
        course_info_schedule: list = []
        # TODO: get detailed Lecture schedule
        for schedule_text in course_info_schedule_text.split(','):
            course_info_schedule.append(schedule_text.split())
        return course_info_schedule

    def convert_instructor_data(self) -> OrderedDict:
        instructor = OrderedDict([])
        instructor['department']: str = self.find_text_data(By.ID, "deptNm")
        instructor['name']: str = self.find_text_data(By.ID, "pName")
        instructor['contact']: str = self.find_readonly_text_data(By.NAME, "gyosuHpNo")
        instructor['email']: str = self.find_readonly_text_data(By.NAME, "gyosuEmail")
        instructor['homepage']: str = self.find_readonly_text_data(By.NAME, "gyosuHomepage")
        return instructor

    def convert_outline(self) -> OrderedDict:
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
        books = OrderedDict([])
        textbooks: list[OrderedDict] = []
        textbooks_element = self.find_element_safe(By.ID, 'gdText')
        if textbooks_element is None:
            return books
        for book_element in self.find_elements_safe(By.XPATH, './tbody/tr', target=textbooks_element):
            if self.find_element_safe(By.CLASS_NAME, 'emptyDataList', target=book_element) is None:
                break
            # TODO: thinking data
        return books

    def convert_evaluation(self) -> OrderedDict:
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

# https://portal.hanyang.ac.kr/openPop.do?header=hidden&url=/haksa/SughAct/findSuupPlanDocHyIn.do&flag=DN&year=2023&term=20&suup=10001&language=ko

# 2023 (10001 ~ 15485)
