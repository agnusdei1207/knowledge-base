---
sidebar:
  order: 151
  label: "151. VM vs 컨테이너 비교 (VM vs Container)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "VM vs 컨테이너 비교 (VM vs Container)"
date: "2026-08-14T01:56:00+09:00"
tags: ["notes-software"]
weight: 151
extra:
  question_no: "151"
  source_status: "기출"
  source_history: "128회, 131회, 132회, 137회"
  priority: 70
  priority_note: "가상머신•컨테이너 격리 비교가 반복 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **가상머신(VM, Virtual Machine)**: 하이퍼바이저(Hypervisor)가 하드웨어를 추상화하여 게스트 OS(Guest OS)를 독립적으로 실행하는 하드웨어 가상화 기술.
- **컨테이너(Container)**: 호스트 OS(Host OS) 커널을 공유하며 리눅스 cgroups(Control Groups) 및 Namespaces(네임스페이스)를 통해 프로세스 수준에서 격리하는 가상화 기술.
- **하이퍼바이저(Hypervisor)**: 물리적 자원을 가상화하여 다수의 Guest OS가 하드웨어를 공유하도록 제어하는 가상화 엔진.

</details>

- 정의/개념: Guest Kernel 분리 VM과 Host Kernel 공유 **Container 비교**
- 배경/필요성: **격리 강도•배포 밀도** 상충으로 실행 경계 선택 필요

#### 한줄 요약

- VM은 하드웨어 단위, 컨테이너는 커널 공유 기반 프로세스 단위 격리로 성능과 격리 강도 차이 발생.

## Ⅱ. 특징

- **VM**은 Guest Kernel별 격리와 이종 OS 실행 지원
- **Container**는 Host Kernel 공유로 빠른 시작•고밀도 배치
- **격리 경계•운영 오버헤드**가 상호 절충 관계

#### 한줄 요약

- 커널 경계를 나누는 VM과 커널을 공유하는 컨테이너는 격리와 효율의 기준이 다르다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **하이퍼바이저 vs 도커 엔진(Hypervisor vs Docker Engine)**: VM은 하이퍼바이저(Hypervisor)가 가상 하드웨어를 생성, 컨테이너는 도커 엔진(Docker Engine)이 커널 cgroups/Namespaces를 제어.

</details>

```text
┌────────────────────────────────────────┬──────────────────────────────────────────┐
│           가상머신 아키텍처             │            컨테이너 아키텍처              │
├────────────────────────────────────────┼──────────────────────────────────────────┤
│ 애플리케이션 A │ 애플리케이션 B          │ 애플리케이션 A   │ 애플리케이션 B         │
│ 라이브러리     │ 라이브러리              │ 라이브러리       │ 라이브러리             │
│ 게스트 OS      │ 게스트 OS               │ 컨테이너 엔진(그룹제어/이름공간)        │
│ 하이퍼바이저                            │ 호스트 OS (리눅스 커널)                  │
│ 물리 하드웨어 인프라                   │ 물리 하드웨어 인프라                     │
└────────────────────────────────────────┴──────────────────────────────────────────┘
```

| 구성요소 | 책임 |
|---|---|
| 애플리케이션•라이브러리 | 실행 코드와 **사용자 공간 의존성** 제공 |
| Guest OS•컨테이너 엔진 | VM별 Kernel 또는 **Process 격리** 제공 |
| Hypervisor•Host OS | 가상 Hardware 또는 **공유 Kernel** 제공 |
| 물리 Hardware | CPU•Memory•Storage•Network 자원 제공 |

#### 한줄 요약

- VM은 Guest OS 계층을 반복하고 컨테이너는 Host Kernel 위에서 사용자 공간만 나눈다.

## Ⅳ. 흐름도

- **시동 지연**: VM은 BIOS/OS 로딩으로 수 분 소요, 컨테이너는 `execve()` 시스템 콜로 수 밀리초(ms) 단위 즉시 실행.

```text
[실행 요청]
      │
1. 격리 요구 판정
      │
2. 실행 모델 선택
 ┌────┴──────────────┐
 │ VM                │ Container
3. 가상 환경 생성    3. 격리 환경 생성
4. Guest OS 시작     4. Image Mount
 └────┬──────────────┘
5. Application 실행
```

### 동작 원리

1. **격리 요구 판정**: Kernel 경계•OS 호환성 확인
2. **실행 모델 선택**: VM 또는 Container 결정
3. **가상•격리 환경 생성**: 가상 Hardware 또는 Namespace 구성
4. **Guest OS 시작•Image Mount**: 선택 모델의 실행층 준비
5. **Application 실행**: Guest 또는 Host Kernel에서 Process 시작

#### 한줄 요약

- VM은 OS를 시작하고 컨테이너는 기존 Kernel 위에 격리 환경과 Process를 만든다.

## Ⅴ. 종류 및 비교

- **카타 컨테이너 / 파이어크래커(Kata Containers / Firecracker)**: 컨테이너의 고속 부팅과 VM의 커널 격리 장점을 융합한 MicroVM / Secure Container 기술.

| 비교 기술 | Pure VM | Pure Container | Secure Container |
|:---|:---|:---|:---|
| 격리 경계 | Hypervisor/Guest OS | Host Kernel | MicroVM Hypervisor |
| 시작 비용 | Guest OS 기동 비용 | Process 기동 중심 | MicroVM 기동 비용 |
| 보안 수준 | Guest Kernel 격리 | Host Kernel 공유 | MicroVM Kernel 격리 |
| 도메인 | 금융 코어 | 일반 MSA | AWS Lambda, SaaS |

#### 한줄 요약

- Secure Container는 컨테이너 운영 모델에 MicroVM Kernel 경계를 결합한다.

## Ⅵ. 실무 고려사항 및 대책

- **멀티테넌트 보안 위협**: 이종 고객을 동일 호스트에서 구동 시 커널 분리가 가능한 VM 사용 필수.

| 3대 구축 의사결정 상황 | 최적 추천 아키텍처 기술 | 선택 사유 및 실무 대책 |
|:---|:---|:---|
| 1. 멀티테넌트 SaaS 보안 | **VM 또는 Kata Containers** | 테넌트별 Kernel 경계 확보 |
| 2. K8s 수평 오토스케일링 | **Docker Container** | 빠른 복제와 고밀도 배치 |
| 3. Windows 레거시 SW | **VM (Windows Guest OS)** | Linux Host 커널에서 Windows SW 구동 불가 |

> 사례: **AWS Lambda (Firecracker MicroVM 사용) 및 쿠팡 / 당근마켓 K8s Container 혼용**

#### 한줄 요약

- 신뢰 경계•OS 호환성•확장 속도를 함께 평가해 실행 격리를 선택한다.

## Ⅶ. 결론

- Kernel 신뢰 경계는 **VM**, 동일 Kernel 고밀도 배포는 Container 선택

#### 한줄 요약

- 커널을 분리해야 하면 VM, 공유해도 되는 짧은 수명 서비스는 컨테이너를 선택한다.
