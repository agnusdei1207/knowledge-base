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

- AUTOSAR는 차량 ECU 소프트웨어의 표준 계층 구조와 인터페이스를 정의하는 플랫폼임
- 핵심 계층은 SWC, RTE, BSW, MCAL임
- Classic과 Adaptive는 적용 대상과 운영 방식이 다름

## Ⅰ. 개요

- **정의/개념**: AUTOSAR는 차량 ECU 소프트웨어를 응용 기능과 런타임과 기본 소프트웨어와 하드웨어 추상화 계층으로 분리해 재사용성과 공급사 독립성과 통합 검증성을 높이는 자동차 소프트웨어 표준 플랫폼임
- **배경/필요성**: 차량 기능과 ECU 수가 급증하면서 공급사별 독자 구조로는 재사용과 통합 검증과 장기 유지보수가 어려워져, 공통 아키텍처가 필요해짐

## Ⅱ. 특징

- 하드웨어 의존성과 응용 기능을 분리해 이식성과 재사용성을 높임
- ARXML 기반 설정과 코드 생성 흐름이 개발 생산성을 좌우함
- Classic은 결정성과 제어 ECU에, Adaptive는 서비스 지향 고성능 ECU에 적합함
- 표준 구조를 도입해도 툴 체인과 통합 검증 비용은 여전히 큼

## Ⅲ. 종류 및 비교

| 판단 기준 | 전통 ECU 구조 | AUTOSAR Classic | AUTOSAR Adaptive |
|:---|:---|:---|:---|
| 구조 | 공급사별 독자 구현 | 정적 계층형 제어 중심 | 서비스 지향 동적 실행 |
| 적합 영역 | 소규모 ECU | 제동, 조향, 바디 제어 | ADAS, 인포테인먼트 |
| 재사용성 | 낮음 | 높음 | 높음 |
| 운영 특성 | 하드웨어 종속 큼 | 결정성 중시 | 업데이트와 연결성 중시 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| SWC | 제동과 조향 같은 차량 기능 로직을 표준 포트 단위로 캡슐화함 |
| RTE | SWC와 BSW 사이 호출과 통신을 중개해 하드웨어 의존성을 줄임 |
| BSW | 통신과 진단과 운영체제와 메모리 서비스를 제공하는 공통 계층임 |
| MCAL, ARXML | MCU 드라이버를 추상화하고 ECU 구성을 모델링해 코드 생성의 기반이 됨 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 기능 모델링    | --> | ECU 설정      | --> | 코드 생성/통합  | --> | HIL/SIL 검증   |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **기능 모델링**: 차량 기능을 SWC와 포트로 정의함
2. **ECU 설정**: ARXML로 BSW와 네트워크와 메모리를 구성함
3. **코드 생성 및 통합**: RTE와 설정 코드를 생성해 응용 기능과 결합함
4. **HIL, SIL 검증**: 통신과 타이밍과 안전 요구를 시험함

## Ⅵ. 문제점 및 해결 방안

1. 문제: ARXML와 툴 체인 의존성이 크면 설정 오류 하나가 광범위한 통합 실패로 이어질 수 있음
   - 해결방안: configuration validation 자동화를 적용하고 generation error rate와 integration defect count로 검증함
2. 문제: 표준 계층이 추가되면서 자원 제약이 큰 ECU에서는 메모리와 성능 오버헤드가 커질 수 있음
   - 해결방안: ECU 등급별 플랫폼 범위를 조정하고 memory footprint와 runtime overhead로 적합성을 검증함
3. 문제: 다수 공급사 협업 환경에서는 인터페이스 해석 차이와 버전 불일치가 프로젝트 지연을 유발할 수 있음
   - 해결방안: interface governance와 CI 기반 통합 검증을 운영하고 interoperability issue count와 release delay로 검증함

## Ⅶ. 적용 사례

- 파워트레인 ECU 개발에서는 AUTOSAR Classic을 적용하고, reuse rate와 timing determinism로 결과를 확인함
- ADAS 중앙 컴퓨팅에서는 Adaptive Platform을 적용하고, service scalability와 update flexibility로 결과를 확인함
- 다수 공급사 통합 프로젝트에서는 ARXML 중심 협업을 운영하고, integration defect count와 release predictability로 결과를 확인함

## Ⅷ. 결론

AUTOSAR의 본질은 차량 기능을 표준 계층으로 분리해 재사용과 통합성을 얻는 데 있으므로, 표준 준수보다 설정 품질과 협업 체계가 실제 성패를 좌우함.
