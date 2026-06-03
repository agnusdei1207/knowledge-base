+++
title = "56. 호스트드 하이퍼바이저 (Hosted Hypervisor)"
date = 2026-05-01

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 호스트드 하이퍼바이저는 호스트 OS 위에서 동작하는 Type 2 하이퍼바이저다.
> 2. **가치**: 설치와 사용이 쉽고 개발/테스트 환경에 적합하다.
> 3. **판단 포인트**: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 격리성은 베어메탈(Type 1)보다 약할 수 있다.

---

## Ⅰ. 개요 및 필요성

호스트드 하이퍼바이저는 이미 설치된 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 위에서 VM을 실행한다. 데스크톱 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)와 실습 환경에서 많이 쓰인다.

쉽게 시작할 수 있다는 것이 큰 장점이다.

- **📢 섹션 요약 비유**: 호스트드 하이퍼바이저는 기존 집 안에 서브룸을 만드는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

호스트 OS가 기본 자원을 관리하고, 그 위에서 하이퍼바이저가 VM을 실행한다. 따라서 호스트 OS의 드라이버와 스케줄링 영향을 받는다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Physical HW</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Host OS</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Hosted Hypervisor</div>
<div class="kb-diagram-tree-item" style="--depth:1">VM1</div>
<div class="kb-diagram-tree-item" style="--depth:1">VM2</div>
</div>
</div>



| 요소 | 역할 | 포인트 |
| :--- | :--- | :--- |
| Host OS | 기본 운영 | 드라이버 |
| [Hypervisor](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) | [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 실행 | Type 2 |
| [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) | 격리 환경 | 개발/테스트 |

핵심은 호스트 OS가 중간층으로 존재해 설치와 관리가 편하지만, 그만큼 오버헤드가 생긴다는 점이다.

- **📢 섹션 요약 비유**: 호스트드 하이퍼바이저는 큰 건물 안에 임시 칸막이를 세우는 것이다.

---

## Ⅲ. 비교 및 연결

호스트드 하이퍼바이저는 베어메탈보다 가볍고, 개인용/실습용에 적합하다. 반대로 대규모 서버 운영에는 Type 1이 더 적합하다.

| 항목 | Hosted | Bare Metal |
| :--- | :--- | :--- |
| 설치 | 쉬움 | 전문적 |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 중간 | 높음 |
| 용도 | 데스크톱/실습 | 서버/클라우드 |

대표적으로 VirtualBox, VMware Workstation 같은 도구가 있다.

- **📢 섹션 요약 비유**: 호스트드는 가정용 연습장, 베어메탈은 경기장이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 편의성, [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/), [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 호스트 OS 의존성을 함께 본다. 개발/실습에서는 충분하지만 운영에는 한계가 있다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 사용 목적이 개발/테스트인가?
2. 호스트 OS 자원에 의존하는가?
3. [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 요구가 높지 않은가?
4. 장치 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)이 필요한가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 운영 서버를 hosted만으로 책임지려는 경우
- 호스트 OS 업데이트 영향을 무시하는 경우
- [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 요구를 과소평가하는 경우

기술사 관점에서는 hosted hypervisor가 접근성과 편의성을 제공하지만, 서버급 안정성은 bare metal에 미치지 못한다는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: 호스트드는 쉬운 연습 도구지만, 무거운 배를 끄는 데는 부족할 수 있다.

---

## Ⅴ. 기대효과 및 결론

호스트드 하이퍼바이저는 빠른 시작과 쉬운 사용성을 제공한다. 학습과 검증에 특히 유용하다.

정리하면, 이미 있는 OS 위에 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 계층을 얹는 방식이다.

- **📢 섹션 요약 비유**: 호스트드는 이미 있는 책상 위에 작은 책상을 하나 더 놓는 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Host OS | 기반 |
| Type 2 | [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) | 실행 환경 |
| Driver | 장치 지원 |
| Developer Tools | 활용 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">물리 하드웨어</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">호스트 OS</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Hosted Hypervisor</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">가상 머신</div>
</div>
</div>



이 흐름은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 위에 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 계층을 얹는 구조를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 호스트드 하이퍼바이저는 이미 있는 집 안에 작은 방을 만드는 거예요.
2. 만들기 쉽고 바로 써 볼 수 있어요.
3. 하지만 아주 큰 일엔 좀 약할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 56 / 800

← **이전**: [55. 베어메탈 하이퍼바이저 (Bare Metal Hypervisor)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/055_bare_metal_hypervisor/)
**다음**: [57. 전가상화 (Full Virtualization) - 이진 변환 (Binary Translation)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) →

---
