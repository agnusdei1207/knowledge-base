+++
weight = 69
title = "69. 직접 수열 확산 스펙트럼 (DSSS, Direct Sequence Spread Spectrum) - PN 시퀀스"
description = "PN 시퀀스를 사용하여 데이터를 넓은 대역으로 직접 확산시키는 무선 통신 핵심 원리"
date = "2024-05-24"
[taxonomies]
tags = ["DSSS", "PN Sequence", "CDMA", "확산스펙트럼", "Processing Gain"]
categories = ["데이터통신"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DSSS는 PN 시퀀스로 데이터를 직접 확산해 넓은 대역에 퍼뜨리는 방식이다.
> 2. **가치**: 처리 이득(processing gain)으로 잡음과 간섭에 강해진다.
> 3. **판단**: 송신과 수신이 같은 PN 코드로 [[212_synchronization_mechanisms|동기화]]되어야 복원이 가능하다.

---

## Ⅰ. 개요 및 필요성

좁은 대역 [[130_signal|신호]]는 간섭에 취약하다. DSSS는 데이터를 넓게 퍼뜨려 이를 완화한다.

그래서 [[957_cdma_code_division_multiple_access_dsss_orthogonality|CDMA]] 같은 [[087_다중접속_Multiple_Access|다중 접속]] 기술의 핵심 개념이 된다.

- **📢 섹션 요약 비유**: 작은 점을 넓은 종이에 흩뿌려 찾기 어렵게 만드는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Data
  ↓ XOR / Multiply
PN Sequence
  ↓
Spread Signal
  ↓
Despread with Same PN
```

| 요소 | 역할 |
| :-- | :-- |
| PN Sequence | 의사난수 확산 코드 |
| Spreading | 대역 확장 |
| Despreading | 원 [[130_signal|신호]] 복원 |

DSSS는 송신 측에서 원 [[130_signal|신호]]를 PN 코드로 확산하고, 수신 측에서 같은 코드로 다시 좁혀 복원한다.

- **📢 섹션 요약 비유**: 같은 퍼즐 조각표를 알아야 다시 맞출 수 있다.

---

## Ⅲ. 비교 및 연결

| 방식 | 특징 | 장점 |
| :-- | :-- | :-- |
| [[956_dsss_direct_sequence_spread_spectrum_chipping_code|DSSS]] | 코드 기반 확산 | 처리 이득 |
| [[955_fhss_frequency_hopping_spread_spectrum_bluetooth|FHSS]] | 주파수 점프 | 재밍 회피 |

| 개념 | 의미 |
| :-- | :-- |
| Processing Gain | 잡음 저항성 향상 |
| PN [[082_process_memory_structure|Code]] | 확산/복원 핵심 |

DSSS는 잡음에 강하고, [[212_synchronization_mechanisms|동기화]]가 맞으면 복원이 정확하다.

- **📢 섹션 요약 비유**: 같은 암호문을 알고 있어야 흩어진 글을 다시 모을 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. PN 시퀀스 [[212_synchronization_mechanisms|동기화]]가 가능한가?
2. 처리 이득을 설명할 수 있는가?
3. DSSS와 [[955_fhss_frequency_hopping_spread_spectrum_bluetooth|FHSS]] 차이를 아는가?
4. 다중 사용자 환경에서 활용 가능한가?
5. 잡음/간섭 환경을 고려했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- DSSS를 단순 대역 확장으로 보는 설계
- [[212_synchronization_mechanisms|동기화]] 문제를 무시하는 설계
- PN 코드의 역할을 이해하지 않는 설계
- 보안성과 성능을 혼동하는 설계

기술사 관점에서는 DSSS를 "PN 코드 기반 확산 통신"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 같은 지도 없이는 흩어진 길을 다시 찾기 어렵다.

---

## Ⅴ. 기대효과 및 결론

DSSS는 간섭에 강하고 다중 사용자 환경에서 유리하다. 그래서 무선 통신의 중요한 기초가 된다.

결론적으로 DSSS는 PN 시퀀스로 데이터를 직접 확산하는 방식이다.

- **📢 섹션 요약 비유**: 데이터를 넓게 퍼뜨렸다가 같은 코드로 다시 모은다.

---

## 관련 개념 맵

```text
PN Sequence
  ↓
DSSS
  ↓
Despreading
  ↓
CDMA
```

---

## 관련 키워드 및 발전 흐름도

```text
Spread Spectrum
  ↓
DSSS
  ↓
Processing Gain
  ↓
CDMA
```

---

## 어린이를 위한 3줄 비유 설명

작은 글자를 넓게 퍼뜨려요.  
같은 암호표로 다시 모아요.  
DSSS는 그런 통신 방법이에요.
