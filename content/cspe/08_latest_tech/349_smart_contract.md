---
title: "Smart Contract 스마트 계약 (Smart Contract)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 349
extra:
  question_no: "349"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- Smart Contract는 블록체인 위에서 조건 충족 시 상태 전이를 자동 실행하는 프로그램 가능한 계약 로직임
- 법률 계약 전체를 대체한다기보다 합의된 조건의 자동 집행 부분을 디지털화하는 구조로 보는 편이 정확함
- 코드 취약점과 oracle 의존성과 업그레이드 거버넌스가 핵심 운영 리스크임

## Ⅰ. 개요

- **정의/개념**: Smart Contract는 블록체인 가상머신 위에서 실행되며 사전에 정의된 조건과 규칙에 따라 자산 이동과 상태 변경을 자동 수행하는 불변성 기반의 프로그램형 계약 로직임
- **배경/필요성**: 중개자 없이도 거래 조건을 투명하게 집행하려는 요구와 디지털 자산 및 탈중앙 서비스 확산이 결합되면서 자동 실행 가능한 계약 메커니즘이 중요해짐

## Ⅱ. 특징

- 배포된 코드가 합의된 상태 머신으로 작동해 자동 집행과 추적성이 높음
- 자산 이전과 권한 검증과 조건 분기를 온체인 상태 전이로 처리함
- DeFi와 NFT와 DAO 같은 응용 서비스의 핵심 실행 기반이 됨
- 한번 배포된 코드의 오류 수정과 거버넌스 변경이 어렵다는 구조적 제약이 큼

## Ⅲ. 종류 및 비교

| 판단 기준 | Traditional Contract | Smart Contract | Off-chain Workflow Automation |
|:---|:---|:---|:---|
| 집행 방식 | 사람과 기관 중심 | 코드 자동 집행 | 중앙 시스템 자동화 |
| 투명성 | 문서 해석 의존 | 온체인 추적 가능 | 시스템 로그 의존 |
| 변경 용이성 | 협상 기반 수정 | 배포 후 제한적 | 운영자 변경 가능 |
| 대표 리스크 | 해석 분쟁 | 코드 취약점 | 중앙 장애와 조작 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Contract Code | 상태 변수와 함수와 조건 분기를 정의해 실제 계약 집행 논리를 구현하는 실행 핵심부임 |
| Blockchain VM and Consensus | 노드들이 같은 코드와 상태 전이를 검증해 계약 결과를 공통 원장으로 유지하는 기반 계층임 |
| State Storage | 잔고와 권한과 거래 상태를 저장해 계약 실행의 지속 상태를 관리하는 데이터 계층임 |
| Trigger and Transaction Interface | 사용자의 호출과 이벤트와 자산 전송을 받아 계약 실행을 시작하는 입력 계층임 |
| Oracle and Governance Layer | 외부 데이터 연계와 업그레이드 권한을 관리해 현실 세계 연동과 운영 통제를 담당하는 확장 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Transaction | -> | Contract    | -> | VM /        | -> | State /     |
| / Trigger   |    | Code        |    | Consensus   |    | Events      |
+-------------+    +-------------+    +-------------+    +-------------+
        ^
        |
+-------------+
| Oracle / Gov|
+-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 트랜잭션 제출  | -> | 조건 검사     | -> | 상태 전이 실행 | -> | 합의/블록 반영 | -> | 이벤트/자산 처리 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **트랜잭션 제출**: 사용자가 함수 호출이나 자산 전송을 요청함
2. **조건 검사**: 계약 코드가 권한과 조건을 확인함
3. **상태 전이 실행**: 조건 충족 시 내부 상태를 변경함
4. **합의와 블록 반영**: 네트워크가 상태 변경을 검증하고 기록함
5. **이벤트와 자산 처리**: 결과 이벤트와 자산 이동을 확정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 코드 취약점이 배포 후 발견되면 자산 손실과 서비스 중단으로 이어질 수 있지만 수정은 쉽지 않을 수 있음
   - 해결방안: formal verification plus audit pipeline과 staged contract release를 적용하고 critical vulnerability escape rate와 post deployment incident count로 검증함
2. 문제: 외부 가격이나 현실 데이터에 의존하는 oracle이 신뢰되지 않으면 온체인 로직도 잘못된 결과를 실행할 수 있음
   - 해결방안: multi source oracle governance와 oracle failure fallback rule을 적용하고 oracle discrepancy detection rate와 oracle induced contract incident count로 검증함
3. 문제: 업그레이드 가능 계약은 운영 유연성을 주지만 관리자 권한 집중이 커져 탈중앙 신뢰를 약화시킬 수 있음
   - 해결방안: timelock plus multisig governance와 privileged action transparency를 적용하고 governed upgrade coverage와 admin trust exception count로 검증함

## Ⅶ. 적용 사례

- DeFi 프로토콜이 정형 검증과 감사 파이프라인을 운영하며 확인 지표는 critical vulnerability escape rate와 post deployment incident count임
- 온체인 서비스가 다중 소스 oracle 거버넌스를 적용하며 확인 지표는 oracle discrepancy detection rate와 oracle induced contract incident count임
- DAO 운영 구조가 timelock 멀티시그를 적용하며 확인 지표는 governed upgrade coverage와 admin trust exception count임

## Ⅷ. 결론

스마트 계약은 자동 실행의 강점만큼 코드와 oracle과 거버넌스가 곧 신뢰의 전부가 되므로 배포 전 검증과 운영 통제가 핵심임.
