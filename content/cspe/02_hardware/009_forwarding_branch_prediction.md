---
title: 파이프라인 포워딩·분기 예측 (Pipeline Forwarding/Branch Prediction)
date: 2026-07-05
tags: ["cspe-hardware"]
weight: 9
---

## Ⅰ. 개요
- 정의: 파이프라인 해저드를 최소화하기 위한 데이터 우회(Forwarding) 및 분기 추측 기술
- 배경: 지연(Stall)으로 인한 파이프라인 성능 손실을 방지하여 처리 속도 유지 필요
- 출제 의도: 데이터 의존성 해결 메커니즘과 조건문 처리 최적화 기법 이해

## Ⅱ. 구성요소
- ASCII 구조도 (Forwarding)
  [EX Stage] --+--> [EX Stage]
               | (Forward Path)
               v
  [Register] --+--> [ALU Input]

- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Forwarding Unit | 연산 결과를 레지스터 저장 전 다음 단계로 전달 | 퀵서비스 |
| Branch Predictor | 분기 명령의 결과(Taken/Not)를 미리 추측 | 예보 |
| BTB (Target Buffer) | 분기될 목적지 주소를 저장하는 캐시 | 즐겨찾기 |
> 요약: 포워딩은 데이터 지연을, 분기 예측은 흐름 지연을 해결함

## Ⅲ. 절차
- ASCII 흐름도
  (Branch Inst) -> (Predict in BTB) -> (Speculative Fetch) -> (Check)
                                                            |
                    +---(Correct)---<---(Flush/Restart)---(Wrong)

- 4단계 설명
1. 감지: 데이터 의존성 발생 시 포워딩 유닛이 소스/타겟 레지스터 매칭 확인
2. 우회: 연산 완료 즉시 결과를 래치에서 가로채 다음 사이클의 ALU 입력으로 주입
3. 예측: 분기 명령 시 과거 이력을 바탕으로 분기 여부 추측 및 해당 주소 로드
4. 확인: 실제 분기 결과 확인 후 예측 실패 시 파이프라인 플러시 및 재시작
> 요약: 예측을 통해 미리 달리고, 실패 시 뒤로 돌아가 수정하는 메커니즘임

## Ⅳ. 문제점
- 예측 실패 비용: 오예측 시 파이프라인에 투입된 명령어 폐기로 성능 급감
- 하드웨어 오버헤드: 복잡한 예측 테이블(PHT) 및 비교 로직으로 면적/전력 증가

## Ⅴ. 개선방안
- (단기) 2-bit Predictor: 상태 천이도를 활용하여 일시적 변화에 대한 내성 강화
- (중기) 전역/지역 혼합 예측: Gshare 등 패턴 기반 예측을 통한 정확도 향상
- (장기) AI 기반 예측: 퍼셉트론(Perceptron) 등 신경망을 활용한 고도화된 예측

## Ⅵ. 전망
- 로드맵: 대용량 TAGE(Tagged Geometric History) 예측기 도입으로 정확도 99% 도전
- CSF: 투적 실행(Speculative) 보안 취약점을 차단하면서도 높은 성능을 유지하는 균형
