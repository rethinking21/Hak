# 필요한 정보 요약 (canvasapi)

---
✅ : python api에서 직접적으로 확인되는 변수입니다. 변동될 수 있으며, 없을시 `AttributeError` 예외를 발생합니다.

목차
- [1.canvasapi.course.Course 변수](#📆-canvasapi.course.Course)
- [2.canvasapi.assignment.Assignment 변수](#📝-canvasapi.assignment.Assignment)
- [3.canvasapi.module.Module 변수](#📑-canvasapi.module.Module)
- [4.canvasapi.module.ModuleItem 변수](#🎁-canvasapi.module.ModuleItem)
---

## 📆 canvasapi.course.Course

아래는 Course 객체의 변수들과 그에 대한 자세한 설명입니다.
- [관련 python canvasapi 문서](https://canvasapi.readthedocs.io/en/stable/course-ref.html#course)
- [관련 canvas LMS API 문서](https://canvas.instructure.com/doc/api/courses.html)

### 기본 정보
- `id`: (정수) 강좌의 고유 ID ✅
- `sis_course_id`: (문자열) SIS 강좌 ID (SIS 정보 보기 권한 있는 경우)
- `uuid`: (문자열) 강좌의 UUID ✅
- `integration_id`: (문자열) 강좌의 통합 ID (SIS 정보 보기 권한 있는 경우)
- `sis_import_id`: (정수) SIS 가져오기의 고유 ID (SIS 정보 관리 권한 있는 경우)

### 강좌 정보
- `name`: (문자열) 강좌의 전체 이름 또는 별칭 ✅
- `course_code`: (문자열) 강좌 코드 ✅
- `original_name`: (문자열) 원래 강좌 이름 (별칭이 있는 경우)
- `workflow_state`: (문자열) 강좌 상태 ('unpublished', 'available', 'completed', 'deleted') ✅
- `account_id`: (정수) 강좌와 연결된 계정 ID ✅
- `root_account_id`: (정수) 강좌와 연결된 최상위 계정 ID ✅
- `enrollment_term_id`: (정수) 강좌와 연결된 등록 기간 ID ✅

### 날짜 정보
- `start_at`: (문자열) 강좌 시작 일시 (ISO 8601 형식) ✅
- `end_at`: (문자열) 강좌 종료 일시 (ISO 8601 형식) ✅

### 기타 정보
- `locale`: (문자열) 강좌 로케일
- `total_students`: (정수) 활성 및 초대된 학생 수
- `default_view`: (문자열) 사용자가 강좌에 처음 접속했을 때 볼 페이지 유형 ✅
- `syllabus_body`: (문자열) 강좌의 개요에 대한 사용자 생성 HTML
- `needs_grading_count`: (정수) 현재 사용자의 채점 권한이 있는 경우 필요한 채점 제출물 수

### 고급 정보
- `term`: (객체) 등록 기간 객체 (선택 사항)
- `course_progress`: (객체) 강좌 진행 정보 (선택 사항)
- `apply_assignment_group_weights`: (부울) 과제 그룹 비중 적용 여부
- `permissions`: (객체) 사용자 권한 (선택 사항)
- `is_public`: (부울) 공개 강좌 여부 ✅
- `is_public_to_auth_users`: (부울) 인증된 사용자에게 공개 여부 ✅
- `public_syllabus`: (부울) 공개 개요 여부 ✅
- `public_syllabus_to_auth`: (부울) 인증된 사용자에게 공개 개요 여부 ✅
- `public_description`: (문자열) 공개 강좌 설명
- `storage_quota_mb`: (정수) 저장 용량 할당량 (MB) ✅
- `storage_quota_used_mb`: (정수) 사용 중인 저장 용량 (MB)
- `hide_final_grades`: (부울) 최종 성적 숨김 여부 ✅
- `license`: (문자열) 라이선스 정보 ✅
- `allow_student_assignment_edits`: (부울) 학생 과제 편집 허용 여부
- `allow_wiki_comments`: (부울) 위키 댓글 허용 여부
- `allow_student_forum_attachments`: (부울) 학생 포럼 첨부파일 허용 여부
- `open_enrollment`: (부울) 개방적 등록 여부
- `self_enrollment`: (부울) 자체 등록 여부
- `restrict_enrollments_to_course_dates`: (부울) 등록 기간 제한 여부 ✅
- `course_format`: (문자열) 강좌 형식 ✅
- `access_restricted_by_date`: (부울) 날짜 제한 설정으로 인한 강좌 보기 제한 여부
- `time_zone`: (문자열) 강좌의 시간대 이름 ✅
- `blueprint`: (부울) 블루프린트 강좌 여부 ✅
- `blueprint_restrictions`: (객체) 블루프린트 제한 설정 (선택 사항)
- `blueprint_restrictions_by_object_type`: (객체) 객체 유형별 블루프린트 제한 설정 (선택 사항)
- `template`: (부울) 템플릿 강좌 여부 (선택 사항)


## 📝 canvasapi.assignment.Assignment

아래는 Assignment 객체의 변수들과 그에 대한 자세한 설명입니다.
- [관련 python canvasapi 문서](https://canvasapi.readthedocs.io/en/stable/assignment-ref.html#assignment)
- [관련 canvas LMS API 문서](https://canvas.instructure.com/doc/api/assignments.html)

### 기본 정보
- `id`: (정수) 과제의 고유 ID ✅
- `name`: (문자열) 과제의 이름 ✅
- `description`: (문자열) 과제에 대한 설명 ✅
- `created_at`: (문자열) 과제 생성 일시 (ISO 8601 형식) ✅
- `updated_at`: (문자열) 과제 업데이트 일시 (ISO 8601 형식) ✅

### 기한 및 잠금
- `due_at`: (문자열) 과제 제출 마감 일시 (ISO 8601 형식) ✅
- `lock_at`: (문자열) 과제 잠금 일시 (ISO 8601 형식) ✅
- `unlock_at`: (문자열) 과제 잠금 해제 일시 (ISO 8601 형식) ✅

### 과제 정보
- `course_id`: (정수) 과제가 속한 강좌의 ID ✅
- `html_url`: (문자열) 과제의 웹 페이지 URL ✅
- `submissions_download_url`: (문자열) 모든 제출물을 다운로드할 수 있는 ZIP 파일 URL ✅
- `assignment_group_id`: (정수) 과제 그룹의 ID ✅
- `due_date_required`: (부울) 계정 수준 설정에 따라 과제 제출 기한이 필요한지 여부 ✅
- `allowed_extensions`: (문자열 배열) 허용된 파일 확장자들의 리스트
- `max_name_length`: (정수) 과제 이름 최대 길이 ✅
- `turnitin_enabled`: (부울) Turnitin 플러그인 활성화 여부
- `vericite_enabled`: (부울) VeriCite 플러그인 활성화 여부
- `turnitin_settings`: (객체) Turnitin 설정 정보 (선택 사항)
- `grade_group_students_individually`: (부울) 그룹 과제일 경우 학생 개별 평가 여부 ✅
- `external_tool_tag_attributes`: (객체) 외부 도구 관련 속성 (선택 사항) ✅
- `peer_reviews`: (부울) 피어 리뷰 필요 여부 ✅
- `automatic_peer_reviews`: (부울) 자동 피어 리뷰 여부 ✅
- `peer_review_count`: (정수) 각 사용자에게 할당된 피어 리뷰 수
- `peer_reviews_assign_at`: (문자열) 피어 리뷰 할당 일시 (ISO 8601 형식)
- `intra_group_peer_reviews`: (부울) 그룹 과제일 경우 그룹 내 피어 리뷰 가능 여부 ✅
- `group_category_id`: (정수) 과제의 그룹 범주 ID ✅
- `needs_grading_count`: (정수) 채점이 필요한 제출물 수
- `needs_grading_count_by_section`: (객체 배열) 섹션 별 채점 필요 제출물 수 정보
- `position`: (정수) 그룹 내에서의 과제 순서 ✅
- `post_to_sis`: (부울) SIS에 성적 정보 동기화 여부 ✅
- `integration_id`: (문자열) 제3자 통합 ID
- `integration_data`: (객체) 과제 통합 데이터
- `points_possible`: (부동소수점) 과제 만점
- `submission_types`: (문자열 배열) 허용되는 제출 유형들의 리스트 ✅
- `has_submitted_submissions`: (부울) 적어도 하나의 학생이 제출했는지 여부 ✅
- `grading_type`: (문자열) 과제 평가 유형 ✅
- `grading_standard_id`: (정수) 평가 기준 ID (선택 사항) ✅
- `published`: (부울) 과제 게시 여부 ✅
- `unpublishable`: (부울) 제출물이 있는 경우 게시 취소 불가 여부

### 상태 및 보안
- `only_visible_to_overrides`: (부울) 오버라이드만 볼 수 있는지 여부 ✅
- `locked_for_user`: (부울) 사용자에게 잠긴 과제인지 여부 ✅
- `lock_info`: (객체) 잠금 정보 (선택 사항) ✅
- `lock_explanation`: (문자열) 잠금 설명 (선택 사항) ✅
- `quiz_id`: (정수) 퀴즈 연결 ID (선택 사항)
- `anonymous_submissions`: (부울) 익명 제출 가능 여부 (퀴즈 과제인 경우)
- `discussion_topic`: (객체) 관련 토론 주제 정보 (선택 사항)
- `freeze_on_copy`: (부울) 복사 시 과제 동결 여부 (선택 사항)
- `frozen`: (부울) 사용자에게 과제가 동결되었는지 여부 (선택 사항)
- `frozen_attributes`: (문자열 배열) 과제의 동결된 속성들의 리스트 (선택 사항)

### 평가 및 보안
- `moderated_grading`: (부울) 중재 평가 여부 ✅
- `grader_count`: (정수) 중재 평가 담당자 수 ✅
- `final_grader_id`: (정수) 중재 평가 담당자 ID
- `grader_comments_visible_to_graders`: (부울) 평가자에게 중재 평가 의견 표시 여부 ✅
- `graders_anonymous_to_graders`: (부울) 중재 평가자들 간 익명 여부 ✅
- `grader_names_visible_to_final_grader`: (부울) 최종 평가자에게 중재 평가자 식별 정보 표시 여부 ✅
- `anonymous_grading`: (부울) 익명 평가 여부 ✅
- `allowed_attempts`: (정수) 제출 횟수 제한 ✅
- `post_manually`: (부울) 수동으로 성적 게시 여부 ✅
- `score_statistics`: (객체) 성적 통계 정보 (선택 사항)
- `can_submit`: (부울) 과제 제출 권한 여부
- `annotatable_attachment_id`: (정수) 학생이 주석을 달 파일의 첨부 파일 ID (선택 사항)
- `anonymize_students`: (부울) 학생 이름 익명화 여부 (선택 사항) ✅
- `require_lockdown_browser`: (부울) LockDown Browser® 필요 여부 (선택 사항) ✅
- `important_dates`: (부울) 중요한 날짜가 있는지 여부 (선택 사항)
- `anonymous_peer_reviews`: (부울) 익명 피어 리뷰 여부 ✅
- `anonymous_instructor_annotations`: (부울) 익명 강사 주석 여부 ✅
- `graded_submissions_exist`: (부울) 채점된 제출물이 있는지 여부
- `is_quiz_assignment`: (부울) 퀴즈 과제 여부 ✅
- `in_closed_grading_period`: (부울) 닫힌 평가 기간에 있는지 여부 ✅
- `can_duplicate`: (부울) 과제 복제 가능 여부 ✅
- `original_course_id`: (정수) 복제된 경우 원본 과제의 강좌 ID ✅
- `original_assignment_id`: (정수) 복제된 경우 원본 과제의 ID ✅
- `original_lti_resource_link_id`: (정수) 복제된 경우 원본 과제의 LTI 리소스 링크 ID
- `original_assignment_name`: (문자열) 복제된 경우 원본 과제의 이름
- `original_quiz_id`: (정수) 복제된 경우 원본 과제의 퀴즈 ID ✅
- `workflow_state`: (문자열) 과제 상태 ✅

## 📑 canvasapi.module.Module

아래는 Module 객체의 변수들과 그에 대한 자세한 설명입니다.
- [관련 python canvasapi 문서](https://canvasapi.readthedocs.io/en/stable/module-ref.html#module)
- [관련 canvas LMS API 문서](https://canvas.instructure.com/doc/api/modules.html#Module)

### 기본 정보
- `id`: (정수) 모듈의 고유 식별자입니다.
- `workflow_state`: (문자열) 모듈의 상태를 나타냅니다. 'active'는 활성화된 상태, 'deleted'는 삭제된 상태를 의미합니다.
- `position`: (정수) 모듈이 강좌에서의 위치를 나타냅니다. 1부터 시작하는 정수입니다.
- `name`: (문자열) 모듈의 이름입니다.
- `unlock_at`: (날짜 및 시간) 모듈의 잠금이 해제되는 날짜 및 시간을 나타냅니다.
- `require_sequential_progress`: (부울) 모듈 항목들을 순차적으로 해제해야 하는지 여부를 나타냅니다.
- `prerequisite_module_ids`: (정수 배열) 이 모듈이 해제되기 전에 완료되어야 하는 선행 모듈의 식별자(ID) 목록입니다.
- `items_count`: (정수) 모듈 내의 항목(item) 수를 나타냅니다.
- `items_url`: (URL) 이 모듈의 항목들을 가져오기 위한 API URL입니다.
- `items`: (배열) 이 모듈의 내용을 나타내는 Module Items의 배열입니다.
- `state`: (문자열) 호출하는 사용자의 모듈 상태를 나타냅니다. 'locked', 'unlocked', 'started', 'completed' 중 하나입니다. (학생인 경우 또는 'student_id' 옵션을 포함한 경우에만 제공됨)
- `completed_at`: (날짜 및 시간) 호출하는 사용자가 모듈을 완료한 날짜와 시간을 나타냅니다. (학생인 경우 또는 'student_id' 옵션을 포함한 경우에만 제공됨)
- `publish_final_grade`: (부울) 이 모듈을 완료하면 학생의 최종 학점을 SIS에 게시해야 하는지 여부를 나타냅니다.
- `published`: (부울) 이 모듈이 게시되었는지 여부를 나타냅니다. 게시되지 않은 모듈을 볼 수 있는 권한이 있는 경우에만 제공됩니다.

## 🎁 canvasapi.module.ModuleItem

아래는 ModuleItem 객체의 변수들과 그에 대한 자세한 설명입니다.
- [관련 python canvasapi 문서](https://canvasapi.readthedocs.io/en/stable/module-ref.html#moduleitem)
- [관련 canvas LMS API 문서](https://canvas.instructure.com/doc/api/modules.html#Module)

### 기본 정보
- `id`: (정수) 모듈 항목의 고유 식별자입니다.
- `module_id`: (정수) 이 항목이 속한 모듈의 식별자(ID)입니다.
- `position`: (정수) 모듈 내에서 이 항목의 위치를 나타냅니다. 1부터 시작하는 정수입니다.
- `title`: (문자열) 항목의 제목입니다.
- `indent`: (정수) 0부터 시작하는 들여쓰기 수준으로, 모듈 항목을 계층적으로 나타낼 수 있습니다.
- `type`: (문자열) 항목이 가리키는 객체의 유형 중 하나를 나타냅니다. 'File', 'Page', 'Discussion', 'Assignment', 'Quiz', 'SubHeader', 'ExternalUrl', 'ExternalTool' 중 하나입니다.
- `content_id`: (정수) 해당 객체의 식별자(ID)입니다. 'File', 'Discussion', 'Assignment', 'Quiz', 'ExternalTool' 유형에 적용됩니다.
- `html_url`: (URL) Canvas에서 항목에 대한 링크 URL입니다.
- `url`: (URL) 해당하는 Canvas API 객체의 링크 URL입니다. (해당되는 경우에만)
- `page_url`: (문자열) 'Page' 유형에만 해당하는 고유한 위키 페이지의 위치입니다.
- `external_url`: (URL) 'ExternalUrl' 및 'ExternalTool' 유형에만 해당하는 항목이 가리키는 외부 URL입니다.
- `new_tab`: (부울) 'ExternalTool' 유형에만 해당하며, 외부 도구가 새 탭에서 열리는지 여부를 나타냅니다.
- `completion_requirement`: (객체) 이 모듈 항목의 완료 요구 사항을 나타냅니다.
- `content_details`: (객체) 'include[]=content_details'를 통해 요청한 경우, 연관된 객체에 대한 추가 세부 정보를 제공합니다.
- `published`: (부울) 이 모듈 항목이 게시되었는지 여부를 나타냅니다. 게시되지 않은 항목을 볼 수 있는 권한이 있는 경우에만 제공됩니다.
