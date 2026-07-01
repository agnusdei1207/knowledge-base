---
title: "사이드채널 공격 (Side-Channel Attack)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 211
---

# 📖 【암기용】 개념 완전 이해

> 목적: 사이드채널 공격을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 암호 알고리즘의 결과가 아니라 실행 중 새는 물리·시간 신호로 비밀값을 추정하는 공격
- **왜 필요한가**: AES, RSA, ECC 수식이 맞아도 처리 시간, 캐시 적중, 전력, 전자파가 키 비트와 상관되면 키가 노출된다.
- **핵심 직관**: 금고 비밀번호를 직접 보지 않고 버튼 누르는 시간과 소리 차이로 숫자를 맞추는 방식이다.

## 깊이 이해
- **배경·문제의식**: 전통 암호 분석은 평문·암호문·알고리즘을 본다. 사이드채널은 CPU, 캐시, 전원선, EM probe에서 측정 가능한 부가 신호를 본다.
- **작동 원리**: 공격자는 동일 연산을 수천~수백만 회 관측해 키 후보별 중간값과 누설 신호의 상관관계를 계산한다. DPA/CPA는 전력 파형과 해밍 가중치 모델을 맞춰 키 바이트를 복원한다.
- **비유**: 시험 답안은 가려졌지만 연필 움직임, 지우개 사용 횟수, 페이지 넘김 시간을 보고 어떤 문제를 푸는지 추론하는 것과 같다.
- **구체 예시**: AES S-box 출력의 해밍 가중치를 가정하고 5만 trace를 수집한 뒤 CPA 상관계수 0.25 이상 키 후보를 선택하면 1바이트 단위 키 추정 가능.
- **흔한 오해·주의점**: "암호 알고리즘이 표준이면 충분"하지 않다. 구현이 branch, table lookup, 캐시 접근 패턴을 키에 따라 바꾸면 표준 알고리즘도 누설된다.

## 연결 개념
- Constant-Time 구현: 키 값과 무관한 실행 경로·메모리 접근
- Masking: 중간값을 난수 share로 분해해 통계 상관 제거
- TVLA: Welch t-test로 누설 존재 여부를 정량 검정

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 공격 기법 나열이 아니라 누설원, 분석법, 대응 구현, 검증 지표를 연결해 작성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 사이드채널 공격은 처리 시간·캐시·전력·전자파 등 부가 신호와 비밀키의 통계 상관을 이용하는 구현 공격이다.
> 2. **가치**: 암호 수식의 안전성과 구현 누설은 별도 문제이므로 구현 단계에서 constant-time, masking, leakage test가 필요하다.
> 3. **판단 포인트**: 대응은 알고리즘 교체보다 키 의존 분기 제거, 난수 마스킹, 측정 기반 TVLA 통과 여부로 판단해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 암호 구현 공격 이해 확인 | timing, cache, power, EM 누설원과 DPA/CPA 분석 연결 | 암호 알고리즘 취약점으로만 설명 |
| 대응 설계 역량 확인 | constant-time, masking, blinding, noise, shield | "암호화 적용"만 쓰고 구현 통제 누락 |
| 검증 기준 확인 | TVLA, leakage assessment, trace 수, t-value | 대응 존재만 쓰고 측정 절차 누락 |

> 요약: 이 문제는 수학적 암호 안전성보다 구현 누설을 어떻게 측정·차단하는지 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 실행 부가 신호 기반 키 추정 공격
- 배경: AES·RSA·ECC 알고리즘이 안전해도 CPU branch, cache line, power trace, EM radiation이 키 값과 상관되면 구현 단계에서 비밀키가 노출됨
- 필요성: HSM·TPM·스마트카드·IoT 보안칩은 TVLA abs(t) 4.5 미만, secret-dependent branch 0건 기준으로 누설 통제를 검증해야 함

---

## Ⅱ. 구조 및 구성요소

```text
암호 구현 -> 누설원 timing/cache/power/EM -> trace 수집
         -> 통계 분석 DPA/CPA -> 키 후보 추정
         -> 대응 constant-time/masking/noise -> TVLA 검증
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 누설원 | 시간, 캐시, 전력, 전자파 신호 발생 | 키 의존 분기·테이블 접근 |
| 수집 장비 | oscilloscope, EM probe, performance counter | kHz~GHz 대역 측정 |
| 분석 모델 | Hamming weight, Hamming distance, cache hit/miss | CPA·DPA 상관 분석 |
| 대응 구현 | constant-time, masking, blinding | compiler 최적화 영향 검토 |
| 검증 체계 | TVLA, leakage assessment | Welch t-test 기준 사용 |

> 요약: 사이드채널은 누설원·측정·통계 분석·구현 대응·검증 체계가 결합된 공격면이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
입력 선택 -> 암호 연산 반복 -> trace 수집
-> 키 후보별 중간값 계산 -> 누설 모델 상관 분석
-> 후보 키 선택 -> 대응 적용 -> 재측정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 평문·암호문과 전력/EM trace 동시 수집 | trace 10,000~100,000개 |
| 2 | S-box, modular exponent 중간값 가정 | 키 후보 256개 또는 비트 후보 |
| 3 | CPA/DPA로 상관계수·차분 평균 계산 | 상위 후보와 2위 간 peak 분리 |
| 4 | constant-time, masking, random delay 적용 | 키 의존 branch 0건 |
| 5 | TVLA로 누설 잔존 확인 | abs(t) 4.5 미만 목표 |

> 요약: 공격은 반복 측정과 통계 상관으로 키 후보를 좁히며, 대응 효과는 재측정 지표로 확인한다.

---

## Ⅳ. 특징

| 구분 | 기존 암호 분석 | 사이드채널 공격 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 공격 대상 | 알고리즘 수식 | 구현과 물리 신호 | 동일 AES라도 구현별 위험 상이 |
| 관측 데이터 | 평문·암호문 | timing/cache/power/EM trace | trace 1만~100만 개 |
| 대표 기법 | 차분·선형 분석 | timing attack, cache attack, DPA, CPA | CPA 상관계수 peak 확인 |
| 대응 기준 | 키 길이, 모드 | constant-time, masking, TVLA | abs(t) 4.5 미만 |

> 요약: 사이드채널은 암호 강도보다 구현 누설량과 측정 가능성이 공격 성공률을 좌우한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 소프트웨어 암호 라이브러리 | 누설 평가 포함 보안 구현 | 키 의존 분기·메모리 접근 존재 여부 |
| 비용/성능 | 일반 최적화 | constant-time과 masking 비용 반영 | 지연 증가 5~30% 허용 범위 |
| 운영/위험 | 기능 테스트 중심 | leakage assessment 정기 수행 | 펌웨어 변경마다 TVLA 재수행 |

> 요약: 보호 대상 키가 장기 사용되고 물리 접근이 가능하면 성능 비용을 감수하고 누설 검증을 포함한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 키 추정 | 키 의존 실행 시간·캐시 접근 | constant-time, table lookup 제거 | timing variance p-value |
| 통계 누설 | 중간값과 전력 파형 상관 | masking, hiding, randomization | CPA peak 감소율 |
| 대응 무력화 | compiler가 분기·lookup 재도입 | binary audit, compiler flag 고정 | object diff, side-channel CI |

> 요약: 주요 위험은 키 의존 패턴 재발생이며, 소스·바이너리·측정 결과를 함께 점검해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 누설 검정 | abs(t) 4.5 미만 | TVLA fixed-vs-random test |
| 상관 분석 | CPA 최대 상관계수 0.05 미만 | power/EM trace 분석 |
| 구현 통제 | secret-dependent branch 0건 | ctgrind, dudect, static analysis |

> 요약: 성공 여부는 TVLA, CPA 상관계수, secret-dependent branch 수로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. AES/ECC 구현은 bitslicing, constant-time scalar multiplication, cache-line 독립 접근으로 secret-dependent branch 0건 목표 설정
2. 전력·EM 대응은 Boolean masking, random precharge, clock jitter를 적용하고 trace 50,000개 기준 TVLA 수행
3. 릴리스 파이프라인은 dudect, ctgrind, leakage CI를 포함해 compiler 최적화 변경 시 재평가 수행

**결론 (2줄):**
- 기술사 판단: 물리 접근 가능한 HSM·IoT·카드 환경이면 constant-time만으로 부족하며 masking과 TVLA를 함께 적용함
- 향후 방향: PQC·AI 가속기 보안칩에서도 전력·EM 누설 평가를 제품 인증 전 단계에 포함해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "사이드채널 공격을 설명하시오" | 누설원, DPA/CPA 원리, TVLA 흐름 | timing/cache/power/EM 비교와 적용 환경 |
| 요구사항 명시형 | "대응 방안을 제시하시오", "검증하시오" | constant-time, masking, 재측정 절차 | TVLA 기준, 리스크·지표, 선택 기준 |

> 요약: 설명형은 공격 원리 폭을, 방안형은 구현 통제와 측정 검증을 중심으로 목차를 전환한다.
