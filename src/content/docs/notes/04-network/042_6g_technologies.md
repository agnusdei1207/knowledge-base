---
sidebar:
  order: 42
  label: "042. 6G 핵심 기술 (6G Vision & Technologies)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "6G 핵심 기술 (6G Vision & Technologies)"
date: "2026-08-13T17:02:00+09:00"
tags:
  - "notes-network"
weight: 42
extra:
  question_no: "042"
  source_status: "기출"
  source_history: "128회, 135회"
  priority: 70
  priority_note: "설명•설계형: 128•135회 6G 반복"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **국제 이동통신 2030(International Mobile Telecommunications 2030, IMT-2030)**: ITU-R에서 제정한 2030년대 차세대 6G 이동통신의 비전, 목표 성능 및 사용 시나리오 규격이다.
- **국제전기통신연합(International Telecommunication Union, ITU)**: 전 세계 전기통신 및 무선 주파수 표준화를 조정하는 유엔 산하 전문 기구이다.
- **6세대 이동통신(Sixth-Generation Mobile Communication, 6G)**: IMT-2030 성능•사용 시나리오를 지향하는 차세대 이동통신이다.
- **5세대 이동통신(Fifth-Generation Mobile Communication, 5G)**: eMBB, URLLC, mMTC 중심의 4세대 이후 상용화된 이동통신 기술 규격이다.
- **인공지능(Artificial Intelligence, AI)**: 네트워크 무선/코어 제어 플레인에 직접 내재되어 오토스케일링 및 전파 제어를 자율 수행하는 지능 기술이다.

</details>

- 정의/개념: ITU-R **IMT-2030** 프레임워크의 차세대 이동통신
- 배경/필요성: 5G만으로는 **센싱•AI•입체 연결 요구 통합 불가**

#### 한줄 요약

- 통신•센싱•AI•입체 연결을 통합하는 IMT-2030

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **비지상망(Non-Terrestrial Network, NTN)**: 저궤도 인공위성(LEO), 고고도 무인 항공 플랫폼(HAPS)을 무선 기지국으로 활용하여 전 지구 3D 입체 커버리지를 제공하는 망이다.
- **통신·센싱 통합(Integrated Sensing and Communication, ISAC)**: 동일 무선 자원 파형으로 고속 데이터 전송과 주변 3D 공간의 물체/기상 감지를 동시에 수행하는 기술이다.
- **인공지능 내재형(Artificial Intelligence-Native, AI-Native)**: 통신 프로토콜, 자원 할당, 무선 빔포밍 등 네트워크 전 영역에 AI를 기본 제어 엔진으로 내재화한 구조이다.
- **국제전기통신연합 전파통신부문(International Telecommunication Union Radiocommunication Sector, ITU-R)**: IMT 표준 및 글로벌 무선 주파수 분배를 관장하는 ITU 산하 부문이다.
- **테라헤르츠(Terahertz, THz)**: 100GHz~3THz 대역의 극초광대역 주파수로, 1Tbps 피크 속도를 보장하기 위한 6G 핵심 후보 대역이다.
- **재구성 지능형 표면(Reconfigurable Intelligent Surface, RIS)**: 메타물질 음영 표면 소자의 위상을 동적 조정하여 전파 음영 구역으로 빔을 자율 반사·회절시키는 기술이다.

</details>

- **Sub-THz 극초광대역 전송**: 넓은 후보 대역으로 고속 전송을 연구한다.
- **ISAC 기반 통신 및 감지 융합**: 전파 반사 파형을 분석하여 기상, 위치, 이동 객체 형상을 레이더처럼 센싱하는 레이더-통신 통합 기능을 제공한다.
- **3D 공간 입체 연결(NTN)**: 위성과 지상망으로 커버리지 범위를 확장한다.

#### 한줄 요약

- Sub-THz 주파수, RIS 전파 제어, ISAC 통신-센싱 융합, NTN 위성 입체망 및 AI-Native 자원 통제로 5G 성능 한계 극복.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **분산 컴퓨팅(Distributed Computing)**: 단말, 에지(MEC), 코어망 및 위성 인프라 전반에 컴퓨팅 연산 자원을 분산 배치하여 AI 추론을 고속 처리하는 아키텍처이다.

</details>

```text
6G 입체 통합 통신망 아키텍처
├─ 인공지능 내재형 제어 평면 (AI-Native Control Plane)
├─ 심층 분산 컴퓨팅 인프라 (Deep Distributed Computing)
├─ 지상 및 비지상망 통합 접속 (Terrestrial & NTN Integrated RAN)
└─ 서브 테라헤르츠 및 재구성 지능형 표면 (Sub-THz & RIS Spatial Modulation)
```

선의 의미: AI-Native 제어 평면이 지상 및 NTN 위성망 접속, Sub-THz/RIS 무선 채널, 심층 분산 컴퓨팅 연산 자원을 지능적으로 통합 관제하는 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| AI-Native 제어 평면 | 딥러닝 기반 무선 채널 추정, 실시간 오토스케일링 및 사용자 핸드오버 자율 통제 |
| 심층 분산 컴퓨팅 | 단말-MEC-위성 간 연산 자원 공유를 통해 초저지연 AI 추론 및 분산 처리 수행 |
| 지상 및 NTN 통합 접속 | 지상 6G 기지국(gNB)과 저궤도 위성(LEO NTN) 간 seamless 3D 무선 접속 중계 |
| Sub-THz 및 RIS 무선 | 100GHz 이상 초고주파 변복조 및 메타물질 반사판(RIS)을 통한 무선 커버리지 음영 해소 |

#### 한줄 요약

- AI-Native 지능형 제어와 분산 컴퓨팅을 기반으로 지상 셀과 NTN 위성망이 결합하여 Sub-THz 및 RIS 전파 경로를 통합 제어하는 아키텍처.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **디지털 트윈(Digital Twin)**: 실제 무선 채널, 기지국 상태, 이동 단말 위치를 가상 디지털 공간에 실시간 동기화하여 전파 환경을 시뮬레이션하는 기술이다.
- **폐루프 제어(Closed-Loop Control)**: 관측된 네트워크 상태 및 실행 결과를 모니터링하여 자원 배정 및 빔포밍 정책을 능동적으로 실시간 피드백 조정하는 방식이다.

</details>

```text
1. 주파수 채널 및 공간 센싱 데이터 측정 (Channel & ISAC Sensing)
      │
      v
2. 디지털 트윈 상태 동기화 및 전파 예측 (Digital Twin Prediction)
      │
      v
3. AI-Native 기반 지상/위성 및 RIS 반사 경로 최적화 (AI Policy Generation)
      │
      v
4. 비지상망(NTN) 및 Sub-THz 초저지연 패킷 전달 (Packet Transmission)
      │
      v
5. 엔드투엔드 실시간 품질 모니터링 및 Closed-Loop 피드백 (Closed-loop Feedback)
```

### 동작 원리

1. **무선 채널 및 공간 센싱**: 무선 신호 전파와 ISAC 센싱 신호를 활용해 주변 지형, 반사체, 이동체 위치 정보를 실시간 측정한다.
2. **디지털 트윈 동기화**: 측정된 정밀 센싱 데이터를 디지털 트윈 모델에 입력하여 미래 전파 경로 및 도플러 효과를 시뮬레이션한다.
3. **AI 정책 기반 자원 결정**: AI-Native 엔진이 최적의 지상/위성 접속 경로, RIS 위상 변조값 및 무선 빔포밍을 결정한다.
4. **비지상망(NTN) 및 Sub-THz 초저지연 패킷 전달**: 선택 경로로 전송
5. **폐루프(Closed-Loop) 피드백**: 실제 전송 품질(SLI)을 수집하여 AI 엔진에 피드백함으로써 다음 주기의 제어 파라미터를 자율 튜닝한다.

#### 한줄 요약

- 채널/센싱 상태 수집, 디지털 트윈 전파 예측, AI 정책 기반 경로 지정, 패킷 전송 및 닫힌 루프 피드백으로 연결되는 6G 자원 통제 흐름.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **기술 성숙도(Technology Readiness Level, TRL)**: 신기술의 핵심 원리 연구부터 시험, 상용화까지의 단계적 완성도 평가 기준이다.

</details>

| 비교 항목 | **6G (IMT-2030)** | **5G (IMT-2020)** |
|:---|:---|:---|
| 최고 전송속도 / 지연 | 연구 목표 50~200Gbps / 0.1~1ms | 최고 20Gbps / 1ms URLLC |
| 핵심 주파수 대역 | Sub-THz (100GHz ~ 3THz) | Sub-6GHz (3.5GHz) / mmWave (28GHz) |
| 커버리지 영역 | 3차원 입체망 (지상 + 저궤도 위성 NTN) | 2차원 지상 셀 중심 커버리지 (육상 한정) |
| 특화 신기술 | ISAC (통신+센싱), RIS (전파 제어), AI-Native | eMBB, URLLC, mMTC, Network Slicing |
| 지능화 수준 | 코어/무선 전 구간 AI 완전 내재화 (AI-Native) | AI 기반 동적 자원 스케줄링 부분 적용 |

> 요약: IMT-2030은 향상 통신과 센싱•AI•커버리지를 연구한다.

#### 한줄 요약

- IMT-2030은 ISAC•AI•NTN을 후보 역량으로 확장

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **수동 복구(Manual Fallback)**: AI 제어 알고리즘이나 위성 연결 오작동 시 안전한 기본 제어 파라미터나 지상망으로 라우팅을 즉시 전환하는 비상 복구 메커니즘이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| Sub-THz 극심한 대기 감쇄 | 100GHz 이상 전파의 대기 수분 흡수 및 직진성 강함 | 건물 외벽 RIS 메타표면 억제 배치 및 초고밀도 셀 | 전파 장애물 우회 회절 및 초광대역 품질 보장 |
| AI-Native 블랙박스 오판 | 딥러닝 기반 무선 제어 시 예외 채널 환경에서 오작동 | Rule-based 경계 파라미터 검증 및 Manual Fallback | 망 멜트다운 방지 및 운용 안정성 확보 |
| 저궤도 위성 핸드오버 지연 | LEO 위성의 고속 이동에 따른 기지국 핸드오버 빈번 | 위성 궤도 예측 기반 사전 무손실 Seamless 핸드오버 | 위성 통신 수용 시 데이터 끊김 현상 제거 |
| 표준화 미확정 리스크 | 3GPP 6G 표준(Rel-21~) 미확정 상태의 조기 선점 위험 | IMT-2030 표준 가이드라인 준수 및 가상화 SW 구현 | 미성숙 기술 도입에 따른 투자 손실 예방 |

#### 한줄 요약

- RIS 반사판 초밀도 배치, AI 오판 방지 Fallback 메커니즘 구축, 지상-위성(NTN) Doppler 궤도 보정을 통해 6G 기술 안정성 제어.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **단계 도입(Phased Deployment Strategy)**: IMT-2030 시나리오별 기술 성숙도(TRL) 검증을 거쳐 검증된 요소 기술부터 단계적으로 망에 적용하는 전략이다.

</details>

- 상용 도입 전 **IMT-2030 표준•TRL**을 검증해 단계 적용

#### 한줄 요약

- IMT-2030 시나리오별 기술 성숙도 평가 및 지상-비지상(NTN) 통합 체계 단계별 도입 필수.
