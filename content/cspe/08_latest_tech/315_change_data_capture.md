---
title: "Change Data Capture 변경 데이터 캡처 (Change Data Capture)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 315
extra:
  question_no: "315"
  exam_status: "기출"
  exam_history: "136회"
---

## 미리 알고가기

- CDC는 원천 데이터 전체를 다시 읽지 않고 변경분만 포착해 전달하는 동기화 방식임
- log based CDC가 정확성과 부하 측면에서 대표 방식으로 쓰이지만 snapshot과 schema 관리가 함께 필요함
- downstream 정합성은 delete 처리와 idempotent sink 설계에 크게 좌우됨

## Ⅰ. 개요

- **정의/개념**: Change Data Capture는 데이터베이스의 insert와 update와 delete 변경을 transaction log나 변경 추적 메커니즘으로 감지해 다른 시스템에 증분 이벤트로 전달하는 데이터 동기화 방식임
- **배경/필요성**: 운영 DB와 분석 플랫폼과 검색 엔진과 캐시 사이 동기화 수요가 커졌지만 전체 재적재 방식은 지연과 부하와 삭제 누락 문제가 커져 변경분 기반 전파가 필요해짐

## Ⅱ. 특징

- 전체 스캔 없이 변경분만 전파해 원천 시스템 부하와 전송량을 줄임
- 이벤트 기반 아키텍처와 결합해 운영계와 분석계를 느슨하게 연결하기 좋음
- snapshot 이후 log stream을 이어붙여 초기 적재와 지속 동기화를 함께 처리함
- schema 변화와 tombstone 처리와 offset 복구가 약하면 정합성 문제가 빠르게 드러남

## Ⅲ. 종류 및 비교

| 판단 기준 | Full Reload | Query Polling | Log Based CDC |
|:---|:---|:---|:---|
| 원천 부하 | 높음 | 중간 | 낮음 |
| 지연 특성 | 높음 | polling 주기 의존 | 낮음 |
| 삭제 반영 | 약함 | 제한적 | 강함 |
| 대표 활용 | 주기 배치 동기화 | 단순 증분 조회 | 실시간 이벤트 전파 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Source Database Log | commit 순서와 변경 내용을 기록해 CDC의 사실상 원천 데이터가 되는 변경 이력 계층임 |
| Snapshot Loader | 초기 기준 데이터를 적재해 log 기반 증분 동기화가 시작될 수 있는 출발 상태를 만드는 초기화 계층임 |
| CDC Connector | log를 읽어 operation type과 before after 정보를 이벤트로 변환하고 offset을 관리하는 추출 계층임 |
| Event Broker | 변경 이벤트를 버퍼링하고 여러 소비자에게 분배해 원천 DB와 downstream 시스템을 느슨하게 분리하는 전달 계층임 |
| Sink Applier | upsert와 delete를 반영하고 중복 처리를 제어해 최종 대상 시스템 정합성을 유지하는 반영 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| Source DB   | -> | Snapshot /  | -> | CDC Conn    | -> | Broker      | -> | Sink Apply  |
| Log         |    | Log Capture |    |             |    |             |    |             |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 초기 snapshot | -> | log 위치 고정  | -> | 변경 이벤트 생성 | -> | broker 발행   | -> | sink 반영     |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **초기 snapshot**: 기준 시점 데이터를 먼저 적재함
2. **log 위치 고정**: snapshot 이후 이어질 변경 로그 시작점을 확보함
3. **변경 이벤트 생성**: connector가 operation type과 변경 내용을 이벤트로 변환함
4. **broker 발행**: 여러 소비자가 활용할 수 있도록 이벤트를 분배함
5. **sink 반영**: 대상 시스템이 upsert와 delete를 적용하고 offset을 기록함

## Ⅵ. 문제점 및 해결 방안

1. 문제: schema 변경이 이벤트 포맷과 sink 해석 규칙에 반영되지 않으면 동기화 파이프라인이 중단되거나 데이터 손상이 발생할 수 있음
   - 해결방안: schema registry integration과 compatibility policy를 적용하고 schema break incident count와 compatible change ratio로 검증함
2. 문제: delete 이벤트와 tombstone 처리가 누락되면 검색 색인과 캐시와 분석 테이블에 오래된 데이터가 계속 남을 수 있음
   - 해결방안: delete propagation test와 tombstone handling standard를 적용하고 stale deleted record count와 delete replication success rate로 검증함
3. 문제: log 기반 수집 권한과 offset 복구 절차가 미흡하면 장애 후 중복 반영이나 누락 반영 위험이 커질 수 있음
   - 해결방안: privileged access hardening과 offset recovery runbook을 적용하고 replay error count와 recovery point accuracy로 검증함

## Ⅶ. 적용 사례

- 데이터 통합 플랫폼이 스키마 레지스트리 연계를 운영하며 확인 지표는 schema break incident count와 compatible change ratio임
- 검색 색인 동기화 체계가 tombstone 표준을 적용하며 확인 지표는 stale deleted record count와 delete replication success rate임
- 운영 데이터 허브가 offset 복구 절차를 표준화하며 확인 지표는 replay error count와 recovery point accuracy임

## Ⅷ. 결론

CDC는 단순 증분 복제가 아니라 변경 이력과 삭제 처리와 복구 지점을 함께 관리하는 동기화 체계이므로 downstream 정합성 설계가 성패를 가름함.
