---
title: 70. ASIC (주문형 반도체)
date: '2026-03-19'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ASIC은 특정 용도에 맞게 한 번 설계·제작된 전용 [[009_semiconductor|반도체]]다.
> 2. **가치**: FPGA보다 최적화된 [[282_performance_tactics|성능]]과 전력 효율을 얻을 수 있다.
> 3. **판단**: 유연성은 낮지만 대량 생산과 고성능 요구에 적합하다.

---

## Ⅰ. 개요 및 필요성

범용 칩으로는 [[282_performance_tactics|성능]]과 전력 최적화에 한계가 있다. ASIC은 이런 요구를 해결하기 위해 등장했다.

그래서 모바일 칩, 네트워크 장비, [[190_ai_llm_requirements_specification|AI]] 가속기 등에 쓰인다.

- **📢 섹션 요약 비유**: 맞춤 양복처럼 한 사람에게 딱 맞게 만든 칩이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Specification
  ↓ design
Fabrication
  ↓
Fixed Hardware
```

| 특징 | 의미 |
| :-- | :-- |
| Custom Design | 용도 특화 |
| High [[282_performance_tactics|Performance]] | 최적화 [[282_performance_tactics|성능]] |
| Low Flexibility | 변경 어려움 |

ASIC은 설계가 끝나면 하드웨어가 고정된다. 그래서 개발 [[459_quic_fec_forward_error_correction|초기]] [[395_verification_process_review|검증]]이 매우 중요하다.

- **📢 섹션 요약 비유**: 한번 뜨면 다시 고치기 어려운 도장이다.

---

## Ⅲ. 비교 및 연결

| 구분 | ASIC | [[606_dynamic_partial_reconfiguration|FPGA]] |
| :-- | :-- | :-- |
| [[282_performance_tactics|성능]] | 매우 높음 | 높음 |
| 유연성 | 낮음 | 높음 |
| 비용 | [[459_quic_fec_forward_error_correction|초기]] 높음 | 중간 |

| 사용처 | 예 |
| :-- | :-- |
| 대량 생산 | 모바일 [[131_soc|SoC]] |
| 특수 연산 | [[190_ai_llm_requirements_specification|AI]] 가속 |

ASIC은 대량 생산 시 단가와 [[282_performance_tactics|성능]] 이점이 커진다. 반면 설계 შეც 오류는 수정이 어렵다.

- **📢 섹션 요약 비유**: 공장에서 많이 찍어낼수록 이득이 커지는 도장판이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 대량 생산 수요가 있는가?
2. [[282_performance_tactics|성능]]/전력 최적화가 중요한가?
3. 설계 변경 가능성이 낮은가?
4. [[459_quic_fec_forward_error_correction|초기]] [[395_verification_process_review|검증]]이 충분한가?
5. FPGA와 비교했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 변경 가능성이 큰데 ASIC을 선택하는 설계
- [[395_verification_process_review|검증]] 없이 테이프아웃하는 설계
- 비용/기간을 무시하는 설계
- [[606_dynamic_partial_reconfiguration|FPGA]] 대안을 검토하지 않는 설계

기술사 관점에서는 ASIC을 "고정형 고성능 [[009_semiconductor|반도체]]"로 설명해야 한다.

- **📢 섹션 요약 비유**: 바꾸기 어려운 대신 아주 잘 맞는 칩이다.

---

## Ⅴ. 기대효과 및 결론

ASIC은 [[282_performance_tactics|성능]]과 전력 효율이 중요한 대량 생산 환경에서 강하다.

결론적으로 ASIC은 특정 용도에 최적화된 전용 [[009_semiconductor|반도체]]다.

- **📢 섹션 요약 비유**: 한 가지 일을 아주 잘하는 맞춤 칩이다.

---

## 관련 개념 맵

```text
Specification
  ↓
ASIC
  ↓
Fabrication
  ↓
High Efficiency
```

---

## 관련 키워드 및 발전 흐름도

```text
Custom Chip
  ↓
ASIC
  ↓
SoC
  ↓
Specialized Hardware
```

---

## 어린이를 위한 3줄 비유 설명

딱 하나의 일을 잘하게 만들어요.  
수정은 어렵지만 아주 빨라요.  
ASIC은 그런 특별한 칩이에요.
