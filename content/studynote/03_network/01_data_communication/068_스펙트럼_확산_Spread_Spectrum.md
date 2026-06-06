---
title: "Spread Spectrum"
date: "2024-05-24"
description: "전송 신호의 대역폭을 의도적으로 넓혀 잡음 강인성과 보안성을 확보하는 통신 기술"
tags:
  - "network"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스펙트럼 확산은 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 대역을 넓게 퍼뜨려 잡음과 간섭에 강하게 만드는 기법이다.
> 2. **가치**: 통신 품질, [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/), 다중 사용자 공존을 높이는 데 유리하다.
> 3. **판단**: DSSS와 [FHSS](/studynote/03_network/19_frequent_topics_terms/955_fhss_frequency_hopping_spread_spectrum_bluetooth/) 같은 대표 방식의 차이를 이해해야 실제 적용을 설명할 수 있다.

---

## Ⅰ. 개요 및 필요성

좁은 대역에 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 몰아넣으면 잡음과 간섭에 약해진다. 스펙트럼 확산은 이를 의도적으로 넓혀 대응한다.

그래서 군용 통신, [CDMA](/studynote/03_network/19_frequent_topics_terms/957_cdma_code_division_multiple_access_dsss_orthogonality/), 무선 보안에 자주 쓰였다.

- **📢 섹션 요약 비유**: 한 줄로 몰려 있던 사람들을 넓은 운동장에 흩어 놓는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Data Signal
  v
Spreading Code / Hop Pattern
  v
Wideband Transmission
  v
Receiver Despreading
```

| 방식 | 특징 |
| :-- | :-- |
| [DSSS](/studynote/03_network/19_frequent_topics_terms/956_dsss_direct_sequence_spread_spectrum_chipping_code/) | 코드로 [직접 확산](/studynote/03_network/19_frequent_topics_terms/956_dsss_direct_sequence_spread_spectrum_chipping_code/) |
| [FHSS](/studynote/03_network/19_frequent_topics_terms/955_fhss_frequency_hopping_spread_spectrum_bluetooth/) | 주파수를 빠르게 이동 |

스펙트럼 확산은 수신 측에서 같은 코드나 패턴으로 다시 모아야 원래 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 복원할 수 있다. 그래서 간섭과 [도청](/studynote/03_network/14_network_security_threats/701_sniffing_eavesdropping_promiscuous/)에 더 강하다.

- **📢 섹션 요약 비유**: 흩뿌린 퍼즐 조각을 같은 지도에서 다시 모으는 일이다.

---

## Ⅲ. 비교 및 연결

| 방식 | 장점 | 단점 |
| :-- | :-- | :-- |
| [DSSS](/studynote/03_network/19_frequent_topics_terms/956_dsss_direct_sequence_spread_spectrum_chipping_code/) | 간섭에 강함 | 코드 동기 필요 |
| [FHSS](/studynote/03_network/19_frequent_topics_terms/955_fhss_frequency_hopping_spread_spectrum_bluetooth/) | [도청](/studynote/03_network/14_network_security_threats/701_sniffing_eavesdropping_promiscuous/)/재밍에 강함 | [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 필요 |

| 효과 | 설명 |
| :-- | :-- |
| Noise Immunity | 잡음 저항성 증가 |
| [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) | [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 추적 어려움 |
| [Multiple Access](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) | 사용자 분리 가능 |

스펙트럼 확산은 단순히 넓히는 것이 아니라, 확산 코드와 복호화 규칙을 함께 쓰는 기술이다.

- **📢 섹션 요약 비유**: 소리를 크게 키우는 게 아니라, 넓게 퍼뜨려 찾기 어렵게 만드는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. DSSS와 [FHSS](/studynote/03_network/19_frequent_topics_terms/955_fhss_frequency_hopping_spread_spectrum_bluetooth/) 차이를 설명할 수 있는가?
2. 잡음 강인성과 [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)의 관계를 아는가?
3. [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)의 중요성을 이해하는가?
4. 다중 사용자 환경에 적용 가능한가?
5. [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 증가의 의미를 이해하는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 스펙트럼 확산을 단순한 대역 확장으로만 보는 설계
- 코드 동기를 무시하는 설계
- [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)과 성능을 혼동하는 설계
- 간섭 환경을 고려하지 않는 설계

기술사 관점에서는 스펙트럼 확산을 "잡음에 강한 확산 기반 통신"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 넓게 흩어 놓으면 잡기가 어려워진다.

---

## Ⅴ. 기대효과 및 결론

스펙트럼 확산은 간섭과 잡음에 강하고, [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)도 높이는 데 도움이 된다.

결론적으로 스펙트럼 확산은 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 넓게 퍼뜨려 통신 품질을 높이는 기술이다.

- **📢 섹션 요약 비유**: 넓은 운동장에 흩어진 공을 찾으려면 규칙이 필요하다.

---

## 관련 개념 맵

```text
Data Signal
  v
Spread Spectrum
  v
DSSS / FHSS
  v
Robust Wireless
```

---

## 관련 키워드 및 발전 흐름도

```text
Narrowband
  v
Spread Spectrum
  v
CDMA
  v
Robust Communication
```

---

## 어린이를 위한 3줄 비유 설명

한곳에 몰아두지 않고 넓게 퍼뜨려요.
그래서 찾기 어렵고, 흔들려도 버텨요.
스펙트럼 확산은 그런 통신 방법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 68 / 1120

<- **이전**: [67. 경사 과부하 잡음 (Slope Overload Noise) / 그래뉼러 잡음 (Granular Noise)](/studynote/03_network/01_data_communication/067_경사과부하_그래뉼러_잡음/)
**다음**: [69. 직접 수열 확산 스펙트럼 (DSSS, Direct Sequence Spread Spectrum) - PN 시퀀스](/studynote/03_network/01_data_communication/069_직접_수열_확산_DSSS/) ->

---
