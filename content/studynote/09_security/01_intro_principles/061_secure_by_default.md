+++
title = "61. Secure by Default (기본값 안전)"
date = 2026-04-05

[taxonomies]
tags = ["studynote-security"]

[extra]
tags = ["studynote-security"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Secure by Default는 시스템이 처음 켜지는 순간부터 가장 안전한 기본 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)으로 동작하도록 설계하는 원칙이다.
> 2. **가치**: 사용자가 보안 전문가가 아니어도 최소 권한, 차단 우선, 비공개 우선 상태가 유지되어 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 실수의 피해를 줄인다.
> 3. **판단**: 클라우드, [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) (Internet of Things), 계정, [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 모두에서 "기본값"이 실제 보안 수준을 결정한다.

---

## Ⅰ. 개요 및 필요성

많은 보안 사고는 복잡한 해킹보다 기본 비밀번호, 공개 버킷, 열린 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)처럼 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 약해서 발생한다. 사용자가 항상 보안 전문가일 것이라 기대하는 것은 현실적이지 않다.

Secure by Default는 사용자가 아무것도 바꾸지 않아도 안전하게 시작되도록 시스템을 설계하자는 약속이다. 즉, 위험한 기능은 기본적으로 꺼 두고, 정말 필요할 때만 켜게 만든다.

- **📢 섹션 요약 비유**: 새 가전제품이 처음부터 잠금장치가 걸린 상태로 나와야 한다는 뜻이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
기본 설치
   v
안전한 기본값
   v
명시적 Opt-in
   v
감사 로그 / 모니터링
```

| 원칙 | 의미 |
| :-- | :-- |
| Deny by Default | 허용이 없으면 차단 |
| [Least Privilege](/knowledge-base/studynote/09_security/01_intro_principles/010_least_privilege/) | 필요한 권한만 부여 |
| [Fail-safe](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/459_fail_safe/) | 오류 시 안전한 상태로 복귀 |
| Secure Defaults | 제품 출고 시 안전한 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 적용 |

| 적용 영역 | 예시 |
| :-- | :-- |
| Cloud | 공개 버킷 차단, 기본 암호화 |
| Identity | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비밀번호 강제 변경, [MFA](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/) ([Multi-Factor Authentication](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/)) |
| Device | 원격 접속 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 기본 차단 |
| [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 없이는 접근 불가 |

보안은 사용자가 "켜는 것"이 아니라, 시스템이 "이미 안전하게 시작하는 것"에서 출발한다.

- **📢 섹션 요약 비유**: 문을 기본적으로 잠가 두고, 정말 필요한 사람만 열쇠로 열게 하는 방식이다.

---

## Ⅲ. 비교 및 연결

| 항목 | Secure by Default | [Security by Design](/knowledge-base/studynote/09_security/01_intro_principles/058_security_by_design/) |
| :-- | :-- | :-- |
| 범위 | 기본 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 전체 설계 철학 |
| 초점 | 출고 직후 안전 | 개발 단계부터 안전 |
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 실천 원칙 | 상위 개념 |

| 대표 사례 | 보안 기본값 |
| :-- | :-- |
| S3 버킷 | Block Public Access |
| 공유기 | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비밀번호 강제 변경 |
| [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) (Identity and Access [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/1013_management/)) | 최소 권한 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 기본화 |
| 프레임워크 | [CSRF](/knowledge-base/studynote/03_network/14_network_security_threats/728_csrf_cross_site_request_forgery_concept/), CORS, 비밀키 비노출 기본값 |

Secure by Default는 사용자 편의성을 해치지 않으면서도, 위험을 사용자가 직접 선택하게 만드는 구조다. 결과적으로 보안 사고의 절반 이상을 차지하는 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 실수를 줄인다.

- **📢 섹션 요약 비유**: 자동차가 출고될 때부터 안전벨트가 기본으로 걸려 있는 상태와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 처음 실행 시 가장 위험한 기능이 꺼져 있는가?
2. 계정, [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 버킷, API가 기본 차단 상태인가?
3. 사용자가 켜기 전에는 공개되지 않는가?
4. 보안 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 문서가 아니라 제품 동작에 반영되는가?
5. 예외를 열 때도 감사와 로깅이 남는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비밀번호를 그대로 두는 설계
- 공개/비공개 전환이 기본값에서 헷갈리게 만드는 설계
- 보안 옵션을 숨겨 두고 사용자가 찾아야만 하는 설계
- "사용자 책임"만 강조하고 제조사 책임을 비우는 설계

기술사 관점에서는 기본값이 곧 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이라는 점을 기억해야 한다. 보안 옵션은 기능 추가가 아니라 제품 책임의 일부다.

- **📢 섹션 요약 비유**: 처음부터 창문에 철창이 달려 있어야 도둑이 들어오기 어렵다.

---

## Ⅴ. 기대효과 및 결론

Secure by Default는 사고를 없애는 만능열쇠는 아니지만, 가장 흔한 실수를 크게 줄여 준다. 그래서 현대 보안 설계에서 가장 실용적인 출발점이다.

결국 보안은 사용자의 선의에 기대지 않고, 시스템의 기본값으로 책임지는 일이다.

- **📢 섹션 요약 비유**: 안전한 집은 주인이 똑똑해서가 아니라, 문과 창문이 처음부터 잘 잠겨 있어서 안전한 것이다.

---

## 관련 개념 맵

```text
Security by Design
   v
Secure by Default
   v
Least Privilege
   v
Fail-safe / Opt-in
   v
Secure Product Baseline
```

---

## 관련 키워드 및 발전 흐름도

```text
기본 비밀번호
   v
초기 설정 실수
   v
Secure by Default
   v
기본값 보안 강화
   v
Zero Trust
```

---

## 어린이를 위한 3줄 비유 설명

새 장난감은 처음부터 잠금이 걸려 있어야 해요.
그래야 아무나 함부로 못 만져요.
필요할 때만 주인이 직접 열어 쓰는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 61 / 1108

<- **이전**: [60. Privacy by Design (PbD) - 7대 기본 원칙](/knowledge-base/studynote/09_security/01_intro_principles/060_privacy_by_design/)
**다음**: [62. 시큐어 코딩 (Secure Coding)](/knowledge-base/studynote/09_security/01_intro_principles/062_secure_coding/) ->

---
