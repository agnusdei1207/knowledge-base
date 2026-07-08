---
title: "OpenTelemetry (OpenTelemetry)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 276
extra:
  question_no: "276"
  exam_status: "기출"
  exam_history: "135회"
---

## 미리 알고가기

- OpenTelemetry는 메트릭과 로그와 추적 수집을 표준화하는 관측성 오픈 표준임
- 벤더 종속성을 낮추고 instrumentation 방식을 일관화하는 데 목적이 있음
- SDK와 Collector와 Semantic Convention의 역할을 구분하면 구조가 명확해짐

## Ⅰ. 개요

- **정의/개념**: OpenTelemetry는 애플리케이션과 인프라의 메트릭과 로그와 트레이스를 공통 API와 SDK와 Collector로 수집하고 전송하기 위한 개방형 관측성 표준이자 생태계임
- **배경/필요성**: 시스템마다 서로 다른 추적과 메트릭 에이전트를 쓰면 벤더 종속성과 계측 중복이 커져 공통 데이터 모델과 파이프라인이 필요해짐

## Ⅱ. 특징

- telemetry 신호를 하나의 표준 모델로 정렬함
- 다양한 백엔드와 연동 가능해 벤더 종속성을 낮춤
- auto instrumentation과 collector 파이프라인으로 도입 효율을 높임
- semantic convention 설계가 품질과 검색 효율을 좌우함

## Ⅲ. 종류 및 비교

| 판단 기준 | OpenTelemetry | Vendor Specific Agent | Custom Logging Only |
|:---|:---|:---|:---|
| 표준성 | 높음 | 낮음 | 낮음 |
| 이식성 | 높음 | 낮음 | 중간 |
| 신호 범위 | metrics, logs, traces | 제품별 상이 | logs 중심 |
| 도입 가치 | 통합 계측과 유연성 | 빠른 단일 제품 연계 | 최소 수준 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| API and SDK | 애플리케이션 코드에서 추적과 메트릭과 로그를 생성하게 하는 계측 라이브러리 계층임 |
| Instrumentation | 프레임워크와 미들웨어를 자동 또는 수동으로 계측해 신호를 생성하는 연결 계층임 |
| Collector | 수집과 필터링과 변환과 라우팅을 수행해 백엔드 의존성을 낮추는 중간 파이프라인임 |
| Semantic Convention | 서비스명과 HTTP 속성 같은 공통 필드 규칙을 정의해 일관된 해석을 가능하게 하는 표준 계층임 |
| Backend Exporter | 생성된 신호를 다양한 저장소와 분석 플랫폼으로 내보내는 출력 계층임 |

```text
+-------------+    +----------------+    +----------------+    +----------------+
| App / SDK   | -> | Instrumentation| -> | OTel Collector | -> | Backend        |
+-------------+    +----------------+    +----------------+    +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 계측 삽입    | -> | 신호 생성    | -> | Collector 수집 | -> | 변환과 라우팅 | -> | 백엔드 저장    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **계측 삽입**: SDK나 auto instrumentation을 애플리케이션에 연결함
2. **신호 생성**: trace와 metric과 log를 생성함
3. **Collector 수집**: Collector가 신호를 모음
4. **변환과 라우팅**: 필드 정규화와 샘플링과 목적지 분기를 수행함
5. **백엔드 저장**: 각 관측 백엔드에 데이터를 전달함

## Ⅵ. 문제점 및 해결 방안

1. 문제: semantic convention이 팀마다 다르면 같은 서비스라도 검색과 상관 분석 품질이 크게 떨어질 수 있음
   - 해결방안: telemetry schema governance와 naming convention review를 적용하고 semantic field consistency score와 query success rate로 검증함
2. 문제: 무분별한 auto instrumentation은 수집량과 성능 오버헤드를 동시에 키울 수 있음
   - 해결방안: selective instrumentation과 sampling policy를 적용하고 instrumentation overhead ratio와 telemetry volume growth rate로 검증함
3. 문제: Collector 파이프라인이 단일 장애점이 되면 관측 신호 자체가 유실되어 운영 가시성이 급격히 떨어질 수 있음
   - 해결방안: HA collector topology와 backpressure buffering을 적용하고 telemetry drop rate와 collector availability로 검증함

## Ⅶ. 적용 사례

- 멀티팀 플랫폼이 계측 스키마 거버넌스를 운영하며 확인 지표는 semantic field consistency score와 query success rate임
- 대규모 서비스가 선택적 자동 계측을 적용하며 확인 지표는 instrumentation overhead ratio와 telemetry volume growth rate임
- 관측 플랫폼이 고가용 Collector 구성을 운영하며 확인 지표는 telemetry drop rate와 collector availability임

## Ⅷ. 결론

OpenTelemetry는 관측성 표준화를 위한 핵심 기반이므로 계측 통일성과 Collector 안정성과 비용 제어가 함께 설계되어야 함.
