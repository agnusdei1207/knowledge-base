---
sidebar:
  order: 90
  label: "090. 3D 적층 메모리 (3D Stacked Memory)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "3D 적층 메모리 (3D Stacked Memory)"
date: "2026-08-13T10:12:00+09:00"
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

<details><summary>핵심 용어</summary>

- **3D 적층 메모리(3D Stacked Memory)**: 여러 층의 DRAM 다이(Die)를 수직으로 수평 적층하고 TSV(Through-Silicon Via) 전극으로 관통 연결하여 메모리 대역폭과 밀도를 극대화하는 반도체 기술.
- **TSV(Through-Silicon Via)**: 실리콘 다이 수직 몸체를 마이크로미터 단위 핀홀 관통 형성하여 전원 및 광폭 1024-bit 전송 버스를 구축하는 기술.
- **Base Die(Logic Die)**: 적층 DRAM 맨 하단에 위치하여 PHY 인터페이스, 테스트 래치, 자가 수리(Self-Repair) 및 메모리 컨트롤러 연동을 총괄하는 로직 다이.

</details>

- 정의/개념: DRAM을 수직 적층하고 **TSV**로 연결하여 초고대역폭을 달성하는 메모리
- 배경/필요성: **2D 평면 배선** 한계와 전력 누수로 **메모리 벽** 극복 불가

#### 한줄 요약

- 3D 적층 메모리는 TSV 광폭 경로로 대역폭과 면적 밀도를 확대한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Wide I/O**: 기존 DRAM의 32-bit/64-bit I/O 선로 폭을 1024-bit 이상으로 확장하여 초고속 대역폭을 얻는 비트 폭 기술.
- **Microbump**: Base Die와 적층 DRAM 다이 간의 접합 패드를 잇는 수십 μm 크기의 극소 볼 핀.
- **KGD(Known Good Die)**: 적층 적재 전 수율 하락을 방지하기 위해 100% 정상 작동이 검증된 단품 다이 선별 체계.

</details>

- **TSV** 전극 기반 1024-bit 초광폭 **Wide I/O** 버스 구축
- 배선 길이 단축으로 전력 소비를 줄이고 **KGD** 수율 확보 요구
- 물리 칩셋 수직 적층으로 **열 밀도** 증가 및 방열 제어 필수

#### 한줄 요약

- 넓은 I/O의 대역폭 이득과 열 밀도•적층 수율 사이에는 상충 관계가 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

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
| 메모리 제어기 | GPU/SoC 내 1024-bit 광폭 채널 명령어 및 주소 스케줄링 |
| Silicon Interposer | 물리 패키지 상에서 수천 개의 초미세 배선을 매개하여 1024-bit 전송 인가 |
| Base Die (Logic Die) | TSV 물리 신호 리타이밍, **KGD** 수리(BIST) 및 물리 인터페이스 관리 |
| TSV • Microbump | 수직 3D 다이 간 전기 전원 공급 및 1024-bit 데이터 버스 통로 역할 |
| DRAM Core Stack | HBM/3D-RAM 셀 어레이 상주 및 뱅크(Bank) 병렬 연산 처리 |

#### 한줄 요약

- 인터포저, 베이스 다이, TSV•마이크로 범프가 수평•수직 광폭 경로를 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

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

<details><summary>핵심 용어</summary>

- **HBM(High Bandwidth Memory)**: 3D 적층 메모리의 대표적 상용화 규격으로, HBM3e/HBM4 기준 1.2TB/s~2TB/s 초고대역폭 제공.
- **3D V-NAND**: DRAM이 아닌 NAND 플래시 메모리 셀을 수직 100층 이상 쌓아올려 고용량을 달성하는 저장 매체.

</details>

| 비교 항목 | HBM (3D Stacked DRAM) | 3D V-NAND Flash | 2D DDR5 DIMM |
|:---|:---|:---|:---|
| 적층 대상 | DRAM 칩셋 수직 적층 (4~16층) | Flash Memory 셀 어레이 수직 적층 | 평면 PCB 상에 칩 수평 배치 |
| 신호 연결 | **TSV** 및 **Microbump** (Wide I/O) | 수직 Charge Trap Flash 셀 직결 | PCB 구리 버스선 (64-bit) |
| 주요 강점 | 초고대역폭 (1TB/s 이상), 최저 면적 | 초고용량 (TB 단위 저장), 저비용 | 용량 증설 용이, 모듈 교체성 |
| 주요 한계 | 고비용, 패키징 난도 및 열 발열 | 접근 속도 지연 (~μs 수치) | 대역폭 및 핀 수 물리 한계 |

#### 한줄 요약

- 대역폭•패키지 면적이 중요하면 HBM, 용량 확장성과 교체 비용이 중요하면 보드형 메모리가 유리하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Thermal Throttling**: 3D 수직 적층 구조 특성상 발열이 내부에 누적되어 칩 손상을 막기 위해 동작 속도를 하향하는 제어.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 다이 적층 수 증가 시 내부 열 집적에 따른 **Thermal Throttling** | 액체 냉각(Liquid Cooling) 및 방열 TSV/TIM 소재 채택 | 온열 경감 및 성능 유지 |
| 1개 층만 불량 발생해도 전체 스택이 폐기되는 수율 위험 | **KGD(Known Good Die)** 사전 선별 및 수리 비트 맵핑 | 적층 수율 확보 |
| 초미세 1024-bit 전송선 동시 변환 시 전원 노이즈 발생 | 디커플링 콘덴서 및 **PDN(Power Delivery Network)** 튜닝 | 신호 무결성(SI/PI) 보장 |

> 사례: **HBM3e (24GB/36GB 12-High)** 3D 적층 메모리 기반 AI 수퍼컴퓨터 가속기 인프라 구축

#### 한줄 요약

- 가속기에 인접한 인터포저와 TSV•마이크로 범프의 짧은 광폭 경로로 메모리 병목을 완화한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **3D 적층 메모리 선택 기준(3D Memory Architecture Selection Criteria)**: 소요 대역폭(TB/s), 수율/패키징 단가 및 방열 인프라에 기초한 수립 체계.

</details>

- 초고성능 AI 가속 요구 시 **소요 대역폭•수율** 기준 **HBM3e/4** 채택

#### 한줄 요약

- TSV 실콘 관통 전극 및 베이스 다이 결합 기반 초고대역폭 HBM 3D 적층 메모리 아키텍처 구축 체계 적용.
