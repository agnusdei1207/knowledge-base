---
title: "AMBA 버스 프로토콜 (AMBA Bus Protocol)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 93
extra:
  question_no: "093"
  exam_status: "미출제"
---

## 미리 알고가기

- AMBA는 Arm 계열 SoC 내부 IP를 연결하기 위한 온칩 버스 표준임
- AXI는 고성능 데이터 전송, AHB는 범용 시스템 버스, APB는 저속 제어 버스에 적합함
- Interconnect는 주소 해석과 중재와 라우팅을 담당함

## Ⅰ. 개요

- **정의/개념**: AMBA 버스 프로토콜은 CPU와 DMA와 메모리 컨트롤러와 주변장치 IP를 공통 트랜잭션 규칙으로 연결해 SoC 내부 통신을 표준화하는 온칩 버스 아키텍처임
- **배경/필요성**: SoC는 다양한 공급자의 IP를 한 칩 안에서 통합하므로, 고성능 데이터 경로와 저속 제어 경로를 분리한 표준 버스가 있어야 재사용성과 검증 효율을 확보할 수 있음

## Ⅱ. 특징

- 성능 등급에 따라 AXI와 AHB와 APB로 역할을 분리함
- 주소 채널과 데이터 채널과 응답 채널 규칙이 정해져 IP 재사용성이 높음
- 다수 master와 slave를 interconnect로 연결해 복잡한 SoC 내부 통신을 관리함
- QoS와 클럭 도메인과 브리지 설계가 실제 성능과 검증 난도를 좌우함

## Ⅲ. 종류 및 비교

| 판단 기준 | AXI | AHB | APB |
|:---|:---|:---|:---|
| 주요 용도 | 고대역폭 메모리와 가속기 연결 | 범용 시스템 버스 | 저속 레지스터 제어 |
| 구조 특성 | 채널 분리와 outstanding 지원 | 단순 파이프라인 중심 | setup과 access 위주의 단순 구조 |
| 성능 수준 | 가장 높음 | 중간 | 낮음 |
| 대표 대상 | DDR, NPU, DMA | 내부 컨트롤 블록 | UART, timer, GPIO |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Master IP | CPU와 DMA처럼 요청을 발생시키는 주체로 대역폭 요구와 우선순위 정책의 출발점이 됨 |
| Interconnect | 주소 디코딩과 중재와 라우팅을 수행해 다수 IP 간 충돌을 조정하고 병목 위치를 결정함 |
| Slave IP | 메모리와 주변장치처럼 요청을 실제 처리하며 응답 지연 특성이 전체 성능에 직접 반영됨 |
| Bridge | AXI와 AHB와 APB 사이 속도와 프로토콜 차이를 흡수해 고성능 경로와 저속 제어 경로를 연결함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 요청 발행      | --> | 주소 해석      | --> | 데이터 전송    | --> | 응답 반환      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **요청 발행**: master가 주소와 속성과 burst 정보를 포함한 트랜잭션을 생성함
2. **주소 해석**: interconnect가 대상 slave와 우선순위를 결정함
3. **데이터 전송**: 프로토콜 규칙과 핸드셰이크에 따라 주소와 데이터를 이동함
4. **응답 반환**: slave가 완료와 오류 상태를 master에 돌려주며 트랜잭션을 종료함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 고성능 master가 같은 메모리 경로에 몰리면 interconnect 병목으로 지연과 starvation이 발생할 수 있음
   - 해결방안: 트래픽 모델 기반 sizing과 arbitration 정책 검증을 수행하고 bus utilization과 starvation count로 검증함
2. 문제: 클럭 도메인이 다른 IP를 무리하게 연결하면 CDC 오류와 타이밍 불안정이 시스템 결함으로 이어질 수 있음
   - 해결방안: 표준 bridge와 async FIFO와 CDC 검증 절차를 적용하고 CDC violation count와 timing closure rate로 검증함
3. 문제: QoS와 burst 정책을 잘못 잡으면 실시간 영상이나 제어 IP의 서비스 품질이 흔들릴 수 있음
   - 해결방안: IP별 latency budget과 QoS class를 정의하고 worst-case latency와 frame drop rate로 검증함

## Ⅶ. 적용 사례

- 모바일 SoC 설계에서는 CPU와 NPU와 메모리 사이 AXI 경로를 분리하고, bus utilization과 worst-case latency로 결과를 확인함
- MCU 플랫폼에서는 APB에 저속 주변장치를 배치해 제어 경로를 단순화하고, gate count와 register access latency로 결과를 확인함
- RTL 검증 환경에서는 AMBA protocol checker와 CDC 검증을 회귀 테스트에 포함하고, protocol violation count와 CDC defect count로 결과를 확인함

## Ⅷ. 결론

AMBA는 SoC 내부 연결을 표준화하는 구조 자체가 핵심이므로, 프로토콜 선택은 버스 이름이 아니라 대역폭과 지연과 검증 복잡도를 기준으로 판단해야 함.
