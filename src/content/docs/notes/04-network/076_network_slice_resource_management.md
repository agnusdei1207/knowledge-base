---
sidebar:
  order: 76
  label: "076. 네트워크 슬라이스 자원 관리"
  badge:
    text: "기출 · 50%"
    variant: note
title: "5G/6G E2E 네트워크 슬라이스 자원 관리 : Resource Management"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-network"
weight: 76
extra:
  question_no: "76"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "3GPP 수용 제어(Admission Control), NSI/NSSI 라이프사이클 오케스트레이션 및 SLS 보증"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **NSI (Network Slice Instance)**: RAN, TN, CN 전 도메인의 물리/가상 자원을 결합하여 특정 SLS를 보장하는 종단간 가상 독립망.
- **NSSI (Network Slice Subnet Instance)**: NSI를 구성하는 도메인별(RAN NSSI, TN NSSI, CN NSSI) 독립 자원 단위.

</details>

- 정의/개념: RAN·TN·CN 자원을 **수용 제어·격리**하는 관리 기술
- 배경/필요성: 단일 물리 5G/6G 인프라 위에서 초고속(eMBB), 초저지연(URLLC), 대규모 사물인터넷(mMTC) 등 요구사항이 극단적으로 상이한 이종 서비스들이 공존하는 환경에서, 공용 자원을 단순 공유할 경우 특정 서비스의 트래픽 폭주가 미션 크리티컬 서비스의 자원을 침범하여 종단간 서비스 수준 계약(SLS: Service Level Specification)을 파기하는 한계를 극복하기 위해, RAN(기지국), TN(전송망), CN(코어망) 전 도메인에 걸쳐 가상 자원을 논리적으로 분할하고 오케스트레이션하는 3GPP 표준(TS 28.531) 기반의 네트워크 슬라이스 자원 관리(NSMF/NSSMF) 및 수용 제어(Admission Control)를 도입하여 물리망 증설 없는 다중 독립 가상망 제공, 도메인 간 완벽한 트래픽 보안·성능 격리(Hard/Soft Slicing) 및 SLS 99.999% 보증을 달성할 필요

#### 한줄 요약
- 전 도메인 수용 제어·하이브리드 격리·폐루프 최적화

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Admission Control (수용 제어)**: 신규 슬라이스 생성 요청 시 기존 활성 슬라이스의 SLS 품질을 침해하지 않는지 사전 검증하여 수락/거절을 판정하는 기능.
- **Closed-Loop Assurance (폐루프 보증)**: NWDAF AI 분석 기반으로 실시간 품질 저하 감지 시 사람의 개입 없이 자원을 자동 증설(Scale-Out)하는 자율 복구 체계.

</details>

- E2E 자원 조율: NSMF가 PRB·FlexE·vUPF 통합 제어
- 하드·소프트 격리: 중요도에 따라 전용·공유 자원 배분
- NWDAF 폐루프: SLS 위반을 감지해 자원 자동 확장

#### 한줄 요약
- E2E 조율·SLS 격리·NWDAF 폐루프 제공

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NSMF vs NSSMF**: E2E 슬라이스(NSI)를 총괄 관리하는 NSMF와 각 개별 도메인 서브넷(NSSI)을 전담 제어하는 도메인별 NSSMF.

</details>

```text
[슬라이스 관리 체계]
  ├── [서비스 계층] ─────── [CSMF (서비스 관리)]
  │                           │
  ├── [총괄 관리] ───────── [NSMF (E2E 슬라이스)]
  │                           │
  └── [도메인 제어] ─────── [NSSMF 계층]
        ├── [무선망] ─────── [RAN NSSMF (PRB)]
        ├── [전송망] ─────── [TN NSSMF (SRv6/TSN)]
        └── [코어망] ─────── [CN NSSMF (vUPF)]
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| CSMF | 고객 서비스 요구를 표준 SLS 템플릿으로 변환 관리 |
| **NSMF** | 수용 제어 및 도메인 통합 E2E NSI 라이프사이클 오케스트레이션 |
| RAN NSSMF | 무선 기지국의 PRB, 빔포밍 및 스케줄링 자원 할당 (RAN NSSI) |
| TN NSSMF | 전송망의 FlexE, SRv6, TSN 대역폭 및 지연 보증 자원 할당 (TN NSSI) |
| CN NSSMF | 5G 코어망의 vUPF, AMF, SMF 가상화 인스턴스 자원 배치 (CN NSSI) |

#### 한줄 요약
- NSMF가 고객 요구와 도메인별 NSSMF 사이에 놓여 E2E SLS를 도메인 자원 할당으로 번역하므로, 각 도메인은 전체 서비스 맥락을 알지 못해도 자기 몫만 집행한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **NWDAF (Network Data Analytics Function)**: 3GPP 5G 코어의 AI/ML 기반 데이터 분석 기능으로 슬라이스 부하 및 비정상 트래픽을 실시간 예측.

</details>

```text
서비스 요청
    |
1. SLS 요구 접수
    |
2. 수용 가능성 판정
    +-- 부족: 거부·재협상
    |
3. 도메인별 NSSI 배포
    |
4. E2E NSI 바인딩
    |
5. NWDAF 폐루프 최적화
    |
SLS 보장 결과
```

#### 한줄 요약
- 수용 제어 지점에서 신규 슬라이스의 수락과 거절이 갈리며, 수락은 기존 슬라이스의 여유 자원을, 거절은 매출 기회를 대가로 치른다.

## Ⅴ. 종류 및 비교


| 비교 항목 | 완전 전용 할당 (Dedicated / Hard) | 완전 공유 할당 (Shared / Soft) | 하이브리드 할당 (Hybrid Dynamic) |
|:---|:---|:---|:---|
| 자원 배분 메커니즘 | **물리 자원 영구 독점** | 가중치 기반 **통계적 공유** | **최소 전용·잉여 공유** |
| SLS 품질 보장 | **결정론적 보장** | 폭주 시 위반 가능 | **최소 SLS 보장** |
| 인프라 자원 효율 | **낮음** | **매우 높음** | **높음** |
| 구현 복잡도 | 낮음 | 중간 | **높음** |
| 주요 적용 서비스 | URLLC | mMTC·일반 웹 | **기업망·프리미엄 eMBB** |

#### 한줄 요약
- **Dedicated는 격리**, Shared는 효율, Hybrid는 절충

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Resource Flapping (자원 플래핑)**: 트래픽이 임계치 부근에서 미세하게 진동할 때 자원 할당과 회수가 급격히 반복되어 시스템 오버헤드가 발생하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 전송망/코어망 병목으로 인한 종단 간(E2E) 슬라이스 지연 시간 SLS 위반 | NWDAF 연계 E2E 텔레메트리 및 병목 도메인 NSSI 자동 스케일아웃 | 지연 병목 구간 조기 해소 및 99.999% SLS 준수 |
| 트래픽 임계치 경계에서 빈번한 자원 증감으로 인한 **플래핑(Flapping)** | 자원 스케일링 정책에 히스테리시스(Hysteresis) 및 쿨다운 타이머 적용 | 잦은 제어 진동 억제 및 제어 평면 안정성 확보 |
| 완전 전용 예약(Hard Slicing) 시 유휴 자원 증가로 인한 망 수익성 저하 | 최소 보장 + 잉여 공유의 하이브리드 슬라이싱(Hybrid) 모델 구축 | SLS 품질 무손실 유지 및 자원 활용률 35% 향상 |
| 비인가 단말의 고우선순위 슬라이스 무단 접속 및 자원 고갈 위협 | NSSF (Network Slice Selection Function) 기반 단말 인증 검증 | 미인가 단말 접근 원천 차단 및 슬라이스 보안 격리 |

#### 한줄 요약
- NWDAF로 E2E 지연을 방어하고, 히스테리시스로 플래핑을 방지하며, 하이브리드 슬라이싱으로 자원 효율을 극대화한다.

## Ⅶ. 결론

- 5G Standalone(SA) 코어망의 본격 상용화와 함께 자율주행, 스마트 팩토리, 원격 의료 등 버티컬 산업별 맞춤형 전용망을 구축하는 차세대 통신사 B2B 비즈니스 모델 및 네트워크 가상화의 핵심 인프라 기술로 확립되었으며, 향후 6G AI-Native 기반 제로 터치 자율 오케스트레이션으로 진화하는 가운데, 실무 슬라이스 망 운영 시에는 신규 슬라이스 유입 시 기존 슬라이스의 품질 파괴를 방지하는 수용 제어(Admission Control) 필수 적용, 유휴 자원 낭비를 줄이면서 최소 SLS를 방어하는 하이브리드(Dynamic Hybrid) 격리 모델 채택, 실시간 트래픽 예측 및 자원 자동 증설을 위한 AI 엔진 NWDAF 기반 Closed-Loop 폐루프 오케스트레이션, 비인가 접근을 차단하는 NSSF 단말 인증을 결합하여 완벽한 네트워크 슬라이싱 신뢰성을 완성

#### 한줄 요약
- NSMF/NSSMF·NWDAF 결합으로 E2E SLS 보장
