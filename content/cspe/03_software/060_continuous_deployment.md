---
title: "지속적 배포 (Continuous Deployment)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 60
---

# 📖 【암기용】 개념 완전 이해

> 목적: 지속적 배포를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 품질 게이트를 통과한 변경을 사람 승인 없이 운영 환경에 자동 배포하는 방식
- **왜 필요한가**: 배포 승인 대기와 대량 변경은 lead time을 늘리고 장애 원인 범위를 키운다. 지속적 배포는 작은 변경을 자동으로 운영에 반영해 피드백 시간을 줄인다.
- **핵심 직관**: 배포 버튼을 사람이 누르는 대신, 테스트와 정책 게이트가 배포 여부를 판단한다.

## 깊이 이해
- **배경·문제의식**: 지속적 전달은 운영 배포 직전 사람 승인이 남아 있고, 지속적 배포는 자동 게이트 통과 후 운영 반영까지 자동화한다.
- **작동 원리**: commit이 CI, 보안 스캔, 통합 테스트, 정책 게이트를 통과하면 canary나 blue-green으로 배포되고, error rate와 latency가 기준을 넘으면 자동 rollback된다.
- **비유**: 공항 자동 출입국처럼 사전 등록, 생체 인식, 보안 검사를 통과하면 별도 창구 승인 없이 통과하는 구조와 같다.
- **구체 예시**: 기능은 feature flag 뒤에 숨기고 1% 사용자 canary부터 시작한다. 10분간 error rate 1% 초과 또는 p95 지연 300ms 초과 시 자동 rollback한다.
- **흔한 오해·주의점**: 지속적 배포는 무검증 배포가 아니다. 자동 테스트, 정책 게이트, 관측성, rollback이 없으면 위험한 자동화일 뿐이다.

## 연결 개념
- Continuous Delivery: 운영 배포 가능 상태까지 자동화, 최종 승인은 사람
- Feature Flag: 배포와 기능 공개를 분리
- Canary·Blue-Green: 운영 영향 범위를 제한하는 배포 전략

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 지속적 배포는 자동 운영 배포이며, feature flag, canary, compliance gate, automated rollback이 핵심 통제이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 지속적 배포는 자동 품질·보안·정책 게이트를 통과한 변경을 운영 환경에 자동 반영하는 배포 방식이다.
> 2. **가치**: 작은 변경 단위로 배포해 lead time을 줄이고, canary와 자동 rollback으로 장애 영향 범위를 제한한다.
> 3. **판단 포인트**: 테스트 신뢰도, 관측성, feature flag, 규제 승인 자동화가 갖춰진 조직에서 적용해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CD 단계 구분 확인 | Continuous Delivery와 Continuous Deployment 차이 | 두 용어를 동일하게 사용 |
| 자동 배포 통제 역량 확인 | feature flag, canary, automated rollback, quality gate | 사람 승인 제거만 강조 |
| 규제·운영 리스크 판단 확인 | compliance gate, audit log, segregation of duties | 감사·승인 요구사항 누락 |
> 요약: 출제자는 자동 운영 배포를 품질·보안·감사 통제로 설명하는지를 본다.

---

## Ⅰ. 개요 및 필요성

- 개요: 운영 반영까지 자동화하는 배포
- 배경: 배포 대기와 대량 변경은 장애 원인 추적, 승인 지연, 복구 시간을 증가시키며 수동 승인 중심 배포는 릴리스 병목이 됨.
- 필요성: Automated gate, canary release, feature flag, observability로 change lead time, error budget, rollback time을 통제해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Commit -> CI Test / Security Scan / Policy Gate
Gate Pass -> Artifact Registry -> Deployment Controller
Deployment Controller -> Canary / Blue-Green
Runtime Metric -> Automated Rollback / Progressive Rollout
Feature Flag -> User Segment / Kill Switch
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Quality Gate | 테스트·정적 분석·보안 기준 차단 | coverage, CVE, policy |
| Artifact | 배포 대상 불변 산출물 | commit SHA, digest 매핑 |
| Deployment Strategy | 운영 반영 방식 | canary, blue-green, rolling |
| Feature Flag | 배포와 기능 공개 분리 | 사용자군, kill switch |
| Automated Rollback | 지표 기준 자동 복구 | error rate, latency, saturation |
> 요약: 지속적 배포는 자동 게이트, 불변 artifact, 점진 배포, feature flag, rollback으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
commit merge -> CI / 보안 / 정책 게이트
게이트 통과 -> artifact 선택 -> canary 1%
canary 관측 -> error / latency / saturation 평가
기준 충족 -> 10% / 50% / 100% 확대
기준 초과 -> 자동 rollback -> incident 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | main merge 후 자동 파이프라인 실행 | CI 성공률 95% 이상 |
| 2 | 테스트·SAST·SCA·정책 게이트 평가 | Critical CVE 0건 |
| 3 | canary 1% 배포와 기능 flag 비활성 | 사용자 영향 최소화 |
| 4 | 운영 지표 기반 자동 판정 | error rate 1% 이하, p95 300ms 이하 |
| 5 | 확대 또는 rollback 실행 | rollback 10분 이하 |
> 요약: 지속적 배포는 게이트 통과 후 점진 배포하고 운영 지표가 기준을 넘으면 자동 복구한다.

---

## Ⅳ. 특징

| 구분 | Continuous Delivery | Continuous Deployment | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 최종 배포 | 사람 승인 후 운영 반영 | 게이트 통과 시 자동 운영 반영 | 승인 대기 0분 목표 |
| 변경 크기 | 배포 가능 상태 유지 | 작은 변경 즉시 반영 | PR 400라인 이하 |
| 통제 | 수동 승인 게이트 | 자동 품질·정책 게이트 | Critical CVE 0건 |
| 장애 대응 | 사람이 rollback 판단 | 지표 기반 자동 rollback | rollback 10분 이하 |
| 적합 조직 | 승인형 운영 | 테스트·관측성 성숙 조직 | DORA Elite 목표 |
> 요약: 지속적 배포는 지속적 전달보다 자동 운영 반영 범위가 넓으며, 자동 게이트 신뢰도가 전제이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 수동 승인 배포 | 지속적 배포 | 선택 기준 |
|:---|:---|:---|:---|
| 규제 | 사람이 승인 기록 | 정책 코드와 감사 로그 | 규제 자동화 가능 여부 |
| 테스트 | 부분 자동화 | 자동 게이트 전제 | 테스트 통과 신뢰도 95% 이상 |
| 기능 공개 | 배포와 동시 | feature flag로 분리 | 기능별 사용자군 제어 필요 |
| 운영 | 사후 모니터링 | 실시간 지표 판정 | APM·로그·트레이스 완비 |
> 요약: 자동 게이트와 관측성이 부족하면 지속적 전달을 먼저 적용하고, 기준 충족 후 지속적 배포로 전환한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 결함 자동 확산 | 테스트 공백 | canary, feature flag, mutation test | change failure rate |
| 규제 위반 | 사람 승인 제거 | policy as code, audit log | 승인 정책 통과율 |
| rollback 실패 | DB 변경 비가역 | backward compatible schema | rollback 성공률 |
| flag 부채 | 오래된 feature flag 방치 | 만료일, owner, 정리 배치 | 만료 flag 수 |
> 요약: 지속적 배포 위험은 자동 확산, 규제, rollback, flag 부채이며 게이트와 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 배포 빈도 | 일 1회 이상 운영 배포 | DORA dashboard |
| 실패율 | change failure rate 15% 이하 | incident 연계 |
| 복구 | MTTR 30분 이하, rollback 10분 이하 | 배포·장애 로그 |
| 감사 | 배포별 commit, approver policy, artifact digest 100% | 감사 리포트 |
> 요약: 지속적 배포 성공은 배포 빈도, 실패율, 복구 시간, 감사 추적성으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 자동 게이트에 unit, integration, E2E, SAST, SCA, policy as code를 넣고 Critical CVE 0건과 coverage 80% 이상을 기준으로 둔다.
2. feature flag와 canary 1% -> 10% -> 50% -> 100% 확대를 적용하고 error rate 1% 초과 시 자동 rollback한다.
3. 배포별 commit SHA, artifact digest, 정책 판정, 운영 지표를 감사 로그로 남겨 규제 대응 근거를 확보한다.

**결론 (2줄):**
- 기술사 판단: 자동 테스트와 관측성이 부족하면 Continuous Delivery, 게이트 신뢰도와 rollback 체계가 있으면 Continuous Deployment를 선택함
- 향후 방향: 지속적 배포는 GitOps, progressive delivery, policy as code와 결합해 자동 운영 거버넌스로 발전함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "지속적 배포를 설명하시오" | 게이트부터 canary·rollback까지 흐름 | Continuous Delivery와 차이 |
| 요구사항 명시형 | "운영 방안을 제시하시오", "설계하시오" | feature flag, compliance gate, 자동 rollback | DORA·감사·리스크 지표 |
> 요약: 설명형은 CD 차이, 운영형은 자동 게이트와 점진 배포 통제를 중심으로 작성한다.
