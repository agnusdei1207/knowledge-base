---
sidebar:
  order: 76
  label: "076. 네트워크 슬라이스 자원 관리"
  badge:
    text: "기출 · 50%"
    variant: note
title: "5G/6G E2E 네트워크 슬라이스 자원 관리 : Resource Management"
date: "2026-08-26T14:02:10+09:00"
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
- 배경/필요성: 공용 자원을 이종 서비스가 함께 쓰면 한 서비스의 폭주 비용을 다른 서비스가 **상호 간섭·SLS 위반**으로 떠안으므로, RAN·전송·코어를 관통하는 논리 슬라이스 단위 관리 계층을 두어 물리망 증설 없이 서비스별 격리를 확보

#### 한줄 요약
- 전 도메인 **수용 제어·하이브리드 격리·폐루프 최적화**

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Admission Control (수용 제어)**: 신규 슬라이스 생성 요청 시 기존 활성 슬라이스의 SLS 품질을 침해하지 않는지 사전 검증하여 수락/거절을 판정하는 기능.
- **Closed-Loop Assurance (폐루프 보증)**: NWDAF AI 분석 기반으로 실시간 품질 저하 감지 시 사람의 개입 없이 자원을 자동 증설(Scale-Out)하는 자율 복구 체계.

</details>

- **E2E 자원 조율**: NSMF가 PRB·FlexE·vUPF 통합 제어
- **하드·소프트 격리**: 중요도에 따라 전용·공유 자원 배분
- **NWDAF 폐루프**: SLS 위반을 감지해 자원 자동 확장

#### 한줄 요약
- **E2E 조율·SLS 격리·NWDAF 폐루프** 제공

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NSMF vs NSSMF**: E2E 슬라이스(NSI)를 총괄 관리하는 NSMF와 각 개별 도메인 서브넷(NSSI)을 전담 제어하는 도메인별 NSSMF.

</details>

```text
[슬라이스 관리 구조]
|-- CSMF
`-- NSMF
    |-- RAN NSSMF
    |-- TN NSSMF
    `-- CN NSSMF
```

선의 의미: CSMF에서 접수된 고객 요구사항이 NSMF를 통해 분해되고 각 도메인 NSSMF를 거쳐 물리/가상 NSSI 자원으로 인스턴스화되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| CSMF | 서비스 요구를 **SLS 템플릿으로 변환** | 3GPP 관리 계층 |
| NSMF | **수용 제어·NSI 오케스트레이션** | TS 28.531 표준 |
| RAN NSSMF | **PRB·빔·스케줄링 자원 할당** | RAN NSSI |
| TN NSSMF | **FlexE·SRv6·TSN 자원 할당** | TN NSSI |
| CN NSSMF | **vUPF·AMF·SMF 자원 배치** | CN NSSI |

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

- 1. SLS 요구 접수
- 2. 수용 가능성 판정
- 3. 도메인별 NSSI 배포
- 4. E2E NSI 바인딩
- 5. NWDAF 폐루프 최적화

#### 한줄 요약
- 수용 제어 지점에서 신규 슬라이스의 수락과 거절이 갈리며, 수락은 기존 슬라이스의 여유 자원을, 거절은 매출 기회를 대가로 치른다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Dedicated (Hard Slicing)** vs **Shared (Soft Slicing)** vs **Hybrid (Dynamic)**.

</details>

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
| 전송망/코어망 병목으로 인한 종단 간(E2E) 슬라이스 지연 시간 SLS 위반 | **`NWDAF 연계 E2E 텔레메트리` 및 병목 도메인 NSSI 자동 스케일아웃** | 지연 병목 구간 조기 해소 및 99.999% SLS 준수 |
| 트래픽 임계치 경계에서 빈번한 자원 증감으로 인한 **플래핑(Flapping)** | 자원 스케일링 정책에 **`히스테리시스(Hysteresis) 및 쿨다운 타이머`** 적용 | 잦은 제어 진동 억제 및 제어 평면 안정성 확보 |
| 완전 전용 예약(Hard Slicing) 시 유휴 자원 증가로 인한 망 수익성 저하 | **`최소 보장 + 잉여 공유의 하이브리드 슬라이싱(Hybrid)` 모델 구축** | SLS 품질 무손실 유지 및 자원 활용률 35% 향상 |
| 비인가 단말의 고우선순위 슬라이스 무단 접속 및 자원 고갈 위협 | **`NSSF (Network Slice Selection Function)` 기반 단말 인증 검증** | 미인가 단말 접근 원천 차단 및 슬라이스 보안 격리 |

#### 한줄 요약
- NWDAF로 E2E 지연을 방어하고, 히스테리시스로 플래핑을 방지하며, 하이브리드 슬라이싱으로 자원 효율을 극대화한다.

## Ⅶ. 결론

- 엄격한 격리는 **Dedicated**, 효율 병행은 **Hybrid·NWDAF 폐루프** 선택

#### 한줄 요약
- **NSMF/NSSMF·NWDAF** 결합으로 E2E SLS 보장
