# HYU_S(한양대학교 서울캠퍼스) 수강 정보란 분석🔍

---
## 사이트 정보
ex: https://portal.hanyang.ac.kr/openPop.do?header=hidden&url=/haksa/SughAct/findSuupPlanDocHyIn.do&flag=DN&year=2023&term=20&suup=10001&language=ko

    2023 (10001 ~ 15485)
    수강 정보를 담은 팝업
    year=2023 년도로 추정됨 (년도 별로 꽤 많이 저장 되어 있음)
    term=20 (10 1학기 20 2학기)
    suup =수강 번호
    language=ko (en도 있다)

## html id
### 교과목 정보 (gdLecture)
    suupYear : 수업년도
    suupTermNm : 수업학기
    haksuNo : 학수번호
    suupNo : 수업번호

    gwamokNm : 교과목명(국문)
    courseTypeNm : 과목구분
    gwamokEnm : 교과목명(영문)
    isuUnitCd : 이수단위
    yrGbNm : C-한양핵심역량

    hakjeom : 학점
    ironSigan : 강의
    silsSigan : 실습
    
    slgSosokNm : 설강조직
    gnjSosokNm : 관장조직
    suupTimeStr : 강의시간
    
### 교강사 정보 (gdTchr)
    deptNm : 소속
    pName : 성명
    gyosuHpNo : 연락처
    gyosuEmail : Email
    gyosuHomepage : 홈페이지

### 수업 개요, 목표
    gwamokYoyak : 교과목개요
    gwamokMokpyo : 수업목표 및 안내
    lastGupgCmt : 지난학기 강의평가 반영사항
    detailGoal1 : 세부 수업목표1
    detailGoal1 : 세부 수업목표2
    detailGoal1 : 세부 수업목표3
    gwamokGaeyo : 교과목 주요주제
    seonsuGwamok : 선수과목안내

### 교재, 부교재
    gdText : 교재
    아래의 내용이 묶여있음 rn : 넘버
    주의, readonly 가 있음
    
    textNm(name) : 교재명
    textJeoja(name) : 저자
    textPublisher(name) : 출판사
    textIsbn(name) : ISBN
    textPrice(name) : 가격
    
    gdTextAn : 부교재 (밑 내용도 같을 것으로 추정됨)

### 평가 항목 (gdPg)
    gdPg2: 평가항목으로 추정됨
    attendRatio(name) : 출석 (attendHiddn, attendHiddn2 (chulseokOffRatio) 가 있는데 무슨 기능인지 모르겠음)
    quizRatio(name) : 퀴즈
    reportRatio(name) : 과제
    midexamRatio(name) : 중간고사
    discussRatio(name) : 토론
    finalexamRatio(name) : 기말고사
    teamprojectRatio(name) : 팀프로젝트
    studyactivityRatio(name) : 학습참여도

    gdEtc : 기타 평가 항목 (기타 평가항목은 name도 없고, etcValue(name)로 비율이 표시되어 있음)

### 주별 강의 계획 및 과제 (weekArea)
    해당 id > tbody 내에 들어있음
    hyuilNm : 휴일이 들어있는 주차일 때 정보를 써놓음
    jucha : 주차
    subject(name) : 주제
    hyuilNotice : 휴일이 들어있는 주차일 때 써놓는 문구
    hwaldong(name, id) : 활동 사항 (readonly이지만 보이는 듯)
    suupViewtype : 수업 형태 (보통 설정 안해놓는 것 같음)
        value 값으로 확인 가능

존재하지만 잘 안쓰는 것 같아 기재해놓지 않은 내용은 추후 필요시 업데이트 예정