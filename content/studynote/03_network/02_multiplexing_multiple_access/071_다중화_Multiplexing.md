+++
title = "71. 다중화 (Multiplexing) 개념 및 특징"
description = "다중화의 본질적 개념, 아키텍처(MUX/DeMUX) 구조, 프로토콜 레이어 융합 및 실무 경제성 분석"
date = 2024-05-20

[taxonomies]
tags = ["network"]

[extra]
tags = ["network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 다중화는 하나의 전송 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)를 여러 신호가 공유하도록 묶는 기술이다.
> 2. **가치**: 회선 효율을 높이고 비용을 줄인다.
> 3. **판단**: MUX와 DeMUX의 역할, 그리고 시간/주파수/파장 분할을 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

전송 자원은 비싸다. 여러 신호가 한 회선을 나눠 쓰면 경제적이다.

다중화는 그런 자원 공유 기술이다.

- **📢 섹션 요약 비유**: 한 도로를 여러 차가 시간표대로 나눠 쓰는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Signals
  ↓ MUX
Single Medium
  ↓ DeMUX
Signals
```

| 방식 | 의미 |
| :-- | :-- |
| TDM | 시간 분할 |
| FDM | 주파수 분할 |
| WDM | 파장 분할 |

MUX는 여러 입력을 합치고, DeMUX는 다시 분리한다. 전송 대역을 효율적으로 나누는 것이 핵심이다.

- **📢 섹션 요약 비유**: 여러 줄 서 있는 사람을 하나의 문으로 통과시키는 느낌이다.

---

## Ⅲ. 비교 및 연결

| 방식 | 기준 | 예 |
| :-- | :-- | :-- |
| TDM | 시간 | 디지털 통신 |
| FDM | 주파수 | 아날로그/무선 |
| WDM | 파장 | 광통신 |

| 장점 | 의미 |
| :-- | :-- |
| Efficiency | 자원 효율 |
| Scalability | 확장성 |

다중화는 네트워크 경제성과 밀접하다. 따라서 물리 계층과 전송 계층의 설계를 함께 본다.

- **📢 섹션 요약 비유**: 시간, 색, 공간으로 길을 나누는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [MUX](/knowledge-base/studynote/03_network/19_frequent_topics_terms/944_mux_demux_multiplexer_demultiplexer_circuit_sharing/)/DeMUX 구조를 아는가?
2. TDM/FDM/WDM 차이를 설명할 수 있는가?
3. 자원 효율을 계산할 수 있는가?
4. [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)/지연을 고려하는가?
5. 전송 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 특성에 맞는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 다중화를 단순 압축으로 보는 설계
- 방식별 차이를 무시하는 설계
- 회선 효율을 고려하지 않는 설계
- 물리 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 특성을 무시하는 설계

기술사 관점에서는 다중화를 "전송 자원을 공유하는 효율화 기법"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 한 길을 여러 사람이 규칙적으로 나눠 쓰는 것이다.

---

## Ⅴ. 기대효과 및 결론

다중화는 회선과 대역 자원의 활용도를 높인다.

결론적으로 다중화는 하나의 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)를 여러 신호가 공유하게 하는 기술이다.

- **📢 섹션 요약 비유**: 길을 같이 쓰되, 규칙은 지켜야 한다.

---

## 관련 개념 맵

```text
MUX
  ↓
Multiplexing
  ↓
DeMUX
  ↓
Shared Medium
```

---

## 관련 키워드 및 발전 흐름도

```text
TDM / FDM / WDM
  ↓
Multiplexing
  ↓
Efficiency
  ↓
Network Resource Sharing
```

---

## 어린이를 위한 3줄 비유 설명

한 길을 같이 써요.
규칙대로 나눠 가요.
다중화는 그런 방법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 71 / 1120

← **이전**: [70. 주파수 도약 확산 스펙트럼 (FHSS, Frequency Hopping Spread Spectrum)](/knowledge-base/studynote/03_network/01_data_communication/070_주파수_도약_확산_FHSS/)
**다음**: [72. 공간 분할 다중화 (SDM, Space Division Multiplexing)](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/072_공간_분할_다중화_SDM/) →

---
