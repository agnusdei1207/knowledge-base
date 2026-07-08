---
title: "Sidecar Proxy 사이드카 프록시 (Sidecar Proxy)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 267
extra:
  question_no: "267"
  exam_status: "기출"
  exam_history: "136회, 138회"
---

## 미리 알고가기

- 사이드카 프록시는 애플리케이션 옆에 붙어 통신과 보안과 관측 기능을 대행하는 보조 프로세스 또는 컨테이너임
- Service Mesh의 데이터 플레인 기본 단위로 자주 등장함
- 코드 변경 없이 공통 기능을 붙일 수 있지만 자원 오버헤드가 따른다는 점이 핵심 trade-off임

## Ⅰ. 개요

- **정의/개념**: Sidecar Proxy는 애플리케이션과 같은 배포 단위 안에서 함께 실행되며 네트워크 프록시 역할을 수행해 트래픽 제어와 보안과 로깅과 추적 기능을 애플리케이션 대신 처리하는 보조 컴포넌트임
- **배경/필요성**: 마이크로서비스마다 공통 통신 기능을 코드로 중복 구현하면 개발과 운영 부담이 커져 애플리케이션 외부 프록시 계층으로 기능을 분리하는 방식이 도입됨

## Ⅱ. 특징

- 애플리케이션 코드 수정 없이 공통 네트워크 기능을 부여할 수 있음
- 로컬 프록시라 세밀한 트래픽 제어와 관측이 가능함
- 각 워크로드마다 프록시가 붙어 자원 오버헤드가 발생함
- 프록시 장애가 애플리케이션 통신 장애로 이어질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Sidecar Proxy | Embedded Library | Node Level Proxy |
|:---|:---|:---|:---|
| 코드 침투성 | 낮음 | 높음 | 낮음 |
| 세밀한 제어 | 높음 | 높음 | 중간 |
| 자원 오버헤드 | 높음 | 낮음 | 중간 |
| 배포 독립성 | 높음 | 낮음 | 중간 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Application Container | 비즈니스 로직을 수행하며 실제 트래픽은 사이드카를 통해 송수신하는 주 워크로드임 |
| Sidecar Proxy | 로컬 네트워크 경계에서 라우팅과 보안과 재시도와 관측 기능을 수행하는 프록시 컨테이너임 |
| Local Traffic Intercept | 애플리케이션의 송수신 흐름을 프록시로 우회시켜 정책을 적용하게 하는 연결 경로임 |
| Policy Source | 프록시가 적용할 라우팅과 인증과 제한 규칙을 제공하는 제어 정보 원천임 |
| Telemetry Sink | 프록시가 생성한 메트릭과 로그와 추적 정보를 수집하는 관측 수집 지점임 |

```text
+---------------- Pod ----------------+
| App Container <-> Sidecar Proxy    |
+------------------------------------+
                 |
                 v
            Network / Mesh
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 요청 생성    | -> | 로컬 프록시 통과 | -> | 정책 적용    | -> | 원격 서비스 호출 | -> | 로그와 추적 수집 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **요청 생성**: 애플리케이션이 서비스 호출을 시작함
2. **로컬 프록시 통과**: 요청이 사이드카를 거침
3. **정책 적용**: 프록시가 라우팅과 보안과 재시도 정책을 적용함
4. **원격 서비스 호출**: 대상 서비스로 요청을 전달함
5. **로그와 추적 수집**: 통신 메타데이터를 관측 시스템에 보냄

## Ⅵ. 문제점 및 해결 방안

1. 문제: 워크로드마다 프록시가 붙으면 CPU와 메모리 오버헤드가 누적되어 노드 밀도와 비용 효율이 떨어질 수 있음
   - 해결방안: sidecar sizing policy와 selective injection strategy를 적용하고 per pod proxy overhead와 node packing efficiency로 검증함
2. 문제: 프록시 설정 오류나 버전 불일치가 생기면 애플리케이션 코드가 멀쩡해도 통신 장애가 발생할 수 있음
   - 해결방안: config validation pipeline과 proxy version governance를 적용하고 proxy induced incident rate와 config rollout failure rate로 검증함
3. 문제: 프록시 체인이 복잡해질수록 요청 경로 추적과 문제 진단 시간이 길어질 수 있음
   - 해결방안: trace propagation standard와 proxy observability dashboard를 적용하고 trace completeness rate와 mean time to isolate fault로 검증함

## Ⅶ. 적용 사례

- 메시 기반 플랫폼이 선택적 주입 정책을 적용하며 확인 지표는 per pod proxy overhead와 node packing efficiency임
- 대규모 서비스가 프록시 검증 파이프라인을 운영하며 확인 지표는 proxy induced incident rate와 config rollout failure rate임
- 분산 추적 체계가 프록시 관측 대시보드를 제공하며 확인 지표는 trace completeness rate와 mean time to isolate fault임

## Ⅷ. 결론

사이드카 프록시는 공통 통신 기능 분리에 강력하지만 자원 오버헤드와 설정 복잡도를 통제할 운영 체계가 함께 필요함.
