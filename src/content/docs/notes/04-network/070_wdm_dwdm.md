---
sidebar:
  order: 70
  label: "070. WDM•DWDM 광 다중화 (WDM DWDM)"
  badge:
    text: "미출 • 30%"
    variant: note
title: "WDM•DWDM 광 다중화 (WDM DWDM)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-network"
weight: 70
extra:
  question_no: "070"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "비교•설계형: 광 Backbone WDM 선택 기반"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **파장 분할 다중화(Wavelength Division Multiplexing, WDM)**: 단일 광섬유(Optical Fiber) 코어 내에 서로 다른 개별 빛의 파장(Wavelength, $\lambda$)을 결합(Mux)하여 독립된 다중 데이터 채널을 동시에 병렬 전송하는 광 다중화 기술이다.
- **저밀도 파장 분할 다중화(Coarse Wavelength Division Multiplexing, CWDM)**: 20nm의 널찍한 채널 간격을 적용하여 비냉각(Uncooled) 레이저 소자로 제작함으로써 설치 비용을 낮춘 단거리 광 다중화 기술이다.
- **고밀도 파장 분할 다중화(Dense Wavelength Division Multiplexing, DWDM)**: ITU-T C/L 대역 표준 격자(100GHz/50GHz 간격: 0.8nm/0.4nm)를 적용하여 80~160개 이상의 초고밀도 파장 채널을 1개 광섬유에 집적 전송하는 대용량 백본 광전송 기술이다.
- **유연 격자(Flexible Grid, Flex-Grid)**: 기존 고정 주파수 격자 한계를 극복하고 12.5GHz 단위 슬롯 폭으로 대역을 가변 할당(Spectrum Slicing)하여 400G/1Tbps 초고속 광 채널 전송 효율을 극대화하는 기술이다.

</details>

- 정의/개념: **WDM**(Wavelength Division Multiplexing)은 송신 측에서 무선/유선 라우터의 클라이언트 신호들을 이질적인 광 파장으로 변환한 후 단일 광 케이블로 다중화 전송하고, 수신 측에서 파장별로 분리(Demux)하는 광 백본 코어 네트워킹 기술로, 채널 밀도에 따라 **CWDM**, **DWDM**, **Flex-Grid**로 발전하였다.
- 배경/필요성: 백본 트래픽의 폭발적 증가에 대응하여 광케이블 추가 포설(Fiber Trenching) 없이도 기존 가설된 광 케이블 1쌍의 물리적 전송 용량을 100배 이상 극대화하기 위해 전면 채택되었다.

#### 한줄 요약

- 단일 광섬유 내 다중 광 파장을 멀티플렉싱하여 광케이블 추가 굴착 없이 백본 용량을 확장하는 WDM 및 DWDM 광 다중화 기술 적용.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **인접 채널 간섭(Adjacent Channel Interference)**: DWDM과 같이 파장 간격이 매우 좁아질 때(50GHz 이하), 이웃한 파장 채널 간 파장 겹침 및 사파 혼합(FWM)으로 인해 광 신호 품질이 저하되는 현상이다.
- **광 신호대잡음비(Optical Signal-to-Noise Ratio, OSNR)**: 광 영역에서 수신된 빔 신호 전력 대비 EDFA 광증폭기가 유발한 자연방출 잡음(ASE Noise) 전력의 비율(dB)이다.

</details>

- 물리 광케이블 포설 투자를 하지 않고도 단일 광선로의 전송 용량을 방대하게 확장(Protocol & Speed Independent)한다.
- 초고밀도 채널 배치가 이루어지는 DWDM 구간에서는 **인접 채널 간섭** 및 색분산(Chromatic Dispersion) 관리 역량이 핵심 요소로 작용한다.
- 전기적 재생(OEO 3R) 없이 **EDFA** 광증폭기만을 경유하여 장거리 전송 시, 누적된 ASE 잡음으로 인해 **OSNR** 수치가 점진적으로 하락하는 물리적 임계 특징을 가진다.

#### 한줄 요약

- 선로 매설 없는 광 용량 확장 및 OSNR 이득 확보와 인접 파장 간섭(FWM) 제어를 결합한 광 백본 설계 원칙 준수.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **트랜스폰더(Transponder / OEO Transponder)**: 표준 회선 신호(Grey Optical)를 WDM 전용 고정밀 ITU-T 규격 파장(Colored Optical)으로 상호 광-전-광(O-E-O) 변환하는 인터페이스 장치이다.
- **에르븀 첨가 광섬유 증폭기(Erbium-Doped Fiber Amplifier, EDFA)**: 광 신호를 전기 신호로 재변환하지 않고 에르븀 이온 특성을 이용해 C-Band(1530~1565nm) 광 파장들을 아날로그 상태 그대로 일괄 직접 증폭하는 핵심 광 증폭기이다.
- **재구성 광 분기결합 다중화기(Reconfigurable Optical Add-Drop Multiplexer, ROADM)**: Wavelength Selective Switch(WSS) 모듈을 내장하여, 수동 조작 없이 중앙 NMS 제어로 특정 광 파장을 노드에서 동적으로 Add/Drop/Pass-through 스위칭하는 원격 광 디바이스이다.
- **광 채널 모니터(Optical Channel Monitor, OCM)**: WDM 광선로를 흐르는 개별 파장 채널의 Center Frequency, Optical Power, OSNR을 탭(Tap) 파이버로 분기하여 실시간 모니터링하는 감지 장치이다.

</details>

- **트랜스폰더**가 다양한 클라이언트 트래픽을 ITU-T 규격 Colored 파장으로 변환하고, **ROADM** 스위치가 WSS 제어로 파장을 동적 스위칭하며, **EDFA**가 중간 광손실을 보상하고 **OCM**이 OSNR을 정밀 감시한다.

```text
[클라이언트 트래픽] ──► [OEO 트랜스폰더 (Colored Wavelength)] ──► [WDM MUX (파장 결합)]
                                                                          │
[수신 트래픽] ◄── [OEO 트랜스폰더] ◄── [ROADM (WSS Add/Drop)] ◄── [EDFA 광증폭기 & OCM 모니터] ◄┘
```

| 구성요소 | 역할 및 핵심 기능 |
|:---|:---|
| **OEO 트랜스폰더 (Transponder)** | Short-reach 광 신호를 DWDM 계위 ITU-T 규격 파장(Colored Lambda)으로 변환 및 3R 재생 |
| **광 다중화/역다중화기 (MUX/DEMUX)** | AWG(Arrayed Waveguide Grating) 기술 기반으로 다수 파장을 결합 및 분리 |
| **ROADM 노드 (ROADM Node)** | WSS(Wavelength Selective Switch)를 활용해 파장 교차 연결 및 원격 동적 분기결합 처리 |
| **광증폭기 (EDFA / Raman Amp)** | 80km 간격 광선로 감쇠 손실을 전기 변환 없이 광 영역에서 직접 아날로그 일괄 증폭 |
| **광 채널 모니터 (OCM)** | 각 파장의 스펙트럼 밀도, 파장 쏠림(Drift) 및 OSNR 지표를 인라인 모니터링 |

#### 한줄 요약

- OEO 트랜스폰더 파장 변환, EDFA 광 영역 직접 증폭, ROADM 기반 파장 스위칭 및 OCM 품질 감시 아키텍처 적용.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **파장 연속성(Wavelength Continuity Constraint)**: 광 경로(Lightpath) 상에 파장 변환기(Wavelength Converter)가 없을 경우, 출발지부터 목적지 노드까지 동일한 파장 번호($\lambda_k$)가 전 구간 통틀어 연속 비어있어야 하는 제약 조건이다.
- **광 복호 여유(Optical Decoding Margin)**: 수신 트랜스폰더의 최소 요구 OSNR 대비 실제 도착한 OSNR 간의 데시벨(dB) 안전 여유 수치이다.
- **경로·연속 슬롯 조회(Path & Consecutive Slot Lookup)**: 소스 노드부터 데스티네이션 노드까지의 토폴로지 상에서 사용 가능한 빈 파장/슬롯을 탐색하는 단계이다.
- **광 자원 할당(Optical Resource Allocation)**: 파장 경합(Conflict)을 선제 차단하고 해당 파장 번호를 시그널링 예약하는 단계이다.
- **파장·변조 신호 전달(Wavelength & Modulation Signal Delivery)**: 트랜스폰더가 Coherent QPSK/16QAM 변조로 광 신호를 송출하는 단계이다.
- **파장 경로 구성(Optical Path Provisioning)**: ROADM WSS 스위치를 제어하여 물리적 광 전송 터널(Lightpath)을 수립하는 단계이다.
- **광 품질 측정 요청(Optical Quality Measurement Request)**: OCM으로 수신 OSNR과 Dispersion 수치를 정밀 판정하는 단계이다.

</details>

```text
광 경로 수립 요청 (Lightpath Setup Request: Source to Destination)
      │
      ▼
1. 파장 연속성 제약 충족 경로/슬롯 탐색 (Wavelength Continuity & RWA Check)
      ├─ [연속 파장 부재] ──► 타 경로 우회 탐색 또는 Flex-Grid 슬롯 재배치
      └─ [연속 파장 존재]
            │
            ▼
2. WDM 파장 자원 할당 및 파서 연산 (Lambda Resource Allocation)
            │
            ▼
3. Coherent 트랜스폰더 파장 인코딩 송출 (Colored Optical Signal Generation)
            │
            ▼
4. ROADM WSS 동적 파장 스위칭 경로 설정 (ROADM WSS Provisioning)
            │
            ▼
5. EDFA 증폭 및 OCM 기반 OSNR 마진 측정 (OSNR Check & Optical Path Active)
```

### 동작 원리

1. **경로·연속 슬롯 조회**: RWA(Routing and Wavelength Assignment) 알고리즘으로 출발지-목적지 간 **파장 연속성**을 만족하는 파장을 탐색한다.
2. **광 자원 할당**: 충돌이 없는 유효 파장을 선점 및 광 자원으로 최종 등록한다.
3. **파장·변조 신호 전달**: **트랜스폰더**가 100G/400G Coherent 변조 기술을 적용해 정밀 지정 파장을 발사한다.
4. **파장 경로 구성**: **ROADM** 노드의 WSS 스위치를 제어하여 물리적 교차 연결 포트(Express/Add/Drop)를 셋업한다.
5. **광 품질 측정 요청**: **OCM** 장비가 수신 측 **OSNR** 및 **광 복호 여유**를 측정하여 품질 기준 충족 시 즉시 개통한다.

#### 한줄 요약

- RWA 알고리즘 기반 파장 연속성 검증과 ROADM WSS 광 경로 셋업, OCM OSNR 마진 확인 프로세스 준수.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **스펙트럼 단편화(Spectrum Fragmentation)**: Flex-Grid 광망에서 파장 채널의 개설과 해제가 반복되면서 주파수 대역 내에 파편화된 빈 슬롯이 산재하여 대용량 채널을 연속 할당하지 못하는 현상이다.

</details>

- **CWDM**은 파장 간격(20nm)이 넓어 소형 메트로망 및 단거리 연동에 경제적으로 적용된다.
- **DWDM**은 좁은 파장 간격(0.8nm/0.4nm)으로 장거리 대용량 백본에 필수적이며, **Flex-Grid**는 12.5GHz 단위로 대역을 가변 조절하여 400G/1T 초고속 라우터 트래픽을 유연하게 수용한다.

| 비교 항목 | CWDM (Coarse WDM) | DWDM (Dense WDM) | Flex-Grid WDM (Flexible) |
|:---|:---|:---|:---|
| **채널 간격 (Spacing)** | 20 nm (널찍한 간격) | 0.8 nm (100GHz) / 0.4 nm (50GHz) | 12.5 GHz 단위 가변 슬롯 할당 |
| **최대 파장 수 (Capacity)** | 최대 18 파장 내외 | 80 ~ 160 파장 이상 | 주파수 효율성에 따라 100~200+ 파장 |
| **광 증폭기(EDFA) 수용** | 불가 (넓은 대역 폭으로 일괄증폭 불가) | **가능** (C/L-Band 범위 연동 광 증폭) | **가능** (Coherent 광 증폭 기술 연동) |
| **전송 거리 및 비용** | 단거리 ($<80$km) / 저비용 Uncooled 레이저 | 장거리 (수천 km) / 고비용 Coherent 레이저 | 대륙간 장거리 백본 / 최고 수준 연산 비용 |
| **핵심 한계** | 용량 확장 한계, 광증폭 불가 | 고정 격자로 400G/1T 대역 효율 저하 | **스펙트럼 단편화**, 복잡한 RWA 통제 |

> 요약: 메트로 센터 간 저비용 단거리 연결에는 **CWDM**, 전국망 대용량 백본 인프라 구축에는 **DWDM**, 400G/1Tbps 이상의 차세대 백본 코어 전송에는 **Flex-Grid ROADM**을 채택한다.

#### 한줄 요약

- CWDM, 고정 격자 DWDM, 가변 슬롯 Flex-Grid 간 채널 밀도, 전송 거리 및 스펙트럼 효율성 비교 모델 수용.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **광 손실(Optical Loss / Attenuation)**: 광섬유 접속점(Splice), 커넥터 및 유리 매체 자체 감쇠로 인해 빛의 세기(dBm)가 줄어드는 물리적 손실 현상이다.

</details>

| 실무 문제점 | 발생 원인 | 해결 대책 | 기대 효과 |
|:---|:---|:---|:---|
| **파장 연속성 부재 개통 차단** | 특정 중간 노드에서 전 구간 동일 파장 슬롯 고갈 | ROADM 노드 내 파장 변환기(Wavelength Converter) 배치 | 파장 경합 해소 및 RWA 성공률 증대 |
| **장거리 OSNR 수치 미달** | EDFA 다단 다단 직접 증폭 시 발생한 ASE 잡음 누적 | Coherent 수신기 적용 및 Raman 하이브리드 광증폭기 도입 | OSNR 디코딩 마진 확보 및 장거리 무재생 전송 |
| **스펙트럼 단편화 발생** | Flex-Grid 가변 슬롯의 무작위 생성/해제에 따른 파편화 | Defragmentation 알고리즘 적용 및 슬롯 주기적 재배치 | 주파수 스펙트럼 이용률 30% 이상 향상 |
| **색분산 및 비선형 왜곡** | 고속 100G+ 전송 시 광섬유 색분산 및 SPM/XPM 왜곡 발생 | Coherent DSP(Digital Signal Processing) 기반 이퀄라이징 연산 | 물리적 분산보상광섬유(DCF) 제거 및 연산 복구 |

#### 한줄 요약

- Coherent DSP 기반 분산 보정, Raman 증폭 연동 OSNR 개선 및 ROADM 파장 변환기 배치를 통한 WDM 광망 가동성 확보 체계 구축.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **신규 광섬유 없는 용량 확장(Capacity Expansion without Fiber Trenching)**: WDM 파장 다중화를 적용하여 물리적 토목 공사 없이 기존 광케이블 인프라의 전송 용량을 극대화하는 경제적 효과이다.
- **광 경로 공학 제약(Optical Path Engineering Constraints)**: OSNR 하락, 색분산, 사파 혼합 비선형성 및 파장 연속성을 통합 계산하여 광전송망을 설계해야 하는 기술적 경계이다.

</details>

- 백본 망 구축 시 **신규 광섬유 없는 용량 확장** 이점과 **광 경로 공학 제약** 요소들을 다각도로 검토하여, 단거리 구축에는 **CWDM**, 대규모 전국 백본에는 **DWDM**, 차세대 400G+ 대역에는 **Flex-Grid ROADM**을 유연하게 수용하는 지능형 광전송 인프라 구축 체계 적용.

#### 한줄 요약

- Coherent 광전송 기술 및 Flex-Grid ROADM을 결합하여 초고속 광 백본 용량을 극대화하는 WDM 전송 아키텍처 구현 필수.
