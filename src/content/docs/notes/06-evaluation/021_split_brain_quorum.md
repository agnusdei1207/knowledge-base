---
sidebar:
  order: 21
  label: "021. Split Brain•쿼럼 (Split Brain Quorum)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "분산 클러스터 정합성 및 이중 마스터 방어 : 스플릿 브레인과 쿼럼 (Split-Brain & Quorum Fencing)"
date: "2026-08-26T15:41:17+09:00"
tags:
  - "notes-evaluation"
weight: 21
extra:
  question_no: "021"
  source_status: "기출"
  source_history: "126회"
  priority: 30
  priority_note: "126회 기출, 분산 고가용성 클러스터의 핵심 결함인 스플릿 브레인(Split-Brain), 정족수 쿼럼(Quorum: 과반수 원칙 ⌊N/2⌋+1), 홀수 노드(Odd Node) 및 증인 노드(Witness/Arbiter), 세대 번호(Epoch/Term), STONITH 하드웨어 펜싱 및 SCSI-3 PR 스토리지 펜싱 메커니즘"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **스플릿 브레인(Split-Brain)**: 다중 노드 클러스터 환경에서 노드 간의 전용 하트비트(Heartbeat) 통신망이 단절(Network Partition)되었을 때, 각 격리된 진영(Partition)이 상대방 노드가 고장 났다고 오판하여 양쪽 모두 스스로를 '마스터(Active/Primary)'로 승격시켜 공유 스토리지나 데이터베이스에 동시 쓰기를 감행함으로써 데이터가 복구 불가능하게 파괴되는 치명적 클러스터 결함.
- **쿼럼(Quorum / 정족수)**: 스플릿 브레인을 방어하기 위해 클러스터 전체 노드 수($N$) 중 과반수($Q = \lfloor \frac{N}{2} \rfloor + 1$)의 투표 동의를 획득한 단 하나의 분할 그룹에게만 마스터 승격 및 쓰기 권한을 부여하고, 과반수를 얻지 못한 소수 진영은 스스로 쓰기를 중단(Self-fencing)하도록 강제하는 분산 합의(Consensus) 수리 원칙.

</details>

- 정의/개념: 분산 클러스터의 데이터 정합성과 단일 쓰기 원칙(Single-Writer Invariant)을 사수하기 위해 **하트비트 감시 $\rightarrow$ 네트워크 분할 발생 시 과반수 쿼럼($\lfloor \frac{N}{2} \rfloor + 1$) 투표 $\rightarrow$ 증인(Witness) 노드 캐스팅보트 $\rightarrow$ 단조 증가 세대 번호(Epoch/Term) 부여 $\rightarrow$ STONITH 및 SCSI-3 PR 펜싱(Fencing) 기반 패배 노드 물리적 격리** 를 집행하는 **분산 일관성 제어 체계**
- 배경/필요성: 네트워크 분할로 양쪽이 모두 마스터를 자처하면 **동시 쓰기**가 데이터를 복구 불가능하게 파괴해 이중화 투자가 오히려 손실을 키우므로, 과반수 투표와 펜싱을 승격 절차 앞에 두어 상대 노드의 생사 추정을 정족수라는 단일 결정 규칙으로 대체할 필요

#### 한줄 요약
- 스플릿 브레인은 네트워크 분할 시 이중 마스터가 발생하는 결함이며, 과반수 쿼럼과 STONITH 펜싱으로 방어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **쿼럼 및 펜싱 3대 핵심 수리 메커니즘**:
  - **과반수 쿼럼 원칙 ($Q = \lfloor \frac{N}{2} \rfloor + 1$)**: $N$개 노드가 둘로 쪼개졌을 때 과반수를 만족하는 그룹은 수학적으로 오직 1개만 존재함을 보증.
  - **세대 번호 (Epoch / Term)**: 리더 선출 시마다 단조 증가하는 번호를 부여하여 구 마스터의 지연된 쓰기 요청을 스토리지에서 거부.
  - **노드 펜싱 (Fencing / STONITH)**: 과반수를 상실한 구 마스터 노드의 전원(IPMI)이나 스토리지 채널(SCSI-3 PR)을 물리적으로 강제 차단.

</details>

- 동률을 방지하는 **홀수 노드 쿼럼**
- 2노드 동률을 해소하는 **Witness 중재**
- 구 마스터의 전원을 끊는 **STONITH 펜싱**

#### 한줄 요약
- 과반수 쿼럼($\lfloor N/2 \rfloor + 1$), 홀수/증인 노드 구성, 세대 번호(Epoch), STONITH 하드웨어 펜싱을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **스플릿 브레인 방어 4대 아키텍처 계층**:
  1. **Consensus & Quorum Layer**: Corosync, etcd, Zookeeper (Raft/Paxos 쿼럼 합의).
  2. **Monotonic Epoch Tracker**: 리더 세대 번호(Term), 분산 임대권(Lease).
  3. **Storage Fencing Layer**: SCSI-3 Persistent Reservation (PR), SAN 스위치 포트 차단.
  4. **Power Fencing Layer (STONITH)**: IPMI, iLO, BMC, 네트워크 PDU 전원 차단기.

</details>

```text
스플릿 브레인 방어 체계
├─ Consensus·Quorum Layer
├─ Monotonic Epoch Tracker
├─ Storage Fencing Layer
└─ Power Fencing Layer
```

선의 의미: 네트워크 단절 시 다수 진영(Node 2+3)이 과반수 쿼럼을 형성하여 Node 1을 STONITH로 전원 차단하고 단일 쓰기를 사수하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **Consensus·Quorum Layer** | 과반수 합의와 Witness 투표로 리더 선출 |
| **Monotonic Epoch Tracker** | 구 세대의 지연 쓰기 거부 |
| **Storage Fencing Layer** | SCSI-3 PR로 패배 노드의 디스크 차단 |
| **Power Fencing Layer** | STONITH로 고립 노드 전원 차단 |

#### 한줄 요약
- 쿼럼 계층은 다수 진영을 고르는 판정만 할 뿐 패배 노드를 멈추지는 못하므로, 세대 번호가 뒤늦은 쓰기를 논리적으로 거부하고 SCSI-3 PR과 STONITH가 스토리지·전원 수준에서 물리적으로 차단해 합의가 끝나기 전에 발생하는 이중 쓰기 손상을 대신 막는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **스플릿 브레인 방어 및 쿼럼 페일오버 5단계 프로세스**:
  1. 평시 Node 1(Primary), Node 2(Standby), Node 3(Witness) 간 3자 하트비트 교환
  2. 네트워크 스위치 장애로 Node 1이 고립되는 1:2 분할 발생
  3. Node 2와 3이 과반수(2/3) 쿼럼을 달성하고 신규 세대 번호(Term 2) 발급
  4. Node 2가 Node 1에 대해 IPMI STONITH 전원 강제 차단 신호 전송
  5. Node 1의 스토리지 쓰기가 차단된 것을 확인 후 Node 2가 New Primary로 승격

</details>

```text
1. [정상 3노드 쿼럼 클러스터 가동]
    ├─ Node 1(Master), Node 2(Standby), Node 3(Witness)가 500ms 하트비트 교환
    └─ [현재 세대 번호: Term 1, 활성 투표권 총 3표 (과반수 기준 = 2표)]
            │
            ▼
2. [네트워크 분할 (Network Partition) 발생]
    ├─ AZ-1과 AZ-2/3 간의 전용 광케이블 단선 발생
    ├─ Node 1 진영 (1표): "Node 2, 3이 죽었는가?" ➔ 쿼럼(1/3) 미달로 자체 쓰기 동결
    └─ [Node 2+3 진영 (2표): "Node 1과 연결 끊김" ➔ 과반수 쿼럼(2/3) 정상 형성]
            │
            ▼
3. [신규 리더 선출 및 세대 번호 증가]
    ├─ Node 2와 Node 3이 투표 수행 ➔ Node 2가 2표 획득하여 신규 리더로 당선
    └─ [클러스터 세대 번호를 Term 1 ➔ Term 2로 단조 증가 갱신]
            │
            ▼
4. [STONITH 하드웨어 펜싱 집행]
    ├─ Node 2가 Node 1의 잔여 I/O 시도를 원천 차단하기 위해 펜싱 가동
    ├─ 독립된 관리망(Out-of-band IPMI)을 통해 Node 1 서버로 전원 OFF 신호 전송
    ├─ Node 1 하드웨어 완전 셧다운 확인 (STONITH 성공)
    └─ [공유 SAN 스토리지에 SCSI-3 PR 키 등록 ➔ Term 1의 잔여 쓰기 원천 거부]
            │
            ▼
5. [New Primary 승격 및 무결점 서비스 개시]
    ├─ Node 2가 VIP를 인수하고 Read-Write 모드로 정상 서비스 재개
    └─ [결과: 이중 마스터 출현 0건, 데이터 정합성 100% 사수 및 RTO 5초 달성]
```

**동작 원리**

1. **정상 3노드 쿼럼 클러스터 가동**: 하트비트 교환
2. **네트워크 분할 발생**: 다수·소수 진영 판정
3. **신규 리더 선출 및 세대 번호 증가**: Term 갱신
4. **STONITH 하드웨어 펜싱 집행**: 구 리더 전원·쓰기 차단
5. **New Primary 승격 및 서비스 개시**: 단일 쓰기 재개

#### 한줄 요약
- 1표만 남은 진영이 스스로 쓰기를 동결하고 2표 진영만 승격하는 대가로 소수 쪽 가용성을 버리지만, 그 대신 이중 마스터가 만들어 낼 정합성 훼손과 사후 데이터 정정 비용을 치르지 않는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **클러스터 쿼럼 구성 2대 방식 비교**:
  - 홀수 노드 쿼럼 (3-Node / 5-Node): 노드 간 완전 대등 투표 (표준 Raft/Paxos).
  - 짝수 노드 + 증인 쿼럼 (2-Node + Witness): 2노드 Active-Standby에 경량 증인 추가.

</details>

| 비교 항목 | 홀수 노드 구성 (3-Node Quorum) | 짝수 노드 + 증인 (2-Node + Witness) | 2노드 무증인 구성 (2-Node No Witness) |
|:---|:---|:---|:---|
| **클러스터 노드 수**| **3대 (모두 데이터 저장 및 연산)** | **2대 (데이터) + 1대 (경량 Witness)**| **2대 (증인 없음, 비추천)** |
| **과반수 쿼럼 기준**| **2표 이상 (2/3)** | **2표 이상 (2/3)** | **2표 전원 일치 (2/2)** |
| **단일 노드 장애 시**| 1대 다운되어도 2대로 정상 가동 | 1대 다운되어도 Witness와 2대로 가동 | **1대 다운 시 쿼럼 상실로 전체 셧다운**|
| **스플릿 브레인 방어**| **완벽 방어 (과반수 자동 판정)** | **완벽 방어 (Witness가 캐스팅보트)**| **방어 불가 (50:50 동률로 양쪽 마스터)**|
| **인프라 구축 비용**| 중간 ($3\times$ 하드웨어) | **경제적 ($2\times$ + 초경량 VM 1대)** | 최저 ($2\times$ 하드웨어) |
| **적용 시스템** | **etcd, Kafka, ZooKeeper, Ceph** | **Oracle Data Guard, MySQL MHA** | 단순 개발 환경 |

#### 한줄 요약
- 3노드는 자체 과반수 해결, 2노드+Witness는 경제적 동률 해결, 2노드 무증인은 스플릿 브레인에 취약하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **스플릿 브레인 실무 방어 시 3대 위험 요소와 엔지니어링 대책**:

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 2개 노드로만 클러스터를 구성하여 네트워크 단선 시 **양쪽 서버가 모두 마스터로 승격하여 DB 데이터가 완전히 엇갈리고 영구 파괴** | **독립된 제3의 가용영역(AZ-3)에 경량 Witness 노드를 추가하여 3-Node 과반수 쿼럼 구조 강제** | 50:50 동률 해소 및 스플릿 브레인 100% 원천 차단 |
| 소프트웨어적 펜싱 명령만 믿고 마스터를 승격했으나 **구 마스터가 죽지 않고 백그라운드 디스크 쓰기를 계속하여 데이터베이스 블록 손상** | **IPMI/PDU를 통해 비정상 노드의 전원을 물리적으로 강제 차단하는 STONITH 하드웨어 펜싱 필수 구현** | 이전 마스터의 잔여 I/O 시도 물리적 100% 박멸 |
| 3개 노드를 동일한 데이터센터 랙(Rack)에 배치하여 **랙 PDU 전원 단락 시 3개 노드가 동시 셧다운되어 쿼럼 자체가 붕괴** | **3개 노드를 물리적으로 전원과 네트워크가 분리된 3개 가용영역(Multi-AZ)에 1대씩 분산 배치** | 단일 데이터센터 정전 시에도 2개 노드로 무중단 쿼럼 유지 |

#### 한줄 요약
- Witness 노드로 동률을 막고, STONITH로 잔여 I/O를 박멸하며, Multi-AZ 분산으로 쿼럼 붕괴를 방어한다.

## Ⅶ. 결론

- 네트워크 분할 시 **과반수 쿼럼**만 쓰기를 허용하고 소수 진영은 **펜싱**

#### 한줄 요약
- 쿼럼은 분할 시 소수 진영의 가용성을 포기해 정합성을 사는 규칙이므로, 노드를 짝수로 두거나 증인을 빠뜨리면 방어 장치가 오히려 전체 정지의 원인이 된다.
