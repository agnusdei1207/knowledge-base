---
sidebar:
  order: 145
  label: "145. SAST•DAST•IAST•RASP"
  badge:
    text: "기출 · 70%"
    variant: note
title: "애플리케이션 보안 테스팅 및 런타임 자가 방어 : SAST vs DAST vs IAST vs RASP (OWASP Top 10 & CWE)"
date: "2026-08-26T15:22:43+09:00"
tags:
  - "notes-security"
weight: 145
extra:
  question_no: "145"
  source_status: "기출"
  source_history: "128회, 135회"
  priority: 70
  priority_note: "128회·135회 기출, 4대 애플리케이션 보안 검증 및 방어 기술(SAST 정적 소스코드 분석, DAST 동적 퍼징 테스트, IAST 바이트코드 계측 상호작용 분석, RASP 런타임 자가 방어), White-box vs Black-box vs Glass-box vs In-App Protection, Taint Analysis 및 Bytecode Instrumentation, OWASP ASVS 연계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **애플리케이션 보안 테스팅 및 자가 방어(AST & RASP / OWASP ASVS)**: 소프트웨어 개발 생명주기(SDLC) 전반에 걸쳐 소스코드 문법 분석(SAST: Static AST), 외부 HTTP 페이로드 주입(DAST: Dynamic AST), 바이트코드 계측(IAST: Interactive AST), 그리고 프로덕션 런타임 메모리 후킹 자가 방어(RASP: Runtime Application Self-Protection)를 결합하여 소프트웨어 취약점을 조기 탐지하고 제로데이 공격을 능동 차단하는 애플리케이션 보안 프레임워크.
- **단일 검증 도구의 사각지대 및 오탐 결함(Siloed AST Blind Spot Defect)**: SAST 단독 사용 시 실행 컨텍스트 부재로 수천 건의 오탐(False Positive)이 발생하고, DAST 단독 사용 시 정확한 소스코드 라인을 알 수 없으며(No Line Number), 릴리스 후 런타임 제로데이 공격에 무방비로 노출되는 구조적 결함.

</details>

- 정의/개념: 애플리케이션의 본원적 소프트웨어 복원력을 확보하기 위해 **코딩 시 SAST Taint 오염 분석 $\rightarrow$ QA 시 IAST 바이트코드 계측 $\rightarrow$ 스테이징 시 DAST 웹 취약점 퍼징 $\rightarrow$ 런타임 RASP 컨텍스트 기반 실시간 쿼리 위변조 차단** 을 집행하는 **계층적 응용 보안 파이프라인 아키텍처**
- 배경/필요성: 정적 분석은 코드 위치를 알지만 실행 맥락이 없어 오탐 검증 비용을 남기고 동적 분석은 그 반대이므로, 실행 중 계측으로 둘을 잇는 **IAST**와 런타임에 상주하는 RASP를 단계별로 배치해 검증 시점을 개발 주기 전반에 분산한 것

#### 한줄 요약
- SAST(정적), DAST(동적), IAST(계측), RASP(자가방어)를 결합하여 개발부터 런타임까지 전주기 보안을 완성한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **4대 AST 기술의 가시성(Visibility) 및 접근 모델**:
  - **SAST (White-box)**: AST(추상 구문 트리) 및 CFG/DFG 그래프 기반의 소스코드 화이트박스 정적 분석.
  - **DAST (Black-box)**: 외부에서 공격 페이로드를 주입하고 HTTP 응답 패턴을 분석하는 블랙박스 동적 테스트.
  - **IAST (Glass-box)**: WAS 내부 바이트코드 인스트루멘테이션(Instrumentation)을 통한 런타임 내부 흐름 계측.
  - **RASP (In-App Protection)**: JVM/CLR 시스템 콜 및 SQL 파서 후킹(Hooking) 기반의 런타임 자가 방어.

</details>

- 개발 단계 탐지와 운영 차단을 잇는 **전주기 방어**
- Source·Sanitizer·Sink를 추적하는 **Taint 분석**
- 실행된 코드 경로만 계측하는 **IAST 오탐 감소**

#### 한줄 요약
- 화이트/블랙/글래스박스 상호보완, Taint 오염 흐름 추적, 런타임 바이트코드 계측, 실시간 자가 방어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **4대 애플리케이션 보안 기술 핵심 아키텍처 컴포넌트**:
  1. **SAST Engine**: Lexer/Parser, Abstract Syntax Tree(AST), 제어 흐름 그래프(CFG), 데이터 흐름 그래프(DFG).
  2. **DAST Engine**: Crawler/Spider, Fuzzer/Payload Generator, HTTP Response Analyzer.
  3. **IAST Agent**: `java.lang.instrument` API, Bytecode Transformer(ASM), Runtime Taint Tracker.
  4. **RASP Engine**: Method Hooking Manager, SQL Syntax Tree Context Analyzer, Threat Action Block Engine.

</details>

```text
애플리케이션 보안 기술
├─ SAST Engine
│  └─ AST·CFG·DFG·Taint Analyzer
├─ DAST Engine
│  └─ Crawler·Fuzzer·Response Analyzer
├─ IAST Agent
│  └─ Bytecode Transformer·Taint Tracker
└─ RASP Engine
   └─ Method Hook·Context Analyzer·Action Engine
```

선의 의미: 소스코드 SAST 분석을 거쳐 스테이징 DAST/IAST 계측 테스트를 통과하고, 프로덕션 RASP 자가 방어로 이어지는 파이프라인 구조

| 기술 구분 | 분석 대상 및 위치 | 핵심 탐지 메커니즘 | 대표 도구 |
|:---|:---|:---|:---|
| **SAST** | 소스코드, 바이트코드 (CI 단계) | AST 파싱, CFG/DFG 데이터 흐름 Taint 분석 | SonarQube, Checkmarx, Fortify |
| **DAST** | 실행 중인 웹/API (Staging 단계) | 크롤링, 퍼징 페이로드 주입, 응답 분석 | OWASP ZAP, Burp Suite Enterprise |
| **IAST** | WAS 런타임 내부 (QA 단계) | 바이트코드 계측(ASM), 런타임 Taint 트래킹 | Contrast Security, Seeker |
| **RASP** | 프로덕션 WAS 내부 (Operate 단계) | 시스템 콜/API 후킹, 런타임 쿼리 구문 파싱 | Imperva RASP, Contrast Protect |

#### 한줄 요약
- 네 엔진은 같은 취약점을 서로 다른 지점에서 보는데, SAST가 실행 없이 코드 구조로 추정하던 자리를 IAST와 RASP는 애플리케이션 내부로 들어가 실제 데이터 흐름으로 대신하고, DAST는 바깥에 남아 공격자와 같은 시야만 확보한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **IAST 및 RASP 바이트코드 계측(Instrumentation) 5단계 프로세스**:
  1. JVM 구동 시 `-javaagent` 인자를 통해 IAST/RASP 에이전트 로드
  2. 클래스 로더가 타겟 클래스(예: `java.sql.Statement`)를 로딩할 때 에이전트 인터셉트
  3. ASM 바이트코드 조작기를 통해 메서드 진입/진출 지점에 보안 훅 코드 위빙(Weaving)
  4. 런타임 사용자 요청 인입 시 변수 메모리 태깅 및 Taint 오염 추적
  5. 악성 쿼리 실행 직전 RASP가 쿼리 트리를 검사하여 위변조 확인 시 예외(Exception) 발생 및 차단

</details>

```text
1. [WAS 구동 및 Agent 위빙]
    ├─ JVM 기동 ➔ `-javaagent:rasp-agent.jar` 인자 실행
    └─ [ClassFileTransformer가 SQL/File I/O 클래스에 보안 계측 코드 동적 삽입]
            │
            ▼
2. [사용자 요청 인입 및 Taint Tagging]
    ├─ 공격자가 HTTP 요청 파라미터로 `' OR 1=1--` 페이로드 전송
    └─ [IAST/RASP 에이전트가 입력 파라미터 객체에 'Tainted' 메모리 태그 부여]
            │
            ▼
3. [애플리케이션 내부 로직 실행]
    ├─ 비즈니스 로직을 거치며 문자열 결합(`SELECT * FROM users WHERE id = '` + input)
    └─ [Taint Tracker가 문자열 결합 과정에서 오염 태그가 전파됨을 실시간 감시]
            │
            ▼
4. [Sink 함수 도달 및 RASP 컨텍스트 분석]
    ├─ `Statement.executeQuery()` 실행 직전 RASP 훅이 쿼리 가로채기
    └─ [SQL Lexer 파싱 ➔ 원본 쿼리 구조(WHERE 절)가 1=1 조건으로 변조됨을 100% 확정]
            │
            ▼
5. [실시간 방어 및 감사 로깅]
    ├─ [RASP Action Engine 작동] ➔ DB로 쿼리 전송 차단 및 SecurityException 강제 발생
    └─ [공격자 IP, HTTP 헤더, 소스코드 호출 스택(Call Stack)을 SIEM으로 실시간 전송]
```

**동작 원리**

1. **WAS 구동 및 Agent 위빙**: 런타임 클래스에 보안 훅 삽입
2. **사용자 요청 인입 및 Taint Tagging**: 입력 객체 오염 표시
3. **애플리케이션 내부 로직 실행**: 연산 경로의 오염 전파 추적
4. **Sink 함수 도달 및 RASP 컨텍스트 분석**: 쿼리 구조 판정
5. **실시간 방어 및 감사 로깅**: 악성 실행 차단과 증적 전송

#### 한줄 요약
- 계측은 실행 맥락을 얻는 대신 런타임 성능을 소모하므로, IAST는 시험 환경에 두고 운영 환경에는 차단이 필요한 RASP만 남기는 배치가 통상적이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **4대 애플리케이션 보안 검증 기술 심층 비교**:
  - SAST: 소스코드 기반 정적 분석 (개발자 친화적, 높은 오탐).
  - DAST: 외부 HTTP 응답 기반 동적 분석 (언어 독립적, 코드 위치 모름).
  - IAST: 바이트코드 계측 하이브리드 분석 (초정밀, QA 최적화).
  - RASP: 런타임 메모리 후킹 자가 방어 (운영 환경 능동 차단).

</details>

| 비교 항목 | SAST (정적 분석) | DAST (동적 분석) | IAST (상호작용 계측) | RASP (런타임 자가방어) |
|:---|:---|:---|:---|:---|
| **분석 대상** | **소스코드, 바이트코드** | **실행 중인 웹/API 응답** | **런타임 앱 내부 흐름 + 트래픽**| **프로덕션 런타임 실행 맥락** |
| **접근 방식** | **White-box (AST/DFG 분석)**| **Black-box (Payload Fuzzing)**| **Glass-box (Bytecode 계측)** | **In-App Self-Protection** |
| **적용 시점** | **개발(IDE), 빌드(CI 단계)** | **테스트(QA), 스테이징 단계** | **테스트 및 자동화 QA 단계** | **프로덕션 운영(Operate) 단계**|
| **코드 라인 특정**| **가능 (정확한 라인 출력)** | **불가능 (URL/파라미터 수준)** | **가능 (정확한 파일/라인 제공)**| **가능 (스택 트레이스 제공)** |
| **오탐률(FP)** | **높음 (실행 맥락 부재)** | 낮음 (실제 취약점 재현) | **매우 낮음 (실행 경로 확인)** | **매우 낮음 (컨텍스트 검증)** |
| **언어 종속성** | **종속적 (언어별 파서 필요)**| **독립적 (HTTP 기반 동작)** | **종속적 (JVM/CLR 에이전트)** | **종속적 (플랫폼 런타임 훅)** |

#### 한줄 요약
- SAST는 코드 조기 검사, DAST는 외부 블랙박스 테스트, IAST는 글래스박스 정밀 계측, RASP는 런타임 실시간 방어이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **OWASP ASVS (애플리케이션 보안 검증 표준) 및 CWE/SANS Top 25**: 소프트웨어 보안 취약점 분류 및 검증 표준 가이드라인.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| SAST의 수천 건 오탐(False Positive)으로 인해 **개발자가 보안 경고를 전면 무시하고 CI 빌드가 지속 중단되는 알람 피로(Alert Fatigue) 발생** | **IAST/DAST 결과와 상호 연관 분석(Correlation)하여 도달 가능성(Reachability)이 입증된 취약점만 우선순위화하고 공통 Sanitizer 룰셋 등록** | 오탐 노이즈 85% 이상 감축 및 개발 생산성 보장 |
| IAST 및 RASP의 바이트코드 계측과 Taint 트래킹으로 인해 **애플리케이션 CPU 사용량 폭증 및 초당 트랜잭션 처리 지연(Latency) 장애 발생** | **정규식 매칭 대신 AST 구문 트리 검증을 적용하고, 민감 Sink API에만 선별적 훅을 적용하여 오버헤드를 3% 이내로 최적화** | 서비스 성능 저하 없는 안전한 런타임 자가 방어 달성 |
| 서버리스(AWS Lambda) 및 MSA 환경에서 런타임 에이전트 설치가 불가능하여 **IAST 및 RASP를 적용할 수 없는 클라우드 네이티브 사각지대 발생** | **eBPF(Extended BPF) 기반의 커널 레벨 시스템 콜 후킹 솔루션(CWP)을 도입하고 서비스 메시(Service Mesh) 분산 트레이싱 연동** | 서버리스 및 컨테이너 환경 전 구간 런타임 가시성 확보 |

#### 한줄 요약
- 연관 분석으로 SAST 오탐을 줄이고, AST 쿼리 검증으로 RASP 성능을 최적화하며, eBPF로 클라우드 사각지대를 방어한다.

## Ⅶ. 결론

- 코드 결함은 **SAST**, 실행 검증·운영 차단은 **DAST·IAST·RASP** 선택

#### 한줄 요약
- SAST, DAST, IAST, RASP의 계층적 연계를 통해 개발부터 런타임까지 무결점 애플리케이션 보안을 완성한다.
