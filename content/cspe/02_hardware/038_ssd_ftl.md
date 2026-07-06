---
title: "SSD FTL 플래시 변환 계층 (Flash Translation Layer)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 38
---

## 미리 알고가기

- LBA: 호스트가 보는 논리 블록 주소이며 저장장치 내부 물리 위치와 분리됨
- NAND page: 읽기·쓰기의 기본 단위임
- erase block: NAND에서 지우기의 기본 단위이며 여러 page를 포함함
- write amplification: 호스트가 쓴 양보다 NAND 내부에서 더 많이 쓰이는 비율임

## Ⅰ. 개요

- **정의**: SSD FTL은 호스트의 논리 블록 주소를 NAND 플래시의 물리 page와 block 위치로 매핑하고, erase-before-write 제약을 숨기기 위해 garbage collection, wear leveling, bad block 관리, 오류 보정을 조정하는 SSD 내부 변환 계층임
- **배경/필요성**: NAND 플래시는 덮어쓰기가 불가능하고 지우기 단위가 쓰기 단위보다 크며 셀 수명이 제한됨. FTL은 이러한 물리 특성을 블록 장치처럼 보이게 만들어 기존 OS와 파일시스템이 SSD를 사용할 수 있게 함
- **비유**: 사용자는 사물함 번호만 기억하고, 관리자가 실제 물건 위치를 계속 옮기며 낡은 칸과 빈 칸을 관리하는 것과 같음

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SSD 내부 동작을 NAND 제약과 주소 변환 관점에서 설명하는 역량 확인 | LBA-PBA 매핑, erase-before-write, GC, wear leveling, write amplification | 단순 캐시로 설명, erase 단위 누락, 성능 변동 누락 |

> 요약: FTL은 NAND의 물리 제약을 숨기고 호스트에 논리 블록 장치 추상화를 제공하는 SSD 핵심 계층임.

## Ⅱ. 특징/비교

| 판단 기준 | 원시 NAND | FTL 적용 SSD |
|:---|:---|:---|
| 주소 모델 | page와 block 물리 위치 직접 관리 | LBA 기반 논리 주소 제공 |
| 쓰기 방식 | 덮어쓰기 불가, erase 필요 | out-of-place write로 새 위치에 기록 |
| 수명 관리 | 사용자가 wear를 직접 고려 | wear leveling과 bad block 관리 |
| 성능 특성 | 물리 제약이 그대로 노출 | GC와 매핑 정책에 따라 지연 변동 |

> 요약: FTL은 NAND를 범용 블록 장치로 보이게 하지만 내부 관리 정책이 SSD 성능을 좌우함.

- page-level mapping은 유연하지만 DRAM 매핑 테이블이 커지고, block-level mapping은 공간은 줄지만 쓰기 증폭이 커질 수 있음
- TRIM 명령은 OS가 더 이상 쓰지 않는 LBA를 알려 FTL의 GC 효율을 높이는 데 도움을 줌
- over-provisioning은 사용자가 보지 못하는 여유 NAND를 확보해 GC와 wear leveling 여지를 제공함

## Ⅲ. 구성요소

```text
+-----------+      +-----------+      +-----------+
| Host LBA  | ---> | FTL Map   | ---> | NAND PBA  |
+-----------+      +-----------+      +-----------+
                        |
                        v
                  +-----------+
                  | GC/WL/ECC |
                  +-----------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 매핑 테이블 | LBA와 실제 NAND 위치를 연결하는 핵심 메타데이터임 | 사물함 위치 장부 |
| 쓰기 버퍼 | 작은 쓰기를 모아 NAND page·block 특성에 맞게 기록함 | 임시 분류대 |
| garbage collection | 유효 page를 옮기고 무효 page가 많은 block을 지워 여유 공간을 만듦 | 창고 빈 칸 정리 |
| wear leveling | block별 지우기 횟수를 고르게 분산해 수명을 늘림 | 칸별 사용 횟수 균등화 |

> 요약: FTL은 매핑, 쓰기 조정, GC, wear leveling을 통해 NAND를 안정적인 블록 장치로 운영함.

## Ⅳ. 절차

```text
+-----------+      +-----------+      +-----------+      +-----------+
| LBA요청   | ---> | 매핑조회  | ---> | NAND처리  | ---> | 메타갱신  |
+-----------+      +-----------+      +-----------+      +-----------+
```

1. **LBA 요청 수신**: 호스트의 read/write 명령과 논리 블록 주소를 받음
2. **매핑 조회와 할당**: read는 기존 PBA를 찾고 write는 새 free page를 할당함
3. **NAND 처리 수행**: 데이터를 읽거나 새 위치에 쓰고 이전 page는 invalid로 표시함
4. **메타데이터 갱신**: 매핑 테이블, 유효 비트, wear 정보, 오류 보정 정보를 갱신함

> 요약: FTL은 논리 주소 요청을 물리 위치 처리로 바꾸고 결과에 맞춰 내부 메타데이터를 계속 갱신함.

## Ⅴ. 문제점

- **P1 write amplification 증가**: 작은 랜덤 쓰기와 GC가 겹치면 NAND 내부 쓰기량이 호스트 쓰기보다 커짐
- **P2 지연 급증**: free block이 부족하거나 GC가 foreground로 동작하면 I/O tail latency가 커짐
- **P3 메타데이터 손상 위험**: 매핑 테이블이 전원 장애나 firmware 오류로 손상되면 데이터 접근 자체가 어려워짐

> 요약: FTL의 핵심 리스크는 쓰기 증폭, GC 지연, 매핑 메타데이터 신뢰성임.

## Ⅵ. 개선방안

1. **단기**: write amplification, free block, GC time, unsafe shutdown 로그를 측정함
2. **중기**: over-provisioning, TRIM, background GC, workload-aware mapping을 적용함
3. **장기**: PLP, 메타데이터 저널링, firmware 검증, QoS 정책을 SSD 선정 기준에 포함함

- **P1 대응**: TRIM과 over-provisioning으로 유효 page 이동량을 줄임 (확인: write amplification factor)
- **P2 대응**: background GC와 QoS-aware 스케줄링으로 foreground GC를 줄임 (확인: p99 write latency)
- **P3 대응**: PLP와 매핑 메타데이터 체크포인트·저널링을 적용함 (확인: 전원 장애 복구 테스트)

> 요약: FTL 안정화는 여유 공간, GC 시점, 메타데이터 보호를 함께 관리해야 함.

## Ⅶ. 전망

- **발전 방향**: QLC, PLC처럼 셀당 비트 수가 늘수록 FTL의 오류 보정, 쓰기 증폭, 데이터 배치 정책이 더 중요해짐
- **기술사적 판단**: Zoned Namespace와 Open-Channel 계열 접근은 호스트가 일부 배치 책임을 나눠 FTL 부담을 줄이는 방향을 제시함
- **기술사 제언**: 기술사는 FTL을 단순 주소 변환 표로 보지 말고 NAND 제약을 운영 품질로 바꾸는 SSD 제어 계층으로 설명해야 함
