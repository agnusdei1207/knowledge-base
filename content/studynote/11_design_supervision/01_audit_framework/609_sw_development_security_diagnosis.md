+++
title = "소프트웨어 개발 보안 진단 (SW Development Security Diagnosis)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-design"]

[extra]
tags = ["studynote-design"]
+++

> **핵심 인사이트 3줄**
> 1. SW 개발 보안 진단은 [시큐어 코딩](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/)([Secure Coding](/knowledge-base/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/)) 준수 여부를 체계적으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해 취약점이 운영 환경에 배포되기 전에 제거하는 예방적 보안 활동이다.
> 2. 행안부 SW 개발 보안 가이드([OWASP Top 10](/knowledge-base/studynote/09_security/05_web_app_security/416_owasp_top_10/) 연계) 기반 43개 보안 약점 진단이 공공기관 정보시스템 사업에 법적으로 의무화되어 있다.
> 3. [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)·[DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/)·[IAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/493_iast_interactive_analysis/) 자동화 도구와 수동 코드 리뷰를 결합한 [DevSecOps](/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/) 파이프라인 통합이 현대적 적용 방향이다.

---

## Ⅰ. SW 개발 보안 진단의 정의와 법적 근거

SW 개발 보안 진단은 <strong>소프트웨어 개발 생명주기(<a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/">SDLC</a>)에서 보안 취약점을 조기 발견·제거</strong>하는 활동이다.

### 법적 근거 (국내)

| 법률·지침                  | 핵심 내용                              |
|-------------------------|--------------------------------------|
| 전자정부법 제45조          | 정보시스템 개발 시 보안 취약점 점검 의무  |
| 행안부 SW 개발 보안 가이드  | 43개 보안 약점 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)·진단 기준           |
| 정보보호관리체계([ISMS-P](/knowledge-base/studynote/12_it_management/05_security_compliance/171_isms_p/))   | 개발 환경·소스코드 보안 통제 요구        |

### 보안 진단 범위

```
요구사항 -> 설계 -> 구현 -> 테스트 -> 배포
    v        v       v       v       v
위협 모델링  보안 설계  소스코드  침투 테스트  취약점 모니터링
              검토    정적 분석
```

📢 **섹션 요약 비유**: SW 보안 진단은 건물 완공 전 소방 검사다 — 완공 후 화재가 나는 것보다 공사 중 배관을 검사하는 게 훨씬 저렴하고 안전하다.

---

## Ⅱ. 행안부 43개 보안 약점 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)

### 주요 카테고리 (7대 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/))

| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)                | 대표 약점                          |
|-------------------|-----------------------------------|
| 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)   | SQL 삽입, [XSS](/knowledge-base/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/), [경로 순회](/knowledge-base/studynote/09_security/05_web_app_security/419_path_traversal/)           |
| [보안 기능](/knowledge-base/studynote/04_software_engineering/11_testing_validation/895_security_features_design/)          | 취약 암호화, 하드코딩 비밀번호     |
| 시간 및 상태        | [TOCTOU](/knowledge-base/studynote/02_operating_system/04_synchronization/273_toctou/) (검사 후 사용)              |
| 오류 처리           | 오류 정보 과다 노출                 |
| 코드 오류           | NULL 포인터 역참조                  |
| 캡슐화              | 중요 정보 평문 저장                 |
| [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 오용            | [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) Lookup에만 의존한 보안 결정    |

### [OWASP Top 10](/knowledge-base/studynote/09_security/05_web_app_security/416_owasp_top_10/) ([2021](/knowledge-base/studynote/04_software_engineering/11_testing_validation/869_owasp_top_10_2021/)) 연계

```
A01 접근 제어 취약점    -- 행안부 #01~05 매핑
A02 암호화 오류         -- 행안부 #11~15 매핑
A03 인젝션              -- 행안부 #16~20 매핑
...
```

📢 **섹션 요약 비유**: 43개 보안 약점은 자동차 안전 점검 항목이다 — 브레이크, 타이어, 에어백처럼 분야별 점검이 모두 통과해야 도로에 나올 수 있다.

---

## Ⅲ. [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/) / [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/) / [IAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/493_iast_interactive_analysis/) 진단 도구

| 도구 유형 | 설명                            | 대표 도구              |
|---------|--------------------------------|-----------------------|
| [SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)    | 소스코드 [정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) (코드 실행 불필요) | [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/), Checkmarx |
| [DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/)    | 실행 중 [동적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/332_dynamic_analysis/) ([블랙박스 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/804_black_box_testing/)) | [OWASP ZAP](/knowledge-base/studynote/09_security/05_web_app_security/485_owasp_zap/), [Burp Suite](/knowledge-base/studynote/09_security/05_web_app_security/486_burp_suite/) |
| [IAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/493_iast_interactive_analysis/)    | 런타임 계측 기반 (에이전트 삽입)   | Seeker, Contrast      |
| [SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/)     | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 구성 분석               | FOSSA, Snyk           |

```
CI/CD 파이프라인 통합:
코드 커밋 -> SAST 자동 스캔 -> PR 차단 or 경고
   v
빌드 -> SCA (종속성 취약점) -> 빌드 차단
   v
스테이징 -> DAST (API 퍼징) -> 배포 차단
   v
프로덕션 -> IAST + RASP (런타임 보호)
```

📢 **섹션 요약 비유**: SAST는 출판 전 교정 교열이고, DAST는 책이 출판된 후 독자 반응 테스트다. IAST는 독서 중 독자 눈 움직임을 실시간 추적한다.

---

## Ⅳ. 진단 절차와 결과 보고

### 수행 절차

```
1. 진단 계획 수립: 범위·일정·도구 선정
2. 정적 분석 (SAST): 소스코드 전수 스캔
3. 동적 분석 (DAST): 빌드 환경 침투 테스트
4. 수동 코드 리뷰: 자동화 미탐지 로직 취약점
5. 결과 분류: 위험도(Critical/High/Medium/Low) 분류
6. 취약점 조치: 개발팀 수정 -> 재진단
7. 결과 보고서: 취약점 현황·조치 결과·잔존 위험
```

### 위험도 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 기준

| 등급        | [CVSS](/knowledge-base/studynote/09_security/04_endpoint_security/407_cvss_scoring/) 점수  | 조치 기한    |
|-----------|-----------|------------|
| Critical  | 9.0~[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/).0  | 즉시 (24h) |
| High      | 7.0~8.9   | 3일 이내   |
| Medium    | 4.0~6.9   | 7일 이내   |
| Low       | 0.1~3.9   | 다음 릴리즈 |

📢 **섹션 요약 비유**: 취약점 위험도 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)는 응급실 중증도 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)와 같다 — Critical은 즉시 수술, High는 당일 입원, Low는 외래 예약이다.

---

## Ⅴ. [DevSecOps](/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/) 통합과 현대화

```
DevOps 파이프라인에 Security 통합:

Plan -> Code -> Build -> Test -> Release -> Deploy -> Operate
  v      v      v       v       v         v        v
위협  SAST   SCA    DAST  서명   RASP    취약점
모델링                         검증           모니터링
```

### 성숙도 모델 ([BSIMM](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/472_bsimm_maturity_model/) / SAMM)

| 수준  | 특징                               |
|------|-----------------------------------|
| 레벨 1 | 수동 점검, 릴리즈 전 1회           |
| 레벨 2 | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 자동화, 이슈 트래킹 연동    |
| 레벨 3 | 실시간 보안 게이트, 자동 수정 제안 |

📢 **섹션 요약 비유**: DevSecOps는 조립 라인 품질 검사와 같다 — 완성품 검사(릴리즈 전 점검)보다 각 공정마다 센서([SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)/[DAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/492_dast_dynamic_analysis/))를 붙이면 불량을 훨씬 빨리 잡는다.

---

## 📌 관련 개념 맵

```
SW 개발 보안 진단
+-- 법적 근거
|   +-- 전자정부법·행안부 가이드
|   +-- 43개 보안 약점 분류
+-- 진단 도구
|   +-- SAST (정적 분석)
|   +-- DAST (동적 분석)
|   +-- IAST (계측 분석)
|   +-- SCA (오픈소스 분석)
+-- 기준
|   +-- OWASP Top 10
|   +-- CWE/CVE
|   +-- CVSS 위험도 점수
+-- 현대화
    +-- DevSecOps 파이프라인 통합
    +-- BSIMM / SAMM 성숙도 모델
    +-- RASP (런타임 자기 보호)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|           SW 개발 보안 진단 발전 흐름                            |
+--------------+--------------------+-----------------------------+
| 2000년대 초  | 사후 침투 테스트   | 운영 중 취약점 발견·패치     |
| 2004년       | OWASP Top 10 등장  | 웹 취약점 표준 분류          |
| 2010년대     | SAST 도구 성숙      | SonarQube·Checkmarx 도입    |
| 2015년       | 행안부 가이드 v2.0 | 공공 SW 개발 보안 의무화     |
| 2018년       | DAST·IAST 통합     | CI/CD 파이프라인 보안 게이트 |
| 2020년대     | DevSecOps 표준화    | 자동화·AI 취약점 탐지       |
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
SDLC -> Secure SDLC -> SAST/DAST -> DevSecOps
  v         v            v
요구사항  위협 모델링  CI/CD 보안 게이트
  v
OWASP Top 10 -> 43개 약점 -> CVSS 점수 -> 조치 우선순위
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. SW 보안 진단은 자동차 출고 전 안전 검사다 — 도로에 나가기 전에 브레이크([보안 기능](/knowledge-base/studynote/04_software_engineering/11_testing_validation/895_security_features_design/))가 제대로 작동하는지 확인한다.
2. SAST는 시험지를 제출 전에 선생님이 미리 검사하는 것이다 — 오답을 미리 찾아서 고칠 수 있다.
3. DevSecOps는 음식 만들면서 맛을 보는 것이다 — 다 만들고 맛보는 것보다 중간중간 확인하면 훨씬 맛있는 요리가 나온다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 41 / 530

<- **이전**: [32. 감리 자동화 도구 (Audit Automation Tools)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/032_audit_automation_tools/)
**다음**: [33. 기능점수 검증 (Function Point Verification)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/033_function_point_verification/) ->

---
