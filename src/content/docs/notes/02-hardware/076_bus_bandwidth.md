---
sidebar:
  order: 76
  label: "076. 버스 대역폭과 전송률 계산"
  badge:
    text: "미출 • 50%"
    variant: note
title: "버스 대역폭과 전송률 계산 (Bus Bandwidth)"
date: "2026-08-13T12:00:06+09:00"
tags:
  - "notes-hardware"
weight: 76
extra:
  question_no: "076"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "단위•방향별 상한과 실측 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **버스 대역폭(Bus Bandwidth)**: 단위 시간(초) 당 버스 선로를 통하여 전송할 수 있는 이론적/실효적 데이터 전송 수치 ($B_{\text{max}}$).
- **전송률(Transfer Rate)**: 버스 상에서 데이터 신호(Bit/Symbol)가 초당 처리되는 횟수 (MT/s, GT/s).
- **실측 처리량(Measured Throughput)**: 프로토콜 오버헤드, 레인 인코딩 및 버스 중재 경합을 제외하고 수신측에 전달된 유효 페이로드 전송률.

</details>

- 정의/개념: 버스 폭(Bus Width) 및 동작 주파수(**전송률**)에 근거하여 **버스 대역폭** 이론치를 산출하고, 오버헤드를 반영해 **실측 처리량**을 정밀 계산하는 수치 평가 기법
- 배경/필요성: 규격 속도만으로는 **인코딩·헤더·경합 후 처리량 예측 불가**

#### 한줄 요약

- 버스 대역폭에 프로토콜 인코딩 오버헤드와 버스 경합 영향을 종합 반영하여 수신자 관점의 실측 처리량을 산출한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **MT/s & GT/s**: 초당 100만 회(Mega Transfers/sec) 및 10억 회(Giga Transfers/sec) 데이터 래칭을 의미하는 단위.
- **인코딩 효율(Encoding Efficiency, $\eta_{\text{enc}}$)**: 물리 직렬 링크에서 실제 데이터를 전달하기 위한 라인 코딩(8b/10b, 128b/130b 등) 비율.
- **프로토콜 효율(Protocol Efficiency, $\eta_{\text{proto}}$)**: 전송 프레임 총 크기 중 헤더/CRC를 제외한 유효 페이로드 비율.

</details>

![프로토콜 효율과 링크 사용률에 따른 전달 대역폭 차트](/study/diagrams/bus-bandwidth-efficiency.svg)

- 버스 클록 에지(DDR/QDR) 인가 횟수에 따른 **전송률** 수치화
- 물리 계층 8b/10b, 128b/130b 비트 매핑에 따른 **인코딩 효율** 반영
- 헤더/패킷 트랜잭션 오버헤드를 포함한 **프로토콜 효율** 차감 계산

$$
B_{\mathrm{serial}} = \frac{b \times n \times \eta_{\mathrm{enc}}}{8} \quad [\text{Byte/s}]
$$

#### 한줄 요약

- 버스 폭과 전송률 및 효율·사용률을 순서대로 반영하여 페이로드 전달량을 산정한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **송신 인터페이스(Transmit Interface)**: 데이터를 물리 버스 규격 폭(bit)에 맞추어 변환 및 패킹하는 발신 컨트롤러.
- **프로토콜 계층(Protocol Layer)**: 주소/제어/CRC 헤더를 부가하여 프레임 패킷을 캡슐화하는 레이어.
- **버스·링크(Bus/Link)**: 병렬 라인 수(Bit Width) 또는 직렬 레인 수(Lane Count, x1, x4, x16) 기반의 물리 통로.
- **측정기(Meter)**: 실시간 Bus Analyzer 및 PMU(Performance Monitoring Unit) 기반 실측 텔레메트리 모듈.

- **순환 중복 검사(Cyclic Redundancy Check, CRC)**: 버스 트랜잭션 프레임의 전송 중 비트 오류 발생 여부를 검증하기 위한 다항식 기반 에러 검출 코드.
</details>

```text
[송신 인터페이스]
        |
[프로토콜 계층]
        |
   [버스•링크]
        |
[수신 인터페이스]
        |
     [측정기]
```

선의 의미: 송신 데이터가 프로토콜 캡슐화 및 물리 버스를 통과하여 수신 파이프라인에서 측정기(Meter)를 통해 집계되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 송신 인터페이스 | 전송 큐 버퍼링 및 데이터 비트 폭 변환 수용 |
| 프로토콜 계층 | 트랜잭션 헤더, ACK/NAK 및 **CRC** 오버헤드 캡슐화 |
| 버스•링크 | 물리 레인(Lane), 클록 에지(DDR) 인가 및 물리 전송 실행 |
| 수신 인터페이스 | 유효 페이로드 추출 및 데이터 버퍼 전달 |
| 측정기 | 실효 **처리량** 및 버스 점유율(Utilization) 계측 |

#### 한줄 요약

- 송신 인터페이스·프로토콜 계층·버스·링크·수신 인터페이스·측정기가 전송과 계량 경로를 구성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **DDR(Double Data Rate)**: 클록 신호의 상승(Rising) 및 하강(Falling) 에지 모두에서 데이터를 전송하는 방식.
- **실측 사용률(Utilization, U)**: 이론적 페이로드 상한 대비 실제 유효하게 전달된 페이로드 비율.

</details>

### 단방향 이론 대역폭 산식

$$
B_{\mathrm{parallel}} = \frac{w \times r}{8},\qquad
B_{\mathrm{serial}} = \frac{b \times n \times \eta_{\mathrm{enc}}}{8}
$$

### 유효 페이로드 상한·실측 사용률 산식

$$
B_{\mathrm{payload,max}} = B_{\mathrm{link}}\eta_{\mathrm{proto}},\qquad
T_{\mathrm{measured}} = \frac{D_{\mathrm{payload}}}{\Delta t},\qquad
U = \frac{T_{\mathrm{measured}}}{B_{\mathrm{payload,max}}}
$$

### 동작 원리

1. 물리 대역폭 산정: **DDR** 에지, 비트 폭, 라인 코딩 비율($\eta_{\text{enc}}$) 기반 이론적 물리 대역폭 계산.
2. 프로토콜 오버헤드 적용: 패킷 헤더/CRC 비율($\eta_{\text{proto}}$)을 감안한 최고 유효 페이로드 대역폭 산출.
3. 실측 처리량 계측: 지정 시간 동안의 유효 수신 데이터 양($D_{\text{payload}}$) 집계.
4. 실측 사용률 분석: **실측 사용률** 및 중재 병목 구간 도출.

#### 한줄 요약

- 인코딩 효율과 프로토콜 효율을 반영한 상한과 실측 처리량의 차이로 경합 및 흐름 제어 손실을 식별한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **병렬 버스(Parallel Bus)**: 넓은 비트 폭(예: 32bit/64bit)을 한 클록에 동시 전송하는 방식 (예: PCI, DDR Bus).
- **직렬 링크(Serial Link)**: 고속 시리얼 레인(x1~x16)을 통해 차동 전압으로 데이터를 고속 래칭하는 방식 (예: PCIe, CXL).

</details>

| 비교 항목 | 병렬 버스 (Parallel Bus) | 직렬 링크 (Serial Link) |
|:---|:---|:---|
| 산정 방식 | $B = \frac{\text{Width(bit)} \times \text{Clock(Hz)} \times \text{DDR}}{8}$ | $B = \frac{\text{Rate(GT/s)} \times \text{Lanes} \times \eta_{\text{enc}}}{8}$ |
| 대역폭 확충 | 비트 라인 폭과 전송률 확충 | 레인 수와 레인당 전송률 확충 |
| 기술적 한계 | 신호 동기화 스큐(Clock Skew) 발생 | 물리 라인 **인코딩 오버헤드**(8b/10b 등) 차감 |

#### 한줄 요약

- 용량의 상한을 설계할 때는 이론 대역폭, 병목을 검증할 때는 같은 조건의 실측 처리량을 사용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **방향별 지표(Directional Metrics)**: 단방향(Simplex) 대역폭과 양방향(Full-Duplex) 통산 대역폭 수치 구분.
- **버스 경합(Bus Contention)**: 다중 노드가 자원을 동시 요청 시 중재 지연으로 인한 처리량 하락 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Bits/s와 Bytes/s 단위 혼용으로 인한 **대역폭 환산 오류** | 8 비트 나누기 규격 적용 및 단방향/양방향 명시 | 수치 산정 왜곡 방지 |
| 고속 직렬 링크 인코딩(8b/10b) 오버헤드 미반영 | **인코딩 효율**($\eta_{\text{enc}}$) 및 프로토콜 헤더 비율 공제 | 정확한 실효 대역폭 산출 |
| 다중 노드 동시 점유 시 **버스 경합** 발생 | 버스 중재 알고리즘 및 DMA 큐 깊이 최적화 | **실측 처리량** 극대화 |

> 사례: PCIe Gen 5 x16 규격 상의 32 GT/s 비트 전송률 및 128b/130b 인코딩 기반 실효 대역폭 산정

#### 한줄 요약

- 단위와 방향 및 메시지 크기·부하 조건을 고정한 뒤 처리량과 지연을 함께 측정해야 병목을 비교할 수 있다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **대역폭 개선 기준(Bandwidth Optimization Criteria)**: 실측 사용률(Utilization), 병목 구간 원인 및 TCO에 기반한 승급/증설 기준.

</details>

- 사용률이 낮으면 **경합·오버헤드 개선**, 포화면 **레인·세대 확장**

#### 한줄 요약

- 사용률이 낮으면 경합·오버헤드를 줄이고 포화면 레인이나 세대를 확장한다.
