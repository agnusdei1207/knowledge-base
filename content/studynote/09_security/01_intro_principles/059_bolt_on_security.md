---
title: "Bolt On Security"
date: "2026-04-05"
tags:
  - "studynote-security"
weight: 59
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 사후 보안(Bolt-on [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))은 시스템을 만든 뒤 외곽에 보안 장비와 솔루션을 덧붙여 막으려는 땜질식 접근이다.
> 2. **가치/한계**: 단기 대응에는 도움이 되지만, 설계 [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)과 비즈니스 로직 취약점은 외곽 장비만으로는 막기 어렵다.
> 3. **판단 포인트**: 진짜 해법은 [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) by Design과 DevSecOps로 보안을 개발 생명주기에 포함하는 것이다.

---

## Ⅰ. 개요 및 필요성

사후 보안은 "기능을 먼저 만들고, 나중에 보안을 붙이자"는 사고에서 나온다. 빠른 출시가 우선이던 시절에는 흔했지만, 지금은 [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)를 크게 남긴다.

외곽 장비는 네트워크 경계의 위협을 막는 데 유용하다. 하지만 애플리케이션 내부의 권한 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [입력 검증](/studynote/09_security/uncategorized/1034_input_validation/), 로직 오류는 코드 자체를 고치지 않으면 사라지지 않는다.

- **📢 섹션 요약 비유**: 집을 허술하게 지은 뒤 문 앞에만 철문을 달아 두는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Bolt-on 방식은 애플리케이션 바깥쪽에 보안 계층을 추가한다. 대표적으로 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/), [IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/)/[IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/), [WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/), 백신, 프록시가 있다.

```text
사용자 요청
   v
WAF / IPS / Firewall
   v
취약한 애플리케이션
   v
DB / 내부 자원
```

| 외곽 보안 | 막기 쉬운 것 | 막기 어려운 것 |
| :-- | :-- | :-- |
| [Firewall](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) | [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)/[프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 통제 | 애플리케이션 로직 오류 |
| [WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/)([Web Application Firewall](/studynote/09_security/05_web_app_security/242_waf_web_application_firewall_l7_protection/)) | 대표적 웹 공격 패턴 | [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 누락, [IDOR](/studynote/09_security/05_web_app_security/418_idor/) |
| [IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/)(Intrusion Prevention System) | 알려진 공격 시그니처 | 설계 [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) |
| 백신/[EDR](/studynote/09_security/04_endpoint_security/325_edr/) | 악성코드 탐지 | 잘못된 권한 설계 |

장비는 트래픽을 통과시키거나 차단할 수 있지만, "이 사용자가 이 데이터를 볼 권리가 있는가" 같은 판단은 애플리케이션이 스스로 해야 한다.

- **📢 섹션 요약 비유**: 문 앞 경비는 수상한 사람을 막을 수는 있어도, 방 안 금고를 잘못 열어 둔 문제까지 해결하진 못한다.

---

## Ⅲ. 비교 및 연결

Bolt-on Security는 [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) by Design과 정반대에 가깝다.

| 방식 | 특징 | 결과 |
| :-- | :-- | :-- |
| Bolt-on [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) | 개발 후 외곽에 붙임 | 임시 대응, [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 증가 |
| [Security by Design](/studynote/09_security/01_intro_principles/058_security_by_design/) | 설계 단계부터 반영 | 구조적으로 안전 |
| [DevSecOps](/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/) | 개발/운영/보안을 통합 | 빠른 배포와 보안 동시 추구 |

Bolt-on은 종종 "[Defense in Depth](/studynote/09_security/01_intro_principles/012_defense_in_depth/)"와 혼동된다. 하지만 방어 심화는 여러 계층을 함께 설계하는 것이고, Bolt-on은 이미 잘못 만든 시스템 위에 나중에 덧붙이는 것이다.

- **📢 섹션 요약 비유**: 튼튼한 집을 여러 겹으로 짓는 것과, 무너진 집에 비닐만 덧씌우는 것은 완전히 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

긴급 패치나 0-day 대응에서 임시 Bolt-on은 필요할 수 있다. 하지만 그것은 최종 해법이 아니라, 구조 개선 전까지 버티는 가교여야 한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 코드 수준의 [입력 검증](/studynote/09_security/uncategorized/1034_input_validation/)과 권한 검사가 있는가?
2. 외곽 장비가 아닌 설계 수정 계획이 있는가?
3. 보안 요구사항이 요구 분석 단계부터 반영되었는가?
4. 보안 솔루션이 기능 마비를 숨기고 있지는 않은가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- WAF를 붙였으니 안전하다고 생각하는 설계
- 취약한 권한 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 장비로 대신하려는 설계
- 출시 후 문제를 보안팀 책임으로만 돌리는 문화

- **📢 섹션 요약 비유**: 삐걱거리는 의자에 테이프를 감아 버티는 것은 가능해도, 결국 다리 구조를 고쳐야 한다.

---

## Ⅴ. 기대효과 및 결론

사후 보안은 단기적으로 편해 보이지만 장기적으로는 사고 비용을 키운다. 결국 보안은 붙이는 것이 아니라 만들어 넣는 것이다.

따라서 기술사는 "무엇을 덧댈 것인가"보다 "어떤 [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)을 코드와 구조에서 제거할 것인가"를 먼저 판단해야 한다.

- **📢 섹션 요약 비유**: 약을 먹는 것보다 병의 원인을 먼저 고쳐야 진짜 건강해진다.

---

## 관련 개념 맵

```text
기능 우선 개발
   v
Bolt-on Security
   v
기술 부채 / 우회 공격
   v
Security by Design / DevSecOps
```

---

## 관련 키워드 및 발전 흐름도

```text
사후 방어
   v
WAF / IPS / Firewall
   v
보안 설계 내재화
   v
Shift-Left / DevSecOps
```

---

## 어린이를 위한 3줄 비유 설명

사후 보안은 다 만든 뒤에 문만 잠그는 거예요.
문이 튼튼해도, 집 안 구조가 약하면 문제를 못 막아요.
그래서 처음부터 안전하게 짓는 게 더 좋아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 59 / 1108

<- **이전**: [58. 내재적 보안 (Security by Design) - 설계 단계 보안 고려](/studynote/09_security/01_intro_principles/058_security_by_design/)
**다음**: [60. Privacy by Design (PbD) - 7대 기본 원칙](/studynote/09_security/01_intro_principles/060_privacy_by_design/) ->

---
