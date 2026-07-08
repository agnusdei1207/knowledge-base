---
title: "AUTOSAR Adaptive (AUTOSAR Adaptive)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 333
extra:
  question_no: "333"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- AUTOSAR Adaptive는 고성능 연산이 필요한 차량 도메인을 위한 서비스 지향 차량 소프트웨어 플랫폼임
- Classic AUTOSAR와 달리 POSIX 기반 실행 환경과 동적 업데이트와 고성능 애플리케이션 구성을 강조함
- 자율주행과 중앙집중형 차량 컴퓨팅과 SDV 확산과 함께 중요성이 커짐

## Ⅰ. 개요

- **정의/개념**: AUTOSAR Adaptive는 고성능 차량 컴퓨팅 환경에서 서비스 지향 통신과 동적 애플리케이션 실행과 업데이트를 지원하도록 설계된 차세대 차량 소프트웨어 플랫폼 표준임
- **배경/필요성**: 자율주행과 인포테인먼트와 차량 연결 서비스는 기존 정적 ECU 소프트웨어 구조만으로는 처리 유연성과 계산 성능을 감당하기 어려워 보다 유연한 실행 플랫폼이 필요해짐

## Ⅱ. 특징

- 서비스 지향 아키텍처를 기반으로 차량 기능을 느슨하게 결합함
- POSIX 기반 환경에서 고성능 애플리케이션 실행과 동적 배포에 유리함
- 중앙집중형 컴퓨팅과 SDV 구조에 적합한 플랫폼 표준을 제공함
- Classic AUTOSAR와 공존해야 하므로 이종 플랫폼 통합 복잡도가 높음

## Ⅲ. 종류 및 비교

| 판단 기준 | Classic AUTOSAR | AUTOSAR Adaptive | Proprietary Vehicle Platform |
|:---|:---|:---|:---|
| 실행 특성 | 정적, 실시간 ECU 중심 | 동적, 고성능 연산 중심 | 벤더 종속 |
| 통신 모델 | 신호 중심 | 서비스 지향 | 구현별 상이 |
| 대표 용도 | 제어 ECU | 자율주행, HPC, 인포테인먼트 | 특정 OEM 맞춤 |
| 확장성 | 제한적 | 높음 | 벤더 설계 의존 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| POSIX Based Execution Environment | 고성능 운영 환경 위에서 애플리케이션을 동적으로 실행해 복잡한 차량 기능을 수용하는 기반 계층임 |
| Service Oriented Communication | 서비스 발견과 요청 응답과 이벤트 전달을 표준화해 차량 기능 간 유연한 통합을 가능하게 하는 통신 계층임 |
| Execution and Lifecycle Management | 애플리케이션 시작과 종료와 상태 전이를 제어해 차량 플랫폼 운영 일관성을 유지하는 관리 계층임 |
| Update and Configuration Management | 소프트웨어 패키지와 설정 변경을 관리해 OTA와 차량 수명주기 운영을 지원하는 배포 계층임 |
| Safety and Security Integration | 보안 인증과 안전 요구를 플랫폼 수준에서 연결해 차량 기능 실행을 신뢰 가능한 범위 안에 두는 통제 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Apps /      | -> | Service     | -> | Execution   | -> | Compute HW  |
| Functions   |    | Communication|   | Management  |    | / OS        |
+-------------+    +-------------+    +-------------+    +-------------+
        ^
        |
+-------------+
| Update / Sec|
+-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 기능 서비스 정의 | -> | 실행 환경 배치 | -> | 서비스 발견/호출 | -> | 수명주기 관리 | -> | 업데이트 반영 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **기능 서비스 정의**: 차량 기능을 서비스 단위로 설계함
2. **실행 환경 배치**: Adaptive 플랫폼 위에 애플리케이션을 배치함
3. **서비스 발견과 호출**: 기능 간 통신을 서비스 방식으로 수행함
4. **수명주기 관리**: 상태와 실행 흐름을 플랫폼이 제어함
5. **업데이트 반영**: 변경 기능을 동적으로 배포하고 관리함

## Ⅵ. 문제점 및 해결 방안

1. 문제: Classic AUTOSAR 기반 ECU와 Adaptive 기반 플랫폼이 혼재하면 기능 경계와 통신 설계가 복잡해져 통합 검증 비용이 급증할 수 있음
   - 해결방안: classic adaptive partitioning guideline과 interface governance를 적용하고 cross platform interface defect rate와 integration rework effort로 검증함
2. 문제: 고성능 플랫폼의 자원 사용이 예측 가능하지 않으면 차량 기능 간 성능 간섭과 안정성 문제가 발생할 수 있음
   - 해결방안: resource isolation policy와 performance budget enforcement를 적용하고 cross application interference incident count와 real time budget compliance rate로 검증함
3. 문제: 서비스 지향 구조의 장점을 살리지 못하고 벤더별 확장만 늘어나면 표준 기반 재사용성이 떨어질 수 있음
   - 해결방안: standard first service model과 reusable middleware component strategy를 적용하고 standards compliant service ratio와 reusable platform asset coverage로 검증함

## Ⅶ. 적용 사례

- 차량 플랫폼 부문이 Classic Adaptive 분리 기준을 운영하며 확인 지표는 cross platform interface defect rate와 integration rework effort임
- 중앙 컴퓨팅 팀이 성능 예산 통제를 적용하며 확인 지표는 cross application interference incident count와 real time budget compliance rate임
- OEM 플랫폼 조직이 표준 우선 서비스 모델을 추진하며 확인 지표는 standards compliant service ratio와 reusable platform asset coverage임

## Ⅷ. 결론

AUTOSAR Adaptive는 고성능 차량 플랫폼의 공통 기반이지만 Classic 공존 전략과 자원 통제가 정리되어야 표준의 이점이 실질적으로 살아남음.
