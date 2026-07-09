---
title: "AUTOSAR 소프트웨어 플랫폼 (AUTOSAR)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 79
extra:
  question_no: "079"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- AUTOSAR는 차량 ECU 소프트웨어의 계층 구조와 인터페이스를 표준화한 플랫폼임
- SWC, RTE, BSW, MCAL이 핵심 계층임
- Classic과 Adaptive는 대상 ECU와 운영 방식이 다름

## Ⅰ. 개요

- **정의/개념**: AUTOSAR는 차량 ECU 소프트웨어를 응용 기능, 런타임, 기본 소프트웨어, 하드웨어 추상화 계층으로 나눠 재사용성과 공급사 독립성, 통합 검증성을 확보하는 자동차 SW 표준 플랫폼임
- **배경/필요성**: 차량 기능과 ECU 수가 늘어나면서 공급사마다 다른 구조로는 재사용과 통합 검증과 장기 유지보수가 어려워져, 공통 아키텍처와 인터페이스 표준이 필요해짐

## Ⅱ. 특징

- 응용 기능과 하드웨어 의존성을 분리해 이식성과 재사용성을 확보함
- ARXML 기반 설정과 코드 생성 품질이 개발 생산성을 좌우함
- Classic은 결정성과 제어 ECU에, Adaptive는 서비스 지향 고성능 ECU에 적합함
- 표준을 도입해도 툴 체인 관리와 통합 시험 부담은 남음

## Ⅲ. 종류 및 비교

| 판단 기준 | 전통 ECU 독자 구조 | AUTOSAR Classic | AUTOSAR Adaptive |
|:---|:---|:---|:---|
| 구조 방식 | 공급사별로 드라이버와 응용이 강하게 결합되는 경우가 많음 | 정적 계층 구조로 제어 중심 ECU를 표준화함 | 서비스 지향 구조로 고성능 ECU를 유연하게 운영함 |
| 적합 업무 | 소규모 단일 기능 ECU에 맞음 | 제동과 조향과 바디 제어처럼 결정성이 중요한 업무에 맞음 | ADAS와 인포테인먼트와 중앙 컴퓨팅에 맞음 |
| 장점 | 초기 진입은 빠르지만 재사용이 제한됨 | 인터페이스 표준화와 공급사 협업에 유리함 | 업데이트와 연결성과 서비스 확장에 유리함 |
| 유의점 | 통합 규모가 늘수록 유지보수 비용이 증가함 | 설정 오류와 자원 오버헤드를 관리해야 함 | 자원 사용량과 서비스 복잡도를 엄격히 통제해야 함 |

> 요약: Classic은 정적 제어 ECU, Adaptive는 서비스 지향 고성능 ECU에 맞음.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| SWC | 제동과 조향 같은 차량 기능 로직을 표준 포트 단위로 캡슐화함 |
| RTE | SWC와 BSW 사이 호출과 통신을 중개해 하드웨어 의존성을 줄임 |
| BSW | 통신과 진단과 운영체제와 메모리 서비스를 제공하는 공통 계층임 |
| MCAL·ARXML | MCU 드라이버를 추상화하고 ECU 구성을 모델링해 코드 생성의 기반을 만듦 |

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 기능 모델링    | --> | ECU 설정      | --> | 코드 생성·통합  | --> | HIL·SIL 검증   |
+-------------+     +-------------+     +-------------+     +-------------+
```

> 요약: AUTOSAR는 SWC, RTE, BSW, MCAL·ARXML 계층으로 응용과 하드웨어 의존성을 분리함.

## Ⅴ. 원리 및 절차 흐름도

1. **기능 모델링**: 차량 기능을 SWC와 포트 단위로 정의함
2. **ECU 설정**: ARXML로 통신과 메모리와 BSW 구성을 정함
3. **코드 생성·통합**: RTE와 설정 코드를 생성해 응용 기능과 결합함
4. **HIL·SIL 검증**: 타이밍과 통신과 안전 요구를 시험함

> 요약: 기능을 SWC로 모델링하고 ARXML 설정, 코드 생성, HIL·SIL 검증으로 통합함.

## Ⅵ. 실무 적용 및 유의점

1. 파워트레인·바디 ECU는 ARXML·툴 설정 오류가 통합 실패로 번질 수 있으므로 설정 검증과 CI 통합 검증을 두고 integration defect count, code generation error rate, timing compliance로 확인함
2. ADAS·도메인 컨트롤러는 서비스 수가 늘수록 메모리와 시작 시간이 흔들릴 수 있으므로 service contract 관리와 profiling을 적용하고 boot time, memory usage, service recovery rate로 확인함

## Ⅶ. 결론

AUTOSAR의 본질은 차량 기능을 표준 계층으로 분리해 재사용과 통합성을 얻는 데 있으므로, 표준 준수보다 설정 품질과 협업 체계가 실제 성패를 좌우함.

## 작성 근거(검토용)

- AUTOSAR는 SWC, RTE, BSW, MCAL, ARXML, Classic·Adaptive 차이를 핵심 축으로 설명함
- 비교표는 전통 ECU 독자 구조, Classic, Adaptive의 구조 방식과 적용 업무를 대비함
- 실무 판단은 integration defect count, code generation error rate, timing compliance, service recovery rate로 검증 가능하게 작성함
