---
title: "PUF 물리적 복제 불가 함수 (Physical Unclonable Function)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 83
extra:
  question_no: "083"
  exam_status: "기출"
  exam_history: "125회"
---

## 미리 알고가기

- PUF는 제조 공정의 미세 편차를 이용해 장치 고유 응답을 생성하는 기술임
- challenge-response pair와 fuzzy extractor와 helper data가 핵심 구조임
- 키를 저장하는 대신 필요할 때 재구성한다는 점이 특징임

## Ⅰ. 개요

- **정의/개념**: PUF는 칩 제조 편차에서 발생하는 고유한 물리 특성을 이용해 장치마다 다른 응답이나 키를 생성하게 하는 하드웨어 보안 기술로, 고유성과 재현성과 예측 불가능성을 기반으로 장치 인증과 키 보호에 사용됨
- **배경/필요성**: 장치 안에 고정 키를 저장하면 복제와 추출 위험이 있으므로, 비밀을 저장하지 않고 장치 고유 특성에서 재구성하는 방식이 필요함

## Ⅱ. 특징

- 동일 설계 칩이라도 장치마다 고유한 응답을 가질 수 있음
- 키를 저장하지 않아 비밀 추출 공격면을 줄일 수 있음
- 온도와 전압과 노화에 따른 응답 흔들림 보정이 필수임
- challenge를 과도하게 노출하면 모델링 공격에 취약해질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | 저장형 키 | PUF 기반 키 |
|:---|:---|:---|
| 비밀 보관 | 메모리에 저장 | 물리 특성에서 재구성 |
| 복제 저항 | 복사 가능성 존재 | 공정 편차 복제 어려움 |
| 안정성 | 비교적 높음 | 환경 보정 필요 |
| 운영 초점 | 키 주입과 보관 | 등록과 오류 보정과 CRP 관리 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Physical Entropy Source | SRAM 초기값이나 지연 차이처럼 제조 편차가 실제 고유성을 제공함 |
| Challenge, Response Logic | 입력에 따라 장치 고유 응답을 만들어 인증 재료를 제공함 |
| Fuzzy Extractor | 흔들리는 응답에서 안정적 키를 복원해 실사용 가능성을 높임 |
| Helper Data, Enrollment DB | 복원 보조 정보와 기준 응답을 관리하며 유출 시 직접 키가 드러나지 않아야 함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 등록 단계 측정   | --> | challenge 입력 | --> | 응답 복원/보정  | --> | 인증/키 사용   |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **등록 단계 측정**: 장치의 기준 응답과 helper data를 생성함
2. **Challenge 입력**: 인증 시 입력 자극을 제공함
3. **응답 복원 및 보정**: fuzzy extractor로 안정적 결과를 만듦
4. **인증 및 키 사용**: 장치 확인이나 세션 키 생성에 활용함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 온도와 전압과 노화 변화로 응답이 흔들리면 같은 장치도 키 복원에 실패할 수 있음
   - 해결방안: 환경 보정과 오류 정정 강화를 적용하고 bit error rate와 key reconstruction success rate로 검증함
2. 문제: challenge-response를 많이 노출하면 공격자가 모델을 학습해 응답을 예측할 수 있음
   - 해결방안: CRP 노출 범위를 제한하고 controlled PUF protocol을 적용하며 model attack success rate로 검증함
3. 문제: helper data 설계가 부실하면 키 유출은 아니더라도 응답 공간을 줄여 보안성을 약화시킬 수 있음
   - 해결방안: 안전한 fuzzy extractor를 적용하고 helper data leakage analysis와 entropy estimate로 검증함

## Ⅶ. 적용 사례

- IoT 장치 인증에서는 PUF 기반 장치 식별을 사용하고 확인 지표는 authentication success rate와 clone resistance임
- 보안 MCU에서는 저장형 키 대신 PUF 복원 키를 활용하고 확인 지표는 key reconstruction success rate와 secret storage reduction임
- 공급망 위조 방지에서는 PUF 응답 등록을 운영하고 확인 지표는 counterfeit detection rate와 enrollment consistency임

## Ⅷ. 결론

PUF의 핵심은 비밀을 저장하지 않고 장치에서 다시 만들어 쓰는 데 있으므로, 고유성만큼 재현성과 모델링 공격 저항성을 함께 봐야 함.
