---
title: "Feature Store"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 253
---

## Ⅰ. 개요
- **정의**: ML 피처를 중앙 저장소에서 등록·공유·서빙하는 데이터 관리 플랫폼임
- **배경/필요성**: 팀별로 피처를 중복 생성하면 학습-서빙 불일치와 개발 비효율이 발생하므로 일원화가 필요함
- **비유**: 식재료 공용 냉장고처럼 한번 손질한 재료를 여러 요리사가 꺼내 쓰는 구조임

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 학습-서빙 피처 일관성 확보 방안 | Online/Offline Store 이원 구조 | 단순 DB로만 설명 시 감점 |

> 요약: 피처 재사용과 학습-서빙 일관성을 보장하는 중앙 관리 플랫폼임

## Ⅱ. 구성요소
```text
Data Source --> Transformation --> Offline Store (Batch)
                                       |
                                       v
                               Online Store (Low-latency)
                                       |
                                       v
                   Feature Registry <---+---> SDK/API
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Offline Store | 배치 학습용 대량 피처 저장(Parquet, DW 등) | 대형 냉동 창고 |
| Online Store | 실시간 서빙용 저지연 피처 저장(Redis, DynamoDB 등) | 주방 앞 미니 냉장고 |
| Feature Registry | 피처 메타데이터·스키마·소유자 정보 관리 | 식재료 라벨 카탈로그 |
| Transformation | 원천 데이터를 피처로 변환하는 로직 정의 | 식재료 손질 레시피 |
| SDK/API | 학습·서빙 코드에서 피처 조회 인터페이스 제공 | 주문 접수 창구 |

> 요약: Offline/Online 이원 저장소와 Registry·변환 로직·API로 구성됨

## Ⅲ. 절차
```text
Define Feature --> Materialize Offline --> Sync Online --> Serve via API
```
- 1단계: 피처 정의 — 변환 로직·스키마·메타데이터를 Registry에 등록
- 2단계: Offline 적재 — 배치 파이프라인으로 Offline Store에 피처 값 산출·저장
- 3단계: Online 동기화 — Offline Store에서 최신 피처를 Online Store로 동기화
- 4단계: API 서빙 — 학습 시 Offline, 추론 시 Online Store에서 동일 피처 제공

> 요약: 정의 → 배치 적재 → 온라인 동기화 → API 서빙의 4단계로 운영함

## Ⅳ. 문제점
- 동기화 지연: Offline→Online 동기화 주기에 따라 실시간성이 저하됨
- 피처 폭증: 관리 없이 등록이 늘어나면 중복·미사용 피처가 누적됨
- 인프라 비용: Online Store 저지연 요구로 인메모리 인프라 비용이 증가함

> 요약: 동기화·피처 관리·인프라 비용 세 축에서 운영 부담이 발생함

## Ⅴ. 개선방안
1. 단기: 스트리밍 파이프라인 도입으로 Offline→Online 동기화 지연 최소화
2. 중기: 피처 사용량 추적·만료 정책 적용으로 미사용 피처 자동 정리
3. 장기: 티어링 전략(Hot/Warm/Cold) 적용으로 인프라 비용 최적화

> 요약: 스트리밍·정리 정책·티어링으로 단계적으로 운영 효율을 개선함

## Ⅵ. 전망
- 발전 방향: 실시간 피처 계산과 벡터 임베딩 저장이 Feature Store에 통합되는 추세임
- 기술사적 판단: ML 시스템 성숙도 평가에서 피처 재사용률이 핵심 지표임
- 기술사 제언: 소규모 팀은 경량 오픈소스부터 시작해 점진적 확장이 필요함
