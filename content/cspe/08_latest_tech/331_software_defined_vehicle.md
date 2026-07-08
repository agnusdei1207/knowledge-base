---
title: "Software Defined Vehicle 소프트웨어 정의 차량 (Software Defined Vehicle)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 331
extra:
  question_no: "331"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- SDV는 차량 기능 가치와 사용자 경험이 하드웨어 교체보다 소프트웨어 업데이트로 진화하는 차량 아키텍처를 뜻함
- 핵심 변화는 분산 ECU 중심 구조에서 중앙집중 또는 zonal compute 구조로 이동하는 점임
- OTA와 차량 플랫폼 소프트웨어와 기능 안전과 사이버보안이 함께 맞물려야 실현 가능함

## Ⅰ. 개요

- **정의/개념**: Software Defined Vehicle은 차량의 기능과 성능과 서비스 경험을 소프트웨어 중심으로 설계하고 배포해 구매 이후에도 OTA와 플랫폼 업데이트를 통해 지속적으로 진화시키는 차량 시스템 아키텍처임
- **배경/필요성**: 자율주행과 커넥티드 서비스와 차량 내 디지털 경험 경쟁이 심화되면서 하드웨어 출시 주기보다 빠르게 기능을 개선할 수 있는 소프트웨어 중심 차량 구조가 필요해짐

## Ⅱ. 특징

- 차량 기능을 소프트웨어 서비스 단위로 추상화해 업데이트와 재사용이 쉬움
- 중앙집중형 또는 zonal compute 구조를 통해 ECU 복잡도를 줄이는 방향으로 진화함
- OTA와 클라우드 연계를 통해 차량 구매 후 기능 추가와 개선이 가능함
- 기능 안전과 보안과 인증 절차가 함께 강화되지 않으면 업데이트 민첩성이 곧바로 위험으로 바뀔 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Traditional ECU-centric Vehicle | Connected Vehicle | Software Defined Vehicle |
|:---|:---|:---|:---|
| 기능 진화 방식 | 부품 교체 중심 | 연결 서비스 추가 | 소프트웨어 업데이트 중심 |
| 컴퓨팅 구조 | 분산 ECU 다수 | 분산 ECU + 연결 모듈 | 중앙집중 또는 zonal compute |
| 운영 모델 | 출시 후 고정 | 제한적 원격 서비스 | 지속적 배포와 개선 |
| 대표 가치 | 안정적 기능 제공 | 외부 연결성 | 지속 가능한 기능 확장 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Central or Zonal Compute Platform | 다수 ECU 기능을 통합 실행해 소프트웨어 배포와 자원 활용을 단순화하는 차량 내 연산 기반임 |
| Vehicle OS and Middleware | 차량 자원과 통신과 서비스 생명주기를 표준화해 애플리케이션을 하드웨어 세부 구현에서 분리하는 플랫폼 계층임 |
| OTA and Cloud Backend | 업데이트 패키지 배포와 차량 상태 수집과 기능 활성화를 관리해 SDV의 지속 진화 모델을 가능하게 하는 외부 운영 계층임 |
| Application and Service Layer | 인포테인먼트와 주행 보조와 진단 기능을 소프트웨어 서비스 형태로 제공해 차량 가치를 사용자 경험으로 연결하는 계층임 |
| Safety and Cybersecurity Control | 안전 요구와 보안 정책과 인증 검증을 수행해 차량 업데이트가 신뢰 가능한 범위 안에서 이루어지게 하는 통제 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Apps /      | -> | Vehicle OS  | -> | Central /   | -> | Vehicle HW  |
| Services    |    | Middleware  |    | Zonal Compute|   | / Sensors   |
+-------------+    +-------------+    +-------------+    +-------------+
        ^
        |
+-------------+
| OTA / Cloud |
+-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 기능 요구 정의 | -> | 플랫폼 추상화  | -> | 소프트웨어 배포 | -> | 차량 텔레메트리 수집 | -> | OTA 개선 반영 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **기능 요구 정의**: 서비스와 주행 기능 요구를 소프트웨어 관점으로 정의함
2. **플랫폼 추상화**: 차량 자원과 통신을 공통 플랫폼으로 캡슐화함
3. **소프트웨어 배포**: 기능을 모듈 단위로 차량에 배포함
4. **차량 텔레메트리 수집**: 사용 이력과 오류와 성능 데이터를 수집함
5. **OTA 개선 반영**: 분석 결과를 업데이트 정책과 기능 개선에 반영함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 레거시 ECU 구조와 새 중앙집중 구조가 혼재하면 통합 복잡도가 높아져 개발 속도와 검증 비용이 동시에 증가할 수 있음
   - 해결방안: phased architecture transition과 domain consolidation roadmap을 적용하고 consolidated ECU function coverage와 cross domain integration defect rate로 검증함
2. 문제: OTA로 기능을 자주 바꾸는 운영 모델은 보안과 기능 안전 검증이 약하면 차량 리스크를 빠르게 확대할 수 있음
   - 해결방안: safety security gated release pipeline과 staged deployment policy를 적용하고 OTA rollback rate와 safety validated release coverage로 검증함
3. 문제: 차량 플랫폼이 폐쇄적으로 설계되면 공급망 종속성과 애플리케이션 확장 한계가 커질 수 있음
   - 해결방안: modular middleware standard와 vendor portability design을 적용하고 reusable software component ratio와 platform portability score로 검증함

## Ⅶ. 적용 사례

- 완성차 플랫폼 조직이 단계적 도메인 통합 로드맵을 운영하며 확인 지표는 consolidated ECU function coverage와 cross domain integration defect rate임
- OTA 운영팀이 단계적 배포 정책을 적용하며 확인 지표는 OTA rollback rate와 safety validated release coverage임
- 차량 소프트웨어 부문이 모듈형 플랫폼 설계를 추진하며 확인 지표는 reusable software component ratio와 platform portability score임

## Ⅷ. 결론

SDV는 자동차에 소프트웨어를 더하는 수준이 아니라 차량 구조 자체를 플랫폼화하는 변화이므로 중앙 컴퓨팅과 OTA와 안전 통제를 함께 설계해야 함.
