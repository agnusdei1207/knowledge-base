---
title: "Blockchain Trilemma 블록체인 트릴레마 (Blockchain Trilemma)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 348
extra:
  question_no: "348"
  exam_status: "기출"
  exam_history: "125회"
---

## 미리 알고가기

- 블록체인 트릴레마는 탈중앙화와 보안성과 확장성을 동시에 극대화하기 어렵다는 구조적 긴장을 설명하는 개념임
- 처리량을 높이는 선택이 검증자 수를 줄이거나 합의 신뢰를 약화시킬 수 있음
- L2와 샤딩과 모듈형 아키텍처는 이 tradeoff를 완화하려는 접근으로 이해하면 됨

## Ⅰ. 개요

- **정의/개념**: Blockchain Trilemma는 블록체인 설계에서 탈중앙화와 보안성과 확장성 세 목표를 동시에 최대로 달성하기 어렵고 하나를 강화하면 나머지 중 하나 이상과 충돌하기 쉬운 구조적 제약을 설명하는 개념임
- **배경/필요성**: 블록체인이 금융과 서비스 플랫폼으로 확장되면서 높은 처리량을 요구받지만 분산 합의 특성상 검증 비용과 네트워크 지연과 공격 저항성 사이의 충돌이 뚜렷해짐

## Ⅱ. 특징

- 세 요소는 독립 지표가 아니라 합의 구조와 검증 비용에서 서로 얽혀 있음
- 블록 크기와 검증자 수와 상태 저장 부담이 tradeoff의 핵심 변수가 됨
- L1과 L2와 모듈형 설계가 각기 다른 타협점을 제시함
- 트릴레마 해소를 주장하는 설계도 실제로는 목표 간 우선순위를 재배치하는 경우가 많음

## Ⅲ. 종류 및 비교

| 판단 기준 | Monolithic L1 | Layer 2 / Rollup | Permissioned Chain |
|:---|:---|:---|:---|
| 탈중앙화 | 높음 가능 | L1 의존 | 낮거나 제한적 |
| 보안성 | 합의 구조에 의존 | L1 보안 활용 | 참여자 신뢰에 의존 |
| 확장성 | 제한적 | 높음 지향 | 상대적으로 높음 |
| 대표 tradeoff | 처리량 제약 | 복잡한 브리지 | 신뢰 중앙화 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Decentralization Dimension | 검증자 수와 참여 개방성과 노드 실행 비용이 분산 신뢰 수준을 결정하는 축임 |
| Security Dimension | 합의 공격 저항성과 검증 무결성과 상태 일관성이 체인의 안전성을 형성하는 축임 |
| Scalability Dimension | 처리량과 지연과 상태 성장 관리가 대규모 사용자 수용 능력을 결정하는 축임 |
| Consensus and Network Design | 블록 생성과 전파와 검증 구조가 세 축의 균형점을 실제로 결정하는 설계 계층임 |
| Off chain or Modular Extension | 롤업과 샤딩과 데이터 가용성 분리가 트릴레마 부담을 완화하려는 확장 계층임 |

```text
+------------------+
| Decentralization |
+------------------+
         / \
        /   \
       v     v
+-------------+    +-------------+
| Security    |<-->| Scalability |
+-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 목표 우선순위 정의 | -> | 합의/검증 구조 선택 | -> | 확장 전략 설계 | -> | 보안/노드 비용 평가 | -> | 균형점 조정     |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **목표 우선순위 정의**: 탈중앙화와 보안성과 확장성 우선순위를 정함
2. **합의와 검증 구조 선택**: 블록 생성과 검증 방식을 설계함
3. **확장 전략 설계**: L2나 샤딩 같은 보완 구조를 선택함
4. **보안과 노드 비용 평가**: 공격 저항성과 참여 비용을 점검함
5. **균형점 조정**: 목표 간 tradeoff를 다시 조정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 처리량 확대만 우선하면 검증 노드 요구사항이 커져 실제 참여자 수가 줄고 탈중앙화가 약화될 수 있음
   - 해결방안: node participation budget review와 scalable verification design을 적용하고 full node accessibility score와 validator participation diversity로 검증함
2. 문제: 보안과 확장성을 외부 브리지나 L2에 의존할 때 경계 설계가 약하면 새로운 공격 표면이 커질 수 있음
   - 해결방안: bridge security assurance와 layered risk assessment를 적용하고 cross layer incident count와 secured bridge asset coverage로 검증함
3. 문제: 트릴레마 논의를 추상 수준에만 두면 실제 서비스 요구에 맞는 체인 설계 우선순위를 정하지 못할 수 있음
   - 해결방안: workload specific chain architecture review와 explicit tradeoff documentation을 적용하고 architecture decision traceability score와 workload fit satisfaction rate로 검증함

## Ⅶ. 적용 사례

- 프로토콜 설계팀이 노드 참여 비용 검토를 운영하며 확인 지표는 full node accessibility score와 validator participation diversity임
- 멀티체인 서비스가 브리지 보안 보증을 적용하며 확인 지표는 cross layer incident count와 secured bridge asset coverage임
- 플랫폼 아키텍트가 워크로드별 체인 검토를 수행하며 확인 지표는 architecture decision traceability score와 workload fit satisfaction rate임

## Ⅷ. 결론

블록체인 트릴레마는 세 가지를 동시에 버리는 문제가 아니라 어떤 목표를 어디까지 양보할지 명시적으로 설계하라는 요구이므로 서비스 요구 기반 우선순위가 필수임.
