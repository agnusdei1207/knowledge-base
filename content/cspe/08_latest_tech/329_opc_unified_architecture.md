---
title: "OPC UA 산업 표준 통신 (OPC Unified Architecture)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 329
extra:
  question_no: "329"
  exam_status: "기출"
  exam_history: "137회"
---

## 미리 알고가기

- OPC UA는 단순 통신 프로토콜이 아니라 정보 모델과 보안을 포함한 산업 상호운용 표준임
- client server와 pubsub 방식을 모두 지원해 설비 통합과 산업 데이터 배포에 활용됨
- 벤더 중립성과 의미 기반 주소공간이 핵심 차별점임

## Ⅰ. 개요

- **정의/개념**: OPC Unified Architecture는 산업 장비와 시스템이 표준화된 주소공간과 정보 모델과 보안 메커니즘을 통해 데이터를 의미 있게 교환하도록 설계된 벤더 중립 산업 통신 및 상호운용 표준임
- **배경/필요성**: PLC와 로봇과 SCADA와 MES가 제조사별 전용 프로토콜로 분리되면서 설비 데이터 통합과 보안 연결과 의미 해석을 동시에 해결할 표준이 요구됨

## Ⅱ. 특징

- 데이터 값뿐 아니라 구조와 의미를 정보 모델로 함께 전달함
- 플랫폼 독립성과 보안 통신과 인증 체계를 내장해 OT와 IT 연결에 적합함
- client server와 pubsub를 지원해 조회형과 이벤트형 통합을 모두 다룸
- 모델 설계와 인증서 운영이 복잡하면 도입 난도가 빠르게 올라갈 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | OPC UA | Modbus/TCP | MQTT |
|:---|:---|:---|:---|
| 의미 모델 | 강함 | 약함 | 약함 |
| 보안 내장 | 강함 | 제한적 | 추가 설계 필요 |
| 통신 방식 | client server, pubsub | 요청 응답 | pubsub |
| 대표 활용 | 산업 설비 통합 | 단순 장비 제어 | 경량 이벤트 전달 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Address Space | 노드와 속성과 관계로 장비 데이터를 표현해 단순 값 전달을 넘어 의미 있는 탐색과 통합을 가능하게 하는 정보 구조임 |
| Information Model | 장비와 공정 개체를 표준 객체로 모델링해 벤더가 달라도 같은 의미 체계로 데이터를 해석하게 하는 의미 계층임 |
| OPC UA Server and Client | 서버가 주소공간을 노출하고 클라이언트가 browse와 read와 write를 수행해 상호운용 통신을 담당하는 실행 계층임 |
| Security and Session Management | 인증서와 암호화와 세션 제어를 제공해 산업 통신의 신뢰성과 접근 통제를 보장하는 보안 계층임 |
| PubSub and Gateway Integration | 이벤트 배포와 레거시 프로토콜 연계를 지원해 현대적 데이터 배포와 기존 설비 통합을 이어주는 확장 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Device Data | -> | Address     | -> | OPC UA      | -> | Client /    |
|             |    | Space/Model |    | Server      |    | Gateway     |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 장비 모델링   | -> | 주소공간 노출  | -> | 보안 세션 수립 | -> | browse/read/pubsub | -> | 상위 시스템 연계 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **장비 모델링**: 장비 속성과 상태를 정보 모델로 정의함
2. **주소공간 노출**: 서버가 표준 노드 구조를 제공함
3. **보안 세션 수립**: 인증서와 암호화로 신뢰 연결을 생성함
4. **browse와 read와 pubsub**: 클라이언트가 데이터를 탐색하거나 구독함
5. **상위 시스템 연계**: MES와 historian과 analytics가 표준 방식으로 활용함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 주소공간과 정보 모델을 설비 특성에 맞게 설계하지 못하면 표준을 써도 실제 상호운용성과 재사용성이 낮아질 수 있음
   - 해결방안: domain specific information modeling guide와 reusable namespace standard를 적용하고 interoperable model reuse rate와 custom mapping reduction rate로 검증함
2. 문제: 인증서와 보안 설정 운영이 복잡하면 현장에서는 편의상 보안 기능을 약화시켜 OT 보안 위험이 커질 수 있음
   - 해결방안: certificate lifecycle automation과 secure default deployment policy를 적용하고 expired certificate incident count와 secure configuration compliance rate로 검증함
3. 문제: 레거시 프로토콜 게이트웨이 의존이 크면 지연과 의미 손실이 누적되어 실시간 통합 품질이 떨어질 수 있음
   - 해결방안: gateway performance baseline과 semantic preservation validation을 적용하고 gateway induced latency와 data semantic loss incident count로 검증함

## Ⅶ. 적용 사례

- 설비 통합 조직이 공통 namespace 표준을 운영하며 확인 지표는 interoperable model reuse rate와 custom mapping reduction rate임
- OT 보안팀이 인증서 자동화를 도입하며 확인 지표는 expired certificate incident count와 secure configuration compliance rate임
- 레거시 설비 연계 사업이 게이트웨이 검증을 수행하며 확인 지표는 gateway induced latency와 data semantic loss incident count임

## Ⅷ. 결론

OPC UA는 값 전송보다 의미와 보안과 상호운용을 함께 제공하는 표준이므로 정보 모델 설계와 인증서 운영 수준이 실제 품질을 결정함.
