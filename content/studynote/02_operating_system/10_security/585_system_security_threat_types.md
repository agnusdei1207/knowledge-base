+++
title = "585. 시스템 보안 위협 유형 (System Security Threat Types)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정보 보안의 3대 목표는 <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a>(<a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">Confidentiality</a>)</strong>, <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a>(<a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">Integrity</a>)</strong>, <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a>(<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a>)</strong>이며, 이에 <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>(<a href="/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/">Authentication</a>)</strong>을 더하여 4가지 보안 위협 유형으로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)한다.
> 2. **가치**: 이 <strong><a href="/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a> 체계(CIA+Auth)</strong>를 통해 다양한 해킹 공격을 체계적으로 분석하고, 각 위협 유형에 대응하는 보안 기술을 적용할 수 있다.
> 3. **한계**: 실제 공격은 여러 위협 유형을 조합하여 발생하므로,(단일) 기술만으로는 완벽한 보안을 달성할 수 없다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) ([Confidentiality](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/))

**"인가된 사람만이 정보에 접근할 수 있다"**

| 위협 유형 | 설명 | 예시 |
|:---|:---|:---|
| **가로채기 (Interception)** | 정보가 [도청](/knowledge-base/studynote/03_network/14_network_security_threats/701_sniffing_eavesdropping_promiscuous/)당함 | 네트워크 스니핑, 패킷 캡처 |

### 1.2 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) ([Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/))

**"정보가 권한 없이 변조되지 않는다"**

| 위협 유형 | 설명 | 예시 |
|:---|:---|:---|
| **변조 (Modification)** | 정보가(중도)에서 변경됨 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변경, man-in-the-middle 공격 |

### 1.3 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) ([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))

**"정보와 시스템에 필요할 때 접근할 수 있다"**

| 위협 유형 | 설명 | 예시 |
|:---|:---|:---|
| **차단 (Interruption)** | 시스템이 이용 불가 상태가 됨 | DDoS, [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/) |

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 가로채기 (Interception): [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 침해

```
[ 통신 흐름 ]
Sender ----(데이터)----> Receiver
^
|
【해커가 도청】
```

**예시**:
- 네트워크 스니핑
- 이메일 가로채기
-(통화) [도청](/knowledge-base/studynote/03_network/14_network_security_threats/701_sniffing_eavesdropping_promiscuous/)

**대응 기술**:
- [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/)/SSL 암호화
- [VPN](/knowledge-base/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/)
- 암호화 통신

### 2.2 변조 (Modification): [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 침해



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">통신 흐름</div></div>
<div class="kb-diagram-note">Sender ----(정상 데이터)---&gt; Receiver</div>
<div class="kb-diagram-note">【해커가 데이터 변조】</div>
<div class="kb-diagram-tree-item" style="--depth:0">(변조된 데이터)---&gt; Receiver</div>
</div>
</div>



**예시**:
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변경 공격
- [DNS Spoofing](/knowledge-base/studynote/03_network/19_frequent_topics_terms/976_dns_spoofing/)
- [HTTPS](/knowledge-base/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)(다운그레이드)

**대응 기술**:
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 검사 (Hash/[MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/))
- 디지털 서명
- [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 보안

### 2.3 차단 (Interruption): [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 침해

```
[ 통신 흐름 ]
Sender -X-(데이터)-X-> Receiver
【해커가 통신 차단】
```

**예시**:
- DDoS 공격
- [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/)
- 시스템 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 삭제

**대응 기술**:
-([방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/))
- DDoS 방어 시스템
- [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 및 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)

### 2.4 위조 (Fabrication): [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 침해

```
[ 통신 흐름 ]
(진짜 Sender 없음)
【해커가 가짜 Sender 역할】
----(가짜 데이터)---> Receiver
```

**예시**:
- [IP Spoofing](/knowledge-base/studynote/03_network/14_network_security_threats/704_ip_spoofing_trust_injection/)
- 신원 도용
-Session([세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)) 하이재킹

**대응 기술**:
- [Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/) ([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))
-(디지털 서명)
- [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 3.1 기관별우선순위

| 기관 유형 | 가장 중요한 목표 |
|:---|:---|
| **군사/정보 기관** | [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) > [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) > [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) |
| **은행/금융** | [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) > [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) > [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) |
| **전자상거래** | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) > [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) > [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) |

### 3.2 Trade-off [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

세 가지 목표는 상호 Trade-off [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)에 있다:



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">예시</div></div>
<div class="kb-diagram-note">기밀성을 높이면 -&gt; 복잡한 암호화 -&gt; 가용성 저하</div>
<div class="kb-diagram-note">무결성을 높이면 -&gt; 많은 검증 -&gt; 성능 저하</div>
</div>
</div>



- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- **체계적 분석**: 위협을 4가지 유형으로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하여 체계적으로 분석 가능
- **적절한 대응**: 위협 유형에 따라 적합한 보안 기술 선별 가능
- **총체적 보안**: 여러 기술을 조합한 다층 방어([Defense in Depth](/knowledge-base/studynote/09_security/01_intro_principles/012_defense_in_depth/)) 필요

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

시스템 보안 위협 유형 (System [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Threat Types)은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [보호와 보안](/knowledge-base/studynote/02_operating_system/01_overview_architecture/043_protection_security/) 메커니즘을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 [트로이 목마](/knowledge-base/studynote/02_operating_system/10_security/586_trojan_horse_wrapper/) ([Trojan Horse](/knowledge-base/studynote/02_operating_system/10_security/586_trojan_horse_wrapper/)) / 래퍼 (Wrapper)처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [SELinux](/knowledge-base/studynote/02_operating_system/10_security/583_selinux/) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [AppArmor](/knowledge-base/studynote/02_operating_system/10_security/584_apparmor/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [트로이 목마](/knowledge-base/studynote/02_operating_system/10_security/586_trojan_horse_wrapper/) ([Trojan Horse](/knowledge-base/studynote/02_operating_system/10_security/586_trojan_horse_wrapper/)) / 래퍼 (Wrapper) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [트랩 도어](/knowledge-base/studynote/02_operating_system/10_security/587_backdoor_trapdoor/) ([Trap](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/) Door / [Backdoor](/knowledge-base/studynote/09_security/15_malware_attack_vectors/727_backdoor/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">AppArmor</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">시스템 보안 위협 유형 (System Security Threat Types)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">트로이 목마 (Trojan Horse) / 래퍼 (Wrapper)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">트랩 도어 (Trap Door / Backdoor)</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a></strong>은 놀이공원에서 <strong>"비밀번호 없이는 입장 불가"</strong>와 같다. 비밀번호를 모르는 사람은 놀이시설을 탈 수 없다.

2. <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a></strong>은 놀이공원에서 <strong>"표시가 있는 표찰"</strong>과 같다.표찰에 표시된 내용을에(승강장에) 변경할 수 없어야 한다.

3. <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a></strong>은 놀이공원에서 <strong>"언제든 입장 가능"</strong>과 같다. 놀이시설이 고장나면 아무도 놀지 못한다.

4. <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a></strong>은 놀이공원에서 <strong>"본인 <a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a>"</strong>과 같다. 신분증을 제시하여 "진짜 Alice 맞구나"를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것과 같다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 585 / 800

← **이전**: [584. AppArmor](/knowledge-base/studynote/02_operating_system/10_security/584_apparmor/)
**다음**: [586. 트로이 목마 (Trojan Horse) / 래퍼 (Wrapper)](/knowledge-base/studynote/02_operating_system/10_security/586_trojan_horse_wrapper/) →

---
