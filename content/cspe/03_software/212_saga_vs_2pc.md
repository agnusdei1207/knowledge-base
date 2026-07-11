---
title: "마이크로서비스 사가 패턴 vs 2PC (Saga vs 2PC)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 212
extra:
  question_no: "212"
  exam_status: "기출"
  exam_history: "121회"
---

## 미리 알고가기

- Saga는 여러 서비스의 Local Transaction을 순서대로 실행하고 실패 시 완료 단계의 보상 Transaction을 역방향 수행함
- Choreography는 Event가 다음 단계를 촉발하고 Orchestration은 중앙 Orchestrator가 Command·Reply와 상태를 관리함
- 2PC는 Coordinator가 모든 Participant의 Prepare 성공을 확인한 뒤 Commit 또는 Rollback을 결정함
- 2PC Participant는 Prepared 상태에서 결정 Log를 기다리며 Lock·자원을 유지할 수 있음
- Saga의 보상은 DB Rollback이 아니라 업무 의미의 반대 동작이므로 외부 발송·시간 경과·동시 변경을 완전히 되돌리지 못할 수 있음

## 작성 근거(검토용)

- Saga와 2PC는 Transaction 경계, 조정 방식, 중간 상태, 실패 복구, 자원 점유, 결합, 적합 조건으로 비교함
- 절차는 정상 진행·실패 시 Saga 보상과 2PC Prepare·결정·In-Doubt 복구를 병렬로 설명함
- 주문 처리와 DB·메시지 원자 갱신은 보상 실패율·완료 시간·In-Doubt 건수·Prepare Lock 시간으로 검증함

## Ⅰ. 개요

- **정의/개념**: Saga는 Local Transaction과 보상 동작으로 서비스 간 업무 일관성을 수렴시키고, 2PC는 Participant의 Prepare·Commit 투표로 분산 Transaction의 원자적 결과를 확정함
- **배경/필요성**: 서비스별 DB 소유와 독립 장애를 유지할지, XA 등 하나의 Transaction Manager가 참여 자원의 Commit을 통제할지에 따라 분산 업무 변경의 복구 방식을 선택해야 함

## Ⅱ. 특징

- Saga 각 단계는 자체 DB에 Commit되므로 후속 실패 전까지 중간 상태가 다른 요청에 보일 수 있음
- 보상 Command도 중복 전달·부분 실패가 가능하므로 멱등 키·재시도·수동 복구 상태를 설계함
- Choreography는 중앙 제어점을 줄이지만 Event 연쇄가 길어지면 전체 상태와 원인 추적이 분산됨
- Orchestration은 단계·Timeout·보상을 한 상태 머신에서 관리하지만 Orchestrator 가용성과 상태 저장이 필요함
- 2PC는 Prepare에서 변경·Lock을 유지하고 Coordinator 결정 Log로 모든 Participant의 Commit·Rollback을 일치시킴
- Coordinator·Network 장애가 길어지면 Prepared Participant가 In-Doubt 상태로 남아 Lock 해제와 수동 복구 판단이 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | Saga | Two-Phase Commit |
|:---|:---|:---|
| Transaction 경계 | 서비스별 Local Transaction 연쇄 | 여러 Participant의 하나의 Global Transaction |
| 조정 방식 | Event Choreography 또는 Orchestrator | Transaction Coordinator의 Prepare·Commit 결정 |
| 중간 상태 | 단계별 Commit 상태가 외부에 노출 가능 | 최종 결정 전 Prepared 변경을 Commit하지 않음 |
| 실패 복구 | 완료 단계의 업무 보상·재시도·수동 처리 | Coordinator Log에 따라 Commit·Rollback 복구 |
| 자원 점유 | 단계 종료 시 Local Lock 해제 | Prepared 상태에서 Lock·Undo·연결 자원 유지 가능 |
| 참여자 결합 | 보상 가능한 API·Event 계약 | XA·2PC와 Transaction Manager 지원 필요 |
| 적합 조건 | 서비스별 DB·장기 업무·비동기 수렴 허용 | 같은 관리 영역의 짧은 원자 갱신·참여 자원 지원 |

> 요약: Saga는 단계별 Commit과 업무 보상으로 수렴하고 2PC는 모든 Participant의 Prepare 후 하나의 Commit·Rollback을 결정함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Saga Step·Local DB | 서비스별 업무 변경을 독립 Transaction으로 Commit함 |
| Event·Command·Reply | 다음 단계 실행과 성공·실패 결과를 전달함 |
| Orchestrator·Saga Log | 현재 단계·Timeout·재시도·보상 상태를 기록함 |
| Compensation Handler | 완료 동작의 업무 효과를 취소·상쇄하는 멱등 동작을 수행함 |
| 2PC Coordinator·Log | Global Transaction ID와 Prepare 투표·최종 결정을 영속 기록함 |
| 2PC Participant·Resource Manager | 변경을 Prepare하고 결정에 따라 Commit·Rollback함 |

```text
Saga: Step1 Commit -> Step2 Commit -> Fail -> Compensate2 -> Compensate1
2PC : Prepare All -> Vote All Yes -> Commit All | Any No -> Rollback All
```

> 요약: Saga Log는 진행·보상 상태를, 2PC Coordinator Log는 Prepare 투표와 전역 Commit 결정을 복구 기준으로 보존함.

## Ⅴ. 원리 및 절차 흐름도

| 처리 단계 | Saga | Two-Phase Commit |
|:---|:---|:---|
| 시작 | Orchestrator·Event가 첫 Local Transaction 실행 | Coordinator가 Global Transaction을 시작 |
| 정상 진행 | Commit 후 Event·Reply로 다음 단계 실행 | 각 Participant에 Prepare 요청 전송 |
| 성공 확정 | 마지막 단계 Commit 후 Saga 완료 상태 기록 | 모든 Yes 투표 후 Commit 결정·Log 기록 |
| 실패 처리 | 실패 단계 이전의 완료 동작을 역순 보상 | No 투표면 Rollback 결정·전파 |
| 장애 복구 | Saga Log에서 미완료 단계·보상을 재시도 | Participant가 Coordinator 결정 조회 후 In-Doubt 해소 |

> 요약: Saga 실패는 완료 단계의 보상으로, 2PC 실패는 Coordinator의 영속 결정에 따른 전역 Rollback·복구로 처리함.

## Ⅵ. 실무 사례

1. 주문·결제·재고 처리는 Saga Orchestrator와 멱등 보상을 적용하고 보상 실패율·완료 시간을 확인함
2. DB·메시지 원자 갱신은 XA 2PC를 적용하고 In-Doubt Transaction 수·Prepare Lock 시간을 확인함

## Ⅶ. 결론

- Saga와 2PC는 서비스별 독립성·중간 상태 허용·보상 가능성·참여 자원 지원·Lock 유지 시간을 기준으로 선택해야 함
