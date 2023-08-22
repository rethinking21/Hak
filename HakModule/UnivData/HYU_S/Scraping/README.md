# HYU_S(한양대학교 서울캠퍼스) 수강 정보란 분석🔍

---
## 사이트 정보
ex: https://portal.hanyang.ac.kr/openPop.do?header=hidden&url=/haksa/SughAct/findSuupPlanDocHyIn.do&flag=DN&year=2023&term=20&suup=10001&language=ko

    2023 (10001 ~ 15485) (10001~13430, 15001~15485)
    수강 정보를 담은 팝업
    year=2023 년도로 추정됨 (년도 별로 꽤 많이 저장 되어 있음)
    term=20 (10 1학기 20 2학기)
    suup =수강 번호
    language=ko (en도 있다)

## html id
### 정상적인 사이트인지 확인
    messageBox : 알림 메세지 (없는 강의일때 뜸)

### 첨부파일 (student) Attach files
    강의 소개 영상이 있지만, 쓴적이 없어서 놔둠

### 교과목 정보 (gdLecture) Course information (data: course_info)
    suupYear : 수업년도 School year (data: year)
    suupTermNm : 수업학기 School Semester (data: semester)
        (1학기 여름학기 2학기 겨울학기) (first summer second winter)
    haksuNo : 학수번호 Class number (data: number)
    suupNo : 수업번호 Class code (data: code)

    gwamokNm : 교과목명(국문) Course name (data: name_kr)
    courseTypeNm : 과목구분 Course classification (data: type)
    gwamokEnm : 교과목명(영문) Course name (English) (data: name_en)
    isuUnitCd : 이수단위 (data: unit)
    yrGbNm : C-한양핵심역량 (data: c_hy)

    hakjeom : 학점 Credit (data: credit)
    ironSigan : 강의 Theory (data: time_theory)
    silsSigan : 실습 Practice (data: time_pratice)
    
    slgSosokNm : 설강조직 Lecturing department (data: department_lecture)
    gnjSosokNm : 관장조직 Department in charge (data: department_charge)
    suupTimeStr : 강의시간 Lecture schedule (data: schedule)
    
### 교강사 정보 (gdTchr) Information about faculty (data: instructor)
    deptNm : 소속 Department (data: department)
    pName : 성명 Name (data: name)
    gyosuHpNo(name) : 연락처 Contact	(data: contact)
    gyosuEmail(name) : Email (data: email)
    gyosuHomepage(name) : 홈페이지 Homepage (data: homepage)

### 수업 개요, 목표 (data: outline)
    gwamokYoyak : 교과목개요 Course outline (data: outline)
    gwamokMokpyo : 수업목표 및 안내 Lecture guide & objective (data: guide)
    lastGupgCmt : 지난학기 강의평가 반영사항 Matters to be reflected on from last semester’s lecture evaluation (data: last_eval)
    detailGoal1 : 세부 수업목표1 Detailed objective 1 (data: details)
    detailGoal2 : 세부 수업목표2 Detailed objective 2
    detailGoal3 : 세부 수업목표3 Detailed objective 3
    gwamokGaeyo : 교과목 주요주제 Main subject (data: main_subject)
    seonsuGwamok : 선수과목안내 Prerequisites (data: prerequisites)

### 교재, 부교재 (data: books)
    gdText : 교재 Textbook (data: first)
    아래의 내용이 묶여있음 rn : 넘버
    주의, readonly 가 있음
    내용이 없으면 emptyDataList(class)가 있음
    
    textNm(name) : 교재명 Textbook name (data: name)
    textJeoja(name) : 저자 Author (data: author)
    textPublisher(name) : 출판사 Publishing company (data: publish)
    textIsbn(name) : ISBN (data: isbn)
    textPrice(name) : 가격 Price (data: price)
    
    gdTextAn : 부교재 (밑 내용도 같을 것으로 추정됨) Secondary textbook (data: second)

### 평가 항목 (gdPg) Evaluation (data: eval)
    gdPg2: 평가항목으로 추정됨
    (attendHiddn, attendHiddn2 (chulseokOffRatio) 가 있는데 무슨 기능인지 모르겠음)
    attendRatio(name) : 출석 Attendance (data: attendance)
    quizRatio(name) : 퀴즈 Quiz (data: quiz)
    reportRatio(name) : 과제 Report (data: report)
    midexamRatio(name) : 중간고사 Midterm exam (data: exam_mid)
    discussRatio(name) : 토론 Debate (data: debate)
    finalexamRatio(name) : 기말고사 Final exam (data: exam_final)
    teamprojectRatio(name) : 팀프로젝트 Team project (data: team)
    studyactivityRatio(name) : 학습참여도 Study participation (data: participation)

    gdEtc : 기타 평가 항목 (기타 평가항목은 name도 없고, etcValue(name)로 비율이 표시되어 있음)

### 주별 강의 계획 및 과제 (weekArea) Weekly course schedule and assignments (data: weekly_course)
    해당 id > tbody 내에 들어있음
    jucha : 주차 Week no. (data: number)

    (data: holiday - 휴일인지 아닌지 확인)
    hyuilNm : 휴일이 들어있는 주차일 때 정보를 써놓음 (data: holiday_name)
    hyuilNotice : 휴일이 들어있는 주차일 때 써놓는 문구 (data: holiday_notice)
    
    subject(name) : 주제 Subject (data: subject)
    hwaldong(name, id) : 활동 사항 (readonly이지만 보이는 듯) Experience career (data: career)
    suupViewtype : 수업 형태 (보통 설정 안해놓는 것 같음, value 값으로 확인 가능) Course Measure (data: view_type)
        

존재하지만 잘 안쓰는 것 같아 기재해놓지 않은 내용은 추후 필요시 업데이트 예정