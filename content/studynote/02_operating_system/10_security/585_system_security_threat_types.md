---
title: 585. 시스템 보안 위협 유형 (System Security Threat Types)
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정보 보안의 3대 목표는 **[[002_confidentiality|기밀성]]([[002_confidentiality|Confidentiality]])**, **[[003_integrity|무결성]]([[003_integrity|Integrity]])**, **[[452_availability|가용성]]([[452_availability|Availability]])**이며, 이에 **[[303_authentication_authorization_patterns|인증]]([[604_authentication_factors|Authentication]])**을 더하여 4가지 보안 위협 유형으로 [[104_classification_analysis|분류]]한다.
> 2. **가치**: 이 **[[104_classification_analysis|분류]] 체계(CIA+Auth)**를 통해 다양한 해킹 공격을 체계적으로 분석하고, 각 위협 유형에 대응하는 보안 기술을 적용할 수 있다.
> 3. **한계**: 실제 공격은 여러 위협 유형을 조합하여 발생하므로,单一(단일) 기술만으로는 완벽한 보안을 달성할 수 없다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [[002_confidentiality|기밀성]] ([[002_confidentiality|Confidentiality]])

**"인가된 사람만이 정보에 접근할 수 있다"**

| 위협 유형 | 설명 | 예시 |
|:---|:---|:---|
| **가로채기 (Interception)** | 정보가 [[701_sniffing_eavesdropping_promiscuous|도청]]당함 | 네트워크 스니핑, 패킷 캡처 |

### 1.2 [[003_integrity|무결성]] ([[003_integrity|Integrity]])

**"정보가 권한 없이 변조되지 않는다"**

| 위협 유형 | 설명 | 예시 |
|:---|:---|:---|
| **변조 (Modification)** | 정보가中途(중도)에서 변경됨 | [[001_dikw_pyramid|데이터]] 변경, man-in-the-middle 공격 |

### 1.3 [[452_availability|가용성]] ([[452_availability|Availability]])

**"정보와 시스템에 필요할 때 접근할 수 있다"**

| 위협 유형 | 설명 | 예시 |
|:---|:---|:---|
| **차단 (Interruption)** | 시스템이 이용 불가 상태가 됨 | DDoS, [[730_ransomware|랜섬웨어]] |

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 가로채기 (Interception): [[002_confidentiality|기밀성]] 침해

```
[ 통신 흐름 ]
 Sender  ----(데이터)---->  Receiver
              ^
              |
         【해커가 도청】
```

**예시**:
- 네트워크 스니핑
- 이메일 가로채기
-通话(통화) [[701_sniffing_eavesdropping_promiscuous|도청]]

**대응 기술**:
- [[694_thread_local_storage_tls|TLS]]/SSL 암호화
- [[983_vpn_virtual_private_network|VPN]]
- 암호화 통신

### 2.2 변조 (Modification): [[003_integrity|무결성]] 침해

```
[ 통신 흐름 ]
 Sender  ----(정상 데이터)--->  Receiver
              【해커가 데이터 변조】
              ----(변조된 데이터)--->  Receiver
```

**예시**:
- [[001_dikw_pyramid|데이터]] 변경 공격
- [[976_dns_spoofing|DNS Spoofing]]
- [[471_https_http_over_tls|HTTPS]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]ダウングレード(다운그레이드)

**대응 기술**:
- [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]] 검사 (Hash/[[673_mac_message_authentication_code|MAC]])
- 디지털 서명
- [[295_protocol_field_tcp_udp_icmp|프로토콜]] 보안

### 2.3 차단 (Interruption): [[452_availability|가용성]] 침해

```
[ 통신 흐름 ]
 Sender  -X-(데이터)-X->  Receiver
         【해커가 통신 차단】
```

**예시**:
- DDoS 공격
- [[730_ransomware|랜섬웨어]]
- 시스템 [[501_file_definition_logical_record|파일]] 삭제

**대응 기술**:
-防火墙([[690_firewall_generation_evolution|방화벽]])
- DDoS 방어 시스템
- [[555_backup_and_restore_strategy|백업]] 및 [[658_ir_recovery|복구]]

### 2.4 위조 (Fabrication): [[303_authentication_authorization_patterns|인증]] 침해

```
[ 통신 흐름 ]
  (진짜 Sender 없음)
 【해커가 가짜 Sender 역할】
              ----(가짜 데이터)--->  Receiver
```

**예시**:
- [[704_ip_spoofing_trust_injection|IP Spoofing]]
- 신원 도용
-Session([[160_session_controlling_terminal|세션]]) 하이재킹

**대응 기술**:
- [[604_authentication_factors|Authentication]] ([[303_authentication_authorization_patterns|인증]])
-デジタル署名(디지털 서명)
- [[303_authentication_authorization_patterns|인증]]서

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 3.1 기관별優先순위

| 기관 유형 | 가장 중요한 목표 |
|:---|:---|
| **군사/정보 기관** | [[002_confidentiality|기밀성]] > [[003_integrity|무결성]] > [[452_availability|가용성]] |
| **은행/금융** | [[003_integrity|무결성]] > [[452_availability|가용성]] > [[002_confidentiality|기밀성]] |
| **전자상거래** | [[452_availability|가용성]] > [[002_confidentiality|기밀성]] > [[003_integrity|무결성]] |

### 3.2 Trade-off [[083_relationship_in_er_model|관계]]

세 가지 목표는 상호 Trade-off [[083_relationship_in_er_model|관계]]에 있다:

```text
[ 예시 ]
기밀성을 높이면 -> 복잡한 암호화 -> 가용성 저하
무결성을 높이면 -> 많은 검증 -> 성능 저하
```

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- **체계적 분석**: 위협을 4가지 유형으로 [[104_classification_analysis|분류]]하여 체계적으로 분석 가능
- **적절한 대응**: 위협 유형에 따라 적합한 보안 기술 선별 가능
- **총체적 보안**: 여러 기술을 조합한 다층 방어([[012_defense_in_depth|Defense in Depth]]) 필요

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

시스템 보안 위협 유형 (System [[283_security_tactics|Security]] Threat Types)은 [[001_operating_system_purpose|운영체제]] [[043_protection_security|보호와 보안]] 메커니즘을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 [[586_trojan_horse_wrapper|트로이 목마]] ([[586_trojan_horse_wrapper|Trojan Horse]]) / 래퍼 (Wrapper)처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[583_selinux|SELinux]] | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[584_apparmor|AppArmor]] | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[586_trojan_horse_wrapper|트로이 목마]] ([[586_trojan_horse_wrapper|Trojan Horse]]) / 래퍼 (Wrapper) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[587_backdoor_trapdoor|트랩 도어]] ([[677_trap_based_system_call_implementation|Trap]] Door / [[727_backdoor|Backdoor]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[AppArmor]
    │
    ▼
[시스템 보안 위협 유형 (System Security Threat Types)]
    │
    ├──▶ [트로이 목마 (Trojan Horse) / 래퍼 (Wrapper)]
    └──▶ [트랩 도어 (Trap Door / Backdoor)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. **[[002_confidentiality|기밀성]]**은 놀이공원에서 **"비밀번호 없이는 입장 불가"**와 같다. 비밀번호를 모르는 사람은 놀이시설을 탈 수 없다.

2. **[[003_integrity|무결성]]**은 놀이공원에서 **"표시가 있는 표찰"**과 같다.표찰에 표시된 내용을勝手に(승강장에) 변경할 수 없어야 한다.

3. **[[452_availability|가용성]]**은 놀이공원에서 **"언제든 입장 가능"**과 같다. 놀이시설이 고장나면 아무도 놀지 못한다.

4. **[[303_authentication_authorization_patterns|인증]]**은 놀이공원에서 **"본인 [[396_validation|확인]]"**과 같다. 신분증을 제시하여 "진짜 Alice 맞구나"를 [[396_validation|확인]]하는 것과 같다.
