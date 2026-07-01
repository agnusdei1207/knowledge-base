---
title: "오류 예산 (Error Budget)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 281
---

# 📖 【암기용】 개념 완전 이해

> 목적: Error Budget을 장애를 허용하자는 말이 아니라 SLO 미달 허용량을 정량화해 배포와 신뢰성 투자를 조정하는 장치로 이해하게 만든다.

## 한눈에
- **개요**: SLO에서 허용한 실패율 또는 실패 시간을 운영 의사결정에 쓰는 예산
- **왜 필요한가**: 신뢰성을 무한정 높이면 비용과 배포 지연이 커지고, 변경을 무제한 허용하면 장애 위험이 커진다.
- **핵심 직관**: 한 달 지출 한도처럼 장애 위험도 허용 한도를 정하고, 많이 썼으면 다음 지출을 줄이는 방식이다.

## 깊이 이해
- **배경·문제의식**: 개발팀은 배포 속도를 원하고 운영팀은 장애 감소를 원해 충돌하기 쉽다.
- **작동 원리**: SLO 99.9%이면 0.1%가 error budget이며, 실제 오류율이 30일 예산을 며칠 만에 소진하면 배포를 멈추고 신뢰성 작업을 우선한다.
- **비유**: 프로젝트 일정에 예비일이 있으면 작은 지연은 흡수하지만 예비일을 다 쓰면 범위 축소나 일정 조정을 해야 한다.
- **구체 예시**: 30일 1,000,000건 요청에서 availability SLO 99.9%는 오류 1,000건을 허용하며, 3일 만에 700건을 쓰면 burn rate가 높아 release freeze가 필요하다.
- **흔한 오해·주의점**: Error budget은 장애를 일부러 내도 된다는 뜻이 아니다. 허용 위험을 수치화해 변경 정책과 개선 작업을 합의하는 기준이다.

## 연결 개념
- SLO — error budget의 기준 목표
- SRE — error budget 정책을 운영 의사결정에 사용
- Burn Rate Alert — 예산 소진 속도 기반 알림

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Error Budget은 SLO 위반 허용량을 배포 정책과 신뢰성 투자 판단에 연결하는 계량 지표다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Error Budget은 SLO 목표에서 허용되는 실패율·실패 시간을 계산한 신뢰성 위험 한도임.
> 2. **가치**: 변경 속도와 장애 감소 사이의 논쟁을 budget remaining과 burn rate 기준으로 조정함.
> 3. **판단 포인트**: 계산식, 평가 기간, burn rate alert, release freeze, 예외 승인 정책이 함께 필요함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SRE 운영 원리 확인 | SLO와 error budget 관계 | 장애 허용 논리로 오해 |
| 배포 정책 판단 확인 | budget burn, release gate | 예산 잔여율과 위험도 구분 없이 배포 중단으로 단순화 |
| 지표 설계 확인 | 기간, 오류 정의, 제외 조건 | 단순 가용성 수치만 제시 |

> 요약: 이 문제는 신뢰성 위험을 수치화해 배포와 개선 우선순위를 결정하는 체계를 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: SLO 미달 허용 예산
- 배경: 서비스 운영은 변경 속도와 신뢰성 요구가 충돌하므로 감정적 판단이 아니라 합의된 위험 한도가 필요함.
- 필요성: error budget과 burn rate로 배포 허용, 배포 보류, 신뢰성 개선 전환 시점을 결정해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
SLI Measurement -> SLO Target -> Error Budget
Error Budget -> Budget Remaining / Burn Rate
Burn Rate -> Alert / Release Freeze / Reliability Work
Policy -> Exception / Review / Stakeholder Agreement
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| SLO Target | 예산 계산 기준 | 99.9% 등 목표값 |
| Budget Remaining | 남은 실패 허용량 | 요청 수 또는 시간 단위 |
| Burn Rate | 예산 소진 속도 | multi-window alert |
| Policy | 소진 시 실행 조치 | 배포 중단, 개선 작업 |

> 요약: Error Budget은 SLO에서 예산을 계산하고 소진 속도에 따라 운영 정책을 실행하는 구조다.

---

## Ⅲ. 동작원리 및 흐름도

```text
SLO 설정 -> 허용 실패율 계산 -> 실제 실패 측정
-> budget remaining 산정 -> burn rate 계산
-> 정책 판단 -> 배포 허용 / 제한 / 안정화 작업
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | SLO 목표와 평가 기간 정의 | SLO document |
| 2 | 허용 오류량 산정 | 1 - SLO |
| 3 | 실제 오류율과 소진 속도 측정 | burn rate |
| 4 | 정책에 따라 release gate와 개선 작업 실행 | policy compliance |

> 요약: Error Budget은 목표 대비 실제 위반량과 소진 속도를 계산해 배포 정책을 제어한다.

---

## Ⅳ. 특징

| 구분 | 단순 장애 건수 관리 | Error Budget | 판단 기준 |
|:---|:---|:---|:---|
| 기준 | 장애 횟수 | SLO 미달 허용량 | 사용자 영향 |
| 의사결정 | 회의 판단 | budget remaining | 정책 일관성 |
| 배포 통제 | 수동 승인 | burn rate 기반 gate | 변경 위험 |
| 한계 | 영향도 반영 약함 | SLO 오설정 시 왜곡 | 지표 품질 |

> 요약: Error Budget은 장애 횟수보다 SLO 위반량과 소진 속도를 기준으로 변경 위험을 조정한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 고정 배포 정책 | Error Budget 정책 | 선택 기준 |
|:---|:---|:---|:---|
| 배포 허용 | 일정·승인 중심 | 예산 잔여율 반영 | 서비스 위험 |
| 개선 우선순위 | 장애 후 판단 | burn rate 초과 시 전환 | 신뢰성 투자 |
| 조직 합의 | 개발·운영 충돌 가능 | 제품·SRE 공동 기준 | 의사결정 투명성 |

> 요약: Error Budget 정책은 배포 속도와 신뢰성 개선의 우선순위를 같은 수치 기준으로 정렬한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 예산 과소 | SLO 과도 설정 | 사용자 기대와 비용 기반 조정 | frequent freeze count |
| 예산 과다 | 낮은 SLO 목표 | 고객 불만과 support ticket 대조 | customer impact |
| 정책 무력화 | 예외 승인 남발 | 예외 사유·기간·승인자 기록 | exception count |

> 요약: Error Budget은 SLO 수준과 예외 정책이 맞지 않으면 배포 통제 기준으로 작동하지 않는다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 예산 계산 | SLO별 budget 산정 자동화 | SLO dashboard |
| 소진 감시 | burn rate alert 작동 | alert history |
| 정책 준수 | 소진 시 release gate 실행 | change record |

> 요약: 운영 성과는 예산 계산, 소진 알림, release gate 준수로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. SLO별 error budget을 요청 수, 오류 수, downtime 중 서비스 특성에 맞는 단위로 계산하고 dashboard에 공개함.
2. short-window와 long-window burn rate alert를 함께 구성해 급격한 장애와 지속적 저하를 구분함.
3. 예산 소진 기준에 따라 신규 기능 배포 제한, reliability sprint 전환, postmortem action item 완료 조건을 정책화함.

**결론 (2줄):**
- 기술사 판단: Error Budget은 장애를 허용하는 면책 장치가 아니라 변경 위험과 신뢰성 투자의 균형을 정하는 통제 기준임.
- 향후 방향: Error Budget은 progressive delivery와 feature flag에 연결되어 canary 자동 중단과 rollback 판단 기준으로 활용됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Error Budget을 설명하시오" | SLO 기반 계산과 burn rate 흐름 | 단순 장애 관리 대비 차이 |
| 요구사항 명시형 | "배포와 신뢰성 균형 방안을 제시하시오" | release gate 정책 절차 | 예산 오설정, 예외 남발 리스크 |

> 요약: 설명형은 계산 원리, 방안형은 정책 실행과 조직 합의를 중심으로 작성한다.
