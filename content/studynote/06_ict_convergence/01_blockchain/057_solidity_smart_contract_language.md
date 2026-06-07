---
title: "057. Solidity Smart Contract Language"
date: "2026-06-07"
tags:
  - "ict_convergence"
  - "studynote-ict-convergence"
weight: 57
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 솔리디티(Solidity)는 이더리움에서 스마트 컨트랙트를 작성하기 위한 정적 타입(Statically Typed) 언어다.
> 2. **가치**: 상태 변수, 매핑([mapping](/studynote/05_database/01_db_architecture_relational/010_schema_mapping/)), 주소(address), 이벤트(event) 같은 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 전용 개념을 자연스럽게 다룰 수 있다.
> 3. **판단 포인트**: [EVM](/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) ([Ethereum Virtual Machine](/studynote/06_ict_convergence/01_blockchain/023_evm_ethereum_virtual_machine/)), [Gas](/studynote/06_ict_convergence/01_blockchain/024_gas/), 접근 제어, 보안 패턴을 함께 이해해야 실무 코드가 된다.

---

## Ⅰ. 개요 및 필요성

솔리디티는 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 위에서 자동 실행되는 프로그램을 만들기 위해 고안되었다. 코드가 배포되면 수정이 어렵기 때문에, 언어 자체가 안전성과 명확성을 강하게 요구한다.

이더리움은 단순한 송금 시스템이 아니라 범용 실행 플랫폼이므로, 복잡한 비즈니스 로직도 컨트랙트로 구현할 수 있다.

- **📢 섹션 요약 비유**: 솔리디티는 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 위에 올리는 자동판매기 설명서다.

---

## Ⅱ. 문법과 핵심 특징

솔리디티는 `contract`를 중심으로 코드를 작성한다. 상태 변수와 함수, 이벤트가 하나의 컨트랙트 안에 들어간다.

- **정적 타입**: 자료형을 명확히 선언해야 한다.
- **주소 타입**: 지갑 주소를 안전하게 다룬다.
- <strong>매핑(<a href="/studynote/05_database/01_db_architecture_relational/010_schema_mapping/">mapping</a>)</strong>: 키-값 저장 구조를 제공한다.
- **전역 변수**: `msg.sender`, `msg.value` 같은 실행 문맥 정보를 사용할 수 있다.

```text
contract
 +- state variables
 +- functions
 +- events
 +- modifiers
```

- **📢 섹션 요약 비유**: 부엌에서 그릇, 재료, 조리법을 미리 라벨링해 두는 것과 같다.

---

## Ⅲ. 컴파일과 [가스](/studynote/06_ict_convergence/01_blockchain/024_gas/) 제약

솔리디티 코드는 그대로 실행되지 않고 [EVM](/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) ([Ethereum Virtual Machine](/studynote/06_ict_convergence/01_blockchain/023_evm_ethereum_virtual_machine/))이 이해하는 바이트코드로 컴파일된다.

[블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 실행은 공짜가 아니다. 모든 연산은 Gas를 소비하므로, 저장소 사용과 반복 계산을 줄이는 것이 중요하다.

- **📢 섹션 요약 비유**: 전기를 쓰는 기계처럼, 움직일수록 동전이 빠져나간다.

---

## Ⅳ. 보안과 개발 패턴

솔리디티는 강력하지만 취약점도 많다. 그래서 다음 패턴을 자주 쓴다.

- `require` / `revert` / `assert`로 조건을 검증한다.
- 접근 제어로 관리자 권한을 묶는다.
- Checks-Effects-Interactions 순서를 지켜 재진입을 막는다.
- Solidity 0.8 이후의 기본 산술 검사도 이해한다.

가장 위험한 실수는 외부 호출과 상태 변경 순서를 잘못 두는 것이다.

- **📢 섹션 요약 비유**: 문을 열기 전에 자물쇠부터 거는 습관이 보안을 만든다.

---

## Ⅴ. 실무 적용과 배포 흐름

실무에서는 단순히 문법을 아는 것만으로는 부족하다. 테스트, 배포, 업그레이드, [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)까지 생각해야 한다.

- 단위 테스트와 시뮬레이션을 먼저 돌린다.
- 배포 후에는 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 가능성을 검토한다.
- 업그레이드 가능한 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 패턴도 이해한다.
- [가스](/studynote/06_ict_convergence/01_blockchain/024_gas/) 비용과 상태 저장 비용을 함께 본다.

솔리디티는 "[블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 전용 JavaScript"가 아니라, 돈을 직접 다루는 안전 규칙이 훨씬 더 엄격한 언어다.

- **📢 섹션 요약 비유**: 돈이 들어 있는 장난감 상자는 한 번 잠그면 다시 열기 어렵기 때문에, 처음 설계가 제일 중요하다.

---

## 관련 개념 맵

```text
Solidity
   v
EVM 바이트코드
   v
Gas / 상태 저장
   v
스마트 컨트랙트 배포
```

---

## 관련 키워드 및 발전 흐름도

1. 튜링 완전 언어 -> 복잡한 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 로직 표현
2. contract 중심 구조 -> 상태와 동작 통합
3. [EVM](/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) 바이트코드 -> 이더리움 실행 환경 표준화
4. [가스](/studynote/06_ict_convergence/01_blockchain/024_gas/)와 보안 패턴 -> 비용과 안전성 동시 관리
5. 업그레이드 패턴과 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) -> 실무 배포의 핵심

---

## 어린이를 위한 3줄 비유 설명

솔리디티는 [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/)에서 돌아가는 규칙 책이에요.
책에 적힌 대로만 움직이기 때문에, 처음부터 잘 써야 해요.
돈이 걸려 있어서 장난처럼 쓰면 안 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 57 / 552

<- **이전**: [56. 스마트 컨트랙트 보안 취약점 - 재진입 (Re-entrancy), 오버플로우/언더플로우, 권한 탈취](/studynote/06_ict_convergence/01_blockchain/056_smart_contract_vulnerability_reentrancy/)
**다음**: [58. 하이퍼레저 패브릭 (Hyperledger Fabric) - 허가형 기업용 블록체인](/studynote/06_ict_convergence/01_blockchain/058_hyperledger_fabric_private_blockchain/) ->

---
