---
sidebar:
  order: 89
  label: "089. 광 인터커넥트"
  badge:
    text: "미출 · 70%"
    variant: note
title: "광 인터커넥트 (Optical Interconnect)"
date: "2026-08-17T09:25:00+09:00"
tags:
  - "notes-hardware"
weight: 89
extra:
  question_no: "089"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "인공지능 클러스터 대역폭•에너지 병목 대응"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Optical Interconnect(광 인터커넥트)**: 전자 회로 간의 데이터 통신 경로를 구리선 대신 광섬유(Optical Fiber)와 광 도파로(Waveguide)를 이용한 빛 신호로 대체하는 고속 인터커넥트 기술.
- **E/O & O/E Conversion(전기광/광전 변환)**: 송신단에서 전기 신호를 레이저 다이오드로 빛으로 변조(E/O)하고, 수신단에서 포토다이오드로 빛을 다시 전기로 복원(O/E)하는 과정.
- **CPO(Co-Packaged Optics)**: 광 트랜시버를 스위치/GPU ASIC과 동일한 서브스트레이트 기판 위에 칩렛(Chiplet) 형태로 초근접 패키징하는 차세대 광학 아키텍처.

</details>

- 정의/개념: AI/HPC 클러스터 내부의 GPU, 스위치 ASIC 및 메모리 간 고속 데이터 전송 시, 구리선(Copper)의 물리적 전송 한계(신호 감쇄, 대역폭 장벽, 발열)를 극복하기 위해 전기 신호를 광 신호(Laser)로 변환하여 광섬유(Optical Fiber) 및 실리콘 포토닉스로 전송하는 기술
- 배경/필요성: 초고속 SerDes 환경에서 구리 배선의 전송 거리 및 전력 소모 한계 극복과 대규모 가속기 클러스터의 광학 대역폭 확장 필요

#### 한줄 요약

- 구리 배선의 물리적 한계를 극복하고 **실리콘 포토닉스 광전 변환으로 테라비트급 전송을 실현하는 광 인터커넥트** ## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **WDM(Wavelength Division Multiplexing, 파장 분할 다중화)**: 단일 광섬유 코어에 서로 다른 파장($\lambda_1, \lambda_2, \dots$)의 레이저를 다중화하여 전송 대역폭을 수십 배로 증대하는 기술.
- **Link Budget(광 링크 버짓)**: 송신 광출력에서 커넥터/광섬유 삽입 손실을 차감한 후 수신 감도(Sensitivity)를 충족할 수 있도록 확보하는 광 신호 파워 마진(dB).
- **EMI Immunity(전자파 면역성)**: 빛을 매개로 하므로 고전압 전원부나 인접 고속 신호선으로부터 발생하는 전자파 노이즈 간섭을 전혀 받지 않는 특성.

</details>

- 고주파 영역에서도 신호 감쇄(Attenuation)가 극도로 작아 수백 미터 이상 무손실 전송이 가능하며 **EMI 전자파 간섭에 완전 면역**
- 단일 광섬유에 다수의 광 파장을 중첩하여 테라비트($\text{Tbps}$)급 대역폭을 구현하는 **파장 분할 다중화(WDM)**
- 광전 변환 시 발생하는 광학 삽입 손실을 정밀 제어하는 **광 링크 버짓(Link Budget) 및 에너지 효율(pJ/bit) 최적화** #### 한줄 요약

- **WDM 파장 다중화 고밀도 대역폭·EMI 전자파 노이즈 완전 면역·링크 버짓(Link Budget) 기반 광 손실 통제** ## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SerDes(Serializer/Deserializer)**: 병렬 데이터 버스를 고속 직렬 차동 신호로 변환하여 광 변조기로 전달하는 인터페이스 회로.
- **Silicon Photonics Modulator**: 마하-젠더 간섭계(MZM) 또는 마이크로링 공진기(MRR)를 사용하여 전기 전압으로 레이저 빛을 고속 스위칭하는 실리콘 소자.
- **Mux / Demux**: 다파장 광 신호를 단일 광섬유로 결합(Multiplexing)하거나 파장별로 분리(Demultiplexing)하는 광학 필터.

</details>

```text
[ 광 인터커넥트 송수신 아키텍처 및 실리콘 포토닉스 계층 ]
 
 [ 1. 송신단 (Transmitter) ]                   [ 2. 수신단 (Receiver) ]
┌──────────────────────────────┐              ┌──────────────────────────────┐
│ SerDes (전기 직렬화: PAM4)   │              │ SerDes (전기 역직렬화 복원)  │
├──────────────────────────────┤              ├──────────────────────────────┤
│ 실리콘 포토닉스 E/O 변조기   │              │ 포토다이오드 (O/E 광 검출기) │
├──────────────────────────────┤              ├──────────────────────────────┤
│ 파장 결합기 (Optical Mux)    │              │ 파장 분리기 (Optical Demux)  │
└──────────────┬───────────────┘              └──────────────▲───────────────┘
               │                                             │
               └──────────► [ 3. 광섬유 패치 케이블 ] ───────┘
                            (Low-Loss Single-Mode Fiber)
```

선의 의미: SerDes 전기 신호, 실리콘 포토닉스 E/O 변조기, Mux/Demux 파장 다중화 및 광 수신 포토다이오드(PD) 간의 광 인터커넥트 구조도.

| 구성요소 | 책임 |
|:---|:---|
| SerDes 회로 | 병렬 디지털 데이터를 고속 직렬 차동 신호(PAM4)로 인코딩하여 광 변조기로 전달 |
| 실리콘 포토닉스 변조기(E/O) | 전기 신호 전압으로 레이저 빛을 고속 변조하여 광 펄스로 변환하는 마이크로 광학 소자 |
| 광 Mux / Demux | WDM 기반 다파장 광 신호를 단일 코어로 결합(Mux)하거나 파장별로 분리(Demux)하는 필터 |
| 광 수신 포토다이오드(O/E) | 광섬유를 통해 수신된 빛 신호를 감지하여 고속 전기 전류 신호로 복원 |

#### 한줄 요약

- **SerDes(직렬화/역직렬화)·실리콘 포토닉스 변조기(E/O)·광 Mux/Demux 필터·광 검출기(O/E Photo Diode)** ## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **PAM4 Optical Modulation**: 광 펄스의 진폭을 4개 레벨(00, 01, 10, 11)로 변조하여 심볼당 2비트를 전송하는 고속 광 변조 방식.

</details>

```text
[ 광전 변환 및 WDM 다중화 데이터 전송 시퀀스 ]
                         │
                         ▼
   [ 1. ASIC 내부 병렬 데이터를 고속 SerDes 가 PAM4 직렬 전기 신호로 변환 ]
                         │
                         ▼
   [ 2. 실리콘 포토닉스 변조기가 CW 레이저 광을 PAM4 광 펄스로 변조 (E/O) ]
                         │
                         ▼
   [ 3. 광 Mux 가 서로 다른 파장의 레이저 신호들을 단일 광섬유로 다중화 결합 ]
                         │
                         ▼
   [ 4. 단일모드 광섬유(SMF)를 통해 원격 노드로 광 펄스 전송 ]
                         │
                         ▼
   [ 5. 광 Demux 가 파장별로 분리 ──> 포토다이오드가 전류 변환(O/E) ──> SerDes 복원 ]
```

**동작 원리** 1. **전기 직렬화**: 스위치 코어의 데이터를 SerDes가 112Gbps PAM4 전기 신호로 인코딩
2. **광 변조**: 실리콘 도파로를 통과하는 연속파(CW) 레이저에 전기 전압을 가해 광 펄스로 변조(E/O)
3. **파장 다중화**: 각기 다른 레이저 파장($\lambda_1\sim\lambda_8$)을 광 결합기(Mux)로 묶어 단일 코어로 방출
4. **광 전송**: 광섬유를 통해 수십~수백 미터를 마이크로초 지연으로 고속 통과
5. **광전 복원**: 광 분리기(Demux)를 거쳐 고감도 PIN/APD 포토다이오드가 빛을 전류로 변환(O/E) 후 디지털 복원

#### 한줄 요약

- SerDes PAM4 직렬화 $\to$ **실리콘 포토닉스 E/O 광 변조 $\to$ WDM 다중 파장 결합(Mux) $\to$ 광섬유 전송 $\to$ Demux 파장 분리 $\to$ O/E 포토다이오드 전기 신호 복원** ## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Pluggable Module vs CPO vs DAC Copper**:
  - Pluggable: 전면 패널 착탈식(QSFP-DD/OSFP), 교체 용이, SerDes PCB 손실 큼
  - CPO: ASIC과 동일 기판 초근접 실장, 전력 $30\sim 50\%$ 절감, 유지보수 난이도 높음
  - DAC: 패시브 구리선 직결, 초저비용/초저전력, 전송 거리 $1\sim 2\,\text{m}$ 한계

</details>

| 구분 | 플러거블 광 트랜시버 (Pluggable Optical Module) | 동반 패키지 광학 (Co-Packaged Optics, CPO) | 근거리 구리선 (Direct Attach Copper, DAC) |
|:---|:---|:---|:---|
| 구현 위치 및 폼팩터 | 스위치 전면 패널 착탈식 포트 (OSFP, QSFP-DD) | 스위치/ASIC 기판에 광 엔진 직접 패키징 | 구리 케이블 직결 (패시브/액티브 DAC) |
| 전송 거리 및 전력 소모 | 수백 $\text{m}\sim$ 수십 $\text{km}$, 채널당 높은 SerDes 전력 |  수십 $\text{m}\sim$ 수 $\text{km}$, 채널당 전력 $30\sim 50\%$ 절감 |  $1\sim 3\,\text{m}$ 초단거리 제한, 초저전력 |
| 한계 및 유지보수성 | SerDes 배선 손실 및 전면 패널 밀도 한계 | 광원 고장 시 수리 난이도 극심 (ELS 모듈 분리 필요) | 100G+ 대역폭 시 전송 거리 $1\,\text{m}$ 이하로 급감 |

#### 한줄 요약

- 범용 장거리는 **플러거블**, AI 초고밀도 저전력은 **CPO**, 랙 내 초단거리는 **구리선(DAC)** ## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ELS(External Laser Source)**: 발열에 취약한 고출력 레이저 다이오드를 CPO 메인보드 밖으로 분리하여 핫스왑 교체가 가능하도록 만든 외장형 광원 표준.
- **Active Alignment**: 서브미크론($<1\,\mu\text{m}$) 단위의 광섬유 정렬 오차로 인한 광 손실을 막기 위해 머신비전과 피에조 모터로 최적 광 결합 위치를 맞추는 정밀 패키징 공정.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 고출력 레이저 발열로 인한 파장 드리프트(Wavelength Drift) 및 광 출력 왜곡 발생 | 열전소자(TEC, Thermo-Electric Cooler) 기반 정밀 온도 제어 및 방열 설계 적용 | 레이저 중심 파장 안정화 및 WDM 광학 채널 간섭 방지 |
| CPO(Co-Packaged Optics) 구조에서 온칩 실장된 레이저 소자 고장 시 전체 보드 교체 위험 | **외장형 레이저 광원(ELS, External Laser Source)** 모듈 분리 및 핫스왑(Hot-Swap) 교체 체계 구축 | 유지보수 비용 절감 및 시스템 평균 수리 시간(MTTR) 단축 |
| 광섬유 코어와 실리콘 도파로 간 서브미크론 미세 정렬 오차로 인한 광 삽입 손실(Coupling Loss) 폭증 | **머신비전 기반 초정밀 능동 정렬(Active Alignment)** 및 렌즈 결합 구조 적용 | 광학 결합 손실(Coupling Loss) 1dB 이하 최소화 및 링크 버짓 마진 확보 |

#### 한줄 요약

- **외장형 레이저 광원(ELS: External Laser Source) 모듈 분리·TEC 온도 제어·능동 광학 정렬(Active Alignment) 손실 최소화** ## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Optical I/O Chiplet 진화**: PCIe/CXL 인터페이스를 네이티브 광 신호로 변환하는 광학 I/O 칩렛(Ayar Labs TeraPHY 등)을 통해 GPU-GPU 및 메모리 풀링의 스케일아웃 한계 극복.

</details>

- 차세대 51.2T/102.4T 스위치 및 대규모 GPU 슈퍼클러스터에서 **Silicon Photonics 기반 CPO 및 OIO(Optical I/O Chiplet) 표준 채택** #### 한줄 요약

- **전송 거리와 에너지 효율(pJ/bit)** 을 극대화하는 광 인터커넥트 패브릭 구축
