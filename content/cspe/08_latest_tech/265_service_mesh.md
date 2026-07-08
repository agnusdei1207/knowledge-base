---
title: "Service Mesh 서비스 메시 (Service Mesh)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 265
extra:
  question_no: "265"
  exam_status: "기출"
  exam_history: "123회, 136회, 138회"
---

## 미리 알고가기

- Service Mesh는 서비스 간 통신 기능을 애플리케이션 코드 밖의 인프라 계층으로 분리하는 구조임
- 트래픽 제어와 보안과 관측성을 일관되게 적용하는 것이 핵심 목적임
- API Gateway와 달리 동서 트래픽 제어에 강하다는 점을 구분해야 함

## Ⅰ. 개요

- **정의/개념**: Service Mesh는 마이크로서비스 간 통신에 필요한 라우팅과 보안과 재시도와 관측 기능을 프록시 계층과 제어 평면으로 분리해 일관되게 제공하는 네트워크 운영 아키텍처임
- **배경/필요성**: 서비스 수가 많아질수록 애플리케이션 코드 안에 통신 로직을 중복 구현하면 운영 정책 일관성과 장애 대응 속도가 크게 저하됨

## Ⅱ. 특징

- 서비스 간 통신 정책을 애플리케이션 코드와 분리함
- mTLS와 트래픽 분기와 재시도 정책을 중앙에서 제어함
- 관측성과 보안 표준화를 동시에 강화할 수 있음
- 프록시 오버헤드와 운영 복잡도가 추가될 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Service Mesh | API Gateway | Client Library |
|:---|:---|:---|:---|
| 주 대상 트래픽 | 동서 트래픽 | 남북 트래픽 | 애플리케이션 내부 호출 |
| 정책 적용 방식 | 프록시와 제어 평면 | 게이트웨이 집중 | 코드 삽입 |
| 장점 | 일관된 통신 제어 | 외부 API 관리 용이 | 가벼움 |
| 한계 | 운영 복잡도 | 내부 통신 제어 한계 | 중복 구현 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Data Plane Proxy | 각 서비스 옆에서 트래픽을 가로채 라우팅과 보안과 관측 기능을 수행하는 프록시 계층임 |
| Control Plane | 정책 배포와 인증서 관리와 구성 동기화를 담당해 메시 전체 동작을 제어하는 관리 계층임 |
| Traffic Policy | 라우팅과 재시도와 타임아웃과 카나리 분기 규칙을 정의하는 정책 집합임 |
| Identity and mTLS | 서비스 간 신원과 암호화를 제공해 제로트러스트 통신을 실현하는 보안 계층임 |
| Observability Stack | 메트릭과 로그와 트레이스를 수집해 서비스 간 호출 상태를 가시화하는 관측 계층임 |

```text
+----------+   proxy   +----------+   proxy   +----------+
| Service A|<--------->| Service B|<--------->| Service C|
+----------+           +----------+           +----------+
       ^                     ^                     ^
       |________________ Control Plane ____________|
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 정책 정의    | -> | 프록시 배포  | -> | 트래픽 가로채기 | -> | 정책 적용    | -> | 관측 및 보안  |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **정책 정의**: 트래픽 제어와 보안 정책을 선언함
2. **프록시 배포**: 각 서비스 옆에 프록시를 주입함
3. **트래픽 가로채기**: 서비스 간 호출이 프록시를 통과함
4. **정책 적용**: 라우팅과 mTLS와 재시도 규칙을 적용함
5. **관측 및 보안**: 메트릭과 추적과 인증을 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 모든 트래픽이 프록시를 통과하면 지연과 자원 사용량이 늘어 고성능 서비스에서 오버헤드가 커질 수 있음
   - 해결방안: selective mesh adoption과 proxy resource tuning을 적용하고 added network latency와 proxy CPU memory overhead로 검증함
2. 문제: 메시 정책과 인증서 체계가 복잡해지면 장애 시 원인 분석과 운영 변경이 더 어려워질 수 있음
   - 해결방안: policy standardization과 certificate lifecycle automation을 적용하고 configuration error rate와 certificate rotation success rate로 검증함
3. 문제: 메시를 도입해도 서비스 경계와 API 설계가 불안정하면 통신 문제를 구조적으로 해결하지 못할 수 있음
   - 해결방안: service boundary review와 API governance를 적용하고 retry storm rate와 inter service failure propagation score로 검증함

## Ⅶ. 적용 사례

- 마이크로서비스 플랫폼이 선택적 메시 도입을 운영하며 확인 지표는 added network latency와 proxy CPU memory overhead임
- 금융 서비스가 인증서 자동화를 적용하며 확인 지표는 configuration error rate와 certificate rotation success rate임
- 대규모 주문 시스템이 API 거버넌스를 병행하며 확인 지표는 retry storm rate와 inter service failure propagation score임

## Ⅷ. 결론

Service Mesh는 서비스 간 통신을 표준화하는 강력한 구조이지만 프록시 오버헤드와 정책 복잡도를 감당할 운영 성숙도가 함께 필요함.
