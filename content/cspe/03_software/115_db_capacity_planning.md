---
title: "데이터베이스 용량 산정 (DB Capacity Planning)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 115
---

# 📖 【암기용】 개념 완전 이해

> 목적: 데이터베이스 용량 산정을 처음 보는 사람도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 업무량과 데이터 증가를 수치화해 DB CPU·메모리·IOPS·스토리지·연결 수를 산정하는 활동
- **왜 필요한가**: DB는 사용자가 늘기 전부터 용량을 준비해야 한다. TPS/QPS, row size, index size, peak factor를 계산하지 않으면 피크 시간에 지연과 장애가 발생한다.
- **핵심 직관**: 식당 좌석·주방 화구·재료 창고를 예상 손님 수와 회전율로 미리 계산하는 일이다.

## 깊이 이해
- **배경·문제의식**: DB 장애는 CPU보다 IOPS, connection pool, buffer pool, lock wait에서 먼저 드러나는 경우가 많다. 용량 산정은 평균이 아니라 피크와 성장률을 기준으로 한다.
- **작동 원리**: 사용자 수와 업무 빈도에서 TPS/QPS를 산출하고, 데이터 모델에서 row size와 index size를 계산한다. 이후 peak factor, 보관기간, 복제본, 백업 여유율을 반영한다.
- **비유**: 출퇴근 시간 지하철은 하루 평균 승객이 아니라 8시 피크 승객을 기준으로 배차한다.
- **구체 예시**: DAU 100만, 사용자당 주문 조회 20회/일, 피크 10%가 1시간에 몰리면 QPS는 `100만*20*0.1/3600=556`이고, 캐시 miss와 복제 조회를 반영해 DB QPS를 산정한다.
- **흔한 오해·주의점**: 스토리지만 넉넉하면 된다는 판단은 틀리다. buffer pool miss, random IOPS, connection saturation, WAL 쓰기량이 병목이 될 수 있다.

## 연결 개념
- TPS/QPS — 쓰기·읽기 업무량 산정 기준
- IOPS — 랜덤 읽기·쓰기 처리 여력
- Buffer pool — 자주 쓰는 데이터·인덱스를 메모리에 유지하는 영역
- Peak factor — 평균 대비 피크 부하 배수

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 용량 산정은 장비 스펙 나열이 아니라 업무량, 데이터량, 피크, 성장률, 운영 여유율을 수식으로 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DB 용량 산정은 TPS/QPS, 데이터 증가량, IOPS, buffer pool, connection, peak factor를 계량화하는 계획 활동이다.
> 2. **가치**: 피크 부하와 성장률을 기준으로 CPU·메모리·스토리지·복제·백업 용량을 선제 확보한다.
> 3. **판단 포인트**: 평균 사용량이 아니라 p95 지연, 피크 시간 QPS, write amplification, 보관기간, 여유율 30%를 기준으로 판단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DB 규모 산정 방법론 확인 | TPS/QPS, row size, index size, storage growth | 스토리지 용량만 계산 |
| 성능 병목 예측 역량 확인 | IOPS, buffer pool hit ratio, connection pool | CPU 코어 수만 제시 |
| 운영 여유율 판단 확인 | peak factor, growth rate, backup, replica, HA | 평균 트래픽 기준 산정 |

> 요약: 이 문제는 업무량을 자원 수요로 변환하고 피크·성장·복제 여유를 반영하는 계산형 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: DB 용량 산정은 자원 수요 예측이다.
- 배경: 사용자 증가, 데이터 보관기간, 피크 트래픽을 반영하지 않으면 connection 부족, IOPS 포화, 저장공간 부족이 발생한다.
- 필요성: TPS/QPS, row size, index size, peak factor, 여유율 30%를 기준으로 CPU, 메모리, IOPS, 스토리지를 산정해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Business Forecast -> Workload Model
  / TPS/QPS -> CPU and connection
  / Row size and growth -> storage
  / Read/write pattern -> IOPS and buffer pool
Peak Factor -> HA/Backup Margin -> Capacity Plan
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 업무량 모델 | 사용자 수와 거래 빈도 산출 | DAU, MAU, 요청/사용자/일 |
| 데이터 모델 | 행 크기와 인덱스 크기 계산 | row overhead, index multiplier 포함 |
| IO 모델 | random/sequential IO 산정 | read/write ratio, WAL 반영 |
| 메모리 모델 | buffer pool·sort·connection 메모리 산정 | working set 크기 기준 |
| 성장 모델 | 피크·월 성장률·보관기간 반영 | 12~36개월 전망 필요 |

> 요약: DB 용량 산정은 업무량, 데이터량, IO, 메모리, 성장률 모델을 결합해 자원 요구량을 도출한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
업무 예측 수집 -> TPS/QPS 산정
  / read path -> cache hit 반영 -> DB QPS
  / write path -> WAL and index write 반영 -> IOPS
데이터 증가 계산 -> 피크 배수 적용 -> 여유율 반영 -> 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용자 수, 거래 빈도, 피크 시간대 수집 | DAU/MAU, peak hour ratio |
| 2 | TPS/QPS와 read/write 비율 계산 | p95 목표 지연과 비교 |
| 3 | row size, index size, 보관기간으로 저장공간 계산 | 월 증가량 GB |
| 4 | working set과 buffer pool 크기 산정 | buffer hit ratio 95% 이상 |
| 5 | PoC·부하테스트로 산정값 보정 | 예상 대비 오차 20% 이하 |

> 요약: 용량 산정은 예측값을 계산한 뒤 부하테스트와 운영 지표로 오차를 줄이는 반복 절차이다.

---

## Ⅳ. 특징

| 구분 | 경험 기반 증설 | 용량 산정 적용 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 기준 | 과거 장애·감 | TPS/QPS·IOPS·GB/month | 산식과 근거 보유 |
| 피크 | 평균 사용량 중심 | peak factor 2~5배 적용 | peak hour ratio |
| 저장공간 | 현재 용량 기준 | row+index+backup+replica | 12개월 여유 30% |
| 메모리 | 기본값 의존 | working set, buffer pool | hit ratio 95% 이상 |
| 검증 | 운영 후 확인 | 부하테스트와 APM 보정 | 오차 20% 이하 |

> 요약: 용량 산정은 평균이 아니라 피크와 성장률을 기준으로 자원 요구량을 수치화한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 산정 방식 | 장비 스펙 추정 | 업무량 기반 계산 | 신규 서비스·대규모 증설 |
| 성능 기준 | CPU 사용률 | p95 지연, IOPS, lock wait | SLA 100ms/300ms 등 |
| 저장 기준 | 원본 데이터 | 인덱스·복제·백업 포함 | 원본 대비 3~6배 가능 |
| 확장 방식 | 사후 증설 | 임계치 기반 scale plan | CPU/IO 70% 도달 전 |
| 검증 | 단일 쿼리 테스트 | 혼합 workload 부하테스트 | read/write 비율 반영 |

> 요약: 용량 산정은 장비 중심이 아니라 SLA와 업무량을 자원 모델로 바꾸는 접근이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 과소 산정 | 피크·인덱스·WAL 누락 | peak factor, write amplification 반영 | CPU/IO 70% 초과 시간 |
| Connection 고갈 | WAS pool 합산 누락 | pool 상한, proxy, backpressure | active connection 수 |
| Buffer miss | working set 과소 추정 | buffer pool 증설, 인덱스 조정 | buffer hit ratio |

> 요약: 산정 리스크는 누락 변수와 과도한 여유이며, 임계치와 비용 지표를 동시에 본다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| TPS/QPS | 피크 목표의 1.3배 처리 | 부하테스트, APM |
| IOPS | 디스크 한계의 70% 이하 | CloudWatch, iostat |
| Buffer hit | 95% 이상 | DB metric |
| Connection | max 대비 70% 이하 | pool metric |

> 요약: DB 용량은 TPS/QPS, IOPS, buffer hit, connection, storage 여유율을 기준으로 관리한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 업무량 산식화: `피크 QPS = DAU * 요청수 * 피크집중률 / 3600`으로 계산하고 캐시 hit ratio·read/write 비율을 반영함
2. 자원 모델링: row size, index multiplier 1.5~3배, replica 2개, backup 7~30일을 포함해 저장공간과 IOPS를 산정함
3. 검증·운영: JMeter/k6와 production trace replay로 p95 지연, lock wait, buffer hit를 검증하고 70% 임계치에서 증설 알람을 설정함

**결론 (2줄):**
- 기술사 판단: 신규 DB는 피크 부하 1.3배와 12개월 성장률을 기준으로 산정하고, 운영 DB는 실제 지표로 월 1회 보정해야 함
- 향후 방향: 클라우드 DB에서는 autoscaling이 가능하지만 connection, lock, index bloat는 자동 증설만으로 해결되지 않으므로 모델 기반 관리가 필요함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DB 용량 산정을 설명하시오", "기술하시오" | 업무량에서 자원 요구량으로 변환하는 흐름 | 경험 기반 증설 대비 차이 |
| 요구사항 명시형 | "산정 방안을 제시하시오", "설계하시오" | TPS/QPS·IOPS·스토리지 계산 절차 | 피크·성장률·여유율·검증 지표 |

> 요약: 설명형은 산정 요소를 넓게, 방안형은 산식과 검증 지표 중심으로 답안을 구성한다.
