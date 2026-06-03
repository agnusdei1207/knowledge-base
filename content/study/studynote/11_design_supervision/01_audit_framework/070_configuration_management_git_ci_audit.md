+++
weight = 70
title = "70. 형상 관리 저장소 (Git, SVN) 및 지속적 통합(CI) 감리"
date = "2026-04-10"
[extra]
categories = "studynote-design"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[020_software_configuration_management|형상 관리]] 저장소와 CI는 변경 통제, 추적성, 자동 [[395_verification_process_review|검증]]을 위한 감리 핵심 대상이다.
> 2. **가치**: [[288_version_ihl_tos_total_length|버전]] 이력과 빌드 결과를 통해 품질과 책임 소재를 명확히 한다.
> 3. **판단**: 저장소 관리와 [[090_configuration_item|CI]] 파이프라인이 분리되지 않고 연결되어야 진짜 통제가 된다.

---

## Ⅰ. 개요 및 필요성

소스가 어디서 어떻게 바뀌었는지 모르면 감리도 어렵다. 그래서 [[020_software_configuration_management|형상 관리]]와 CI를 함께 본다.

이 둘이 있어야 변경과 [[395_verification_process_review|검증]]이 연결된다.

- **📢 섹션 요약 비유**: 원고의 수정 이력과 인쇄 전 검사표를 함께 보는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Repo (Git/SVN)
  ↓ commit
CI Pipeline
  ↓ build/test
Audit Trace
```

| 요소 | 의미 |
| :-- | :-- |
| Repository | 형상 저장 |
| [[090_configuration_item|CI]] | 자동 [[395_verification_process_review|검증]] |
| [[228_blockchain_smart_contract_traceability|Traceability]] | 추적성 |

[[020_software_configuration_management|형상 관리]]는 누가 무엇을 바꿨는지 기록하고, CI는 그 변경이 깨지지 않았는지 [[395_verification_process_review|검증]]한다.

- **📢 섹션 요약 비유**: 수정본을 저장하고, 인쇄 전에 다시 읽는 과정이다.

---

## Ⅲ. 비교 및 연결

| 개념 | 역할 | 차이 |
| :-- | :-- | :-- |
| Git/SVN | 이력 관리 | [[288_version_ihl_tos_total_length|버전]] 통제 |
| [[090_configuration_item|CI]] | 자동 [[395_verification_process_review|검증]] | 품질 [[396_validation|확인]] |
| [[363_audit|Audit]] | 통제/점검 | 증적 확보 |

| 점검 항목 | 예 |
| :-- | :-- |
| Branch [[164_policy|Policy]] | [[571_protection_vs_security|보호]] 규칙 |
| Build Status | 빌드 결과 |
| Test Evidence | 테스트 증거 |

[[020_software_configuration_management|형상 관리]]와 CI는 감리에서 증적을 남기는 핵심 수단이다.

- **📢 섹션 요약 비유**: 누가 언제 고쳤는지와, 잘 되는지 [[396_validation|확인]]하는 기록이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 형상 저장소가 중앙에 있는가?
2. 브랜치 정책이 있는가?
3. CI가 자동으로 동작하는가?
4. 빌드/테스트 증적이 남는가?
5. 변경 추적이 가능한가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 로컬 파일만으로 [[288_version_ihl_tos_total_length|버전]] 관리하는 설계
- [[090_configuration_item|CI]] 없이 수동 배포하는 설계
- 승인 기록이 없는 설계
- 저장소와 파이프라인이 분리된 설계

기술사 관점에서는 [[020_software_configuration_management|형상 관리]]와 CI를 "변경 통제와 [[395_verification_process_review|검증]]의 증적 체계"로 설명해야 한다.

- **📢 섹션 요약 비유**: 고친 기록과 [[396_validation|확인]] 결과가 같이 있어야 안심할 수 있다.

---

## Ⅴ. 기대효과 및 결론

[[020_software_configuration_management|형상 관리]]와 CI가 잘되면 변경 이력과 품질이 모두 투명해진다.

결론적으로 [[020_software_configuration_management|형상 관리]] 저장소와 CI는 감리에서 필수적인 통제 수단이다.

- **📢 섹션 요약 비유**: 수정본과 검사표를 같이 보관하는 것이다.

---

## 관련 개념 맵

```text
Repository
  ↓
CI
  ↓
Traceability
  ↓
Audit
```

---

## 관련 키워드 및 발전 흐름도

```text
Version Control
  ↓
Git / SVN
  ↓
CI
  ↓
Audit Evidence
```

---

## 어린이를 위한 3줄 비유 설명

고친 기록을 남겨요.  
잘 되는지도 자동으로 [[396_validation|확인]]해요.  
[[020_software_configuration_management|형상 관리]]와 CI는 그런 약속이에요.
