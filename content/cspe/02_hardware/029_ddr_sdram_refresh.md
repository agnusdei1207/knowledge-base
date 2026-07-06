---
title: "DDR SDRAM·갱신 방식 (DDR SDRAM Refresh)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 29
---

## 미리 알고가기

- SDRAM: 동기식 동적 램(Synchronous Dynamic Random Access Memory, SDRAM)은 외부 클록에 동기화해 명령과 데이터를 주고받는 동적 메모리임
- DDR: 더블 데이터 레이트(Double Data Rate, DDR)는 클록 상승·하강 에지에서 모두 데이터를 전송해 전송률을 높이는 방식임
- refresh: 동적 램(Dynamic Random Access Memory, DRAM) 셀의 전하 누설로 데이터가 사라지기 전에 주기적으로 다시 기록하는 동작임
- bank: DRAM 내부를 병렬 접근이 가능한 여러 메모리 영역으로 나눈 단위임

## Ⅰ. 개요

- **정의**: DDR SDRAM은 클록 양 에지에서 데이터를 전송하는 동기식 DRAM이며, 갱신 방식은 커패시터 전하가 누설되기 전에 행 단위 데이터를 주기적으로 재충전해 데이터 보존과 실효 대역폭을 균형화하는 제어 기법임
- **배경/필요성**: DRAM은 고집적·저비용이지만 저장 전하가 시간이 지나며 약해짐. 고속 시스템에서는 refresh로 인한 접근 중단과 데이터 보존 요구를 함께 관리해야 메모리 대역폭과 신뢰성을 유지할 수 있음
- **비유**: 물이 조금씩 새는 수조를 일정 주기로 보충하면서도 사용자가 물을 꺼내는 시간을 최대한 방해하지 않는 운영과 같음

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DRAM 고속 전송과 데이터 보존 제어를 함께 설명하는 역량 확인 | DDR, 상승/하강 에지, row/bank, refresh, 메모리 컨트롤러 | DDR을 클록 증가로만 설명, refresh 원인 누락, 실효 대역폭 영향 누락 |

> 요약: DDR SDRAM은 전송률을 높인 DRAM이고 refresh는 전하 누설을 보정하는 필수 유지 동작임.

## Ⅱ. 특징/비교

| 판단 기준 | SDR SDRAM | DDR SDRAM |
|:---|:---|:---|
| 데이터 전송 | 클록 한 주기당 한 번 전송 | 상승·하강 에지에서 두 번 전송 |
| 성능 초점 | 동기화와 burst 전송 | prefetch, bank 병렬성, 채널 대역폭 |
| 제어 부담 | 기본 refresh와 타이밍 관리 | 더 엄격한 타이밍, 전력, 신호 무결성 관리 |

> 요약: DDR은 같은 클록 체계에서 데이터 전송 기회를 늘리지만 컨트롤러의 타이밍 제어 부담도 커짐.

- refresh는 전체 행을 일정 주기로 갱신하는 auto refresh와 저전력 상태를 위한 self refresh로 구분할 수 있음
- bank 단위 병렬성과 precharge/activate 타이밍을 조절하면 refresh로 인한 대역폭 손실을 줄일 수 있음
- 온도 상승은 전하 누설을 키워 refresh 요구를 증가시키므로 서버 메모리 운영에서 냉각과 전력 관리가 연결됨

## Ⅲ. 구성요소

```text
+-----------+      +-----------+      +-----------+
| CPU       | ---> | Mem Ctrl  | ---> | DDR SDRAM |
+-----------+      +-----------+      +-----------+
                         |
                         v
                   +-----------+
                   | Refresh   |
                   | Scheduler |
                   +-----------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 메모리 컨트롤러 | read/write, activate, precharge, refresh 명령과 타이밍을 조정함 | 창고 입출고 관리자 |
| 클록·데이터 버스 | DDR 전송을 위해 클록 양 에지에 맞춰 데이터를 전달함 | 왕복 차선을 모두 쓰는 도로 |
| bank와 row | DRAM 내부 병렬성과 행 단위 접근을 구성하는 저장 영역임 | 여러 구역의 선반 |
| refresh 스케줄러 | 데이터 보존 시간 안에 행을 갱신하면서 일반 접근과 충돌을 줄임 | 정기 점검표 |

> 요약: DDR SDRAM은 컨트롤러가 전송 타이밍과 refresh 일정을 함께 제어해야 안정적으로 동작함.

## Ⅳ. 절차

```text
+-----------+      +-----------+      +------------+      +-----------+
| Request   | ---> | Row Open  | ---> | Burst Xfer | ---> | Refresh   |
+-----------+      +-----------+      +------------+      +-----------+
```

1. **요청 수신**: 중앙처리장치(Central Processing Unit, CPU)나 직접 메모리 접근(Direct Memory Access, DMA) 장치의 메모리 읽기·쓰기 요청을 컨트롤러가 큐에 적재함
2. **행과 bank 선택**: 주소를 채널, rank, bank, row, column으로 해석하고 필요한 행을 활성화함
3. **DDR 데이터 전송**: burst 단위로 클록 양 에지에 맞춰 데이터를 주고받음
4. **precharge와 refresh 조정**: 행 닫기와 refresh 명령을 스케줄링해 데이터 보존과 대역폭을 관리함

> 요약: DDR SDRAM 접근은 주소 해석, 행 활성화, burst 전송, refresh 조정이 결합된 타이밍 제어 과정임.

## Ⅴ. 문제점 및 개선방안

- **P1 refresh 대역폭 손실**: refresh 중인 bank나 rank는 일반 접근이 제한되어 지연과 처리량 저하가 발생함
- **P1 대응**: refresh를 bank 단위로 분산하고 메모리 요청 스케줄링을 최적화함 (확인: refresh stall cycles)
- **P2 타이밍 제약 복잡도**: activate, precharge, 열 주소 선택(Column Address Strobe, CAS), refresh 간 제약이 많아 컨트롤러 설계와 검증이 어려움
- **P2 대응**: 국제 반도체 표준화 기구(Joint Electron Device Engineering Council, JEDEC) 타이밍 파라미터 기반 검증과 컨트롤러 서비스 품질(Quality of Service, QoS) 정책을 적용함 (확인: 타이밍 위반 로그)
- **P3 온도와 전력 민감성**: 온도 상승과 고밀도 모듈은 refresh 빈도, 전력, 오류율에 영향을 줌
- **P3 대응**: 온도 기반 refresh와 냉각 정책, ECC 모니터링을 결합함 (확인: corrected error와 듀얼 인라인 메모리 모듈(Dual In-line Memory Module, DIMM) 온도)

> 요약: DDR SDRAM 운영은 전송률보다 실효 대역폭과 refresh 영향을 측정해 조정해야 함.

## Ⅵ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 서버 메모리 운영 | DIMM 온도와 corrected error를 수집해 refresh 정책, 냉각, ECC 경고 기준을 함께 운영함 | DIMM 온도, corrected error, patrol scrub 결과 |
| 메모리 컨트롤러 검증 | JEDEC timing, bank conflict, per-bank refresh 시나리오를 부하별로 검증함 | timing violation, refresh stall cycles |
| 고대역폭 워크로드 | channel·rank·bank 병렬성을 고려해 메모리 배치를 분산하고 row buffer hit를 높임 | effective bandwidth, row buffer hit, p99 latency |

> 요약: 실무 DDR SDRAM 적용은 refresh 손실, 타이밍 안전성, 온도·오류 지표를 함께 확인해야 함.

## Ⅶ. 전망

- **발전 방향**: DDR 세대가 올라갈수록 신호 무결성, 전력, 메모리 컨트롤러 복잡도가 커져 플랫폼 설계의 영향이 확대됨
- **기술사적 판단**: 인공지능(Artificial Intelligence, AI)·고성능 컴퓨팅(High Performance Computing, HPC) 영역은 DDR만으로 부족한 대역폭을 고대역폭 메모리(High Bandwidth Memory, HBM)와 컴퓨트 익스프레스 링크(Compute Express Link, CXL) 메모리 등 보완 계층으로 확장하는 흐름이 강해짐
- **기술사 제언**: 기술사는 DDR을 단순 세대 암기가 아니라 refresh, 타이밍, 채널 구성으로 실효 대역폭을 판단하는 문제로 설명해야 함
