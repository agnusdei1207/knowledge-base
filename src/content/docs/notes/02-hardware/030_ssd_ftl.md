---
sidebar:
  order: 30
  label: "030. SSD FTL 플래시 변환 계층 (Flash Translation Layer)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "SSD FTL 플래시 변환 계층 (Flash Translation Layer)"
date: "2026-08-13T11:51:11+09:00"
tags:
  - "notes-hardware"
weight: 30
extra:
  question_no: "030"
  source_status: "기출"
  source_history: "128회"
  priority: 50
  priority_note: "주소 매핑•GC•쓰기 증폭 판별"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **플래시 변환 계층 (Flash Translation Layer, FTL)**: SSD 컨트롤러 내부 펌웨어 형태로 탑재되어, 호스트의 파일 시스템 논리 주소(LPN/LBA)를 물리 NAND 플래시 주소(PPN/PBA)로 동적 매핑하고 가비지 컬렉션(GC) 및 마모도 평준화(Wear Leveling)를 총괄하는 핵심 펌웨어 엔지니어링 레이어.
- **비제자리 갱신 (Out-of-Place Update)**: NAND Flash 하드웨어 물리 특성상 '제자리 덮어쓰기(Overwrite)'가 불가능하여, 덮어쓸 데이터를 항상 물리적 클린 빈 페이지(Clean Page)에 새로 쓰고 기존 페이지를 무효화(Invalidate)하는 동작 방식.
- **NAND 플래시 (NAND Flash)**: 데이터 읽기/쓰기는 4KB~16KB 페이지(Page) 단위로 실행하고, 삭제는 2MB~8MB 블록(Block) 단위로만 실행 가능한 비휘발성 반도체.

</details>

- 정의/개념: 호스트의 논리적 덮어쓰기 요청을 물리 **비제자리 갱신(Out-of-Place Update)** 방식으로 수습하고, 논리 주소(LPN)와 물리 주소(PPA)를 동적 매핑 변환하는 SSD 핵심 펌웨어 아키텍처 **FTL(Flash Translation Layer)**.
- 배경/필요성: NAND Flash 반도체 고유의 "Erase-before-Write"(쓰기 전 블록 단위 삭제 필수) 및 페이지 읽기/쓰기 대 블록 삭제 단위 불일치 하드웨어 제약을 호스트 OS 파일 시스템에 노출시키지 않고 은닉하기 위해 필수 도입.

#### 한줄 요약
- NAND Flash의 비제자리 갱신, Erase-before-Write 및 수명 한계 제약을 은닉하여 호스트 OS에 일반 블록 장치 형태의 투명한 LPN-PPA 변환을 제공하는 FTL 펌웨어 계층.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **가비지 컬렉션 (Garbage Collection, GC)**: 무효화된(Invalid) 페이지가 적재된 희생 블록(Victim Block)에서 유효(Valid) 페이지만 딴 클린 블록으로 복사 인출한 뒤, 해당 희생 블록 전체를 Erase 복구시키는 재활용 과정.
- **마모도 평준화 (Wear Leveling)**: P/E Cycle(Program/Erase Cycle) 수명 한계를 지닌 NAND 블록들이 특정 블록만 집중 마모되는 것을 막기 위해 전 블록의 P/E Count를 균등화 스위칭하는 기법.
- **쓰기 증폭 (Write Amplification Factor, WAF)**: 호스트가 요청한 논리 쓰기 데이터량 대비, GC 유효 페이지 이동 및 메타데이터 갱신 등으로 실제 NAND Flash에 물리적 기록된 데이터량의 비율 ($WAF \ge 1.0$).

</details>

- **비제자리 갱신(Out-of-Place Update)** 방식을 적용하여 새 빈 페이지에 데이터 로드 후 기존 페이지를 무효 상태(Invalid)로 변경.
- **가비지 컬렉션(GC)**을 비동기 수행하여 무효 페이지가 차 있는 희생 블록을 물리 Erase 시키고 재사용 프레임으로 회수.
- GC 유효 페이지 이동 오버헤드로 인해 **쓰기 증폭(WAF)** 지표가 1.0 이상으로 상승하는 상충 관계 수반.

$$
Write\ Amplification\ Factor\ (WAF) = \frac{NAND\ Physical\ Write\ Amount\ (Bytes)}{Host\ Logical\ Write\ Amount\ (Bytes)}
$$

#### 한줄 요약
- Out-of-Place Update 기반 LPN-PPA 매핑, Garbage Collection 및 Wear Leveling을 통해 SSD의 수명 평준화 및 WAF 최소화를 도모함.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **LPN-PPA 매핑 테이블 (LPN-PPA Mapping Table)**: 호스트 논리 페이지 번호(Logical Page Number)를 실제 낸드 물리 페이지 주소(Physical Page Address)로 대조 변환해 주는 SRAM/DRAM 상의 룩업 표.
- **메타데이터 복구기 (Metadata Recovery Engine / Power-Loss Protection)**: 갑작스러운 불시 정전(SPO) 발생 시, 저널링 로그와 DRAM 매핑 체크포인트를 결합하여 LPN-PPA 테이블을 무결하게 100% 복구하는 하드웨어/소프트웨어 블록.
- **마모도 평준화기 (Wear Leveling Engine)**: 동적(Dynamic) 및 정적(Static) 마모도 알고리즘을 가동하여 P/E Cycle 이력을 실시간 대조하는 유닛.

</details>

```text
[ SSD Controller Internal FTL Architecture ]
┌───────────────────────────────────────────────────────────┐
│ Host Interface (NVMe / PCIe Protocol Handler)             │
├───────────────────────────────────────────────────────────┤
│ FTL (Flash Translation Layer Firmware)                    │
│  ├─ LPN-PPA Mapping Engine (Page / Block / Hybrid)        │
│  ├─ Garbage Collector (Victim Block Select & Copy Engine) │
│  ├─ Wear Leveling Engine (Dynamic / Static P/E Control)   │
│  └─ Power-Loss Protection (PLP & Mapping Journal Recover) │
├───────────────────────────────────────────────────────────┤
│ SRAM Buffer (Mapping Table & Journal) / On-Board DRAM     │
├───────────────────────────────────────────────────────────┤
│ NAND Flash Interface Controller (Multi-Channel / Multi-Die)│
└───────────────────────────────────────────────────────────┘
```

| 구성요소 | 책임 |
|:---|:---|
| LPN-PPA 매핑 엔진 | **논리•물리 페이지 매핑** 관리 |
| 가비지 컬렉터 | **Victim 선택•유효 페이지 이주•Erase** 수행 |
| Wear Leveler | 블록별 **P/E Cycle 분산** 관리 |
| Power-Loss Protection | 정전 시 **데이터•매핑 메타데이터** 보존 |

#### 한줄 요약
- LPN-PPA Mapping Engine, Garbage Collector, Wear Leveler 및 Power-Loss Protection(PLP) 복구 유닛으로 통합 구동됨.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **희생 블록 (Victim Block)**: 가비지 컬렉션(GC) 실행 시 무효(Invalid) 페이지 비율이 가장 높아 유효 데이터 이동 오버헤드가 적은 최적의 소거 대상 물리 블록.
- **매핑 저널 (Mapping Journal)**: LPN-PPA 변경 이력을 Flash NAND 전용 저널링 블록에 로그 형태로 영구 적재하는 복구 롤링 기법.

</details>

```text
[ Host OS Logical Page Write Request (LPN) ]
                     │
                     ▼
      [ 1. 신규 페이지 기록 ]
                     │
                     ▼
      [ 2. 매핑•저널 갱신 ]
                     │
                     ▼
      [ 3. 기존 페이지 무효화 ] ──> Host Write Completed
                     │
         [ Free Block Count < Threshold Check ]
                     ├─ False : Normal Operation Complete
                     └─ True (여유 블록 부족)
                         │
                         ▼
        [ 4. 가비지 컬렉션 ]
          - Select Victim Block (Highest Invalid Ratio)
          - Copy Valid Pages from Victim Block to New Clean Block
          - Execute Physical ERASE on Victim Block ──> Recycled Free Block
```

### 동작 원리

1. **신규 페이지 기록**: 빈 **PPA**를 할당하고 데이터를 Program함.
2. **매핑•저널 갱신**: 신규 PPA 매핑과 복구 로그를 저장함.
3. **기존 페이지 무효화**: 이전 PPA를 Invalid로 표시함.
4. **가비지 컬렉션**: 임계치 아래면 유효 페이지 이주 후 Victim을 Erase함.

#### 한줄 요약
- New Page Write -> LPN-PPA Table/Journal Update -> Old Page Invalidate -> (Free Block 부족 시) GC Valid Copy & Block Erase 순으로 실행됨.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **페이지 매핑 FTL (Page-Level Mapping FTL)**: LPN 4KB 단위마다 독립적인 PPA 4KB를 매핑하는 방식으로, 임의 쓰기 성능은 극상이나 매핑 테이블 크기(DRAM 용량)가 매우 커지는 방식.
- **블록 매핑 FTL (Block-Level Mapping FTL)**: LBN(논리 블록)과 PBN(물리 블록)만 매핑하는 방식으로 매핑 테이블은 극도로 작으나 임의 쓰기 시 병합(Merge) 오버헤드로 WAF가 폭증하는 방식.
- **하이브리드 매핑 FTL (Hybrid Mapping FTL)**: 기본은 블록 매핑을 사용하되, 쓰기는 임시 로그 블록(Log Block)에 페이지 매핑으로 처리한 후 덮어쓰는 혼합 기법.

</details>

| 매핑 FTL 방식 | 페이지 매핑 (Page-Level) | 블록 매핑 (Block-Level) | 하이브리드 매핑 (Hybrid) |
|:---|:---|:---|:---|
| **매핑 굵기 단위** | 4KB Page 단위 세밀 매핑 | 2MB~8MB Block 단위 굵은 매핑 | Block 단위 + Log Block Page 매핑 |
| **매핑 메모리 사용**| 페이지 수에 비례해 큼 | 블록 수에 비례해 작음 | 중간 수준 |
| **임의 쓰기 성능** | **최고 성능** (WAF 극소화) | 최악 성능 (잦은 Block Merge) | 보통 수준 (Log Block 포화 시 병목) |
| **쓰기 증폭 경향** | 임의 쓰기에서 비교적 낮음 | 병합 때 높아질 수 있음 | 로그 병합 정책에 따라 중간 |
| **대표 채택 솔루션**| **엔터프라이즈/소비자용 고성능 SSD 표준** | 과거 구형 SD카드, 저가형 플래시 | 초기 2.5인치 SSD |

#### 한줄 요약
- Page-level 매핑(고성능, 대용량 DRAM 요구, 표준 채택), Block-level 매핑(저용량 DRAM, WAF 취약), Hybrid 매핑(중간 형태)으로 나뉨.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **초과 예비 공간 (Over-Provisioning, OP)**: 전체 물리 낸드 용량 중 호스트 유저에게 노출하지 않고 FTL가 가비지 컬렉션(GC) 및 Wear Leveling 전용 공간으로 감추어 두는 여유 낸드 비율 (보통 7% ~ 28%).
- **TRIM 명령 (TRIM Command)**: 호스트 OS가 파일 삭제 시 해당 논리 블록이 더 이상 쓰이지 않음을 SSD FTL에 명시적으로 통지하여 FTL이 사전 무효화(Invalidate) 처리하도록 돕는 SATA/NVMe 명령.
- **정적 마모도 평준화 (Static Wear Leveling)**: 갱신이 거의 없는 읽기 전용 Cold Data를 억지로 다른 블록으로 옮기고, P/E Count가 적은 깨끗한 블록을 차출하여 Hot Write에 투입하는 정밀 수명 관리 기법.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 호스트 쓰기 지속 시 전경 GC로 **p99 지연** 상승 | 워크로드에 맞는 **Over-Provisioning•TRIM** 연동 | Free Block 여유 확보와 전경 GC 감소 |
| 소규모 무작위 쓰기(Random Write) 지속 시 **쓰기 증폭(WAF)** 지표 폭증 | FTL 내 **Write Buffer Aggregation** 및 Page-level 매핑 구동 | WAF 1.2 이하 안정화 및 SSD 낸드 물리 수명 연장 |
| 특정 Read Only 데이터가 적재된 블록의 마모율 불균형으로 조기 불량 | **Static Wear Leveling** 가동으로 Cold Data 블록 정기 이주 | 전체 낸드 블록의 P/E Count 수명 균등화 |
| 불시 정전(SPO) 시 DRAM 상의 LPN-PPA 매핑 테이블 유실 및 데이터 파손 | 칩 전용 **탄탈륨 커패시터(PLP)** 탑재 및 **매핑 저널** 회복 | 정전 후 부팅 시 LPN-PPA 매핑 100% 무결 복구 |

#### 한줄 요약
- Over-Provisioning(OP) 확충, OS TRIM 연동, Static Wear Leveling 및 PLP Tantalum Capacitor 회로 대책을 가동함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **FTL 최적화 기준 (FTL Optimization Criteria)**: 워크로드의 임의 쓰기 비율, Over-Provisioning(OP) 공간 비율, WAF 및 TRIM 연동 여부를 종합 분석하여 FTL 펌웨어 파라미터를 확정하는 프레임워크.

</details>

- 임의 쓰기가 많으면 **Page Mapping•OP**, 전력 위험이 크면 **PLP•Journal** 강화.

#### 한줄 요약
- WAF•p99•수명•정전 위험을 기준으로 매핑과 GC 정책을 결정함.
