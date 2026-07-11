---
title: "캐싱 전략 — Cache-Aside·Write-Through (Caching Strategy)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 215
extra:
  question_no: "215"
  exam_status: "미출제"
---

## 미리 알고가기

- Cache는 반복 조회 결과를 원본보다 가까운 계층에 저장해 원본 요청량과 조회 경로를 줄이는 복제 계층임
- Cache-Aside는 응용이 Cache Miss에서 원본을 읽어 채우고 원본 쓰기 후 Cache를 삭제·갱신함
- Read-Through·Write-Through는 Cache Provider가 원본 읽기·동기 쓰기를 중개함
- Write-Behind는 Cache 변경을 Queue에 모아 원본에 비동기 반영하므로 유실·순서·중복 복구 기준이 필요함
- TTL만으로 최신성을 보장하지 못하므로 Version Key·Event 무효화·허용 Staleness를 업무 계약에 포함해야 함

## 작성 근거(검토용)

- 캐싱 전략은 읽기·쓰기 주체, 원본 반영 시점, Miss 처리, 장애 영향, 일관성, 적합 조건으로 비교함
- 구조와 절차는 Key·TTL·무효화·Single-Flight·Eviction·원본 복구를 같은 데이터 수명주기로 설명함
- 상품 조회와 사용자 설정은 Cache 적중률·원본 QPS·Stale 응답률·p95 쓰기 지연으로 검증함

## Ⅰ. 개요

- **정의/개념**: 캐싱 전략은 Cache Hit·Miss·쓰기·무효화·만료 시 원본과 Cache 중 누가 데이터를 읽고 갱신할지 정하는 데이터 복제·접근 정책임
- **배경/필요성**: 조회 빈도·변경 주기·허용 Staleness·원본 장애·유실 허용 범위가 다르므로 Hit Rate만 높이지 않고 데이터 정확성과 복구 경로를 함께 설계해야 함

## Ⅱ. 특징

- Cache Key에 Tenant·업무 ID·Query 조건·Schema Version을 포함해 다른 데이터가 같은 Entry를 공유하지 않게 함
- TTL에 Jitter를 적용하고 Single-Flight·Lock으로 같은 Miss의 원본 동시 조회를 합침
- Negative Cache는 존재하지 않는 결과를 짧게 저장하되 생성 직후까지 이전 부재 결과가 남는 시간을 제한함
- 원본 쓰기와 Cache 무효화 사이 실패에 대비해 Outbox·CDC Event와 Version 비교로 누락 무효화를 복구함
- Eviction은 용량 한도와 접근 정책에 따라 Entry를 제거하므로 Hit Rate·Eviction Rate·원본 QPS를 함께 관측함
- Cache 장애 시 Bypass·Rate Limit·Circuit Breaker로 원본에 한꺼번에 요청이 몰리는 경로를 제한함

## Ⅲ. 종류 및 비교

| 판단 기준 | Cache-Aside | Read-Through | Write-Through | Write-Behind |
|:---|:---|:---|:---|:---|
| 읽기 주체 | 응용이 Cache 조회·Miss 원본 조회 | Cache Provider가 Miss에서 원본 조회 | Cache 또는 Read-Through 경로 사용 | Cache에서 최신 쓰기 상태 조회 |
| 쓰기 경로 | 원본 갱신 후 Cache 삭제·갱신 | 별도 쓰기 전략과 결합 | Cache와 원본을 동기 갱신 | Cache·Queue 후 원본 비동기 갱신 |
| 원본 반영 시점 | 응용 Transaction 시점 | 읽을 때 Cache 적재 | 쓰기 응답 전 원본 반영 | Queue 소비 시점 |
| 실패 영향 | 원본 성공·무효화 실패 시 Stale | Loader 실패가 Miss 요청에 전파 | 원본 실패 시 전체 쓰기 실패 | Queue·Cache 유실 시 미반영 가능 |
| 일관성 통제 | TTL·Event 무효화·Version | Provider TTL·Loader 정책 | 쓰기 순서·원자성·Cache 갱신 | 순서·중복·재시도·Durable Queue |
| 적합 조건 | 읽기 중심·응용별 원본 접근 제어 | 공통 Loader와 Cache 추상화 | 읽기 직후 갱신 값이 필요 | 쓰기 지연 허용·일괄 원본 반영 가능 |

> 요약: Cache-Aside는 응용, Read-Through는 Cache가 Miss를 처리하며 Write-Through는 동기, Write-Behind는 비동기로 원본을 갱신함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Cache Key·Namespace | 업무 식별자·Query·Tenant·Schema Version으로 Entry를 구분함 |
| Cache Store·Eviction | 값·TTL을 저장하고 용량·접근 정책에 따라 Entry를 제거함 |
| Loader·Writer | Miss 원본 조회와 동기·비동기 원본 쓰기를 수행함 |
| TTL·Jitter·Refresh | 만료 분산과 사전 갱신으로 동시 Miss 범위를 제어함 |
| Invalidation·Version | 원본 변경 Event와 Version으로 Stale Entry를 삭제·거부함 |
| Single-Flight·Fallback | 같은 Miss를 병합하고 Cache 장애 시 원본 보호 경로를 적용함 |

```text
Read -> Cache Hit -> Value
          └Miss -> Single-Flight -> Source -> Cache Fill
Write -> Source|Cache -> Invalidate·Update·Write-Behind Queue
```

> 요약: Key·TTL이 Entry 수명을 정하고 Loader·Writer·무효화가 원본과 Cache의 읽기·쓰기 순서를 연결함.

## Ⅴ. 원리 및 절차 흐름도

```text
Key 생성 -> Cache 조회 -> Hit 반환 | Miss 병합·원본 조회 -> 적재 -> 만료·무효화
```

1. **Key 생성**: 요청의 데이터 경계·Version·Tenant를 포함한 Cache Key를 만듦
2. **Cache 조회**: Entry 존재·TTL·Version을 확인하고 유효한 Hit를 반환함
3. **Miss 병합**: 같은 Key의 원본 조회를 Single-Flight로 합치고 대기 요청을 연결함
4. **원본 조회·적재**: 원본 결과와 Negative 결과에 서로 다른 TTL·Jitter를 적용함
5. **변경·종료**: 원본 Event·Write Policy로 Entry를 갱신·삭제하고 만료·Eviction을 관측함

> 요약: Cache 조회는 Key·TTL·Version을 검증하고 Miss는 병합한 원본 결과를 적재하며 변경 Event가 Entry를 종료함.

## Ⅵ. 실무 사례

1. 상품 조회 API는 Cache-Aside·TTL Jitter·Single-Flight를 적용하고 적중률·원본 QPS를 확인함
2. 사용자 설정은 Write-Through와 Version 검증을 적용하고 Stale 응답률·p95 쓰기 지연을 확인함

## Ⅶ. 결론

- 캐싱 전략은 읽기·쓰기 주체·허용 Staleness·무효화 실패·동시 Miss·Cache 장애 시 원본 보호를 함께 설계해야 함
