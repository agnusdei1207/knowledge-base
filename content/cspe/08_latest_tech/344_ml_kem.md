---
title: "ML-KEM (Module-Lattice Key Encapsulation Mechanism)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 344
extra:
  question_no: "344"
  exam_status: "기출"
  exam_history: "136회"
  exam_note: "전망"
---

## 미리 알고가기

- ML-KEM은 모듈 격자 문제 기반의 양자내성 키 캡슐화 메커니즘임
- 기존 ECDH 같은 키 교환을 대체하거나 하이브리드로 함께 쓰는 방향이 일반적임
- 공개키와 ciphertext 크기와 구현 보안이 실제 도입의 핵심 고려사항임

## Ⅰ. 개요

- **정의/개념**: ML-KEM은 모듈 격자 기반 난제를 이용해 상대방의 공개키로 공유 비밀을 안전하게 캡슐화하고 상대방이 비공개키로 이를 복원하도록 설계된 양자내성 키 교환용 공개키 암호 기법임
- **배경/필요성**: 양자컴퓨터가 기존 공개키 교환 방식을 위협할 수 있어 TLS와 VPN와 메시징에서 장기적으로 안전한 공유 비밀 생성 수단이 필요해짐

## Ⅱ. 특징

- 양자내성 공개키 교환 수단으로 classical protocol에 상대적으로 쉽게 통합 가능함
- encapsulation과 decapsulation 구조가 분명해 프로토콜 적용이 명확함
- 기존 방식보다 공개키와 ciphertext 크기가 커질 수 있음
- 구현 취약점과 side channel 방어가 부족하면 수학적 안전성과 별개로 실용 보안이 무너질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | ECDH Key Exchange | ML-KEM | Hybrid ECDH + ML-KEM |
|:---|:---|:---|:---|
| 양자내성 | 낮음 | 높음 | 높음 |
| 성숙도 | 매우 높음 | 전환 단계 | 전환 실무형 |
| 키/메시지 크기 | 작음 | 큼 | 더 큼 |
| 대표 활용 | 기존 TLS | PQC 전환 | 단계적 migration |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Key Generation | 공개키와 비밀키를 생성해 양자내성 키 교환의 기본 자격 정보를 준비하는 시작 계층임 |
| Encapsulation Algorithm | 수신자 공개키를 사용해 공유 비밀과 ciphertext를 생성해 전달 가능한 형태로 보호하는 송신 계층임 |
| Decapsulation Algorithm | 수신자가 비밀키로 ciphertext를 복원해 동일한 공유 비밀을 얻는 수신 계층임 |
| Parameter Set and Security Level | 보안 강도와 성능과 크기 tradeoff를 결정해 환경별 적용 선택의 기준이 되는 정책 계층임 |
| Hybrid Protocol Integration | 기존 키 교환과 함께 결합해 상호운용성과 미래 안전성을 동시에 확보하는 실무 통합 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| KeyGen      | -> | Encapsulate | -> | Ciphertext  | -> | Decapsulate |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 키쌍 생성     | -> | 공개키 전달   | -> | encapsulate 수행 | -> | ciphertext 전송 | -> | decapsulate 복원 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **키쌍 생성**: 수신자가 공개키와 비밀키를 생성함
2. **공개키 전달**: 송신자가 공개키를 획득함
3. **encapsulate 수행**: 송신자가 공유 비밀과 ciphertext를 생성함
4. **ciphertext 전송**: 보호된 값을 수신자에게 전달함
5. **decapsulate 복원**: 수신자가 동일한 공유 비밀을 복원함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 큰 키와 ciphertext를 기존 프로토콜에 그대로 넣으면 핸드셰이크 지연과 패킷 분할 문제가 커질 수 있음
   - 해결방안: transport size benchmarking과 handshake fragmentation tuning을 적용하고 handshake completion latency와 packet fragmentation rate로 검증함
2. 문제: decapsulation 과정의 오류 처리나 side channel 방어가 약하면 비밀키 유출 위험이 생길 수 있음
   - 해결방안: constant time implementation과 failure handling hardening을 적용하고 side channel test pass rate와 decapsulation failure leakage score로 검증함
3. 문제: 전환 초기에 상대 시스템 지원 수준이 달라 단독 ML-KEM 적용이 상호운용성 문제를 일으킬 수 있음
   - 해결방안: hybrid handshake strategy와 capability negotiation policy를 적용하고 successful hybrid session ratio와 interoperability failure count로 검증함

## Ⅶ. 적용 사례

- TLS 전환 팀이 전송 크기 벤치마킹을 운영하며 확인 지표는 handshake completion latency와 packet fragmentation rate임
- 암호 구현팀이 constant time 방어를 적용하며 확인 지표는 side channel test pass rate와 decapsulation failure leakage score임
- 보안 아키텍처가 하이브리드 핸드셰이크를 적용하며 확인 지표는 successful hybrid session ratio와 interoperability failure count임

## Ⅷ. 결론

ML-KEM은 PQC 전환의 핵심 키 교환 수단이지만 크기와 구현 보안을 함께 다뤄야 실제 프로토콜 전환이 안정적으로 진행됨.
