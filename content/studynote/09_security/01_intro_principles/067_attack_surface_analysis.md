+++
title = "067. Attack Surface Analysis — 공격 표면 관리"
date = 2026-04-05

[taxonomies]
tags = ["studynote-security"]

[extra]
tags = ["studynote-security"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 공격 표면(Attack Surface)은 공격자가 시스템에 접근할 수 있는 모든 접점의 총합이다.
> 2. **가치**: 표면을 줄이면 보안 위험과 관리 비용이 함께 줄어든다.
> 3. **판단**: 공격 표면 분석은 기능 목록이 아니라 외부 공개 면적과 신뢰 경계를 줄이는 작업이다.

---

## Ⅰ. 개요 및 필요성

시스템이 복잡할수록 공격자가 들어갈 수 있는 길도 많아진다. 그래서 공격 표면을 먼저 보는 것이 중요하다.

불필요한 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 권한, 입력 지점이 많을수록 위험은 커진다.

- **📢 섹션 요약 비유**: 집의 문과 창문이 많을수록 잠가야 할 곳도 많아진다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Users / APIs / Ports / Files / Privileges</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Attack Surface</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Reduction / Hardening</div>
</div>
</div>



| 구성 요소 | 의미 |
| :-- | :-- |
| Entry Point | 공격 진입점 |
| Trust Boundary | 신뢰 경계 |
| Exposure | 외부 공개 면적 |

공격 표면 분석은 "무엇이 노출되었는가"를 식별하고, 불필요한 노출을 제거하는 데 초점을 둔다.

- **📢 섹션 요약 비유**: 밖으로 열려 있는 문이 몇 개인지 세어 보는 일이다.

---

## Ⅲ. 비교 및 연결

| 개념 | 초점 | 차이 |
| :-- | :-- | :-- |
| Attack Surface | 노출 면적 | 공격 가능 접점 |
| [Threat Modeling](/knowledge-base/studynote/09_security/uncategorized/611_threat_modeling/) | 공격 시나리오 | 공격 방식 |
| Hardening | 방어 강화 | [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)/축소 |

| 영역 | 예 |
| :-- | :-- |
| Network | [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| Application | [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 입력값 |
| Identity | 권한, 토큰 |

표면을 줄이는 것은 공격자에게 줄 수 있는 기회를 줄이는 것과 같다.

- **📢 섹션 요약 비유**: 숨길 구멍이 적을수록 도둑이 들어오기 어렵다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 외부 노출 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)와 API를 줄였는가?
2. 불필요한 권한과 기능을 닫았는가?
3. 신뢰 경계를 확인했는가?
4. 입력/[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)/[프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 표면을 점검했는가?
5. 주기적으로 재분석하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 기능을 외부에 노출하는 설계
- 사용하지 않는 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 방치하는 설계
- 권한을 과도하게 주는 설계
- 표면 축소 없이 탐지만 하는 설계

기술사 관점에서는 공격 표면을 "보이는 위험 면적"으로 보고, 설계와 운영에서 계속 줄여야 한다.

- **📢 섹션 요약 비유**: 창문을 적게 만들수록 지키기가 쉬워진다.

---

## Ⅴ. 기대효과 및 결론

공격 표면을 줄이면 사고 가능성과 대응 범위가 작아진다. 그래서 보안 기본 원칙의 출발점이 된다.

결론적으로 공격 표면 분석은 노출 면적을 줄여 보안을 높이는 작업이다.

- **📢 섹션 요약 비유**: 열려 있는 문이 적을수록 집이 안전하다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Exposure</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Attack Surface</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Hardening</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Security Posture</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Threat Modeling</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Attack Surface</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Hardening</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Reduction</div>
</div>
</div>



---

## 어린이를 위한 3줄 비유 설명

밖에 보여 주는 부분이 많을수록 위험해요.  
문과 창문을 줄이면 더 안전해요.  
공격 표면은 그런 열려 있는 곳이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 67 / 1108

← **이전**: [066. PASTA (Process for Attack Simulation and Threat Analysis) — 7단계 위협 모델링](/knowledge-base/studynote/09_security/01_intro_principles/066_pasta_threat_modeling/)
**다음**: [068. 암호학 (Cryptography) — 기밀성·무결성·인증·부인방지 제공](/knowledge-base/studynote/09_security/02_crypto/068_cryptography/) →

---
