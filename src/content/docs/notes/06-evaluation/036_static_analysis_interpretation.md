---
sidebar:
  order: 36
  label: "036. 정적 분석 결과 해석 (Static Analysis Result Interpretation)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "보안 취약점 판별 및 오탐 제어 : 정적 분석 결과 해석 (SAST Taint Analysis & 트리아지)"
date: "2026-08-26T16:05:56+09:00"
tags:
  - "notes-evaluation"
weight: 36
extra:
  question_no: "036"
  source_status: "기출"
  source_history: "128회"
  priority: 50
  priority_note: "128회 기출, 정적 애플리케이션 보안 테스트(SAST: Static Application Security Testing) 결과 해석, 오염 분석(Taint Analysis: Source ➔ Sanitizer ➔ Sink), 오탐(False Positive) vs 진탐(True Positive) 판별 기준, 보안 트리아지(Triage) 절차, 기한부 위험 수용(Time-bound Waiver) 및 DevSecOps 품질 게이트(Quality Gate) 연계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **정적 분석 결과 해석 및 보안 트리아지(Static Analysis Result Interpretation & Triage)**: 정적 분석 도구(SAST: Fortify, SonarQube, Checkmarx 등)가 소스코드를 스캔하여 출력한 수천 건의 원시 보안 경고(Raw Alerts)에 대해, 외부 입력(Source)에서 위험 실행점(Sink)까지의 오염 데이터 흐름(Taint Flow), 살균 함수(Sanitizer)의 유효성, 그리고 런타임 도달 가능성(Reachability)을 정밀 분석하여, 실제 공격 가능한 참 양성(True Positive, TP: 진탐)과 도구의 한계로 인한 거짓 양성(False Positive, FP: 오탐)을 과학적으로 선별·분류하는 전문 보안 엔지니어링 활동.
- **경고 피로증 및 무분별한 예외 억제 결함(Alert Fatigue & Blind Suppression Defect)**: 수천 건의 정적 분석 오탐 경고에 지친 개발팀이 경고를 전면 무시하거나 소스코드에 `@SuppressWarnings` 주석을 남발하여 실제 치명적인 SQL Injection 및 RCE(원격 코드 실행) 참 양성 취약점까지 통째로 은폐시켜 상용 환경에서 대규모 해킹을 당하는 구조적 결함.

</details>

- 정의/개념: SAST 경고의 공격 가능성을 판정하는 **보안 트리아지**
- 배경/필요성: 정적 규칙만으로는 **진탐·오탐 구분 불가**

#### 한줄 요약
- 정적 분석 결과 해석은 Taint 오염 분석과 도달 가능성 검증을 통해 진짜 결함(TP)과 단순 오탐(FP)을 판별한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **오염 분석 3대 핵심 모델 (Taint Analysis Model)**:
  - **오염원 (Source)**: 신뢰할 수 없는 외부 사용자 입력이 시스템으로 유입되는 진입점 (예: `request.getParameter()`, HTTP Body).
  - **정화/살균기 (Sanitizer / Validator)**: 악의적인 특수문자를 무해화하거나 화이트리스트를 검증하는 방어 로직 (예: `PreparedStatement`, HTML Escape).
  - **취약점 실행점 (Sink)**: 정화되지 않은 입력값이 주입될 경우 치명적 명령이 실행되는 위험 함수 (예: `Statement.executeQuery()`, `Runtime.exec()`).

</details>

- Source부터 Sink까지 추적하는 **오염 데이터 흐름**
- 경고 코드의 실행 여부를 확인하는 **도달 가능성 분석**
- 보완 통제와 만료일을 요구하는 **기한부 위험 수용**

#### 한줄 요약
- Source-Sanitizer-Sink 오염 분석, 런타임 도달 가능성 검증, 진탐(TP)/오탐(FP) 판별, 기한부 Waiver 통제를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **정적 분석 결과 4분면 분류 매트릭스 (Confusion Matrix)**:
  1. **참 양성 (True Positive, TP / 진탐)**: 실제 취약점이며 도구도 취약점으로 정확히 경고 (즉각 패치 대상).
  2. **거짓 양성 (False Positive, FP / 오탐)**: 실제로는 안전하나 도구가 취약점으로 잘못 경고 (예외 룰셋 등록).
  3. **거짓 음성 (False Negative, FN / 미탐)**: 실제 취약점이나 도구가 탐지하지 못하고 놓침 (최악의 보안 사고).
  4. **참 음성 (True Negative, TN / 정상)**: 안전한 코드이며 도구도 경고를 발생시키지 않음 (정상).

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. Taint Analysis 기반 정적 분석 결과 해석 및 오탐 판별 구조 ]        │
│                                                                         │
│  [ 1. 오염원 (Source) ] ➔ String input = request.getParameter("id");    │
│            │                                                            │
│            ▼                                                            │
│  [ 2. 정화 여부 판정 (Sanitizer Check) ]                                │
│       ├─ Case A (미정화): String query = "SELECT * FROM u WHERE id=" + input;│
│       │                   └──► [ 3. 위험점 (Sink) ] Statement.execute(query);│
│       │                        └──► [ 판정: 참 양성 (True Positive, TP) ➔ 즉시 차단 ]│
│       │                                                                 │
│       └─ Case B (정화됨): PreparedStatement pstmt = con.prepareStatement(...);│
│                           pstmt.setString(1, input);                    │
│                           └──► [ 판정: 거짓 양성 (False Positive, FP) ➔ 오탐 예외 ]│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (전문가 트리아지 파이프라인)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. 보안 트리아지(Triage) 및 DevSecOps 품질 게이트 연동 ]              │
├───────────────────┬─────────────────────────────────┬───────────────────┤
│ 트리아지 분류     │ 판정 근거 및 보완 조치          │ CI/CD 파이프라인 액션│
├───────────────────┼─────────────────────────────────┼───────────────────┤
│ **참 양성 (TP)**  │ Source ➔ Sink 도달 확인, 정화 없음│ **빌드/배포 즉시 차단 (Block)**│
│ **(진탐 - High)** │ (SQLi, XSS, RCE, 평문 비밀번호) │ Jira 긴급 보안 티켓 자동 발행     │
├───────────────────┼─────────────────────────────────┼───────────────────┤
│ **거짓 양성 (FP)**│ 커스텀 정화 로직 또는 도달 불가 │ **오탐 예외 승인 (Dismiss)**     │
│ **(오탐 - False)**│ (사유서 등록 ➔ 룰셋 튜닝)       │ 파이프라인 무중단 통과            │
├───────────────────┼─────────────────────────────────┼───────────────────┤
│ **위험 수용**     │ 즉각 수정 불가하나 WAF 룰 보완  │ **조건부 승인 (Waiver)**         │
│ **(Waiver)**      │ (보안 리더 서명, 90일 만료제)   │ 90일 경과 시 재차단               │
└───────────────────┴─────────────────────────────────┴───────────────────┘
```

선의 의미: Source에서 Sink로 이어지는 Taint Flow를 분석하여 Case A는 진탐(TP), Case B는 오탐(FP)으로 판정하고 CI/CD 게이트와 연동하는 구조

| 구성요소 | 책임 |
|:---|:---|
| SAST 스캔 엔진 | AST·CFG 기반 **보안 경고** 생성 |
| 오염 분석기 | Source부터 Sink까지 **Taint Flow** 추적 |
| 보안 트리아지 | 도달 가능성과 **Sanitizer 유효성** 판정 |
| Waiver 대장 | 보완 통제와 **만료 기한** 관리 |
| 품질 게이트 | 미해결 고위험 **진탐 배포 차단** |

#### 한줄 요약
- SAST 스캔 엔진, Taint 오염 분석기, 보안 트리아지 팀, 기한부 Waiver 대장, CI/CD 품질 게이트로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **정적 분석 결과 해석 및 조치 5단계 프로세스**:
  1. 개발자가 코드를 Git에 푸시하면 CI 파이프라인에서 SAST 도구가 소스코드 자동 스캔
  2. 도구가 검출한 경고 목록 중 Critical/High 등급 취약점 자동 추출
  3. 보안 엔지니어가 Taint Flow 및 Sanitizer 유효성을 검토하여 TP vs FP 트리아지 수행
  4. 확인된 진탐(TP)은 개발팀에 즉각 수정 요청하고 CI/CD 파이프라인에서 빌드 머지 차단
  5. 수정 코드 재스캔 후 진탐 0건 확인 시 품질 게이트 통과 및 안전한 프로덕션 배포

</details>

```text
1. SAST 경고 수집
    ├─ 소스코드 푸시 ➔ SonarQube / Fortify 정적 분석 자동 트리거
    └─ [스캔 결과: 총 450건 경고 발생 (Critical: 5건, High: 20건, Low: 425건)]
            │
            ▼
2. Taint Flow 추적
    ├─ [경고 1 분석]: `Controller.search()` ➔ `UserService.find()` ➔ `Statement.execute()`
    ├─ 외부 입력 파라미터가 어떤 검증 함수도 거치지 않고 직접 SQL 문자열과 결합 확인
    └─ [판정: SQL Injection 참 양성 (True Positive, Critical TP)]
            │
            ▼
3. TP·FP 판정
    ├─ Critical 5건 중: 3건 진탐(TP), 2건 오탐(FP: 커스텀 프레임워크 자체 암호화 사용)
    ├─ 오탐 2건: 정적 분석 도구의 Custom Sanitizer 룰셋에 등록하여 다음 스캔부터 제외
    └─ [진탐 3건: DevSecOps 품질 게이트에 즉각 'FAILED' 신호 전송]
            │
            ▼
4. 패치·예외 처리
    ├─ GitLab PR(Pull Request) 머지 자동 차단 (Merge Blocked)
    ├─ 개발자가 취약 코드를 `PreparedStatement` 및 MyBatis 파라미터 바인딩(`#`)으로 수정
    └─ [수정 소스코드 재커밋 및 자동 재스캔 수행]
            │
            ▼
5. 재스캔·게이트 판정
    ├─ 재분석 결과: Critical/High 참 양성(TP) 0건 달성 확인
    └─ [품질 게이트 'PASSED' 전환 ➔ 상용 프로덕션 무결점 안전 배포 승인]
```

**동작 원리**

1. **SAST 경고 수집**: 위험도별 원시 경고 목록 생성
2. **Taint Flow 추적**: Source·Sanitizer·Sink 경로 확인
3. **TP·FP 판정**: 공격 가능성과 도달 가능성 분류
4. **패치·예외 처리**: 진탐 수정과 오탐 근거 등록
5. **재스캔·게이트 판정**: 미해결 진탐 기준 배포 결정

#### 한줄 요약
- 자동 SAST 스캔, Taint 경로 추적, 전문가 트리아지, 배포 파이프라인 차단 및 패치, 재스캔 후 품질 게이트 통과 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **정적 분석 트리아지 판정 3대 상태 비교**:
  - 참 양성 (True Positive): 실제 익스플로잇 가능한 결함 (즉각 수정).
  - 거짓 양성 (False Positive): 도구의 한계로 인한 오탐 (예외 등록 및 룰 튜닝).
  - 기한부 위험 수용 (Waiver): 즉각 수정 불가하나 보완 통제 적용 (기한부 허용).

</details>

| 비교 항목 | 진탐 | 오탐 | 기한부 위험 수용 |
|:---|:---|:---|:---|
| 적용 기준 | **공격 가능 경로** 확인 | **안전 경로** 확인 | 즉시 수정 불가한 **실제 위험** |
| 조치 | **즉시 패치** | 근거 기반 **예외 등록** | 보완 통제와 **만료일 설정** |
| 배포 | **게이트 차단** | **정상 통과** | **조건부 승인** |
| 한계 | 미조치 시 **침해 위험** | 오판 시 **취약점 은폐** | 만료 방치 시 **보안 부채** |

#### 한줄 요약
- 진탐(TP)은 배포 차단 및 즉각 패치, 오탐(FP)은 룰셋 예외 처리, Waiver는 90일 기한부 조건부 승인이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **정적 분석 해석 실무 운영 시 3대 위험 요소와 엔지니어링 대책**:

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 임의 예외로 **진탐 은폐** | 보안 담당자의 **중앙 예외 승인** | **취약점 은폐** 방지 |
| 사내 필터 미인식으로 **오탐 증가** | Sanitizer의 **커스텀 룰셋** 등록 | **분석 정확도** 향상 |
| Waiver 만료 후 **위험 방치** | TTL 만료 시 **게이트 재차단** | **보안 부채** 통제 |

#### 한줄 요약
- 중앙 승인으로 주석 남용을 막고, 커스텀 룰셋으로 오탐을 줄이며, 90일 만료제로 Waiver 방치를 차단한다.

## Ⅶ. 결론

- 공격 가능 경로는 **즉시 패치**, 안전 경로는 **근거 기반 예외** 처리

#### 한줄 요약
- Taint 오염 분석과 DevSecOps 품질 게이트를 통해 진짜 보안 취약점(TP)을 선제적으로 완벽히 격리한다.
