---
sidebar:
  order: 145
  label: "145. HBM (고대역폭 메모리)"
  badge:
    text: "기출 · 80%"
    variant: note
title: "HBM (고대역폭 메모리)"
date: "2026-07-31T12:05:07+09:00"
tags:
  - "notes-latest-tech"
weight: 145
extra:
  question_no: "145"
  source_status: "기출"
  source_history: "129회, 131회"
  priority: 80
  priority_note: "HBM 대역폭·패키징 비교가 AI 인프라 핵심임"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **고대역폭 메모리(High Bandwidth Memory, HBM)**: 적층 DRAM과 초광폭 인터페이스를 사용하는 패키지 근접 메모리이다.
- **동적 임의접근 메모리(Dynamic Random-Access Memory, DRAM)**: 저장 값을 유지하려면 주기적으로 재충전해야 하는 휘발성 메모리이다.

</details>

- 정의/개념: **고대역폭 메모리(High Bandwidth Memory, HBM)** 는 적층 **동적 임의접근 메모리(Dynamic Random-Access Memory, DRAM)** 와 초광폭 인터페이스로 가속기에 높은 대역폭을 제공하는 패키지 근접 메모리
- 배경/필요성: 보드 메모리의 제한된 **핀 폭**으로 가속기 데이터 공급 병목

#### 한줄 요약

- 멀리 있는 좁은 창고 문을 빠르게 여닫는 대신 계산기 옆에 층층이 쌓은 창고와 수많은 문을 두어 재료를 동시에 공급하는 것과 같음

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **실리콘 관통전극(Through-Silicon Via, TSV)**: 적층 다이의 신호와 전원을 수직으로 연결하는 전극이다.
- **초광폭 인터페이스**: 다수의 비교적 저속인 신호 핀을 병렬로 사용해 큰 전송 대역폭을 만드는 연결 방식이다.

</details>

- **적층 축**: **실리콘 관통전극(Through-Silicon Via, TSV)** 기반 **동적 임의접근 메모리(Dynamic Random-Access Memory, DRAM) 다이** 수직 연결
- **대역폭 축**: 다수 저속 핀의 초광폭 병렬 채널
- **패키지 축**: 근접 배치로 전송 전력은 감소하나 열·수율 비용 증가

#### 한줄 요약

- 창고 층과 출입문을 늘리면 한꺼번에 더 많은 재료를 보내지만 공간이 좁아지고 열이 쌓이며 한 층의 불량이 전체 묶음 비용에 영향을 줌

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **인터포저(Interposer)**: 가속기와 고대역폭 메모리를 넓고 짧은 배선으로 연결하는 패키지 기판이다.
- **독립 채널**: 메모리 요청을 나누어 여러 뱅크에 동시에 접근하도록 제공하는 병렬 경로이다.

</details>

**인터포저(Interposer)** 는 가속기와 **고대역폭 메모리(High Bandwidth Memory, HBM)** 를 연결하고, **실리콘 관통전극(Through-Silicon Via, TSV)** 은 적층 **동적 임의접근 메모리(Dynamic Random-Access Memory, DRAM)** 다이를 수직으로 잇는다.

```mermaid
block-beta
  columns 3
  A["적층 DRAM"]
  B["TSV"]
  C["인터포저"]
  D["독립 채널"]
  E["열·전력 관리"]
  A --- B
  B --- C
  C --- D
  E --- A
```

| 구성요소 | 책임 |
|:---|:---|
| 적층 DRAM | **수직 적층 뱅크·저장 용량** 구성 |
| TSV | **데이터·주소·전원 수직 전달** |
| 인터포저 | **가속기-HBM 병렬 연결** |
| 독립 채널 | **요청 분산·병렬 접근** 조정 |
| 열·전력 관리 | **온도·전력 밀도 한도** 관리 |

#### 한줄 요약

- 인터포저는 계산기와 다층 창고를 잇는 넓은 바닥 배선이고, 관통 전극은 창고 층을 세로로 잇는 승강로이며, 채널은 동시에 여는 출입문임

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **메모리 뱅크**: 독립적으로 주소를 선택하고 데이터를 읽거나 쓸 수 있는 DRAM 내부 저장 구역이다.
- **주소 인터리빙**: 연속 주소를 여러 채널과 뱅크에 분산해 병렬 접근을 늘리는 배치 방식이다.

</details>

```mermaid
sequenceDiagram
    participant G as AI 가속기
    participant C as 독립 채널
    participant D as 적층 DRAM
    participant T as TSV
    participant I as 인터포저
    G->>C: 메모리 주소·읽기 요청
    C->>D: 1. 채널·뱅크 주소 전달
    D->>T: 2. 다이 데이터 전달
    T->>I: 3. 수직 병렬 데이터 전달
    I-->>G: 초광폭 데이터 반환
```

1. **채널·뱅크 주소 전달**: 요청 분산·병렬 접근
2. **다이 데이터 전달**: 선택 **동적 임의접근 메모리(Dynamic Random-Access Memory, DRAM) 다이·뱅크** 읽기
3. **수직 병렬 데이터 전달**: **실리콘 관통전극(Through-Silicon Via, TSV)·인터포저**로 신호 전송

#### 한줄 요약

- 계산기의 요청을 여러 창고 문과 선반에 나눠 보내고, 찾은 재료를 층간 승강로와 넓은 바닥 통로로 동시에 돌려보냄

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **그래픽 DDR(Graphics Double Data Rate, GDDR)**: 그래픽 처리용으로 높은 핀 속도를 제공하는 보드 실장 메모리이다.
- **DDR(Double Data Rate)**: 클록의 상승·하강 양쪽 변에서 데이터를 전송하는 범용 메모리이다.

</details>

**고대역폭 메모리(High Bandwidth Memory, HBM)**, **그래픽 이중 데이터 전송률 메모리(Graphics Double Data Rate, GDDR)**, **이중 데이터 전송률 메모리(Double Data Rate, DDR)** 는 대역폭·비용·용량 확장성의 우선순위가 다르다.

| 메모리 | HBM | GDDR | DDR |
|:---|:---|:---|:---|
| 적용 기준 | **가속기 대역폭 병목** | **가속기 비용 균형** | **범용 서버 용량 확장** |
| 핵심 특징 | **적층·초광폭·패키지 근접** | **보드 실장·고속 핀** | **모듈·채널 기반 범용성** |
| 한계 | **열·수율·패키징 비용** | **전력·핀 속도 부담** | **상대적으로 낮은 대역폭** |

> 요약: **HBM**은 대역폭, **GDDR**은 비용, DDR은 용량 중심

#### 한줄 요약

- HBM은 계산기 옆 다층 창고, GDDR은 보드 위 빠른 창고, DDR은 멀지만 용량을 쉽게 늘리는 범용 창고에 가까움

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **유효 대역폭**: 이론적 최대치 가운데 실제 워크로드가 병렬 접근으로 활용한 데이터 전송률이다.
- **열 밀도**: 제한된 패키지 면적에서 발생하는 열의 집중 정도이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 불균형 접근으로 **채널 대역폭** 미활용 | 주소 인터리빙·뱅크 병렬 배치 | **고대역폭 메모리(High Bandwidth Memory, HBM) 유효 대역폭** 향상 |
| 적층·근접 배치로 **열 밀도** 상승 | 열 경로·전력 제한·온도 감시 | 패키지 **성능 저하 방지** |

#### 한줄 요약

- 자주 쓰는 재료는 계산기 옆 **고대역폭 메모리(High Bandwidth Memory, HBM)** 창고의 여러 문에 나눠 두고, 공간이 모자라면 덜 쓰는 재료를 큰 **이중 데이터 전송률 메모리(Double Data Rate, DDR)** 창고에 보관했다가 미리 가져옴

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **대역폭 병목**: 메모리 전송률이 연산기가 요구하는 데이터 공급량보다 낮아 처리량을 제한하는 상태이다.
- **메모리 계층**: 속도·용량·비용이 다른 HBM과 DDR 등을 역할별로 배치한 저장 구조이다.

</details>

- 대역폭 병목은 **고대역폭 메모리(High Bandwidth Memory, HBM)**, 용량·확장성 우선은 **이중 데이터 전송률 메모리(Double Data Rate, DDR)** 선택

#### 한줄 요약

- 빠른 창고가 계산을 살리더라도 공간과 열 한계를 넘으면 큰 창고를 함께 쓰고 필요한 재료만 가까이 옮겨야 함
