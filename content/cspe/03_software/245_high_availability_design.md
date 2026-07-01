---
title: "고가용성 설계 — Active-Active·Active-Standby (High Availability Design)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 245
---

# 📖 【암기용】 개념 완전 이해

> 목적: 고가용성 설계를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 장애 시 서비스 중단 시간을 줄이기 위해 이중화와 자동 전환을 설계하는 방식
- **왜 필요한가**: 단일 서버, 단일 DB, 단일 AZ에 의존하면 부품 하나의 장애가 서비스 전체 중단으로 이어진다. HA는 장애 전환 경로를 미리 만든다.
- **핵심 직관**: 예비 타이어를 싣는 Active-Standby와, 두 바퀴가 동시에 굴러가는 Active-Active의 차이를 이해하는 것이 핵심이다.

## 깊이 이해
- **배경·문제의식**: SLA 99.9%는 월 약 43분 중단 허용, 99.99%는 월 약 4.3분 중단 허용이다. 목표 가용성이 높을수록 수동 복구가 아니라 자동 감지·전환·검증 구조가 필요하다.
- **작동 원리**: Active-Standby는 주 노드 장애 시 대기 노드가 승격된다. Active-Active는 여러 노드가 동시에 트래픽을 처리하므로 로드밸런싱과 데이터 정합성 통제가 필요하다.
- **비유**: Active-Standby는 교대 운전자가 대기하는 방식이고, Active-Active는 두 계산대가 동시에 고객을 받는 방식이다. 후자는 처리량이 늘지만 정산 정합성을 맞춰야 한다.
- **구체 예시**: 웹 서버는 Active-Active로 3대 구성하고, 단일 writer DB는 Active-Standby로 구성해 failover 60초 이하를 목표로 한다.
- **흔한 오해·주의점**: 이중화만으로 HA가 완성되지 않는다. 헬스체크, 세션 처리, 데이터 복제 지연, split-brain 방지가 함께 필요하다.

## 연결 개념
- SPOF Elimination — 단일 장애점 제거
- Auto Failover — 장애 감지 후 자동 전환
- RTO/RPO — 가용성 설계 목표값

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: HA 답안은 Active-Active와 Active-Standby를 업무 특성, 데이터 정합성, RTO/RPO 기준으로 선택해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 고가용성 설계는 장애 발생 시 서비스 중단 시간을 SLA 범위 안으로 제한하는 이중화·감지·전환 구조이다.
> 2. **가치**: Active-Active는 트래픽 분산과 AZ 장애 대응, Active-Standby는 단일 writer 정합성과 운영 단순성을 제공한다.
> 3. **판단 포인트**: 목표 가용성, 세션 상태, DB 쓰기 구조, split-brain 방지, failover 시간 측정이 선택 기준이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 이중화 구조 판단 확인 | Active-Active vs Active-Standby 차이 | 용어만 쓰고 선택 조건 누락 |
| 장애 전환 설계 확인 | 헬스체크, LB, quorum, failover | 수동 전환을 HA로 단정 |
| 데이터 정합성 이해 확인 | 동기·비동기 복제, split-brain | 다중 writer 충돌 문제 누락 |

> 요약: HA 문제는 구성도보다 장애 감지와 전환 후 정합성 보장 기준을 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 고가용성 설계는 중단 시간을 SLA 이하로 제한하는 구조이다.
- 배경: 24x7 서비스는 서버·AZ·네트워크 장애를 전제로 이중화와 자동 전환을 설계해야 한다.
- 필요성: Active-Active와 Active-Standby를 업무 특성, SLA, 데이터 정합성 기준에 맞게 선택해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> Load Balancer -> Active Node A / Active Node B
       -> Health Check -> Failover Controller -> Data Replication
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Load Balancer | 트래픽 분산과 장애 노드 제외 | L4/L7, health check |
| Active-Active | 복수 노드가 동시 처리 | 세션 외부화, 충돌 제어 |
| Active-Standby | 주 노드 장애 시 대기 노드 승격 | failover 30~120초 목표 |
| Replication/Quorum | 데이터 복제와 split-brain 방지 | 동기·비동기·과반수 |

> 요약: HA 구조는 트래픽 분산, 상태 관리, 복제, 전환 제어가 함께 작동해야 한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
헬스체크 -> 장애 판정 -> 트래픽 차단
-> 대체 노드 승격/분산 -> 데이터 정합성 확인 -> 서비스 복구
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | LB와 controller가 노드 상태 확인 | 5초 간격, 3회 실패 |
| 2 | 장애 노드 트래픽 제거 | error spike 1분 이내 억제 |
| 3 | Standby 승격 또는 Active 노드 재분산 | failover 60초 이하 |
| 4 | 데이터 복제 지연과 세션 손실 확인 | replication lag 1초 이하 |

> 요약: HA는 장애 감지, 트래픽 차단, 대체 경로 활성화, 데이터 검증 순서로 동작한다.

---

## Ⅳ. 특징

| 구분 | Active-Active | Active-Standby | 수치 판단 |
|:---|:---|:---|:---|
| 처리 방식 | 여러 노드 동시 처리 | 주 노드 처리, 대기 노드 대기 | AA는 TPS 분산, AS는 failover 60초 |
| 정합성 | 세션·쓰기 충돌 관리 필요 | 단일 writer 구성 용이 | replication lag 1초 이하 |
| 비용 | 상시 자원 사용 | 대기 자원 비용 | SLA 99.99%면 AA 우선 검토 |

> 요약: Active-Active는 처리 분산에 적합하고 Active-Standby는 데이터 정합성 통제가 필요한 업무에 적합하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 웹 계층 | 단일 서버 | Active-Active 다중 AZ | 무상태 API, 세션 외부화 가능 |
| DB 계층 | 단일 DB | Active-Standby 또는 Multi-writer | 쓰기 충돌 허용 여부 |
| 장애 전환 | 수동 복구 | 자동 failover | RTO 5분 이하 요구 시 |

> 요약: 웹·API는 Active-Active, 단일 writer DB는 Active-Standby가 기본 선택이며 업무 요구에 따라 조합한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Split-brain | 네트워크 분리 후 양쪽 승격 | quorum, fencing, lease | 이중 writer 0건 |
| 세션 손실 | 서버 메모리 세션 | Redis/session token 외부화 | 로그인 재시도율 0.5% 이하 |
| 전환 실패 | 헬스체크 오류 | synthetic check, runbook | failover 성공률 95% 이상 |

> 요약: HA 리스크는 이중 writer와 상태 손실이므로 quorum과 상태 외부화가 필수 통제이다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 가용성 | SLA 99.9~99.99% | uptime monitor |
| 전환 시간 | failover 60초 이하 | chaos test timestamp |
| 정합성 | replication lag 1초 이하 | DB replica metric |

> 요약: HA 설계 검증은 가용성 비율, 전환 시간, 복제 지연을 함께 측정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 웹/API 계층은 다중 AZ Active-Active와 stateless token으로 구성하고 LB health check를 5초 간격으로 운영
2. DB 계층은 단일 writer Active-Standby, 자동 승격, replication lag 1초 이하 경보를 적용
3. 월 1회 chaos test로 노드·AZ 장애를 주입하고 failover 60초 이하 달성 여부를 기록

**결론 (2줄):**
- 기술사 판단: 무상태 서비스는 Active-Active, 강한 정합성 DB는 Active-Standby를 기본값으로 두고 SLA와 비용에 따라 조합한다
- 향후 방향: HA는 Kubernetes, service mesh, managed database failover와 결합해 애플리케이션 배포 파이프라인에서 검증된다

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "고가용성 설계를 설명하시오" | 장애 감지와 전환 흐름 | Active-Active와 Active-Standby 차이 |
| 요구사항 명시형 | "비교하시오", "설계하시오" | 계층별 구성과 failover 절차 | SLA·정합성·비용 선택 기준 |

> 요약: 비교형은 AA/AS 차이를, 설계형은 계층별 조합과 검증 지표를 중심으로 작성한다.
