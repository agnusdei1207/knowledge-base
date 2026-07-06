---
title: "AMBA 버스 프로토콜 (AMBA Bus Protocol)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 93
---

## 미리 알고가기

- AMBA(Advanced Microcontroller Bus Architecture): Arm 기반 SoC(System on Chip) 내부 IP(Intellectual Property)를 연결하기 위한 온칩 버스 프로토콜 계열임
- AXI(Advanced eXtensible Interface): 고성능 메모리 매핑 트랜잭션을 지원하는 AMBA 프로토콜임
- AHB(Advanced High-performance Bus)/APB(Advanced Peripheral Bus): 각각 고성능 주변 버스와 저전력 저속 주변 버스에 쓰이는 AMBA 프로토콜임
- 인터커넥트: 여러 master와 slave IP 사이 주소 디코딩, 중재, 라우팅을 수행하는 연결 구조임

## Ⅰ. 개요

- **정의**: AMBA는 SoC 내부의 CPU(Central Processing Unit), DMA(Direct Memory Access), 메모리 컨트롤러, 주변장치 IP를 주소 매핑과 트랜잭션 규칙 기준으로 연결하는 온칩 버스 프로토콜 표준임. 재사용 가능한 IP 통합과 성능·전력 특성별 버스 선택을 위해 사용함.
- **배경/필요성**: SoC는 여러 공급자의 IP가 한 칩 안에서 함께 동작하므로 공통 인터페이스가 없으면 통합 검증과 재사용 비용이 커짐. AMBA는 고성능 데이터 경로와 저속 제어 경로를 분리해 설계 복잡도를 낮춤.
- **비유**: 한 건물 안에서 고속 엘리베이터, 화물 엘리베이터, 사무실 복도를 역할별로 나누어 사람과 물건을 이동시키는 구조임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SoC 내부 버스 구조와 선택 기준 | AXI, AHB, APB, master/slave, 주소 디코딩 | Arm CPU 전용 기술로 한정 |

> 요약: AMBA는 SoC 내부 IP 연결을 표준화해 성능 경로와 제어 경로를 분리하는 프로토콜 계열임.

## Ⅱ. 특징/비교

| 판단 기준 | AXI | AHB | APB |
|:---|:---|:---|:---|
| 주요 용도 | 고성능 메모리·DMA 트랜잭션 | 중간 성능 시스템 버스 | 저속 레지스터 제어 |
| 채널 구조 | 읽기/쓰기 주소·데이터·응답 채널 분리 | 단일 파이프라인 버스 중심 | 단순 setup/access 단계 |
| 성능 특성 | outstanding, burst, out-of-order 지원 | 구조가 단순하고 예측 가능 | 저전력·저면적에 유리 |
| 선택 기준 | 고대역폭 master 연결 | 범용 내부 연결 | UART(Universal Asynchronous Receiver/Transmitter), timer, GPIO(General-Purpose Input/Output) 등 주변 제어 |

> 요약: AMBA 선택은 모든 IP에 AXI를 쓰는 것이 아니라 성능 요구와 제어 단순성에 따라 AXI/AHB/APB를 나누는 것임.

- **적용 조건**: IP별 대역폭, 지연, 전력, 레지스터 접근 빈도가 먼저 분리되어야 함
- **선택 지표**: bus utilization, worst-case latency, protocol violation을 함께 확인해야 함
- **운영 관점**: 고성능 경로와 저속 제어 경로를 섞지 않는 것이 검증 비용을 낮춤

## Ⅲ. 구성요소

```text
+----------+      +---------------+      +-------------+
| CPU/DMA  | ---> | AXI interconn | ---> | Mem/Accel   |
+----------+      +---------------+      +-------------+
                         |
                         v
                  +-------------+      +-------------+
                  | Bridge      | ---> | APB devices |
                  +-------------+      +-------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Master IP | CPU, DMA, GPU(Graphics Processing Unit)처럼 버스 요청을 생성하는 주체임 | 이동을 요청하는 승객 |
| Interconnect | 주소 디코딩, 중재, 라우팅, 응답 반환을 처리함 | 건물 교통 관제 |
| Slave IP | 메모리, 레지스터, 주변장치처럼 요청을 처리하는 대상임 | 목적지 사무실 |
| Bridge | AXI-AHB-APB 간 프로토콜과 속도 차이를 변환함 | 환승 통로 |

> 요약: AMBA 시스템은 master, interconnect, slave, bridge로 SoC 내부 트랜잭션을 표준화함.

## Ⅳ. 절차

```text
+----------+      +----------+      +----------+      +----------+
| Request  | ---> | Decode   | ---> | Transfer | ---> | Response |
+----------+      +----------+      +----------+      +----------+
```

1. **요청 발행** — master가 주소, burst 길이, 읽기·쓰기 속성을 포함한 트랜잭션을 생성함
2. **주소 해석·중재** — interconnect가 대상 slave를 찾고 다중 요청 간 우선순위를 결정함
3. **데이터 전송** — 프로토콜별 handshake와 채널 규칙에 따라 데이터와 응답 정보를 이동함
4. **응답 반환** — slave 응답, 오류, 완료 상태를 master로 돌려주고 트랜잭션을 종료함

> 요약: AMBA 트랜잭션은 요청, 라우팅, 전송, 응답의 명확한 규칙으로 IP 간 호환성을 보장함.

## Ⅴ. 문제점

- **P1 인터커넥트 병목**: 여러 고성능 master가 같은 메모리나 인터커넥트 포트를 공유하면 지연과 starvation이 발생함
- **P2 CDC(Clock Domain Crossing)·타이밍 복잡도**: IP별 클럭 도메인과 버스 폭이 다르면 bridge와 FIFO(First-In First-Out) 검증 부담이 증가함
- **P3 QoS(Quality of Service) 설정 오류**: burst 길이, outstanding 수, priority 정책이 맞지 않으면 실시간 IP 성능이 흔들림

> 요약: AMBA 설계의 위험은 프로토콜 자체보다 공유 경로, 클럭 경계, QoS 정책에서 주로 발생함.

## Ⅵ. 개선방안

- **P1 대응**: 트래픽 모델 기반 interconnect sizing, 분리된 메모리 포트, arbitration 정책 검증을 수행함 (확인: bus utilization)
- **P2 대응**: clock domain crossing FIFO, formal protocol checker, timing constraint를 표준화함 (확인: CDC violation count)
- **P3 대응**: IP별 QoS class, burst 제한, latency budget을 문서화하고 시뮬레이션으로 검증함 (확인: worst-case latency)

> 요약: AMBA 품질은 버스 프로토콜 준수와 함께 트래픽·클럭·QoS 검증 체계로 확보함.

## Ⅶ. 전망

- **발전 방향**: AXI 기반 NoC(Network-on-Chip), chiplet 내부 연결, coherency extension과 결합해 복잡한 SoC 통합의 기본 인프라로 지속됨
- **기술사적 판단**: SoC 버스 설계는 IP 수보다 트래픽 특성, 실시간성, 전력, 검증 가능성을 기준으로 선택해야 함
- **기술사 제언**: 설계 초기부터 address map, QoS, CDC, protocol assertion을 산출물로 관리해 통합 후 재작업을 줄여야 함
