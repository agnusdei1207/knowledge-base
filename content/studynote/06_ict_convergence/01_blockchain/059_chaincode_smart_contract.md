---
title: 59. 체인코드 (Chaincode) - 하이퍼레저의 스마트 컨트랙트
date: '2026-04-19'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 체인코드(Chaincode)는 Hyperledger Fabric에서 실행되는 비즈니스 규칙 코드로, [[022_smart_contract|스마트 컨트랙트]] 역할을 한다.
> 2. **가치**: 승인 [[164_policy|정책]](Endorsement [[164_policy|Policy]])과 [[136_variance|분산]] 원장 구조를 함께 써서 권한·[[606_auditing_linux_auditd|감사]] 요구가 강한 기업 환경에 맞는다.
> 3. **판단 포인트**: 결정성(determinism), World [[272_state_pattern|State]] vs Ledger, 설치(Install)·승인(Commit)·업그레이드 절차를 분리해서 봐야 한다.

---

## Ⅰ. 개요 및 필요성

퍼블릭 블록체인은 누구나 참여하는 개방성이 강점이지만, 기업은 오히려 참여자와 권한을 제한해야 한다. 체인코드는 이런 프라이빗/퍼미션드 환경에서 계약 조건과 업무 규칙을 코드로 고정한다.

즉, 체인코드는 원장에 들어갈 값을 직접 수정하는 프로그램이 아니라, "이 트랜잭션을 받아들여도 되는가"를 판단하고 상태 변경을 제안하는 실행 단위다.

- **📢 섹션 요약 비유**: 회사 규정을 적어 둔 자동 도장 기계처럼, 승인된 요청만 장부를 바꾸게 하는 장치다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Fabric의 체인코드는 클라이언트 요청을 받아 상태를 조회하고, [[395_verification_process_review|검증]] 가능한 결과를 만들어 낸다. 실행은 보통 [[063_docker_architecture|Docker]] [[561_container_based_deployment|컨테이너]] 안에서 이루어져 노드와 분리된다.

```text
Client
  ↓ proposal
Endorsing Peer
  ↓ simulate
Chaincode
  ↓ endorsement
Ordering Service
  ↓ block
Committing Peers
  ├─ World State
  └─ Ledger
```

| 구성 요소 | 역할 |
| :-- | :-- |
| Chaincode | 비즈니스 규칙과 상태 변경 로직 |
| Endorsement [[164_policy|Policy]] | 누가 서명해야 유효한지 정의 |
| World [[272_state_pattern|State]] | 현재 최신 상태를 저장하는 [[127_key_value_db|Key-Value DB]] |
| Ledger | 변경 이력을 시간순으로 보관하는 원장 |

체인코드는 `GetState`, `PutState` 같은 API로 상태를 다룬다. 중요한 점은 같은 입력이면 같은 결과를 내는 결정성 코드여야 하며, 시간·난수·외부 네트워크 의존은 최대한 피해야 한다.

- **📢 섹션 요약 비유**: 여러 사람이 같은 장부를 보면서 도장을 찍는 회계 사무실과 같다.

---

## Ⅲ. 비교 및 연결

체인코드는 Ethereum의 [[022_smart_contract|스마트 컨트랙트]]와 목적은 같지만 운영 방식이 다르다.

| 항목 | [[058_hyperledger_fabric_private_blockchain|Hyperledger Fabric]] 체인코드 | Ethereum [[022_smart_contract|스마트 컨트랙트]] |
| :-- | :-- | :-- |
| 네트워크 성격 | 퍼미션드(허가형) | 퍼블릭(개방형) |
| 실행 언어 | Go, Node.js, Java 등 | [[057_solidity_smart_contract_language|Solidity]] 중심 |
| 실행 환경 | [[063_docker_architecture|Docker]] [[561_container_based_deployment|컨테이너]] 기반 | [[152_evm_earned_value_management|EVM]] 기반 |
| 거버넌스 | 설치/승인/커밋 절차 필요 | 배포 즉시 활성화 |

Fabric은 World State와 Ledger를 분리한다. World State는 현재 값, Ledger는 변경 증거다. 이 분리는 조회 성능과 [[606_auditing_linux_auditd|감사]] 추적성을 동시에 얻기 위한 핵심 설계다.

- **📢 섹션 요약 비유**: 현재 페이지와 수정 이력을 따로 보관하는 문서 관리 시스템이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 체인코드는 단순한 코드 배포가 아니라, 여러 조직이 합의한 계약의 실행체다.

### [[435_checklist_based_testing|체크리스트]]

1. 체인코드가 결정성을 만족하는가?
2. 엔도र्स먼트 [[164_policy|정책]]이 실제 운영 거버넌스와 맞는가?
3. 상태 변경과 [[606_auditing_linux_auditd|감사]] 이력 분리가 명확한가?
4. 업그레이드와 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 절차가 정의되어 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 체인코드 안에서 시간, 난수, 외부 API에 의존하는 설계
- 승인 [[164_policy|정책]] 없이 누구나 상태를 바꾸는 설계
- 월드 스테이트만 보고 원장 추적을 포기하는 설계

### 실무 시나리오

- 물류 추적: 출고/입고 이벤트를 체인코드로 기록
- 무역 금융: 다자 승인 후 결제 조건 자동 실행
- [[520_supply_chain_attack_and_ci_cd_security|공급망]]: 참여사별 권한을 제한한 상태에서 이력 공유

- **📢 섹션 요약 비유**: 주문서에 도장이 다 찍혀야 서류가 넘어가는 전자 결재 시스템이다.

---

## Ⅴ. 기대효과 및 결론

체인코드는 블록체인을 "기록 저장소"에서 "업무 실행 플랫폼"으로 바꾼다. 그래서 [[606_auditing_linux_auditd|감사]] 추적성, 권한 통제, 다자 합의가 중요한 업종에 특히 유리하다.

다만 배포 절차가 복잡하고, 코드가 곧 규칙이 되기 때문에 설계 오류가 곧 운영 리스크가 된다. 결국 체인코드는 기술보다 거버넌스가 먼저인 소프트웨어다.

- **📢 섹션 요약 비유**: 모두가 함께 쓰는 계약서에 자동 계산기를 붙여 놓은 것과 같다.

---

## 관련 개념 맵

```text
비즈니스 규칙
   ↓
체인코드(Chaincode)
   ↓
Endorsement Policy
   ↓
World State / Ledger
```

---

## 관련 키워드 및 발전 흐름도

```text
스마트 컨트랙트
   ↓
Hyperledger Fabric
   ↓
체인코드 설치/승인/커밋
   ↓
분산 원장 상태 갱신
   ↓
감사 가능한 업무 자동화
```

---

## 어린이를 위한 3줄 비유 설명

체인코드는 여러 사람이 같이 쓰는 공책에 자동으로 규칙을 적용하는 프로그램이에요.  
아무 요청이나 받는 게 아니라, 먼저 약속된 도장을 확인해요.  
그래서 기록도 남고, 나중에 누가 바꿨는지도 알 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 59 / 552

← **이전**: [[058_hyperledger_fabric_private_blockchain|58. 하이퍼레저 패브릭 (Hyperledger Fabric) - 허가형 기업용 블록체인]]
**다음**: [[060_hyperledger_architecture_peer_orderer_msp|60. 하이퍼레저 아키텍처 - 피어(Peer), 오더러(Orderer), MSP(Membership Service Provider)]] →

---
