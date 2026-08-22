---
sidebar:
  order: 36
  label: "036. 정적 분석 결과 해석 (Static Analysis Result Interpretation)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "보안 취약점 판별 및 오탐 제어 : 정적 분석 결과 해석 (SAST Taint Analysis & 트리아지)"
date: "2026-08-22T08:15:00+09:00"
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

- 정의/개념: 정적 분석의 실효성을 극대화하고 개발 생산성을 보증하기 위해 **SAST 도구 스캔 $\rightarrow$ Source-Sanitizer-Sink 오염 데이터 흐름(Taint Analysis) 추적 $\rightarrow$ 참 양성(TP) / 거짓 양성(FP) / 기한부 위험수용(Waiver) 트리아지 판정 $\rightarrow$ 고위험 진탐(TP) 즉각 패치 $\rightarrow$ CI/CD 품질 게이트(Quality Gate) 자동 배포 차단** 을 집행하는 **DevSecOps 정적 보안 거버넌스 체계**
- 배경/필요성: 정적 분석 도구는 컴파일 시점의 정적 구문만을 검사하므로 문맥(Context)을 이해하지 못해 30~50%의 높은 오탐률을 유발하므로, 도구의 출력을 맹신하지 않고 정밀 해석하는 엔지니어링 절차 필수

#### 한줄 요약
- 정적 분석 결과 해석은 Taint 오염 분석과 도달 가능성 검증을 통해 진짜 결함(TP)과 단순 오탐(FP)을 판별한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **오염 분석 3대 핵심 모델 (Taint Analysis Model)**:
  - **오염원 (Source)**: 신뢰할 수 없는 외부 사용자 입력이 시스템으로 유입되는 진입점 (예: `request.getParameter()`, HTTP Body).
  - **정화/살균기 (Sanitizer / Validator)**: 악의적인 특수문자를 무해화하거나 화이트리스트를 검증하는 방어 로직 (예: `PreparedStatement`, HTML Escape).
  - **취약점 실행점 (Sink)**: 정화되지 않은 입력값이 주입될 경우 치명적 명령이 실행되는 위험 함수 (예: `Statement.executeQuery()`, `Runtime.exec()`).

</details>

- **오염 데이터 흐름(Taint Flow)의 완결성 추적**: Source에서 생성된 더러운 데이터(Tainted Data)가 변수 할당, 함수 인자 전달, 객체 필드 저장을 거쳐 Sink에 도달할 때까지 중간에 안전한 Sanitizer를 거쳤는지 여부를 전수 추적
- **런타임 도달 가능성(Reachability Analysis) 검증**: 경고가 발생한 코드가 실제로 HTTP 엔드포인트를 통해 호출될 수 있는지, 아니면 폐기된 데드 코드(Dead Code)나 테스트 전용 코드인지 판별
- **기한부 위험 수용(Time-bound Waiver) 통제**: 아키텍처 구조상 즉시 수정이 불가능한 진탐(TP)에 대해 웹 방화벽(WAF) 룰 적용 등 보완 통제를 수립하고 최대 90일 기한부로만 조건부 예외 승인

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

| 컴포넌트 | 핵심 기능 및 역할 | 분석 방법론 | 비고 |
|:---|:---|:---|:---|
| **SAST 스캔 엔진** | 소스코드 AST 및 제어 흐름 그래프(CFG) 생성 후 규칙 매칭 | Static Pattern Matching, CFG | Detection |
| **오염 분석기 (Taint)** | 외부 파라미터가 정화 없이 위험 함수로 전달되는 경로 추적 | Inter-procedural Data Flow | Taint Flow |
| **보안 트리아지 팀** | 보안 전문가와 개발자가 모여 경고의 실제 익스플로잇 가능성 검토| CVSS 점수, 런타임 환경 분석 | Triage |
| **Waiver 대장** | 즉각 수정 불가 항목에 대한 기한부 위험 수용 이력 관리 | 90일 TTL, 감사 로그 기록 | Governance |
| **품질 게이트 (Gate)** | 해결되지 않은 Critical/High TP 존재 시 배포 자동 중단 | SonarQube Quality Gate, Jenkins Plugin | Gatekeeper |

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
1. [CI/CD 자동 SAST 스캔 실행]
    ├─ 소스코드 푸시 ➔ SonarQube / Fortify 정적 분석 자동 트리거
    └─ [스캔 결과: 총 450건 경고 발생 (Critical: 5건, High: 20건, Low: 425건)]
            │
            ▼
2. [Taint Data Flow 및 경로 추적]
    ├─ [경고 1 분석]: `Controller.search()` ➔ `UserService.find()` ➔ `Statement.execute()`
    ├─ 외부 입력 파라미터가 어떤 검증 함수도 거치지 않고 직접 SQL 문자열과 결합 확인
    └─ [판정: SQL Injection 참 양성 (True Positive, Critical TP)]
            │
            ▼
3. [전문가 트리아지 (Triage) 판정]
    ├─ Critical 5건 중: 3건 진탐(TP), 2건 오탐(FP: 커스텀 프레임워크 자체 암호화 사용)
    ├─ 오탐 2건: 정적 분석 도구의 Custom Sanitizer 룰셋에 등록하여 다음 스캔부터 제외
    └─ [진탐 3건: DevSecOps 품질 게이트에 즉각 'FAILED' 신호 전송]
            │
            ▼
4. [배포 파이프라인 자동 차단 및 코드 패치]
    ├─ GitLab PR(Pull Request) 머지 자동 차단 (Merge Blocked)
    ├─ 개발자가 취약 코드를 `PreparedStatement` 및 MyBatis 파라미터 바인딩(`#`)으로 수정
    └─ [수정 소스코드 재커밋 및 자동 재스캔 수행]
            │
            ▼
5. [재스캔 검증 및 품질 게이트 통과]
    ├─ 재분석 결과: Critical/High 참 양성(TP) 0건 달성 확인
    └─ [품질 게이트 'PASSED' 전환 ➔ 상용 프로덕션 무결점 안전 배포 승인]
```

**동작 원리**

1. **상호 프로시저 분석(Inter-procedural Analysis)**: 함수 내부뿐만 아니라 함수 A $\rightarrow$ 함수 B $\rightarrow$ 함수 C로 파라미터가 5단계를 거쳐 넘어가도 오염 상태를 100% 추적
2. **커스텀 살균기(Custom Sanitizer)의 룰셋 등록**: 사내 공통 프레임워크의 자체 필터링 함수를 정적 분석 도구에 '안전한 Sanitizer'로 명시 등록하여 수천 건의 오탐을 1초 만에 제거
3. **거짓 양성(FP)의 사유 명문화**: 오탐으로 처리할 때는 반드시 "라인 45번의 XSS 방어 유틸리티에 의해 HTML 인코딩 완료됨"과 같은 기술적 증거를 시스템에 남겨 감사 추적성 확보
4. **만료형 Waiver의 자동 부활**: 기한부 위험 수용(Waiver)으로 넘긴 취약점은 90일이 지나면 시스템이 자동으로 '미해결 TP'로 원복시켜 다음 배포를 자동 차단
5. **Shift-Left 비용 절감**: 컴파일/빌드 단계에서 10분 만에 정적 분석으로 결함을 잡음으로써 상용 환경 침해 사고 대응 비용 대비 99% 비용 절감

#### 한줄 요약
- 자동 SAST 스캔, Taint 경로 추적, 전문가 트리아지, 배포 파이프라인 차단 및 패치, 재스캔 후 품질 게이트 통과 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **정적 분석 트리아지 판정 3대 상태 비교**:
  - 참 양성 (True Positive): 실제 익스플로잇 가능한 결함 (즉각 수정).
  - 거짓 양성 (False Positive): 도구의 한계로 인한 오탐 (예외 등록 및 룰 튜닝).
  - 기한부 위험 수용 (Waiver): 즉각 수정 불가하나 보완 통제 적용 (기한부 허용).

</details>

| 비교 항목 | 참 양성 (True Positive: 진탐) | 거짓 양성 (False Positive: 오탐) | 기한부 위험 수용 (Time-bound Waiver) |
|:---|:---|:---|:---|
| **실제 공격 가능성** | **100% 런타임 공격 가능 (Exploitable)**| **0% 공격 불가능 (Non-exploitable)**| 공격 가능하나 보완 통제로 억제 |
| **조치 우선순위** | **최우선 조치 (P0, 즉각 코드 패치)**| **조치 불필요 (오탐 예외 처리)** | **차기 릴리스 조치 (기한 내 패치)** |
| **배포 게이트 영향** | **배포 즉시 차단 (Build Failure)** | **배포 정상 통과 (Pass)** | **조건부 배포 승인 (Conditional Pass)**|
| **관리 방법** | 버그 픽스 후 재스캔으로 소멸 검증| 오탐 사유 문서화 및 룰셋 튜닝 | CISO 서명 승인 및 90일 TTL 설정 |
| **방치 시 위험도** | **데이터 유출, 서비스 셧다운 참사**| 개발자 신뢰 상실 및 분석 기피 | 기한 만료 후 보안 부채로 전락 |

#### 한줄 요약
- 진탐(TP)은 배포 차단 및 즉각 패치, 오탐(FP)은 룰셋 예외 처리, Waiver는 90일 기한부 조건부 승인이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **정적 분석 해석 실무 운영 시 3대 위험 요소와 엔지니어링 대책**:

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수천 건의 오탐 경고로 인해 개발팀이 분석 결과를 아예 보지 않고 **소스코드에 `@SuppressWarnings` 주석을 도배하여 치명적 진탐까지 은폐** | **개발자의 임의 예외 주석 사용을 금지하고, 보안 담당자의 승인을 거쳐야만 SAST 서버에서 오탐 예외가 등록되는 중앙 통제 거버넌스 확립** | 무분별한 취약점 은폐 100% 방지 |
| 정적 분석 도구의 기본 룰셋만 사용하여 사내 자체 프레임워크의 보안 필터를 인식하지 못해 **모든 DB 쿼리마다 SQLi 오탐이 발생하는 생산성 마비** | **사내 자체 Sanitizer 및 인코더 함수를 SAST 도구의 커스텀 룰셋(Custom Taint Rules)으로 등록하여 오탐 원천 제거** | 분석 정확도 향상 및 오탐률 80% 이상 급감 |
| 즉시 수정이 불가능한 진탐을 Waiver(위험수용)로 등록해두고 5년간 방치하여 **결국 해당 레거시 코드가 해킹당해 고객 정보가 유출되는 사고 발생** | **모든 Waiver 항목에 최대 90일의 만료 시한(TTL)을 강제하고 만료 시 CI/CD 배포를 자동으로 다시 차단하는 만료형 거버넌스 집행** | 장기 보안 부채 누적 원천 차단 |

#### 한줄 요약
- 중앙 승인으로 주석 남용을 막고, 커스텀 룰셋으로 오탐을 줄이며, 90일 만료제로 Waiver 방치를 차단한다.

## Ⅶ. 결론

- 정적 분석 도구가 쏟아내는 수많은 기계적 경고 속에서 진짜 침해 위협을 정확히 골라내고 소프트웨어의 본원적 안전성을 확보하는 핵심 기술인 **정적 분석 결과 해석 및 트리아지 체계**는 단순한 도구 도입을 넘어 개발과 보안의 조화로운 협업을 이끄는 DevSecOps의 핵심 교량이며, 실무 구현 시 **Source-Sanitizer-Sink 기반의 정밀 오염 분석(Taint Analysis)**, **진탐(TP)과 오탐(FP)의 객관적 판별 기준 수립**, **사내 프레임워크 맞춤형 커스텀 룰셋 최적화**, **만료형 Waiver 거버넌스 및 CI/CD 품질 게이트 강제**를 완성하여 최고 수준의 소스코드 보안 무결점과 안전한 지속적 배포를 완성

#### 한줄 요약
- Taint 오염 분석과 DevSecOps 품질 게이트를 통해 진짜 보안 취약점(TP)을 선제적으로 완벽히 격리한다.
