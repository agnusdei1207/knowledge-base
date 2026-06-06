---
title: "DAO, Decentralized Autonomous Organization"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/)([Decentralized Autonomous Organization](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/), [탈중앙화](/studynote/06_ict_convergence/01_blockchain/010_decentralization/) 자율 조직)는 [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/)가 조직의 규칙을 코드화하여, <strong>CEO 없이 토큰 홀더의 투표로 의사결정</strong>이 이루어지는 새로운 조직 형태다.
> 2. **가치**: 거버넌스 토큰(Governance Token)과 타임락(Timelock) 메커니즘이 결합되어 악의적 프로포절을 차단하고, 위임 투표(Delegate [Voting](/studynote/10_ai/03_llm_nlp/258_voting_ensemble/))로 일반 홀더도 의사결정에 참여할 수 있다.
> 3. **판단 포인트**: The [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 해킹(2016, $6000만 손실)이 보여주듯 [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 취약점이 거버넌스 공격 벡터가 되므로, [보안 감사](/studynote/04_software_engineering/11_testing_validation/919_security_audit_trail/)([Audit](/studynote/12_it_management/05_security_compliance/363_audit/))와 타임락이 모든 DAO의 필수 요건이다.

---

## Ⅰ. 개요 및 필요성

### 전통 조직 vs [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/)

전통 기업: CEO -> 이사회 -> 직원 계층적 의사결정, 주주는 연 1회 투표. DAO는 [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/)에 규칙이 코드화되어 <strong>24/7 온체인 투표</strong>로 실시간 의사결정이 가능하다.

**DAO가 필요한 이유**:
- [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 파라미터 변경(이자율, 수수료) -> 커뮤니티 합의 필요
- 트레저리(Treasury) 자금 집행 -> 투명한 거버넌스
- [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 업그레이드 -> 코드 변경의 민주적 승인

- **📢 섹션 요약 비유**: — "DAO는 사장 없는 회사 — 직원(토큰 홀더) 모두가 주주이자 의결권자이고, 회사 규칙([스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/))이 자동으로 집행된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 거버넌스 프로세스

```
+-----------------------------------------------------+
|            DAO 거버넌스 사이클                       |
|                                                     |
|  1. 제안(Proposal)                                  |
|     토큰 홀더 -> 스마트 컨트랙트에 제안 제출         |
|     (최소 토큰 보유량 요건: Proposal Threshold)      |
|                                                     |
|  2. 투표(Voting Period, 예: 3일~7일)                 |
|     홀더: 찬성(For) / 반대(Against) / 기권(Abstain) |
|     위임(Delegation): 투표권 위임 가능               |
|                                                     |
|  3. 쿼럼(Quorum) 달성 확인                          |
|     예: 전체 공급량의 4% 이상 참여 필요              |
|                                                     |
|  4. 타임락(Timelock, 예: 2일~7일)                   |
|     승인된 제안 -> 즉시 실행 아님 -> 대기             |
|     이 기간 긴급 철회(Guardian) 가능                |
|                                                     |
|  5. 실행(Execution)                                 |
|     타임락 만료 -> 스마트 컨트랙트 자동 실행          |
+-----------------------------------------------------+
```

### 주요 [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 거버넌스 비교

| [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) | 거버넌스 토큰 | 쿼럼 | 타임락 | 특징 |
|:---|:---:|:---:|:---:|:---|
| **Uniswap** | UNI | 4% | 2일 | [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 수수료 ON/OFF |
| **MakerDAO** | MKR | 다양 | 48시간 | DAI 안정화 파라미터 |
| **Compound** | [COMP](/studynote/03_network/20_performance_evaluation_advanced/1013_comp_coordinated_multipoint_transmission/) | 4% | 2일 | 대출 이자율 조정 |
| **Aave** | AAVE | 다양 | 1일 | [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 파라미터 |

- **📢 섹션 요약 비유**: — "타임락은 투표로 통과된 법안을 즉시 시행하지 않고 2일 공포 기간을 두는 것 — 악의적 법안을 취소할 마지막 기회다.

---

## Ⅲ. 비교 및 연결

### The [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 해킹 사건 (2016)

```
취약 컨트랙트: splitDAO() 함수
공격자: ETH 출금 -> 잔액 차감 전 재진입 -> 반복 출금
피해: 360만 ETH ($6000만, 당시 ETH 공급의 15%)
결과: 이더리움 하드포크 -> ETH / ETC 분리
교훈: DAO 컨트랙트 보안 감사 필수, 타임락 도입
```

### 거버넌스 공격 유형

| 공격 유형 | 방법 | 방어 방법 |
|:---|:---|:---|
| **플래시론 거버넌스 공격** | 거대 토큰 임시 확보 -> 투표 조작 | [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 투표 (보유 기간 기준) |
| **매수 공격(Bribery)** | 투표권 외부 매수 | 위임 투표 분산화 |
| **저쿼럼 통과** | 참여율 낮을 때 소수로 통과 | 쿼럼 최소 요건 높이기 |
| **악의적 업그레이드** | 코드 변경으로 자산 탈취 | 타임락 + Guardian |

- **📢 섹션 요약 비유**: — "[DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 거버넌스 공격은 주주총회에서 가짜 주주가 대거 참여해 불리한 안건을 통과시키는 것 — 타임락이 '잠깐, 다시 확인하자'의 안전장치다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 설계 핵심 파라미터

1. **제안 임계값(Proposal Threshold)**: 너무 낮으면 스팸, 너무 높으면 과두화
2. **쿼럼(Quorum)**: 4%~[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% 일반적, 낮으면 소수 지배
3. **타임락 기간**: 2~7일 일반, 위급 상황 대응 비용
4. **위임 구조**: 전문 위임자(Delegate) 생태계 활성화 필요

### 기술사 핵심 판단
- DAO는 법인격이 없어 법적 보호가 없음 -> Wyoming [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) [LLC](/studynote/01_computer_architecture/15_advanced_topics/744_load_line_calibration/) 등 법적 구조 연구 필요
- 투표 참여율(Voter Apathy) 문제: Compound [COMP](/studynote/03_network/20_performance_evaluation_advanced/1013_comp_coordinated_multipoint_transmission/) 투표 참여율 2~5% 수준
- **프로그래밍 가능한 규칙의 한계**: 정성적 판단이 필요한 사안은 코드화 어려움
- **멀티시그(Multi-Sig) 병용**: 긴급 대응을 위한 Gnosis [Safe](/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/) 기반 관리자 키

- **📢 섹션 요약 비유**: — "DAO의 이상(理想)은 완전 자율 조직이지만, 현실은 [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/)가 모든 경우를 처리 못하므로 '반자율' 수준에서 운영된다.

---

## Ⅴ. 기대효과 및 결론

| 효과 항목 | 내용 |
|:---|:---|
| **투명한 의사결정** | 모든 투표·실행이 온체인 기록 |
| **글로벌 참여** | 국경 없이 누구나 거버넌스 참여 |
| **인센티브 정렬** | 토큰 홀더 = [이해관계자](/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/) = 의결권자 |
| **새 조직 형태** | 협동조합·[오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)·크라우드펀딩의 Web3 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) |

DAO는 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 기반의 새로운 조직 패러다임이다. 코드화된 규칙과 토큰 인센티브로 국경·법인격 없이 글로벌 협력이 가능하지만, [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 취약점·저참여율·법적 불명확성 등 해결 과제도 존재한다.

- **📢 섹션 요약 비유**: — "DAO는 인터넷 시대의 협동조합 — 출자자(토큰 홀더)가 곧 운영자이고, 규칙은 계약서가 아닌 코드로 자동 실행된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 연결 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 설명 |
| 거버넌스 토큰 | [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 의결권 수단 |
| 타임락 | 악의적 제안 차단 안전장치 |
| The [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 해킹 | [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 역사의 중요 보안 [교훈](/studynote/09_security/13_secops_ir_forensics/659_ir_lessons_learned/) |
| [스마트 컨트랙트](/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) | [DAO](/studynote/06_ict_convergence/01_blockchain/054_dao_decentralized_autonomous_organization/) 규칙 집행 자동화 기반 |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계 설명] -> [DAO 탈중앙화 자율 조직] -> [DAO 규칙 집행 자동화 기반]
```

### 👶 어린이를 위한 3줄 비유 설명

1. DAO는 회장 없는 학생회 — 모든 회원이 토큰(투표권)을 가지고 의견을 낼 수 있어요.
2. 투표로 결정된 일도 바로 실행하지 않고 2~7일 기다리는데, 그 사이 잘못된 결정이면 취소할 수 있어요.
3. 2016년에 해킹으로 큰돈을 잃은 뒤, 지금은 코드를 꼭 검사하고 안전장치를 달아서 운영해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 484 / 552

<- **이전**: [483. 탈중앙화 신원: DID, VC, VP W3C 표준 (Decentralized Identity: DID, VC, VP)](/studynote/06_ict_convergence/01_blockchain/483_did_decentralized_identity_w3c_vc_vp/)
**다음**: [485. 블록체인 공격: 51%, 이클립스, 시빌 (Blockchain Attacks: 51%, Eclipse, Sybil)](/studynote/06_ict_convergence/01_blockchain/485_blockchain_attack_51_eclipse_sybil/) ->

---
