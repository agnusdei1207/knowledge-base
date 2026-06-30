---
title: "합의 알고리즘 (Consensus Algorithm)"
date: "2026-06-30"
weight: 2
tags:
  - "exam-cspe-ict-convergence"
---

## Ⅰ. 정의
> 중앙 통제 없이 분산 노드들이 원장의 단일 상태에 동의하도록 하는 메커니즘으로, 비잔틴 장애(악의 노드) 환경에서도 합의를 보장한다.

## Ⅱ. 구성요소 / 원리
- PoW(Proof of Work): 해시 퍼즐 연산 경쟁, 채굴자가 블록 생성권 획득(비트코인)
- PoS(Proof of Stake): 지분(코인 보유·예치)에 비례해 검증자 선정(이더리움 2.0)
- PBFT(Practical Byzantine Fault Tolerance): 노드 간 투표로 합의, 3f+1 노드로 f개 악의 노드 허용
- DPoS·PoA: 위임·권한 기반 변형으로 처리속도 개선

## Ⅲ. 흐름도 / 구조
```text
[블록 후보] → [검증자 선정]
   PoW : 연산경쟁 → 최초 해시 발견자
   PoS : 지분 가중 무작위 선정
   PBFT: Pre-prepare→Prepare→Commit(2/3 투표)
        → [블록 확정·전파]
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 비잔틴 환경에서 단일 진실 상태 합의 |
| 장점 | 위·변조 방지, 탈중앙 신뢰 형성 |
| 한계 | PoW 에너지 과다, PBFT 노드 수 확장 제약 |

## Ⅴ. 기술사적 적용
- 퍼블릭 체인은 PoW/PoS, 컨소시엄은 PBFT 계열 선택
- 이더리움 머지로 PoW→PoS 전환, 에너지 99% 절감
- 처리량·최종성(Finality)·탈중앙성 트레이드오프 고려한 선정
