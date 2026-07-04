---
title: "추측 디코딩 (Speculative Decoding)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 55
---

# 📖 【암기용】 개념 완전 이해

> 목적: 추측 디코딩을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 작은 draft model이 여러 토큰을 미리 제안하고 큰 target model이 한 번에 검증해 디코딩 지연을 줄이는 기법
- **왜 필요한가**: LLM 생성은 토큰을 하나씩 순차 생성하므로, 대형 모델의 decode 단계가 memory-bound 병목이 됨.
- **핵심 직관**: 작은 draft model이 후보 토큰을 먼저 만들고, target model이 병렬 검증해 일치 토큰만 채택하는 방식임.

## 깊이 이해
- **배경·문제의식**: Prefill 이후 decode는 매 토큰마다 전체 모델을 호출해야 하며, 70B 모델은 토큰당 20~50ms 지연이 누적됨. 작은 모델이 후보 토큰을 선생성하면 대형 모델 호출 횟수를 줄일 수 있음.
- **작동 원리**: draft model이 k개 토큰을 제안하고, target model이 병렬로 확률을 계산해 일치하는 prefix를 수락함. 틀린 지점부터 target model이 직접 샘플링하여 품질을 보존함.
- **비유**: 속기사 초안을 감수자가 확인하면서 맞는 문장은 그대로 통과시키고 틀린 문장부터 다시 쓰는 절차임.
- **구체 예시**: acceptance rate 70%, draft length 4이면 target model 호출 대비 1.8~2.5배 decode 처리량 향상을 기대함.
- **흔한 오해·주의점**: draft model 품질이 낮으면 거절률이 올라가 target 호출이 줄지 않음. target model 출력 분포를 보존해야 품질 저하가 없음.

## 연결 개념
- TPOT — 토큰당 출력 지연 최적화 대상
- LLM Serving — 추측 디코딩 적용 영역
- Draft/Target Model — 추측 디코딩의 두 모델 구조

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Speculative Decoding은 작은 모델이 후보 토큰을 제안하고 큰 모델이 검증해 decode 지연을 줄이는 서빙 최적화임.
> 2. **가치**: target model 출력 분포를 유지하면서 토큰 생성 처리량을 1.5~3배 높일 수 있음.
> 3. **판단 포인트**: draft 품질, acceptance rate, draft length, target 검증 비용이 속도 개선 폭을 결정함.

---

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| draft-target 2모델 구조와 출력 분포 보존 원리를 이해하는지 확인 | draft→target 검증 구조, acceptance rate 70% 기준 1.5~3배 처리량, 출력 분포 보존 | draft 수락률 저하 시 이득 소멸을 누락, "속도가 빨라진다"로 추상 서술 |

> 요약: draft-target 검증 구조와 수락률 기반 처리량 수치를 제시하고, 품질 보존 조건을 명시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 정의: 작은 draft model이 후보 토큰을 제안하고 큰 target model이 검증해 디코딩 지연을 줄이는 서빙 최적화 기법
- 배경: 대형 모델의 decode 단계는 토큰당 20~50ms 지연이 누적되는 memory-bound 병목
- 필요성: target model 출력 분포를 유지하면서 토큰 생성 처리량을 1.5~3배 향상(acceptance rate 70% 기준)

---

## Ⅱ. 구조 및 구성요소

```text
Prompt -> Draft Model -> 후보 토큰 t1..tk -> Target Model 검증 -> Accept/Reject -> Output
              |                                       |
              +-> 빠른 후보 생성(5~20배 소형)         +-> 거절 시 Fallback Decode
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Draft Model | 빠른 후보 토큰 생성 | target보다 5~20배 작음 |
| Target Model | 후보 확률 검증 | 원 모델 품질 보존 |
| Acceptance Rule | 후보 수락/거절 결정 | 확률 보정, prefix accept |
| Fallback Decode | 거절 지점부터 직접 생성 | 품질 저하 방지 |

> 요약: 작은 모델이 추측하고 큰 모델이 검증하므로, 수락률이 높을수록 target 호출당 출력 토큰 수가 증가함.

---

## Ⅲ. 동작원리 및 흐름도

```text
프롬프트 입력 -> draft가 k토큰 생성 -> target 병렬 검증
    -> prefix 수락 -> 거절 지점 fallback -> 다음 반복
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | draft model이 k개 후보 토큰 생성 | draft length k=2~8 |
| 2 | target model이 후보 전체 확률 계산 | 병렬 검증 batch |
| 3 | acceptance rule로 prefix 수락 | acceptance rate 60~80% |
| 4 | 거절 지점 이후 target 직접 샘플링 | 품질 parity, TPOT |

> 요약: 후보 토큰을 한 번에 검증해 target model 1회 호출당 여러 토큰을 출력하도록 만드는 반복 구조임.

---

## Ⅳ. 특징

| 구분 | 일반 디코딩 | Speculative Decoding | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 생성 방식 | target이 1토큰씩 생성 | draft k토큰 제안 후 target 검증 | k=2~8 |
| 품질 | target 분포 그대로 | 보정 시 target 분포 유지 | quality parity 필요 |
| 처리량 | 기준 1× | 1.5~3× | acceptance 70% 이상 |
| 한계 | 지연 누적 | draft/target 2모델 운영 | 메모리·배포 복잡도 |

> 요약: 추측 디코딩은 품질을 유지한 decode 가속 기법이나, draft 수락률이 낮으면 운영 복잡도 대비 이득이 줄어듦.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 일반 디코딩 | Speculative Decoding | 선택 기준 |
|:---|:---|:---|:---|
| 처리량 | target 1토큰/step | 1.5~3×(acceptance 70% 기준) | 장문 비율 50% 이상 시 적용 |
| 품질 | target 분포 그대로 | 확률 보정 시 분포 유지 | quality parity 검증 필수 |
| 운영 복잡도 | 단일 모델 서빙 | draft+target 2모델 관리 | GPU 메모리 여유분 확인 |

> 요약: 장문 생성 비율이 높고 GPU 여유가 있으면 Speculative Decoding의 처리량 이득이 운영 복잡도를 상회한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 수락률 저하 | draft model과 target의 분포 불일치 | draft 모델을 target의 distill 버전으로 교체, k 조정 | acceptance rate, fallback ratio |
| 메모리 부족 | 2모델 동시 로딩 시 GPU 메모리 초과 | draft model 양자화(INT8), 모델 분리 배치 | GPU 메모리 사용률 |
| 품질 회귀 | acceptance rule 미보정 시 분포 왜곡 | 확률 보정 적용, BLEU/ROUGE/정답률 회귀 테스트 | 품질 parity 점수 |

> 요약: draft 품질·메모리·분포 보정 3가지를 관리하여 처리량 이득을 유지한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 처리량 향상 | 일반 디코딩 대비 1.8배 이상 | TPOT 벤치마크, 초당 토큰 수 |
| 품질 유지 | BLEU/ROUGE 차이 1% 이내, 정답률 parity | A/B 테스트, 회귀 점수 비교 |
| 수락률 | acceptance rate 65% 이상 유지 | 서빙 로그, 실시간 대시보드 |

> 요약: 처리량·품질·수락률 3축 지표를 모니터링하여 Speculative Decoding 운영 효과를 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. target 70B 모델에 draft 7B 모델을 결합하고 acceptance rate 70% 이상에서만 프로덕션 활성화
2. 짧은 답변은 일반 디코딩, 512토큰 이상 장문 생성은 speculative path로 라우팅해 오버헤드 분리
3. 관측 지표로 TPOT, acceptance rate, fallback ratio, 품질 회귀점수(BLEU/ROUGE/정답률)를 수집

**결론 (2줄):**
- 기술사 판단: decode 병목·장문 생성 비중이 높고 draft 수락률 60% 이상이면 Speculative Decoding을 적용함.
- 향후 방향: Medusa·EAGLE 등 multi-token prediction 계열과 결합해 draft model 의존도를 줄이는 방향으로 발전함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | draft->target 검증 흐름 | 일반 디코딩 대비 처리량 |
| 요구사항 명시형 | 최적화 방안을 제시하시오 | acceptance rate 기반 적용 절차 | TPOT·품질 회귀·운영 복잡도 |

> 요약: 설명형은 두 모델 검증 구조, 최적화형은 수락률과 TPOT 개선 기준으로 목차를 전환함.
