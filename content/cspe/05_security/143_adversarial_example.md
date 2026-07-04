---
title: "적대적 예제 공격 (Adversarial Example)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 143
---

# 📖 【암기용】 개념 완전 이해

> 목적: 적대적 예제 공격을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 사람이 보기에는 거의 같은 입력에 작은 교란을 넣어 모델만 다른 판단을 하게 만드는 공격
- **왜 필요한가**: AI 모델은 픽셀, 토큰, 음성 파형의 미세한 경계에 민감하다. 공격자는 이 경계를 계산하거나 탐색해 이미지 오분류, 음성 명령 위조, 텍스트 필터 우회를 만든다.
- **핵심 직관**: 사람 눈에는 같은 표지판인데, 모델이 보는 좌표 공간에서는 결정 경계 반대편으로 살짝 밀어 넣는 방식이다.

## 깊이 이해
- **배경·문제의식**: 딥러닝 모델은 고차원 입력에서 통계적 패턴을 학습한다. 고차원 공간에서는 작은 노이즈가 누적되어 모델 내부 특징값을 크게 바꿀 수 있다.
- **작동 원리**: 화이트박스 공격은 gradient를 이용해 손실함수를 키우는 방향으로 입력을 수정한다. 블랙박스 공격은 API 응답을 반복 질의해 비슷한 교란을 찾는다.
- **비유**: 사람은 글씨를 문맥으로 읽지만 OCR 모델은 획의 위치와 밝기 값을 본다. 얇은 점 몇 개가 사람에게는 먼지지만 모델에게는 다른 글자로 보일 수 있다.
- **구체 예시**: FGSM은 입력에 epsilon 크기 교란을 한 번 더해 오분류를 만든다. 이미지에서 epsilon 8/255 수준이면 사람이 구분하기 어렵지만 모델 예측은 바뀔 수 있다.
- **흔한 오해·주의점**: "노이즈 제거 필터를 넣으면 해결"은 부족하다. adaptive attacker는 필터를 포함한 전체 방어 구조를 고려해 새 교란을 만든다.

## 연결 개념
- FGSM/PGD: gradient 기반 적대적 예제 생성 기법
- Adversarial Training: 적대적 샘플을 학습에 포함해 robust accuracy를 높임
- Evasion Attack: 배포된 모델의 추론 시점에서 탐지·분류를 우회함

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 적대적 예제는 데이터 오염과 달리 배포 후 추론 입력을 미세 조작해 모델 결정 경계를 넘기는 회피 공격이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 적대적 예제 공격은 입력에 사람 인지가 어려운 교란을 추가해 모델의 decision boundary를 넘겨 오분류를 유도하는 추론 시점 공격이다.
> 2. **가치**: 방어는 adversarial training, input preprocessing, detection, ensemble, robust evaluation을 함께 적용해야 한다.
> 3. **판단 포인트**: 자율주행·의료·악성코드 탐지처럼 오분류 비용이 큰 모델은 clean accuracy가 아니라 robust accuracy와 perturbation budget으로 평가한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 추론 시점 AI 공격 이해 | epsilon, gradient, decision boundary, white/black-box | 학습 데이터 오염과 혼동 |
| 방어 한계 판단 | adversarial training, adaptive attack, robust accuracy | 단일 필터로 해결 가능하다고 단정 |
| 정량 평가 제시 | clean accuracy, robust accuracy, attack success rate | 정확도만 제시하고 교란 크기 누락 |
> 요약: 이 문제는 미세 교란이 모델 경계를 어떻게 넘는지와 방어 효과를 어떤 지표로 평가하는지 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 미세 교란 기반 모델 회피
- 배경: AI 서비스가 이미지, 음성, 텍스트, 악성코드 탐지에 적용되면서 추론 시점 회피 공격이 운영 위험이 됨.
- 필요성: 정상 정확도, robust accuracy, 공격 성공률, 교란 허용범위를 모델 평가 지표로 함께 측정해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Original Input -> Perturbation Generator -> Adversarial Input
Adversarial Input -> Target Model -> Wrong Prediction
Defense Layer -> Detection / Preprocessing / Robust Model -> Decision
```

| 구성요소 | 역할 | 통제 포인트 |
|:---|:---|:---|
| 원본 입력 | 이미지·음성·텍스트·바이너리 특징 | 입력 정규화, 허용 범위 |
| 교란 생성기 | gradient 또는 API 탐색으로 미세 변형 계산 | epsilon, query budget |
| 대상 모델 | 교란 입력에 대해 오분류 발생 | robust training, ensemble |
| 탐지 계층 | 분포 외 입력·불확실성·노이즈 패턴 감지 | confidence, entropy, OOD score |
| 평가 세트 | 공격·방어 효과 정량 검증 | FGSM, PGD, black-box transfer |
> 요약: 적대적 예제 구조는 입력 교란, 모델 오분류, 방어 평가 세트로 구성되며 epsilon과 robust accuracy가 핵심 지표다.

---

## Ⅲ. 동작원리 및 흐름도

```text
모델/출력 정보 수집 -> 손실 증가 방향 탐색 -> 교란 생성
-> 입력 제약 적용 -> 모델 질의 -> 오분류 성공 여부 평가
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 공격 지식 수준 결정 | white-box gradient, black-box query |
| 2 | FGSM·PGD·CW 등으로 교란 계산 | epsilon 8/255, L2/Linf norm |
| 3 | 교란 입력을 모델에 제출 | confidence, target label |
| 4 | 방어 전후 예측 차이 측정 | robust accuracy, ASR |
| 5 | adaptive attack으로 방어 우회 재평가 | AutoAttack, transfer attack |
> 요약: 공격은 손실함수를 키우는 방향의 입력 변형이며, 방어 검증은 adaptive attack까지 포함해야 한다.

---

## Ⅳ. 특징

| 구분 | 일반 노이즈 | 적대적 예제 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 생성 방식 | 무작위 변형 | 손실함수·결정 경계 기반 최적화 | epsilon, query budget |
| 인지 가능성 | 사람도 품질 저하 인지 | 사람 인지 어려움 | Linf 8/255 등 예산 명시 |
| 공격 시점 | 입력 품질 문제 | 배포 후 추론 시점 공격 | ASR, target success |
| 대응 방식 | denoise, augmentation | adversarial training, robust eval | robust accuracy 70% 이상 목표 |
> 요약: 적대적 예제는 무작위 노이즈가 아니라 모델 경계를 겨냥한 최적화 입력이므로 공격 예산과 robust accuracy로 판단한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 공격면 | 학습 데이터 조작 | 추론 입력 조작 | 공개 API·센서 입력 노출 시 우선 |
| 방어 | 입력 필터·정규화 | adversarial training + detection | 안전 중요 모델, 오분류 비용 상위 |
| 평가 | clean validation | FGSM/PGD/AutoAttack benchmark | robust accuracy 목표 필요 |
> 요약: 적대적 예제 대응은 정상 검증이 아니라 공격 알고리즘별 강건성 평가를 기준으로 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 방어 과신 | 단일 preprocessing만 적용 | adaptive attack 재평가 | AutoAttack ASR |
| 정상 품질 저하 | adversarial training 과도 적용 | clean/robust trade-off 관리 | clean accuracy 하락 2%p 이내 |
| 전이 공격 | 다른 모델에서 만든 교란이 성공 | ensemble, randomized smoothing | transfer ASR |
> 요약: 주요 리스크는 방어 우회, 정상 품질 저하, 전이 공격이며 공격 세트별 지표로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 강건 정확도 | PGD 기준 robust accuracy 70% 이상 | adversarial benchmark |
| 공격 성공률 | target ASR 5% 이하 | FGSM, PGD, CW, black-box test |
| 운영 탐지 | high entropy/OOD precision 80% 이상 | inference log, detector evaluation |
> 요약: 도입 후에는 clean accuracy가 아니라 강건 정확도, 공격 성공률, 탐지 정밀도를 함께 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 평가 체계: FGSM, PGD, CW, AutoAttack, black-box transfer를 CI 평가에 포함하고 epsilon 8/255 기준 ASR 5% 초과 시 배포 차단
2. 모델 방어: adversarial training과 ensemble을 적용하되 clean accuracy 하락 2%p 이내, robust accuracy 70% 이상 기준으로 승인
3. 운영 탐지: confidence entropy, OOD score, 입력 변형 민감도 로그를 수집해 SIEM 경보와 재검증 큐로 연결

**결론 (2줄):**
- 기술사 판단: 외부 입력을 직접 받는 AI 모델은 clean accuracy보다 perturbation budget별 robust accuracy를 우선 평가해야 함
- 향후 방향: 표준 벤치마크와 red-team 자동화가 결합되어 모델 릴리스마다 적대적 강건성 검증이 반복될 것임

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "적대적 예제 공격을 설명하시오" | gradient 기반 교란 생성과 오분류 흐름 | 일반 노이즈, 데이터 오염과의 차이 |
| 요구사항 명시형 | "대응 방안을 제시하시오", "평가하시오" | FGSM/PGD/AutoAttack 평가 절차 | robust accuracy, ASR, clean trade-off |
> 요약: 설명형은 공격 원리, 평가형은 교란 예산과 강건성 지표 중심으로 답안을 구성한다.
