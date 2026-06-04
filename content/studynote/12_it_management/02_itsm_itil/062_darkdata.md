+++
title = "62. 다크 데이터 (Dark Data)"
date = 2026-04-05

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 다크 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(Dark [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))는 수집·저장되지만 분석, 의사결정, 자동화에 거의 쓰이지 않는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)다.
> 2. **가치**: 방치하면 스토리지 비용과 보안·규제 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)만 키우지만, 제대로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하면 미래 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습 자산이나 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 증적이 된다.
> 3. **판단**: 발견-[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)-가치평가-처리-재평가의 생명주기로 관리해야 하며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)와 보존 정책이 핵심이다.

---

## Ⅰ. 개요 및 필요성

기업은 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), 이메일, 센서 기록, 오래된 프로젝트 산출물을 계속 쌓는다. 문제는 "언젠가 쓰겠지"라는 이유로 쌓인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 실제로는 대부분 다시 읽히지 않는다는 점이다.

다크 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 생기는 대표 원인은 세 가지다. 첫째, 자동 수집은 쉽지만 활용 설계는 늦다. 둘째, 부서마다 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 흩어져 서로 존재를 모른다. 셋째, 규제 때문에 지워도 되는지 판단이 늦어져 보존만 계속된다.

- **📢 섹션 요약 비유**: 창고에 박스는 계속 들어오는데, 누가 열어볼지 정해지지 않으면 그 창고는 금방 어둡고 무거워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Dark Data
+- Technical Dark Data
+- Organizational Dark Data
+- Regulatory Dark Data
+- Temporary Dark Data
```

| 유형 | 특징 | 예시 | 처리 방향 |
| :-- | :-- | :-- | :-- |
| Technical | 레거시 시스템에 묶여 접근이 어려움 | 오래된 메인프레임 덤프 | 이관 또는 폐기 |
| Organizational | 부서 안에만 남아 공유되지 않음 | 영업팀 메모, 운영팀 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 등록 |
| Regulatory | 규제 때문에 보존은 하지만 활용은 적음 | [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 의료 기록 | 보존·익명화 |
| Temporary | 중간 산출물, [테스트 데이터](/knowledge-base/studynote/04_software_engineering/11_testing_validation/444_test_data_management/) | [ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 임시 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | 자동 삭제 |

다크 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리는 저장 공간을 비우는 일이 아니라, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 의미와 책임을 다시 부여하는 일이다. 어디에 있는지, 누가 쓰는지, 언제 버릴지 정해야만 자산이 된다.

- **📢 섹션 요약 비유**: 장난감 상자를 종류별로 나누고, 자주 쓰는 것과 안 쓰는 것을 구분해야 진짜 필요한 장난감을 빨리 찾을 수 있다.

---

## Ⅲ. 비교 및 연결

| 구분 | [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | Dark [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | [Data Lake](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) | Archive |
| :-- | :-- | :-- | :-- | :-- |
| 활용 빈도 | 높음 | 낮음 | 미래 분석용 | 거의 없음 |
| 정제 수준 | 높음 | 낮음 | 원시~중간 | 낮음 |
| 관리 초점 | 운영/분석 | 발견/정리 | 적재/탐색 | 보존/[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| 핵심 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) | 품질 저하 | 비용·보안·규제 | 무질서한 적재 | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |

다크 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이크는 자주 헷갈리지만 다르다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이크는 "나중에 분석하자"는 의도가 있는 저장소이고, 다크 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 의도 없이 남아 있거나 누군가도 모르게 방치된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)다.

- **📢 섹션 요약 비유**: 레이크는 잘 정리된 큰 연못이고, 다크 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 정원 구석에 쌓인 비 오는 날의 고인 물에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 처리 절차

```text
자산 인벤토리
  v
접근 빈도·최종 수정일 확인
  v
민감도·보존기한 판단
  v
활용 / 보존 / 삭제 / 익명화
  v
주기적 재평가
```

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)에 위치와 소유자가 적혀 있는가?
2. 마지막 접근 시점과 사용 부서가 추적되는가?
3. [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/), 영업비밀, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 의무가 분리되어 있는가?
4. 자동 삭제 정책과 보존 정책이 충돌하지 않는가?
5. 재평가 일정이 운영 절차에 들어 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- "언젠가 쓰겠지"로 전부 보관하는 설계
- 삭제 가능 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 법적 검토 없이 쌓아 두는 설계
- 익명화 없이 민감 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 분석 레이크로 복사하는 설계
- 소유자 없이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 쌓이고 책임은 없는 설계

기술사 관점에서는 다크 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 단순한 정리 대상이 아니라 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 거버넌스의 시작점으로 봐야 한다. 얼마나 많이 모았는지보다, 얼마나 잘 다루는지가 더 중요하다.

- **📢 섹션 요약 비유**: 집안 청소는 버리기 전에 주인과 쓰임새를 먼저 확인하는 일이다.

---

## Ⅴ. 기대효과 및 결론

다크 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리가 잘 되면 저장 비용이 줄고, 검색과 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)가 쉬워지고, 미래 분석 자산도 더 빨리 찾을 수 있다. 무엇보다 "모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다 저장한다"는 무책임한 습관을 막아준다.

앞으로는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 최소화([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Minimization), 자동 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/), 수명 주기 정책이 결합되어 다크 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 만드는 단계부터 줄어들 것이다.

- **📢 섹션 요약 비유**: 서랍을 한 번 정리해 두면 다음에 필요한 물건을 찾는 시간이 확 줄어든다.

---

## 관련 개념 맵

```text
데이터 수집
  v
미사용 데이터
  v
다크 데이터
  v
분류 · 보존 · 삭제
  v
데이터 거버넌스
```

---

## 관련 키워드 및 발전 흐름도

```text
로그/백업/이메일
  v
방치된 저장소
  v
다크 데이터 탐지
  v
정책 기반 분류
  v
데이터 최소화
```

---

## 어린이를 위한 3줄 비유 설명

창고에 넣어 둔 상자 중에는 안 쓰는 것도 많아요.
어떤 상자는 버려도 되고, 어떤 상자는 꼭 남겨야 해요.
다크 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리는 그 상자들을 똑똑하게 정리하는 일이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 107 / 587

<- **이전**: [61. ITSM (IT Service Management)](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_itsm/)
**다음**: [62. ITIL (IT Infrastructure Library)](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/) ->

---
