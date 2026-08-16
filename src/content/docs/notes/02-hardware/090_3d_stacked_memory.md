---
sidebar:
  order: 90
  label: "090. 3D 적층 메모리 (3D Stacked Memory)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "3D 적층 메모리 (3D Stacked Memory)"
date: "2026-08-13T12:21:04+09:00"
tags:
  - "notes-hardware"
weight: 90
extra:
  question_no: "090"
  source_status: "기출"
  source_history: "126회"
  priority: 50
  priority_note: "대역폭•면적 이득과 열•수율 절충"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **3D 적층 메모리(3D Stacked Memory)**: 여러 DRAM 다이를 수직 적층하고 TSV로 연결해 대역폭과 밀도를 높이는 기술.
- **TSV(Through-Silicon Via)**: 실리콘 다이를 수직 관통해 적층 다이 사이의 전원·신호 경로를 형성하는 기술.
- **Base Die(Logic Die)**: 적층 DRAM 맨 하단에 위치하여 PHY 인터페이스, 테스트 래치, 자가 수리(Self-Repair) 및 메모리 컨트롤러 연동을 총괄하는 로직 다이.

</details>

- 정의/개념: DRAM을 수직 적층하고 **TSV**로 연결하여 초고대역폭을 달성하는 메모리
- 배경/필요성: **2D 평면 배선** 한계와 전력 누수로 **메모리 벽** 극복 불가

#### 한줄 요약

- 3D 적층 메모리는 TSV 광폭 경로로 대역폭과 면적 밀도를 확대한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Wide I/O**: 많은 저속 신호선을 병렬로 사용해 전체 메모리 대역폭을 높이는 인터페이스 방식.
- **Microbump**: Base Die와 적층 DRAM 다이 간의 접합 패드를 잇는 수십 μm 크기의 극소 볼 핀.
- **KGD(Known Good Die)**: 적층 전에 웨이퍼·다이 시험을 통과한 개별 다이.

</details>

- **TSV** 기반 다채널 **Wide I/O** 버스 구축
- 배선 길이 단축으로 전력 소비를 줄이고 **KGD** 수율 확보 요구
- 물리 칩셋 수직 적층으로 **열 밀도** 증가 및 방열 제어 필수

#### 한줄 요약

- 넓은 I/O의 대역폭 이득과 열 밀도•적층 수율 사이에는 상충 관계가 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Silicon Interposer**: 호스트 GPU/CPU ASIC과 3D 적층 메모리를 평면 인접 탑재하여 초고밀도 라우팅을 매개하는 초미세 실리콘 기판.
- **DRAM Core Stack**: 4층, 8층, 12층 또는 16층 형태로 수직 적층된 DRAM 파티션 레이어들.

</details>

```text
[메모리 제어기] -- [인터포저] -- [베이스 다이]
                                      |
                        [TSV•마이크로 범프]
                                      |
                            [메모리 다이 스택]
```

선의 의미: 메모리 제어기가 실리콘 인터포저를 거쳐 베이스 다이 및 TSV/마이크로 범프로 결합된 3D 적층 DRAM 코어 스택과 연동되는 패키징 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 메모리 제어기 | GPU·SoC의 광폭 채널 명령과 주소 스케줄링 |
| Silicon Interposer | 프로세서와 HBM 사이의 고밀도 평면 배선 제공 |
| Base Die (Logic Die) | TSV 신호, 테스트·수리와 물리 인터페이스 관리 |
| TSV • Microbump | 적층 다이 간 전원과 다채널 데이터 경로 제공 |
| DRAM Core Stack | HBM/3D-RAM 셀 어레이 상주 및 뱅크(Bank) 병렬 연산 처리 |

#### 한줄 요약

- 인터포저, 베이스 다이, TSV•마이크로 범프가 수평•수직 광폭 경로를 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Pseudo-Channel**: HBM3/3D 적층 메모리에서 1024-bit 넓은 버스를 논리적으로 분할 독립 구동하는 가상 채널 기술.

</details>

```text
[메모리 읽기 명령•주소]
          │
          ▼
1. 채널•다이•뱅크 해석
          │
          ▼
2. TSV 수직 경로 선택
          │
          ▼
3. 행 활성화•열 선택
          │
          ▼
4. 광폭 데이터 반환
          │
          ▼
 [메모리 제어기 수신]
```

### 동작 원리

1. **채널·다이·뱅크 해석**: 제어기의 **Pseudo-Channel** 주소 및 타깃 층 해석
2. **TSV 수직 경로 선택**: 인터포저와 **Base Die** 통과 후 **TSV** 수직선 라우팅
3. **행 활성화·열 선택**: 타깃 DRAM 층의 뱅크 Row/Column 활성화.
4. **광폭 데이터 반환**: **Wide I/O** 버스로 TSV와 인터포저 거쳐 데이터 반환

#### 한줄 요약

- 채널·다이·뱅크 해석과 TSV 수직 경로 선택 뒤 광폭 데이터 전송으로 메모리에 접근한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **HBM(High Bandwidth Memory)**: 적층 DRAM과 광폭 인터페이스를 사용하는 고대역폭 메모리 규격.
- **3D V-NAND**: NAND 플래시 셀 구조를 수직으로 적층해 저장 밀도를 높인 비휘발 매체.

</details>

| 비교 항목 | HBM (3D Stacked DRAM) | 3D V-NAND Flash | 2D DDR5 DIMM |
|:---|:---|:---|:---|
| 적층 대상 | DRAM 다이 수직 적층 | Flash 셀 어레이 수직 적층 | 평면 PCB에 DRAM 칩 배치 |
| 신호 연결 | **TSV**와 Microbump 기반 Wide I/O | 수직 NAND 셀 스트링 | PCB 메모리 채널 배선 |
| 주요 강점 | 높은 대역폭과 패키지 면적 효율 | 높은 비휘발 저장 밀도 | 용량 증설과 모듈 교체 용이 |
| 주요 한계 | 높은 패키징 비용과 열·수율 부담 | 블록 접근과 쓰기 내구성 제약 | 채널당 대역폭과 핀 수 제약 |

#### 한줄 요약

- 대역폭•패키지 면적이 중요하면 HBM, 용량 확장성과 교체 비용이 중요하면 보드형 메모리가 유리하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Thermal Throttling**: 3D 수직 적층 구조 특성상 발열이 내부에 누적되어 칩 손상을 막기 위해 동작 속도를 하향하는 제어.

- **전력 전달 네트워크(Power Delivery Network, PDN)**: 3D 적층 구조의 복수 다이에 안정적인 전압을 공급하고 IR Drop 및 노이즈를 억제하기 위한 전력 배선망.
</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 다이 적층 수 증가 시 내부 열 집적에 따른 **Thermal Throttling** | 액체 냉각(Liquid Cooling) 및 방열 TSV/TIM 소재 채택 | 온열 경감 및 성능 유지 |
| 1개 층만 불량 발생해도 전체 스택이 폐기되는 수율 위험 | **KGD(Known Good Die)** 사전 선별 및 수리 비트 맵핑 | 적층 수율 확보 |
| 다수 I/O 동시 전환 시 전원 노이즈 발생 | 디커플링 커패시터와 **PDN** 튜닝 | 전원·신호 무결성 여유 확보 |

> 사례: HBM 적층 높이별 대역폭·온도·수율·패키지 비용 비교

#### 한줄 요약

- 가속기에 인접한 인터포저와 TSV•마이크로 범프의 짧은 광폭 경로로 메모리 병목을 완화한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **3D 적층 메모리 선택 기준(3D Memory Architecture Selection Criteria)**: 소요 대역폭(TB/s), 수율/패키징 단가 및 방열 인프라에 기초한 수립 체계.

</details>

- 대역폭·면적 이득이 열·수율·비용을 상회하면 **HBM**, 증설성은 **DIMM** 선택

#### 한줄 요약

- 대역폭·면적 이득이 열·수율 비용보다 크면 HBM, 증설성은 DIMM을 선택한다.
