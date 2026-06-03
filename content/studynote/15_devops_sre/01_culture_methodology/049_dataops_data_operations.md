+++
title = "049. DataOps — 데이터 운영"
date = 2026-04-05

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

> **핵심 인사이트**
> 1. [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/324_dataops/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Operations)는 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 원칙(자동화·[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD·[모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링)을 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)에 적용하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 개발→테스트→배포→운영 사이클을 자동화하는 방법론 — "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링의 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)"로, [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)·품질·속도를 동시에 향상시킨다.
> 2. [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD가 DataOps의 핵심 실천 — 코드 변경처럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환 로직(dbt 모델) 변경도 [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)→자동 테스트→스테이징→프로덕션 배포 워크플로우로 관리하며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 테스트 실패 시 자동 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이 가능해야 한다.
> 3. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Reliability](/knowledge-base/studynote/04_software_engineering/06_software_architecture/345_reliability_security/)) 확보가 DataOps의 궁극적 목표 — "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 다운타임([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Downtime)"([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 정확하지 않거나 사용 불가한 시간)을 최소화하기 위해 [데이터 옵저버빌리티](/knowledge-base/studynote/16_bigdata/13_intro_trends/255_data_observability/)([Data Observability](/knowledge-base/studynote/16_bigdata/13_intro_trends/255_data_observability/))와 [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)를 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에 내재화한다.

---

## Ⅰ. [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/324_dataops/) 개요



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">DataOps (Data Operations):</div>
<div class="kb-diagram-note">데이터 파이프라인에 DevOps 원칙 적용</div>
<div class="kb-diagram-note">DataOps 없을 때:</div>
<div class="kb-diagram-note">데이터 엔지니어: 노트북/수동 스크립트로 파이프라인 작성</div>
<div class="kb-diagram-note">변경: 직접 수정, 테스트 없음</div>
<div class="kb-diagram-note">배포: 수동, 의존성 파악 어려움</div>
<div class="kb-diagram-note">장애: 몇 시간 후 발견, 원인 불명</div>
<div class="kb-diagram-note">결과: 데이터 신뢰도 저하 → 분석팀 불신</div>
<div class="kb-diagram-note">DevOps 원칙의 데이터 적용:</div>
<div class="kb-diagram-note">DevOps → DataOps 매핑:</div>
<div class="kb-diagram-note">CI/CD: 파이프라인 코드 → 자동 테스트 → 배포</div>
<div class="kb-diagram-note">버전 관리: 변환 로직 (dbt 모델) Git 관리</div>
<div class="kb-diagram-note">테스트: 데이터 품질 테스트 자동화</div>
<div class="kb-diagram-note">모니터링: 파이프라인 + 데이터 품질 지표</div>
<div class="kb-diagram-note">인시던트 관리: 데이터 이상 탐지 + 대응</div>
<div class="kb-diagram-note">DataOps 구성 요소:</div>
<div class="kb-diagram-note">코드로서의 파이프라인:</div>
<div class="kb-diagram-note">Airflow DAG, dbt 모델 → Git 버전 관리</div>
<div class="kb-diagram-note">데이터 CI/CD:</div>
<div class="kb-diagram-note">PR → 자동 품질 테스트 → 스테이징 → 프로덕션</div>
<div class="kb-diagram-note">데이터 옵저버빌리티:</div>
<div class="kb-diagram-note">파이프라인 지표, 데이터 품질 모니터링</div>
<div class="kb-diagram-note">이상 탐지 + 알림</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/324_dataops/) = [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공장 자동화 — 소프트웨어 공장([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/))처럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공장도 자동화. 원자재(원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 투입→품질 검사(테스트)→포장(변환)→배포. 수동 공장 대비 품질+속도!

---

## Ⅱ. [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 파이프라인 CI/CD:</div>
<div class="kb-diagram-note">dbt (Data Build Tool) + Git + CI:</div>
<div class="kb-diagram-note">워크플로우:</div>
<div class="kb-diagram-note">1. 데이터 엔지니어: dbt 모델(SQL) 작성</div>
<div class="kb-diagram-note">2. GitHub PR 생성</div>
<div class="kb-diagram-note">3. CI 자동 실행:</div>
<div class="kb-diagram-tree-item" style="--depth:2">dbt compile: SQL 문법 검사</div>
<div class="kb-diagram-tree-item" style="--depth:2">dbt test: 데이터 품질 테스트 실행</div>
<div class="kb-diagram-note">(스테이징 환경에서)</div>
<div class="kb-diagram-tree-item" style="--depth:2">lineage 영향 분석</div>
<div class="kb-diagram-note">4. 리뷰어 코드 리뷰</div>
<div class="kb-diagram-note">5. Merge → 프로덕션 자동 배포</div>
<div class="kb-diagram-note">dbt 테스트 예:</div>
<div class="kb-diagram-note"># schema.yml</div>
<div class="kb-diagram-note">models:</div>
<div class="kb-diagram-tree-item" style="--depth:2">name: orders</div>
<div class="kb-diagram-note">columns:</div>
<div class="kb-diagram-tree-item" style="--depth:4">name: order_id</div>
<div class="kb-diagram-note">tests:</div>
<div class="kb-diagram-tree-item" style="--depth:6">not_null</div>
<div class="kb-diagram-tree-item" style="--depth:6">unique</div>
<div class="kb-diagram-tree-item" style="--depth:4">name: amount</div>
<div class="kb-diagram-note">tests:</div>
<div class="kb-diagram-tree-item" style="--depth:6">not_null</div>
<div class="kb-diagram-tree-item" style="--depth:6">accepted_range:</div>
<div class="kb-diagram-note">min_value: 0</div>
<div class="kb-diagram-note">max_value: 1000000</div>
<div class="kb-diagram-tree-item" style="--depth:4">name: status</div>
<div class="kb-diagram-note">tests:</div>
<div class="kb-diagram-tree-item" style="--depth:6">accepted_values:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">values:</div><div class="kb-diagram-node">'pending', 'completed', 'cancelled'</div></div>
<div class="kb-diagram-note">환경 분리:</div>
<div class="kb-diagram-note">개발: dev_schema (개인 샌드박스)</div>
<div class="kb-diagram-note">스테이징: staging_schema (CI 테스트)</div>
<div class="kb-diagram-note">프로덕션: prod_schema</div>
<div class="kb-diagram-note">dbt profiles.yml:</div>
<div class="kb-diagram-note">target: dev # 개인 개발 시</div>
<div class="kb-diagram-note">prod:</div>
<div class="kb-diagram-note">schema: prod_{{ env_var('DBT_SCHEMA') }}</div>
<div class="kb-diagram-note">Airflow CI/CD:</div>
<div class="kb-diagram-note">GitHub Actions → DAG 유효성 검사 → 자동 배포</div>
<div class="kb-diagram-note">파이프라인 롤백:</div>
<div class="kb-diagram-note">이전 DAG 버전으로 즉시 롤백 가능 (Git 기반)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD = 자동화 품질 검사 라인 — dbt 모델(제조 설계) 변경 시 [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)(품질 검사 요청) → 자동 테스트(공장 검사) → 통과 시만 배포(출하). 불량품(오류) 자동 차단!

---

## Ⅲ. [데이터 옵저버빌리티](/knowledge-base/studynote/16_bigdata/13_intro_trends/255_data_observability/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 옵저버빌리티 (Data Observability):</div>
<div class="kb-diagram-note">데이터 파이프라인의 상태를 실시간으로 파악하는 능력</div>
<div class="kb-diagram-note">5가지 데이터 품질 기둥:</div>
<div class="kb-diagram-note">1. 신선도 (Freshness):</div>
<div class="kb-diagram-note">데이터가 얼마나 최신인가?</div>
<div class="kb-diagram-note">체크: 마지막 업데이트 시간</div>
<div class="kb-diagram-note">알림: 예상보다 2시간 이상 지연 시 알림</div>
<div class="kb-diagram-note">2. 분포 (Distribution):</div>
<div class="kb-diagram-note">데이터 값의 통계적 분포가 정상인가?</div>
<div class="kb-diagram-note">체크: 평균, 표준편차, min/max 추적</div>
<div class="kb-diagram-note">이상: 매출 평균이 갑자기 0이 됨 → 파이프라인 오류</div>
<div class="kb-diagram-note">3. 볼륨 (Volume):</div>
<div class="kb-diagram-note">데이터 행 수가 정상 범위인가?</div>
<div class="kb-diagram-note">체크: 일별 행 수 변동</div>
<div class="kb-diagram-note">이상: 전날 100만 행 → 오늘 10 행 → 오류!</div>
<div class="kb-diagram-note">4. 스키마 (Schema):</div>
<div class="kb-diagram-note">데이터 구조가 변경되었는가?</div>
<div class="kb-diagram-note">체크: 컬럼 추가/삭제/타입 변경 탐지</div>
<div class="kb-diagram-note">이상: 상위 서비스에서 컬럼 이름 변경 → 자동 탐지</div>
<div class="kb-diagram-note">5. 계보 (Lineage):</div>
<div class="kb-diagram-note">데이터가 어디서 왔고 어디에 쓰이는가?</div>
<div class="kb-diagram-note">영향 분석:</div>
<div class="kb-diagram-note">orders 테이블 변경 → 어떤 하위 모델 영향받나?</div>
<div class="kb-diagram-note">도구:</div>
<div class="kb-diagram-note">Monte Carlo: 상용 데이터 옵저버빌리티</div>
<div class="kb-diagram-note">Metaplane: 경량 오픈소스 대안</div>
<div class="kb-diagram-note">dbt Artifacts: 기본 계보 추적</div>
<div class="kb-diagram-note">Great Expectations: 데이터 품질 테스트</div>
<div class="kb-diagram-note">Airflow UI: DAG 실행 현황 + 로그</div>
<div class="kb-diagram-note">Grafana: 파이프라인 지표 대시보드</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [데이터 옵저버빌리티](/knowledge-base/studynote/16_bigdata/13_intro_trends/255_data_observability/) = 공장 품질 제어 대시보드 — 신선도(재고 유통기한), 분포(제품 크기 통계), 볼륨(생산량), [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)(레시피 변경), 계보(원자재 출처). 모두 실시간 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링!

---

## Ⅳ. [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/324_dataops/) 성숙도 모델



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">DataOps 성숙도 단계:</div>
<div class="kb-diagram-note">Level 1 - 수동 (Ad Hoc):</div>
<div class="kb-diagram-note">스크립트 기반 파이프라인</div>
<div class="kb-diagram-note">버전 관리 없음</div>
<div class="kb-diagram-note">품질 체크: 수동</div>
<div class="kb-diagram-note">장애 탐지: 사용자 리포트</div>
<div class="kb-diagram-note">Level 2 - 반자동:</div>
<div class="kb-diagram-note">Git 버전 관리</div>
<div class="kb-diagram-note">Airflow 스케줄링</div>
<div class="kb-diagram-note">일부 품질 체크 자동화</div>
<div class="kb-diagram-note">Level 3 - CI/CD 도입:</div>
<div class="kb-diagram-note">코드 변경 → 자동 테스트 → 배포</div>
<div class="kb-diagram-note">스테이징 환경 분리</div>
<div class="kb-diagram-note">데이터 품질 게이트</div>
<div class="kb-diagram-note">Level 4 - 옵저버빌리티:</div>
<div class="kb-diagram-note">실시간 모니터링</div>
<div class="kb-diagram-note">이상 탐지 자동 알림</div>
<div class="kb-diagram-note">데이터 계보 추적</div>
<div class="kb-diagram-note">SLA 기반 알림</div>
<div class="kb-diagram-note">Level 5 - 완전 자동화:</div>
<div class="kb-diagram-note">자동 치유 (Auto-Healing)</div>
<div class="kb-diagram-note">AIOps 기반 이상 탐지</div>
<div class="kb-diagram-note">셀프서비스 파이프라인</div>
<div class="kb-diagram-note">현실적 목표:</div>
<div class="kb-diagram-note">대부분 기업: Level 1~2</div>
<div class="kb-diagram-note">성숙한 기업: Level 3~4</div>
<div class="kb-diagram-note">Level 5: 극소수 (Netflix, Airbnb 등)</div>
<div class="kb-diagram-note">핵심 지표:</div>
<div class="kb-diagram-note">파이프라인 성공률: &gt;99%</div>
<div class="kb-diagram-note">데이터 다운타임: &lt;1%</div>
<div class="kb-diagram-note">장애 탐지 시간 (MTTD): &lt;1시간</div>
<div class="kb-diagram-note">장애 복구 시간 (MTTR): &lt;4시간</div>
<div class="kb-diagram-note">데이터 품질 점수: &gt;95%</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/324_dataops/) 성숙도 = 공장 자동화 단계 — 수동(장인 공장)→반자동(기계 일부)→[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD(컨베이어 벨트)→[옵저버빌리티](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)(품질 카메라)→완전 자동(자율 공장). 대부분 2단계, 목표는 3~4단계!

---

## Ⅴ. 실무 시나리오 — 이커머스 [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/324_dataops/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">이커머스 DataOps 성숙도 향상:</div>
<div class="kb-diagram-note">AS-IS (Level 1):</div>
<div class="kb-diagram-note">데이터 파이프라인: 수동 Python 스크립트</div>
<div class="kb-diagram-note">배포: 데이터 엔지니어 직접 서버 수정</div>
<div class="kb-diagram-note">장애 탐지: 분석팀이 이상 데이터 발견 → 슬랙 DM</div>
<div class="kb-diagram-note">평균 장애 탐지: 6시간</div>
<div class="kb-diagram-note">월 장애 건수: 12건</div>
<div class="kb-diagram-note">TO-BE 목표: Level 3~4</div>
<div class="kb-diagram-note">구축:</div>
<div class="kb-diagram-note">1. dbt + GitHub + CI (3개월):</div>
<div class="kb-diagram-note">모든 변환 로직 dbt 모델로 전환</div>
<div class="kb-diagram-note">GitHub Actions: PR 시 자동 dbt test</div>
<div class="kb-diagram-note">환경 분리: dev/staging/prod</div>
<div class="kb-diagram-note">효과: 배포 오류 70% 감소</div>
<div class="kb-diagram-note">2. Airflow + 모니터링 (2개월):</div>
<div class="kb-diagram-note">DAG 실행 현황 Grafana 대시보드</div>
<div class="kb-diagram-note">실패 DAG → PagerDuty 알림 (5분 내)</div>
<div class="kb-diagram-note">효과: 장애 탐지 6시간 → 30분</div>
<div class="kb-diagram-note">3. 데이터 옵저버빌리티 (Monte Carlo, 2개월):</div>
<div class="kb-diagram-note">신선도·볼륨·분포 자동 모니터링</div>
<div class="kb-diagram-note">이상 탐지 → Slack 자동 알림</div>
<div class="kb-diagram-note">효과: 데이터 이상 조기 탐지</div>
<div class="kb-diagram-note">(파이프라인 오류 후 1시간 내 탐지)</div>
<div class="kb-diagram-note">최종 결과:</div>
<div class="kb-diagram-note">파이프라인 성공률: 78% → 99.1%</div>
<div class="kb-diagram-note">월 장애 건수: 12건 → 2건</div>
<div class="kb-diagram-note">장애 탐지: 6시간 → 25분 (MTTD)</div>
<div class="kb-diagram-note">데이터 신뢰도 점수: 분석팀 62% → 91%</div>
<div class="kb-diagram-note">데이터 엔지니어 야간 호출: 월 8회 → 0회</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 이커머스 [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/324_dataops/) = 공장 자동화 성과 — 수동 공장(Level 1)에서 컨베이어 벨트+품질 카메라(Level 3~4)로. 장애 탐지 6시간→25분. 야간 호출 월 8회→0회!

---

## 📌 관련 개념 맵

```
DataOps
+-- 핵심 원칙
|   +-- 데이터 CI/CD
|   +-- 버전 관리 (Git)
|   +-- 자동 품질 테스트
|   +-- 옵저버빌리티
+-- 도구
|   +-- dbt (변환 + 테스트)
|   +-- Airflow (오케스트레이션)
|   +-- Great Expectations (품질)
|   +-- Monte Carlo (옵저버빌리티)
+-- 지표
|   +-- 데이터 다운타임
|   +-- MTTD, MTTR
|   +-- 파이프라인 성공률
+-- 관련
    +-- MLOps (ML 파이프라인)
    +-- 데이터 메시 (거버넌스)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[데이터 웨어하우스 ETL (1990s~)]
수동 스크립트
야간 배치 처리
      |
      v
[Airflow 등장 (2014)]
워크플로우 자동화
오케스트레이션
      |
      v
[dbt 등장 (2016)]
SQL 변환 버전 관리
데이터 CI 가능화
      |
      v
[DataOps 개념 (2018~)]
DevOps 원칙 데이터 적용
      |
      v
[데이터 옵저버빌리티 (2020~)]
Monte Carlo, Metaplane
데이터 신뢰성 측정
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/324_dataops/) = [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공장 자동화 — 소프트웨어 공장([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/))처럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공장도 자동화. 수동 스크립트→자동 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD. 품질+속도 동시 향상!
2. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD = 자동 품질 검사 — dbt 모델(설계) 변경 시 자동 테스트. 오류 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배포 차단. 수동 배포 대비 오류 70% 감소!
3. [데이터 옵저버빌리티](/knowledge-base/studynote/16_bigdata/13_intro_trends/255_data_observability/) = 공장 품질 카메라 — 신선도·볼륨·분포 실시간 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링. [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) 6시간→25분. 야간 호출 0회!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 49 / 373

← **이전**: [048. MLOps — 머신러닝 운영](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/048_mlops_machine_learning_operations/)
**다음**: [BizDevOps — 비즈니스 정렬 (BizDevOps Business Alignment)](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/050_bizdevops_business_alignment/) →

---
