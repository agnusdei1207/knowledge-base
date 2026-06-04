---
title: "Blameless Postmortem"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
---


> **핵심 인사이트**
> - [Blameless Postmortem](/studynote/15_devops_sre/03_sre_observability/128_blameless_postmortem/) (무비난 회고)은 장애 원인을 개인이 아닌 시스템·프로세스에서 찾아 근본적 개선을 이끄는 [SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 문화다.
> - 타임라인·근본 원인·영향 분석·재발 방지 액션 아이템이 Postmortem 문서의 4대 필수 요소다.
> - 장애를 숨기지 않고 공유하는 문화가 조직 전체의 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 학습 속도를 높인다.

---

## Ⅰ. Blameless 문화의 필요성

전통적 장애 처리는 "누가 실수했나?"를 찾아 처벌한다. 이는:
- 엔지니어가 장애를 숨기게 만든다.
- 동일 장애가 반복된다.
- 시스템·프로세스 개선 기회를 잃는다.

Blameless Postmortem은 "시스템이 왜 그 실수를 가능하게 했는가?"를 묻는다.

```
+-----------------------------------------------------+
|             Blameless vs Blame 비교                 |
|                                                     |
|  Blame Culture     |  Blameless Culture             |
|  --------------- |  -------------------------     |
|  "누가 잘못?"     |  "시스템 어디가 취약?"         |
|  개인 처벌        |  시스템 개선                   |
|  장애 은폐        |  투명한 공유                   |
|  반복 장애        |  재발 방지 액션 이행            |
+-----------------------------------------------------+
```

> 📢 **Ⅰ 섹션 요약 비유**
> 비행기 사고 조사는 조종사를 처벌하지 않고 항공 시스템 전체를 개선한다 — Blameless Postmortem이 같은 철학이다.

---

## Ⅱ. Postmortem 문서 구조

| 섹션                | 내용                                          |
|---------------------|-----------------------------------------------|
| 요약                | 장애 범위·영향·기간 (2~3줄)                  |
| 타임라인            | 장애 감지~해결까지 시간순 이벤트              |
| 근본 원인 분석      | 5-Why 또는 Fish-bone으로 근본 원인 도출       |
| 영향 분석           | 영향받은 사용자 수, 비즈니스 손실             |
| 재발 방지 액션 아이템| 담당자·기한이 명시된 구체적 개선 과제          |
| 무엇이 잘됐나       | 빠른 감지·대응 등 잘 작동한 것도 기록         |

> 📢 **Ⅱ 섹션 요약 비유**
> Postmortem 문서는 수술 후 의무기록 — "무슨 일이 있었고, 왜 생겼고, 다음엔 어떻게 막을지"를 정확히 기록한다.

---

## Ⅲ. 근본 원인 분석 기법

**5-Why 기법**:

```
왜 서비스가 다운됐나?
-> DB 연결 풀이 고갈됐다
-> 왜? 쿼리 타임아웃 설정이 없었다
-> 왜? 코드 리뷰 체크리스트에 타임아웃 항목이 없었다
-> 왜? Runbook에 DB 설정 가이드가 없었다
-> 왜? 스테이징 환경에서 부하 테스트를 안 했다
-> 근본 원인: 부하 테스트 자동화 미비
```

근본 원인은 보통 "프로세스·도구·설계의 구조적 약점"이다.

> 📢 **Ⅲ 섹션 요약 비유**
> 5-Why는 "왜?"를 다섯 번 물어 표면 증상이 아닌 병의 뿌리(근본 원인)를 찾는 의사의 문진이다.

---

## Ⅳ. 액션 아이템과 후속 관리

효과적인 액션 아이템 조건:
- **Specific**: "DB [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 추가"처럼 구체적
- **Assignee**: 담당자 명시
- **Due Date**: 완료 기한 명시
- **Verifiable**: 완료 여부 측정 가능

Postmortem 리뷰:
- 작성 후 24~48시간 이내 팀 리뷰
- 액션 아이템 완료 여부 주기적 추적
- 사내 Postmortem 저장소에 공유 -> 조직 학습

> 📢 **Ⅳ 섹션 요약 비유**
> 액션 아이템 없는 Postmortem은 처방전 없는 진단서 — 아무리 정확한 진단도 치료 계획이 없으면 의미가 없다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소           | 역할                                    |
|---------------------|-----------------------------------------|
| Blameless           | 개인이 아닌 시스템 원인 분석 원칙        |
| Postmortem          | 장애 후 공식 회고 문서                  |
| 5-Why               | 근본 원인 도출 기법                     |
| 타임라인            | 장애 감지~[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간순 기록              |
| 액션 아이템         | 담당자·기한이 있는 재발 방지 과제        |
| Runbook             | 장애 대응 절차 매뉴얼                   |

### 관련 키워드 및 발전 흐름도

```
Blameless Postmortem
    +-- 5-Why / Fish-bone -> 근본 원인 분석
    +-- 타임라인 -> 장애 흐름 재구성
    +-- 액션 아이템 -> 재발 방지 트래킹
    +-- Postmortem 저장소 -> 조직 학습·지식 공유
```

> 🧒 **어린이 비유**
> 모래성이 무너지면 "네가 잘못 쌓았어!" 하지 않고 "파도가 언제 치는지 몰랐구나, 다음엔 더 뒤에 짓자"라고 말하는 것이 Blameless예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 319 / 373

<- **이전**: [Toil SRE Automation](/studynote/13_cloud_architecture/05_data_engineering/318_process/)
**다음**: [Observability Metrics Logs Traces](/studynote/15_devops_sre/05_devsecops/320_metric/) ->

---
