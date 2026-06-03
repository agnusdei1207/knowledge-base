+++
title = "531. SNMPv1, v2c (Community String 노출 단점)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SNMPv1과 v2c는 네트워크 관리 정보를 교환하기 위해 Community String(커뮤니티 스트링)이라는 평문(Cleartext) 비밀번호를 사용하는 방식으로, 보안 측면에서 치명적인 결함을 가진 초기 SNMP 구현이다.
> 2. **가치**: v2c의 GetBulk 명령은 대량 데이터 수집 효율을 획기적으로 개선했지만, 커뮤니티 스트링이 네트워크에 평문으로 흘러 스니핑에 무방비 상태다. 이 구조적 한계를 이해해야 SNMPv3 전환의 필요성을 설명할 수 있다.
> 3. **판단 포인트**: v1/v2c 환경에서는 커뮤니티 스트링 변경, ACL로 NMS IP 제한, Management VLAN 분리가 최소한의 보안 조치다. 근본적 해결은 SNMPv3 전환뿐이다.

---

## Ⅰ. 개요 및 필요성

SNMP는 보안 기능을 중심으로 진화해 왔다. 가장 초창기 버전인 v1과, 성능을 개선했지만 보안은 여전히 취약했던 v2c가 오랫동안 사용되었다.

1988년 RFC 1067로 처음 발표된 SNMPv1은 당시 인터넷이 지금보다 훨씬 작고 신뢰할 수 있는 환경에서 운영되었기 때문에, 보안보다는 단순성과 구현 용이성을 우선시하여 설계되었다. 커뮤니티 스트링이라는 공유 비밀번호 개념을 도입했지만, 이 문자열이 UDP 패킷에 평문으로 포함되어 전송된다는 치명적 약점이 있었다.

1990년대 초 SNMPv2는 보안 강화를 시도했으나 구현 복잡성으로 실패하고, 결국 보안은 v1 수준을 유지하면서 성능만 개선한 Community-based SNMPv2, 즉 v2c로 타협했다.

이 두 버전은 현재도 수많은 레거시 장비와 환경에서 운용 중이므로, 그 구조와 보안 한계를 정확히 이해하고 올바른 보완책을 적용하는 것이 실무에서 중요하다.

- **📢 섹션 요약 비유**: SNMPv1/v2c는 문에 자물쇠를 달았지만, 열쇠(커뮤니티 스트링)를 투명한 봉투에 넣어 우편으로 보내는 방식이다. 자물쇠는 있지만 열쇠가 다 보인다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 커뮤니티 스트링 (Community String) 동작 원리

SNMPv1과 v2c에서 매니저(NMS)와 에이전트(라우터, 스위치) 간에 데이터를 주고받을 때 사용하는 일종의 비밀번호(Password) 역할을 하는 문자열이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">SNMPv1/v2c 패킷 구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">UDP 헤더 (포트 161/162)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SNMP 버전 (0=v1, 1=v2c)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Community String : "public" ← 평문(Cleartext)!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PDU 타입 (Get-Request / Get-Response 등)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">OID + Value</div></div>
<div class="kb-diagram-note">문제: Wireshark 같은 패킷 캡처 도구로 커뮤니티 스트링이 그대로 노출됨!</div>
</div>
</div>



### 커뮤니티 스트링 유형

실무에서는 권한에 따라 2가지를 나누어 설정한다.

| 유형 | 허용 작업 | 기본값 | 위험도 |
| :--- | :--- | :--- | :--- |
| **RO (Read-Only)** | 정보 조회(Get)만 가능 | `public` | 중 (정보 노출) |
| **RW (Read-Write)** | 설정 변경(Set)까지 가능 | `private` | 최고 (설정 변조 가능) |

### SNMPv1 PDU 유형

| PDU 유형 | 방향 | 설명 |
| :--- | :--- | :--- |
| Get-Request | 매니저 → 에이전트 | 특정 OID 값 요청 |
| Get-Next-Request | 매니저 → 에이전트 | 다음 OID 값 요청 (트리 순회) |
| Set-Request | 매니저 → 에이전트 | OID 값 변경 요청 |
| Get-Response | 에이전트 → 매니저 | 요청에 대한 응답 |
| Trap | 에이전트 → 매니저 | 비동기 이벤트 알림 |

### SNMPv2c의 개선 사항 - GetBulk



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">SNMPv1 방식 - 대량 데이터 조회시 비효율</div></div>
<div class="kb-diagram-note">매니저 에이전트</div>
<div class="kb-diagram-tree-item" style="--depth:0">Get-Request(ifDescr.1) ──→</div>
<div class="kb-diagram-note">←── Get-Response("GE0/0/1") ──</div>
<div class="kb-diagram-tree-item" style="--depth:0">Get-Request(ifDescr.2) ──→</div>
<div class="kb-diagram-note">←── Get-Response("GE0/0/2") ──</div>
<div class="kb-diagram-note">... (100번 반복) ...</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">SNMPv2c 방식 - GetBulk로 한 번에 처리</div></div>
<div class="kb-diagram-note">매니저 에이전트</div>
<div class="kb-diagram-tree-item" style="--depth:0">GetBulk(ifDescr, max-repetitions=100) ──→</div>
<div class="kb-diagram-note">←── Get-Response("GE0/0/1","GE0/0/2",...,"GE0/0/100") ──</div>
<div class="kb-diagram-note">효과: 네트워크 왕복(RTT) 100회 → 1회로 단축!</div>
</div>
</div>



### SNMPv1 vs SNMPv2c 핵심 비교

| 항목 | SNMPv1 | SNMPv2c |
| :--- | :--- | :--- |
| 발표 연도 | 1988 (RFC 1067) | 1993 (RFC 1901) |
| 보안 방식 | 커뮤니티 스트링 평문 | 동일 (개선 없음) |
| 대량 조회 | Get-Next 반복 | **GetBulk** (한 번에) |
| 에러 처리 | 기본 수준 | 개선된 에러 코드 |
| 64비트 카운터 | 미지원 | 지원 (Counter64) |
| Trap 방식 | v1 Trap (확인 없음) | Inform (수신 확인 있음) |
| 현재 사용 | 레거시 구형 장비 | 여전히 광범위 사용 |

- **📢 섹션 요약 비유**: SNMPv1/v2c의 커뮤니티 스트링은 열쇠를 종이에 적어서 공개 우편으로 보내는 것과 같다. 받는 사람(에이전트)은 열쇠를 받아 문을 열어주지만, 중간에 누구든 그 열쇠를 복사할 수 있다.

---

## Ⅲ. 비교 및 연결

### 보안 관점의 SNMP 버전 비교

| 항목 | SNMPv1 | SNMPv2c | SNMPv3 |
| :--- | :--- | :--- | :--- |
| 인증 방식 | 커뮤니티 스트링 | 커뮤니티 스트링 | 사용자 인증 (MD5/SHA) |
| 암호화 | 없음 (평문) | 없음 (평문) | DES/AES 암호화 |
| 무결성 보장 | 없음 | 없음 | HMAC 기반 |
| 접근 제어 | Community 기반 | Community 기반 | VACM (세분화) |
| 메시지 재전송 방지 | 없음 | 없음 | 타임스탬프 기반 |
| 보안 수준 | 매우 낮음 | 낮음 | 높음 |
| 구현 복잡도 | 낮음 | 낮음 | 높음 |

### 알려진 취약점과 공격 유형

| 공격 유형 | 원리 | 피해 |
| :--- | :--- | :--- |
| **패킷 스니핑** | Wireshark로 커뮤니티 스트링 캡처 | 관리 정보 탈취, 설정 변조 |
| **브루트포스** | 일반적인 커뮤니티 스트링 시도 | public/private 기본값 악용 |
| **Trap 위조** | 가짜 Trap 패킷 전송 | NMS 오경보 유발 |
| **정보 수집** | RO 권한으로 네트워크 지도 작성 | APT 공격 초기 정찰 |
| **설정 변조** | RW 권한으로 라우팅 테이블 변경 | 서비스 중단, 트래픽 우회 |

- **📢 섹션 요약 비유**: SNMPv1/v2c 환경에서 기본 커뮤니티 스트링(public/private)을 방치하는 것은, 집 열쇠 복제본을 "열쇠"라고 써 붙인 현관문 앞 화분 밑에 두는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### v1/v2c 사용 시 최소한의 보안 조치



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">보안 강화 단계</div></div>
<div class="kb-diagram-note">1단계: 기본값 변경 필수</div>
<div class="kb-diagram-tree-item" style="--depth:1">"public" → 복잡한 문자열로 변경</div>
<div class="kb-diagram-tree-item" style="--depth:1">"private" → 더욱 복잡한 문자열로 변경</div>
<div class="kb-diagram-tree-item" style="--depth:1">예: "Xk9#mP2@rQ7$" (대소문자+숫자+특수문자 12자 이상)</div>
<div class="kb-diagram-note">2단계: ACL로 NMS IP 제한</div>
<div class="kb-diagram-note">! Cisco IOS 예시</div>
<div class="kb-diagram-note">access-list 10 permit 192.168.1.100 (NMS 서버 IP만 허용)</div>
<div class="kb-diagram-note">snmp-server community Xk9#mP2@rQ7$ RO 10</div>
<div class="kb-diagram-note">3단계: Management VLAN 분리</div>
<div class="kb-diagram-tree-item" style="--depth:1">SNMP 트래픽을 별도 관리 VLAN (VLAN 99 등)으로 격리</div>
<div class="kb-diagram-tree-item" style="--depth:1">방화벽으로 UDP 161/162 포트를 NMS 서버만 허용</div>
<div class="kb-diagram-note">4단계: SNMPv3 전환 로드맵 수립</div>
<div class="kb-diagram-tree-item" style="--depth:1">레거시 장비는 v2c 유지 + 보완책 적용</div>
<div class="kb-diagram-tree-item" style="--depth:1">신규 장비는 반드시 v3로 구성</div>
</div>
</div>



### 설계 판단 체크리스트

1. **커뮤니티 스트링이 기본값(public/private)인가?**: 즉시 변경 필요. 이것이 가장 흔하고 치명적인 보안 실수다.
2. **RW(Read-Write) 커뮤니티 스트링이 필요한가?**: 가능하면 Get-Request만 허용하는 RO로 운영하고, Set이 필요하면 별도 엄격한 관리가 필요하다.
3. **SNMP 접근이 모든 IP에서 가능한가?**: ACL로 NMS 서버 IP만 허용해야 한다.
4. **SNMP 트래픽이 일반 업무망과 같은 VLAN인가?**: Management VLAN 분리로 스니핑 가능 범위를 최소화해야 한다.
5. **SNMPv3 전환 계획이 있는가?**: 신규 도입 장비는 v3로 구성하고, 레거시 장비도 펌웨어 업그레이드 일정을 잡아야 한다.

### 안티패턴

- **기본값 방치**: `public` / `private` 커뮤니티 스트링을 그대로 두면 자동화 스캐너로 수 초 내에 탈취된다.
- **RW 커뮤니티 무분별 배포**: NMS만이 아니라 여러 서버에 RW 커뮤니티를 알려주면, 하나의 서버 침해로 네트워크 전체 설정이 위험에 처한다.
- **SNMP 미사용 포트 개방**: 모니터링하지 않는 장비도 SNMP가 활성화되어 있으면 공격 표면이 된다. 불필요한 장비는 SNMP를 비활성화해야 한다.
- **v3 전환 무기한 연기**: "레거시라서 어쩔 수 없다"는 이유로 v3 전환을 미루면 보안 부채가 쌓인다.

- **📢 섹션 요약 비유**: 클럽(라우터)에 들어갈 때 기도(에이전트)가 "암호가 뭐냐?"라고 묻는다. 내가 "열려라 참깨(Community String)"라고 동네가 떠나가라 큰 소리(평문 전송)로 대답하면 기도가 문을 열어준다. 문제는 옆에서 숨어 듣고 있던 도둑(해커)도 그 암호를 외워서 밤에 클럽 금고를 다 털어간다는 것이다.

---

## Ⅴ. 기대효과 및 결론

SNMPv1/v2c는 네트워크 관리 자동화의 역사에서 빼놓을 수 없는 기반 기술이다. GetBulk(v2c)의 도입은 대규모 네트워크 모니터링 효율을 10배 이상 향상시켰고, 수십 년간 업계 표준으로 기능해왔다.

그러나 커뮤니티 스트링의 평문 전송이라는 구조적 결함은 현대 보안 관점에서 용납되기 어렵다. 실제로 여러 네트워크 침해 사고에서 SNMP Community String 탈취가 초기 정찰 단계에 활용된 사례가 다수 보고되어 있다.

| 기대 효과 | 내용 |
| :--- | :--- |
| **운영 단순성** | 구현이 단순하여 모든 SNMP 지원 장비에서 즉시 사용 가능 |
| **레거시 호환성** | 구형 장비 포함 이기종 환경 통합 관리 가능 |
| **자동화 기반** | NMS 통합 모니터링, 임계치 알림 자동화 |
| **비용 절감** | 별도 에이전트 없이 내장 SNMP로 관리 자동화 |

**미래 방향**: SNMPv3로의 전환이 업계 표준 권고사항이며, 장기적으로는 NETCONF/YANG, gRPC 기반 스트리밍 텔레메트리가 SNMP를 대체해 나갈 전망이다. 그러나 기설치 레거시 장비의 방대한 규모를 고려하면, v1/v2c의 보완 관리 지식은 당분간 실무에서 계속 필요하다.

- **📢 섹션 요약 비유**: SNMPv1/v2c는 자물쇠는 달려 있지만 열쇠가 투명한 금고다. 금고 자체는 쓸 수 있지만, 중요한 것을 보관하기 전에 열쇠를 불투명하게 만드는 작업(ACL, VLAN 분리, 커뮤니티 스트링 변경)이 반드시 필요하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [SNMP](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/528_snmp_simple_network_management_protocol/) | SNMPv1/v2c의 기반 프로토콜 체계 |
| [MIB/OID](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/529_mib_oid_snmp_architecture/) | 커뮤니티 스트링으로 접근하는 관리 정보 구조 |
| [SMI](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/530_smi_structure_of_management_information/) | MIB 객체 정의 언어 규칙 |
| [SNMPv3](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/532_snmp_v3_security_authentication_encryption/) | v1/v2c의 보안 결함을 해결한 차세대 버전 |
| ACL (접근 제어 목록) | v1/v2c 환경에서 NMS IP 제한으로 보안 보완 |
| Management VLAN | SNMP 트래픽 분리로 스니핑 위험 최소화 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">SNMPv1 (1988) - 단순 Get/Set, 커뮤니티 스트링 평문 전송</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">SNMPv2 보안 실패 (1993) - 복잡한 보안 체계, 구현 어려움으로 실패</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">SNMPv2c 타협 (1996) - 성능 개선(GetBulk) + 보안은 v1과 동일</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">보안 침해 사례 증가 - SNMP Community String 탈취 공격 빈발</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">SNMPv3 표준화 (1999) - 사용자 인증 + 메시지 암호화 도입</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">NETCONF/YANG (2006) - 설정 자동화에 더 적합한 차세대 프로토콜</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">현재: v2c 레거시 유지 + v3 병행 + 스트리밍 텔레메트리 전환 추진</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. SNMPv1/v2c는 네트워크 장비에게 "비밀번호는 public이야"라고 크게 소리쳐서 들어가는 방식이에요. 누구든 그 소리를 들으면 비밀번호를 알 수 있어요.
2. v2c는 v1보다 훨씬 빠르게 많은 정보를 가져올 수 있는 GetBulk 기능이 생겼지만, 비밀번호는 여전히 크게 소리쳐야 해요.
3. 그래서 나중에 나온 SNMPv3는 비밀번호를 속삭이고 암호화까지 해서 중간에 누가 들어도 알 수 없게 만들었어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 652 / 1120

← **이전**: [530. SMI (Structure of Management Information)](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/530_smi_structure_of_management_information/)
**다음**: [532. SNMPv3 (사용자 기반 인증, 메시지 암호화 지원 DES/AES)](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/532_snmp_v3_security_authentication_encryption/) →

---
