---
sidebar:
  order: 34
  label: "034. OFDM과 OFDMA"
  badge: { text: "기출 • 30%", variant: note }
title: "OFDM과 OFDMA"
date: "2026-08-13T16:44:00+09:00"
tags: ["notes-network"]
weight: 34
extra:
  question_no: "034"
  source_status: "기출"
  source_history: "125회"
  priority: 30
  priority_note: "125회 출제"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **직교 주파수 분할 다중화(Orthogonal Frequency Division Multiplexing, OFDM)**: 서로 직교하는 복수의 부반송파에 데이터를 분할하여 병렬 전송하는 다중화 방식이다.
- **직교 주파수 분할 다중 접속(Orthogonal Frequency Division Multiple Access, OFDMA)**: OFDM의 부반송파 묶음(RU)을 시간-주파수 영역에서 사용자별로 동적 할당하는 다중 접속 방식이다.
- **자원 단위(Resource Unit, RU)**: OFDMA에서 트래픽 요구량에 맞춰 사용자에게 할당하는 연속된 부반송파의 기본 서브그룹 단위이다.

</details>

- 정의/개념: **OFDM**은 직교성을 가진 부반송파로 대역폭을 분할 전송하는 다중화 기술이며, **OFDMA**는 부반송파 묶음인 **RU(Resource Unit)**를 복수 사용자에게 동시 배정하는 다중 접속 기술이다.
- 배경/필요성: 단일 반송파 광대역 전송 시 다중 경로 지연 확산으로 발생하는 심볼 간 간섭(ISI)과 채널 등화기 복잡도 급증 문제를 해결하기 위해 도입되었다.

#### 한줄 요약

- 광대역 채널을 직교 부반송파로 분할하여 단일 사용자에게 병렬 전송(OFDM)하거나, RU 단위로 다중 사용자에게 동시 할당(OFDMA)하는 무선 전송 기술.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **직교성(Orthogonality)**: 부반송파 간 주파수 스펙트럼이 겹치더라도 심볼 주기 동안의 적분값이 0이 되어 상호 간섭 없이 분리되는 수학적 성질이다.
- **최대 대 평균 전력비(Peak-to-Average Power Ratio, PAPR)**: 신호의 최대 전력과 평균 전력의 비율로, 값이 높을수록 송신 전력 증폭기의 비선형 왜곡과 전력 효율 저하를 유발한다.

</details>

- **스펙트럼 효율 극대화**: 부반송파 간 직교성을 유지하여 스펙트럼을 중첩 배치함으로써 주파수 이용 효율을 극대화한다.
- **다중 경로 지연에 강인**: 단일 반송파 대비 심볼 주기가 길어지고 순환 전치(CP)를 삽입하여 다중 경로 지연 확산 및 ISI를 효과적으로 차단한다.
- **동적 자원 할당(OFDMA)**: 채널 상태 정보(CSI)에 따라 사용자별로 주파수-시간 영역의 RU 크기와 위치를 유연하게 배정하여 고밀도 접속을 처리한다.

#### 한줄 요약

- 직교 부반송파 병렬화로 주파수 효율을 높이고, OFDMA의 RU 할당을 통해 고밀도 동시 접속 및 저지연 전송을 구현.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **역고속 푸리에 변환(Inverse Fast Fourier Transform, IFFT)**: 주파수 영역의 변조 심볼들을 시간 영역의 OFDM 복합 파형으로 변환하는 디지털 신호 처리 연산이다.
- **고속 푸리에 변환(Fast Fourier Transform, FFT)**: 수신된 시간 영역 OFDM 파형을 주파수 영역의 부반송파 심볼들로 다시 분리하는 연산이다.
- **순환 전치(Cyclic Prefix, CP)**: OFDM 심볼의 뒷부분을 복사하여 심볼 앞부분 보호 구간에 삽입함으로써 다중 경로 지연에 의한 ISI를 방지하는 기술이다.

</details>

```text
자원 스케줄러 (Resource Scheduler)
│
심볼·자원 매퍼 (Symbol Resource Mapper)
│
역고속 푸리에 변환 및 순환 전치 송신기 (IFFT·CP Transmitter)
│
무선 채널 (Wireless Channel)
│
고속 푸리에 변환 수신기 (FFT Receiver)
```

선의 의미: 자원 스케줄러와 심볼 매퍼가 부반송파 및 RU 배정을 정의하고, IFFT·CP 송신기와 FFT 수신기가 무선 채널 양단에서 신호 변복조 구조를 형성한다.

| 구성요소 | 책임 |
|:---|:---|
| 자원 스케줄러 | 사용자별 채널 품질(CSI)에 따라 최적의 RU 크기 및 주파수 위치 동적 할당 |
| 심볼·자원 매퍼 | QAM 변조 심볼을 지정된 부반송파 및 자원 단위(RU) 위치에 매핑 |
| IFFT·CP 송신기 | IFFT 연산으로 주파수 신호를 시간 파형으로 합성하고 보호 구간(CP) 삽입 |
| 무선 채널 | 다중 경로 지연 확산, 감쇄, 잡음 및 전파 간섭 환경 반영 |
| FFT 수신기 | CP 제거 후 FFT 연산을 수행하여 시간 파형을 부반송파별 심볼로 분리 복원 |

#### 한줄 요약

- 스케줄러가 RU를 배정하고 IFFT·CP 모듈이 파형 합성 및 보호 구간을 삽입하여 수신기 FFT로 복원하는 구조.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **자원 단위 할당표(Resource Unit Allocation Table, RU Allocation Table)**: 사용자별 채널 상태와 요구 트래픽에 맞춰 배정한 RU 인덱스를 기록한 스케줄링 결과이다.
- **부반송파 심볼(Subcarrier Symbol)**: 각 부반송파 주파수에 싣는 데이터 변조(QPSK, QAM) 값이다.
- **순환 전치 포함 파형(Cyclic Prefix OFDM Waveform)**: IFFT 연산 결과인 시간 파형의 끝부분을 복사해 심볼 전두부에 부착한 송신 파형이다.
- **다중 경로 파형(Multipath Waveform)**: 무선 채널을 통과하며 반사·굴절 및 지연 확산이 반영되어 수신기에 도착한 파형이다.
- **채널 상태 정보(Channel State Information, CSI)**: 수신측에서 측정한 주파수 채널의 신호 세기, PER, 신호 대 잡음비(SNR) 등의 피드백 데이터이다.

</details>

```text
1. 자원 단위 할당표 (RU Allocation Table)
      |
      v
2. 부반송파 심볼 매핑 (Subcarrier Symbol Mapping)
      |
      v
3. 순환 전치 포함 파형 생성 (IFFT / CP Insertion)
      |
      v
4. 다중 경로 페이딩 채널 전파 (Multipath Fading)
      |
      v
5. 수신 신호 고속 푸리에 변환 및 채널 추정 (FFT & CSI Feedback)
      |
      `-- 다음 자원 배정 주기 반복
```

### 동작 원리

1. **자원 단위 할당표**: 수신측 CSI 피드백에 근거해 사용자별 자원 단위(RU)를 동적 배정한다.
2. **부반송파 심볼 매핑**: 사용자 데이터를 QAM 변조 후 할당된 자원 단위(RU) 부반송파에 매핑한다.
3. **순환 전치 포함 파형 생성**: IFFT를 실행하여 시간 파형으로 변환 후 ISI 방지를 위한 CP를 삽입한다.
4. **다중 경로 페이딩 채널 전파**: 다중 경로 지연 확산 및 잡음이 존재하는 무선 공간 채널로 파형을 전송한다.
5. **수신 신호 고속 푸리에 변환 및 채널 추정**: 심볼 분리와 CSI 갱신

#### 한줄 요약

- CSI 피드백 기반 RU 할당, IFFT 파형 합성 및 CP 삽입 후 무선 채널 전송 및 수신측 FFT 복원 절차.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **다중화(Multiplexing)**: 단일 자원/채널에 복수의 데이터 스트림을 결합하여 송신하는 기술이다.
- **다중 접속(Multiple Access)**: 동일한 전송 자원을 다수의 사용자가 동시에 공유하여 통신할 수 있도록 할당하는 기술이다.

</details>

| 비교 항목 | **OFDM (Orthogonal Frequency Division Multiplexing)** | **OFDMA (Orthogonal Frequency Division Multiple Access)** |
|:---|:---|:---|
| 핵심 개념 | 직교 부반송파 기반 단일 사용자 병렬 전송 | 부반송파 그룹(RU) 기반 다중 사용자 동시 접속 |
| 자원 할당 단위 | 전체 대역폭 (Time-domain 단일 사용자 사용) | 주파수-시간 영역 분할 단위 (Resource Unit, RU) |
| 통신 지연시간 | 단일 사용자 시분할(TDM) 방식으로 접속 지연 발생 | 다중 사용자 병렬 동시 접속으로 지연시간 최소화 |
| 소용량 트래픽 효율 | 소용량 전송 시 전체 대역 점유로 주파수 낭비 심함 | 소용량 자원 분할 배정으로 고밀도 환경 자원 효율 극대화 |
| 기술적 한계 | 높은 PAPR 발생 및 도플러 시프트 영향 | 복잡한 자원 스케줄링 알고리즘 및 오버헤드 필요 |

> 요약: 단일 대용량 전송에는 OFDM, 고밀도 환경 다중 사용자 저지연 접속에는 OFDMA 적용.

#### 한줄 요약

- OFDM은 단일 사용자의 고속 데이터 병렬 송신에 특화되며, OFDMA는 자원 단위(RU) 분할을 통해 다중 사용자 동시 접속 및 주파수 효율 극대화.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **지연 확산(Delay Spread)**: 무선 다중 경로 반사파가 수신기에 도착할 때 발생하는 최고 지연 시간차로, CP 길이 결정의 기준이 된다.
- **공정성 스케줄링(Fairness Scheduling)**: 사용자 간 채널 상태뿐만 아니라 데이터 대기 시간과 전송 기회를 보장하는 자원 할당 알고리즘이다.

</details>

| 문제점 | 발생 이유 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 높은 PAPR로 인한 전력 왜곡 | 부반송파 파형의 시간 영역 동상 위상 중첩 | HPA(고전력 증폭기) 출력 백오프 및 Clipping/SLM 적용 | 비선형 신호 왜곡 예방 및 전력 효율 향상 |
| 직교성 훼손 및 ICI 발생 | 위상 잡음, 반송파 주파수 오차(CFO), 도플러 시프트 | 반송파 동기화 알고리즘 및 Guard Band 설정 | 부반송파 간 간섭(ICI) 방지 및 SNR 확보 |
| 심볼 간 간섭(ISI) 잔류 | 채널의 지연 확산이 CP 보호 구간 길이를 초과 | 환경별 지연 확산 측정 기반의 가변 CP(Normal/Extended) 적용 | 다중 경로 잔류 간섭 완전 제거 |
| 특정 사용자 자원 독점 | 채널 상태 우선 스케줄링 시 약전계 단말 기회 박탈 | Proportional Fairness 스케줄링 및 릴레이 채널 도입 | 사용자 간 접속 공정성 보장 및 서비스 음영 해소 |

#### 한줄 요약

- CP 길이 최적화, PAPR 저감 기법 적용, 동기 오차 보정 및 공정성 스케줄링으로 OFDM/OFDMA 전송 품질 확보.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **부반송파(Subcarrier)**: OFDM 파형을 구성하며 직교 관계를 유지하는 좁은 대역폭의 개별 carrier 파형이다.

</details>

- 단일 사용자 병렬 전송은 **OFDM**, 다중 접속은 **OFDMA** 선택

#### 한줄 요약

- 사용자 수와 RU 분할 요구에 따라 OFDM•OFDMA 결정
