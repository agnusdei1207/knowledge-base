---
title: 57. 전가상화 (Full Virtualization) - 이진 변환 (Binary Translation)
date: '2026-03-21'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 전가상화(Full [[190_virtualization_computing_architecture_cloud|Virtualization]])는 [[054_hypervisor|하이퍼바이저]]([[054_hypervisor|Hypervisor]])가 물리 하드웨어를 완전히 흉내 내어, 게스트 [[001_operating_system_purpose|운영체제]](Guest [[001_operating_system_purpose|Operating System]])를 수정 없이 실행하게 만드는 방식이다.
> 2. **가치**: 레거시 [[001_operating_system_purpose|운영체제]]를 그대로 올릴 수 있어 [[344_compatibility_usability|호환성]]이 높지만, 특권 명령 처리 과정에서 [[282_performance_tactics|성능]] 오버헤드가 생긴다.
> 3. **판단 포인트**: 이진 변환(Binary Translation), [[677_trap_based_system_call_implementation|트랩]] 앤 에뮬레이트([[677_trap_based_system_call_implementation|Trap]] and Emulate), [[059_hardware_assisted_virtualization|하드웨어 보조 가상화]]([[021_hardware_assisted_virtualization|Hardware-assisted Virtualization]])의 차이를 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

전가상화는 [[001_operating_system_purpose|운영체제]]를 수정하지 않고도 가상 환경에서 그대로 돌리기 위한 기술이다. 기업이 오래된 [[001_operating_system_purpose|운영체제]]를 폐기하지 않고 새 서버로 옮길 때 특히 유용하다.

게스트 [[001_operating_system_purpose|운영체제]]는 자신이 가상 환경에 있다는 사실을 몰라도 된다. 그래서 기존 소프트웨어를 거의 손대지 않고 이전할 수 있다.

- **📢 섹션 요약 비유**: 전가상화는 원래 집의 구조를 그대로 두고, 안에 보이지 않는 복층을 하나 더 만드는 일이다.

---

## Ⅱ. 기본 구조와 CPU 링 동작

[[015_virtualization|가상화]]에서는 [[054_hypervisor|하이퍼바이저]]가 중간에서 모든 자원을 조정한다.

```text
Application
   ↓
Guest OS
   ↓  특권 명령 시도
Hypervisor
   ↓
Physical Hardware
```

전통적인 x86 환경에서는 특권 명령을 가로채기 어려운 경우가 있어, [[054_hypervisor|하이퍼바이저]]가 실행 코드를 바꾸거나 [[677_trap_based_system_call_implementation|트랩]]을 처리해야 했다.

- **📢 섹션 요약 비유**: 통역사가 말끝마다 대신 확인해 주는 구조라서, 손님은 직접 기계를 만지지 않아도 된다.

---

## Ⅲ. 이진 변환과 [[677_trap_based_system_call_implementation|트랩]] 처리

이진 변환(Binary Translation)은 게스트 [[001_operating_system_purpose|운영체제]]의 실행 코드를 검사해 문제 되는 명령을 [[054_hypervisor|하이퍼바이저]] 호출로 바꾸는 방식이다.

이 방식은 [[344_compatibility_usability|호환성]]을 높이지만 실행 중에 추가 작업이 들어가므로 [[282_performance_tactics|성능]] 손실이 생긴다. 특권 명령이 많을수록 오버헤드가 커진다.

- **📢 섹션 요약 비유**: 원고를 인쇄하기 전에 자동 교정기가 문장을 하나씩 바꿔 적는 느낌이다.

---

## Ⅳ. [[059_hardware_assisted_virtualization|하드웨어 보조 가상화]]와 개선

현대 CPU는 Intel VT-x나 [[659_amd_v|AMD-V]] 같은 [[059_hardware_assisted_virtualization|하드웨어 보조 가상화]]를 제공해 전가상화의 부담을 크게 줄였다.

이 기능은 [[054_hypervisor|하이퍼바이저]]가 특권 명령을 더 직접적으로 처리하게 해 주며, 이전보다 빠르고 안정적인 격리를 가능하게 한다.

- **📢 섹션 요약 비유**: 수동으로 확인하던 통역에 자동 번역기가 더해져 훨씬 빨라진 셈이다.

---

## Ⅴ. 실무 적용과 비교

전가상화는 [[344_compatibility_usability|호환성]]이 중요할 때 강하다. 오래된 서버, 상용 [[001_operating_system_purpose|운영체제]], 수정 불가능한 게스트 환경에 적합하다.

반면 [[282_performance_tactics|성능]]이 가장 중요한 워크로드라면 [[058_paravirtualization|반가상화]]([[192_full_virtualization_vs_para_virtualization|Para-virtualization]])나 다른 경량화 방식과 비교해야 한다. 전가상화는 "그대로 올린다"는 장점과 "그 대가로 비용이 든다"는 단점을 함께 가진다.

- **📢 섹션 요약 비유**: 낡은 자동차를 그대로 실어 나를 수는 있지만, 그만큼 운반 장비가 더 필요하다.

---

## 관련 개념 맵

```text
게스트 운영체제
   ↓
하이퍼바이저
   ↓
이진 변환 / 트랩 처리
   ↓
하드웨어 보조 가상화
```

---

## 관련 키워드 및 발전 흐름도

1. 특권 명령 문제 → [[459_quic_fec_forward_error_correction|초기]] x86 [[015_virtualization|가상화]]의 핵심 난제
2. 이진 변환(Binary Translation) → [[344_compatibility_usability|호환성]] 확보
3. [[677_trap_based_system_call_implementation|트랩]] 앤 에뮬레이트([[677_trap_based_system_call_implementation|Trap]] and Emulate) → 가상 장치 처리
4. VT-x / [[659_amd_v|AMD-V]] → [[059_hardware_assisted_virtualization|하드웨어 보조 가상화]]의 확산
5. 클라우드 인프라 → [[015_virtualization|가상화]] 기반 데이터센터의 표준화

---

## 어린이를 위한 3줄 비유 설명

전가상화는 다른 나라 말을 하는 손님을 대신 통역해 주는 호텔 같아요.  
손님은 원래 하던 말을 그대로 하면 되고, 통역사가 알아서 기계와 이야기해요.  
그래서 낡은 프로그램도 새 컴퓨터에서 그대로 돌아갈 수 있어요.
