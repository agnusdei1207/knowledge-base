---
title: 60. 컨테이너 가상화 (Container Virtualization) - OS 수준 가상화
date: '2026-03-21'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[561_container_based_deployment|컨테이너]] 가상화는 호스트 [[022_kernel_role|커널]]을 공유하면서 프로세스 단위로 격리하는 OS 수준 가상화다.
> 2. **가치**: VM보다 가볍고 빠르며, 이미지 기반 배포로 환경 일관성을 높인다.
> 3. **판단 포인트**: [[061_namespace|Namespace]], [[062_cgroups|cgroups]], 이미지 레이어, 런타임의 역할을 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

가상 머신은 편하지만 무겁다. 앱 하나를 띄우기 위해 게스트 OS를 함께 올려야 해서 자원 낭비가 생긴다.

[[561_container_based_deployment|컨테이너]]는 같은 [[022_kernel_role|커널]] 위에서 사용자 공간만 분리한다. 그래서 빠르게 뜨고, 빠르게 [[016_replication_factor|복제]]되고, 배포 환경도 맞추기 쉽다.

- **📢 섹션 요약 비유**: 각자 집을 짓는 대신, 같은 건물에서 방만 따로 쓰는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[561_container_based_deployment|컨테이너]]는 Namespace로 보이는 세상을 나누고, cgroups로 쓰는 자원을 제한한다. 이미지 레이어는 필요한 것만 공유해 [[016_replication_factor|복제]] 비용을 줄인다.

```text
App
 ↓
Container Runtime
 ↓
Namespace / cgroups
 ↓
Host OS Kernel
```

| 구성 요소 | 역할 |
| :-- | :-- |
| [[061_namespace|Namespace]] | PID, NET, MNT 등의 격리 |
| [[062_cgroups|cgroups]] | CPU, 메모리, I/O 제한 |
| Image Layer | 읽기 전용 레이어 공유 |
| Runtime | 실제 [[561_container_based_deployment|컨테이너]] 실행 |

[[561_container_based_deployment|컨테이너]]는 사실 호스트 입장에서 하나의 격리된 프로세스에 가깝다. 그래서 부팅 오버헤드가 적고, 같은 이미지를 수백 개라도 빠르게 띄울 수 있다.

- **📢 섹션 요약 비유**: 같은 주방에서 각자 칸막이와 전기 사용량만 따로 관리하는 고효율 식당이다.

---

## Ⅲ. 비교 및 연결

| 항목 | [[598_vm_migration_nic|VM]] | [[561_container_based_deployment|컨테이너]] |
| :-- | :-- | :-- |
| 격리 | 하드웨어 수준 | 프로세스/[[022_kernel_role|커널]] 수준 |
| 부팅 | 느림 | 빠름 |
| 자원 사용 | 큼 | 작음 |
| OS 다양성 | 높음 | 호스트 [[022_kernel_role|커널]]에 종속 |

[[561_container_based_deployment|컨테이너]]는 이식성과 확장성이 좋아 MSA와 [[090_configuration_item|CI]]/CD에 잘 맞지만, [[022_kernel_role|커널]]을 공유하므로 보안 설계가 중요하다. 필요하면 Kata Containers나 gVisor처럼 더 강한 격리 런타임을 쓴다.

- **📢 섹션 요약 비유**: 무거운 트럭 대신 규격 박스를 여러 개 쌓아 빠르게 배송하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[[561_container_based_deployment|컨테이너]]는 [[532_microservices_decomposition_patterns|마이크로서비스]], 오토스케일링, 개발 환경 통일에 강하다. 하지만 상태 데이터와 보안은 별도 설계가 필요하다.

### [[435_checklist_based_testing|체크리스트]]

1. 이미지에 취약한 패키지가 남아 있지 않은가?
2. 상태 데이터는 외부 볼륨으로 분리했는가?
3. [[073_container_orchestration_tools|오케스트레이션]]([[205_kubernetes_container_orchestration|Kubernetes]])이 준비됐는가?
4. [[022_kernel_role|커널]] 취약점에 대한 보안 대책이 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 하나의 [[561_container_based_deployment|컨테이너]]에 DB와 앱을 모두 넣는 설계
- 이미지 재현성 없이 수동 설치만 반복하는 설계
- [[561_container_based_deployment|컨테이너]]를 VM처럼 무겁게 운영하는 설계

- **📢 섹션 요약 비유**: 장난감, 설명서, 배터리를 한 상자에 넣어 어디서든 같은 모습으로 꺼내 쓰는 것이다.

---

## Ⅴ. 기대효과 및 결론

[[561_container_based_deployment|컨테이너]]는 배포를 빠르게 하고, 환경 차이를 줄이며, 인프라 활용도를 높인다. 현대 클라우드 네이티브의 기본 단위가 된 이유다.

결국 [[561_container_based_deployment|컨테이너]]는 "가벼움" 자체보다, 가벼움 덕분에 운영과 배포를 반복 가능하게 만드는 데 의미가 있다.

- **📢 섹션 요약 비유**: 여러 칸의 레고 상자를 잘 정리해 두면 어디서나 같은 작품을 빠르게 다시 만들 수 있다.

---

## 관련 개념 맵

```text
Host OS
   ↓
Namespace / cgroups
   ↓
Container Runtime
   ↓
Container Image
```

---

## 관련 키워드 및 발전 흐름도

```text
VM 기반 가상화
   ↓
OS 수준 가상화
   ↓
Docker / Kubernetes
   ↓
Cloud Native / MSA
```

---

## 어린이를 위한 3줄 비유 설명

[[561_container_based_deployment|컨테이너]]는 한 집 안에서 방만 따로 쓰는 거예요.  
문도 잠그고, 전기도 따로 계산해서 안전하게 지내요.  
그래서 필요한 방을 아주 빨리 만들고 없앨 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 60 / 800

← **이전**: [[059_hardware_assisted_virtualization|59. 하드웨어 보조 가상화 (Intel VT-x, AMD-V)]]
**다음**: [[061_namespace|61. 네임스페이스 (Namespace) - 자원 격리]] →

---
