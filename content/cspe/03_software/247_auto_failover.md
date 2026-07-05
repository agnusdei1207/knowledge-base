---
title: "Auto Failover (자동 장애 전환)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 247
---

## Ⅰ. 개요
- **정의**: 장애 감지 시 수동 개입 없이 대기 노드로 자동 전환하여 서비스 연속성을 유지하는 메커니즘임
- **배경/필요성**: 수동 전환은 인적 지연이 발생하여 RTO(244 참조)를 충족하기 어려우므로, 자동화된 전환 체계가 필요함
- **비유**: 정전 시 자동으로 비상 발전기가 가동되는 것과 같음

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Failover 유형과 동작 원리 | Active-Standby vs Active-Active | Failback 절차와 Split-Brain 문제를 함께 설명할 것 |

> 요약: 장애 발생 시 자동으로 대기 노드로 전환하여 다운타임을 최소화하는 메커니즘임

## Ⅱ. 구성요소
```text
  Health Check
      |
      v
  [Active] ---X--- 장애 발생
      |
      v
  Failover Controller
      |
      v
  [Standby] --> Active 승격
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Health Check | Heartbeat·Probe로 노드 생존 여부를 주기적으로 확인함 | 맥박 측정 |
| Failover Controller | 장애 판정 및 전환 로직을 실행하는 제어기임 | 비상 전환 스위치 |
| Standby Node | 대기 상태에서 Active 승격을 준비하는 예비 노드임 | 대기 선수 |
| Failback | 원래 노드 복구 후 역할을 원복하는 절차임 | 선발 투수 복귀 |

> 요약: Health Check, Controller, Standby, Failback으로 자동 전환 체계를 구성함

## Ⅲ. 절차
```text
장애 감지 --> 장애 판정 --> 노드 전환 --> Failback 수행
```
- 1단계: Health Check가 Heartbeat 실패·응답 지연 등 이상 징후를 감지
- 2단계: 임계값 초과 시 Controller가 장애를 확정 판정(오탐 방지를 위한 재확인 포함)
- 3단계: Standby 노드를 Active로 승격하고 VIP/DNS를 전환하여 트래픽 라우팅
- 4단계: 장애 노드 복구 완료 후 데이터 동기화 및 Failback 수행

> 요약: 감지 → 판정 → 전환 → 원복의 4단계로 자동 Failover를 수행함

## Ⅳ. 문제점
- Split-Brain: 네트워크 분할 시 양쪽이 동시에 Active로 동작하여 데이터 불일치 발생함
- 오탐(False Positive): 일시적 네트워크 지연을 장애로 오판하여 불필요한 전환이 발생함
- 데이터 유실: 비동기 복제 환경에서 전환 시 미복제 데이터가 손실될 수 있음

> 요약: Split-Brain, 오탐, 데이터 유실이 자동 Failover의 주요 위험 요소임

## Ⅴ. 개선방안
1. 단기: Quorum(과반수) 투표 기반 장애 판정으로 Split-Brain 방지
2. 중기: 다단계 Health Check(TCP + 애플리케이션 레벨)로 오탐률 감소
3. 장기: 동기식 복제 또는 Semi-Sync 복제 적용으로 전환 시 데이터 유실 최소화

> 요약: Quorum, 다단계 점검, 동기 복제를 통해 Failover 안정성을 강화함

## Ⅵ. 전망
- 발전 방향: Kubernetes Operator 등 선언적 자동 복구가 컨테이너 환경 표준으로 확산될 전망임
- 기술사적 판단: Failover 단독이 아닌 SPOF 제거(246 참조)·HA(245 참조)와 통합 설계하는 것이 바람직함
- 기술사 제언: 정기적 Failover Drill로 전환 시간을 측정하고 RTO 달성 여부를 지속 검증하는 것이 필요함
