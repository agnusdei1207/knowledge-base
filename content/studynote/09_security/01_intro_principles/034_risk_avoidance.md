---
title: "Risk Avoidance & Treatment"
date: "2026-03-04"
tags:
  - "studynote-security"
---

> **핵심 인사이트 3줄**
> 1. 위험 처리([Risk](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) Treatment)는 회피(Avoidance)·감소(Reduction)·전가(Transfer)·수용(Acceptance) 4가지 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 조합으로, 각 위험의 발생 가능성·영향도·비용-편익 분석을 기반으로 선택한다.
> 2. 위험 회피([Risk](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) Avoidance)는 위험 유발 활동 자체를 중단하는 가장 확실한 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이나, 비즈니스 기회 손실을 수반하므로 [잔여 위험](/studynote/09_security/01_intro_principles/038_residual_risk/)([Residual Risk](/studynote/09_security/01_intro_principles/038_residual_risk/))이 허용 불가 수준일 때만 적용한다.
> 3. 현대 사이버보안에서는 [제로 트러스트 아키텍처](/studynote/12_it_management/05_security_compliance/184_zero_trust_architecture/)·보험(사이버보험)·[MFA](/studynote/09_security/11_iam_access_control/552_mfa/)·[EDR](/studynote/09_security/04_endpoint_security/325_edr/) 등 다층적 위험 처리 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 조합이 표준으로, 단일 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)에 의존하는 것은 안티패턴이다.

---

## Ⅰ. 위험 처리 4대 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

```
위험 처리 (Risk Treatment) 옵션:

    발생 가능성
         | 높음
         |   [회피]          [감소]
         |   위험 활동 중단   통제 적용
         |
         |   [수용]          [전가]
         | 낮음 위험 허용     보험/계약
         +--------------------------
              낮음            높음
                    영향도
```

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)        | 정의                          | 적용 상황               |
|-----------|------------------------------|------------------------|
| 회피 (Avoidance) | 위험 활동 자체 중단        | [잔여 위험](/studynote/09_security/01_intro_principles/038_residual_risk/) > 허용 한계   |
| 감소 (Reduction) | 통제 적용으로 위험 축소    | 비용-편익 긍정적        |
| 전가 (Transfer) | 보험·계약으로 책임 이전    | 보험 가능, 계약 가능   |
| 수용 (Acceptance) | 위험 인식 후 허용          | 영향·가능성 모두 낮음   |

�� **섹션 요약 비유**: 위험 처리 4전략은 교통 안전 대응이다 — 그 길을 안 가기(회피), 안전운전(감소), 보험 가입(전가), 작은 스크래치는 그냥 두기(수용).

---

## Ⅱ. 위험 회피 상세 — 언제 적용하는가

### 회피 적용 기준

```
위험 회피 결정 프레임워크:

잔여 위험 = 고유 위험 - 통제 효과
  +- 잔여 위험 > 위험 허용 기준 (Risk Appetite)
     -> 위험 회피 고려

추가 판단:
  1. 통제 비용 > 비즈니스 가치? -> 회피
  2. 규제·법적 요구사항 위반 위험? -> 회피
  3. 평판·브랜드 치명적 영향? -> 회피
```

### 실제 회피 사례

| 상황               | 위험 회피 결정                  |
|-----------------|-------------------------------|
| BYOD [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)        | 개인 기기 전면 금지 (민감 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 위험)|
| [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) | EOL [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 즉시 제거        |
| 특정 국가 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)  | 개인정보법 미충족 국가 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 철수|
| [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 연결         | 취약한 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 기기 네트워크 분리   |

📢 **섹션 요약 비유**: 위험 회피는 폭설 예보에 운전을 안 하는 것이다 — 아무리 좋은 타이어(통제)를 달아도 위험이 너무 크다면, 아예 운전(활동) 자체를 안 하는 것이 최선이다.

---

## Ⅲ. [위험 전가](/studynote/09_security/01_intro_principles/051_risk_transfer/) — [사이버 보험](/studynote/09_security/20_extra_exam_prep/1027_cyber_insurance/)

### [사이버 보험](/studynote/09_security/20_extra_exam_prep/1027_cyber_insurance/) 커버리지

| 유형                | 보장 내용                       |
|------------------|-------------------------------|
| 1차 손해 (First Party) | [사고 대응](/studynote/09_security/01_intro_principles/009_incident_response/)·[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)·포렌식 비용     |
| 3자 배상 (Third Party) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출 피해자 손해배상    |
| 비즈니스 중단       | [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/)·DDoS 피해 수익 손실    |
| 규제 벌금           | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)·[CCPA](/studynote/09_security/16_data_privacy/800_ccpa/) 과징금 일부          |

### [사이버 보험](/studynote/09_security/20_extra_exam_prep/1027_cyber_insurance/) 요율 결정 요소

- [MFA](/studynote/09_security/11_iam_access_control/552_mfa/)(다중 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)) 적용 여부
- [EDR](/studynote/09_security/04_endpoint_security/325_edr/)/[XDR](/studynote/02_operating_system/02_process_thread/127_xdr_external_data_representation/) 솔루션 보유 여부
- 정기 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 및 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 테스트
- 직원 보안 교육 이수율
- 이전 사고 이력

📢 **섹션 요약 비유**: [사이버 보험](/studynote/09_security/20_extra_exam_prep/1027_cyber_insurance/)은 자동차 보험이다 — 좋은 안전장치([MFA](/studynote/09_security/11_iam_access_control/552_mfa/)·[EDR](/studynote/09_security/04_endpoint_security/325_edr/))를 갖출수록 보험료가 낮아지고, 사고가 나도 금전적 손해를 보전받는다.

---

## Ⅳ. 위험 감소 — 다층 방어 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

```
Defense in Depth (심층 방어):

외부 경계: 방화벽·WAF·DDoS 방어
     |
네트워크: 세그멘테이션·VLAN·IDS/IPS
     |
엔드포인트: EDR·안티멀웨어·패치 관리
     |
애플리케이션: SAST·DAST·API 보안
     |
데이터: 암호화·DLP·접근 통제
     |
사람: MFA·보안 교육·피싱 훈련
```

📢 **섹션 요약 비유**: 심층 방어는 양파 껍질이다 — 한 층을 뚫어도 다음 층이 있어서, 공격자가 최종 목표([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에 도달하기 전에 여러 장벽을 넘어야 한다.

---

## Ⅴ. [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)와 위험 처리 통합

```
제로 트러스트 원칙: "절대 신뢰하지 말고, 항상 검증하라"

위험 처리 관점에서:
  회피: 기본 거부 정책 (All deny, explicit allow)
  감소: 최소 권한 원칙 + MFA + 마이크로 세그멘테이션
  전가: 사이버 보험 + SLA 계약
  수용: 저위험 API 엔드포인트 모니터링만

제로 트러스트 핵심 컴포넌트:
  IAM -> MFA -> Conditional Access -> SIEM -> SOAR
```

📢 **섹션 요약 비유**: [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)는 "ID 카드는 있어도 매번 검사"하는 보안이다 — 임직원(신뢰 내부자)도 매번 신원 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)([MFA](/studynote/09_security/11_iam_access_control/552_mfa/))하고, 최소한 접근 권한만 준다.

---

## 📌 관련 개념 맵

```
위험 처리 전략 (Risk Treatment)
+-- 4대 전략
|   +-- 회피 (Avoidance) — 활동 중단
|   +-- 감소 (Reduction) — 통제 적용
|   +-- 전가 (Transfer) — 보험·계약
|   +-- 수용 (Acceptance) — 인식 후 허용
+-- 전가 수단
|   +-- 사이버 보험
|   +-- 계약 SLA·면책 조항
+-- 감소 기법
|   +-- 심층 방어 (Defense in Depth)
|   +-- 제로 트러스트 아키텍처
+-- 관련 프레임워크
    +-- ISO 27005 (위험 관리)
    +-- NIST SP 800-30
    +-- FAIR 모델 (정량적 위험 분석)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|              위험 처리 전략 발전 흐름                            |
+--------------+--------------------+-----------------------------+
| 2002년       | NIST SP 800-30 v1  | 최초 체계적 위험 관리 가이드 |
| 2005년       | ISO 27005:2005     | 정보보안 위험 관리 국제 표준 |
| 2011년       | FAIR 모델          | 정량적 사이버 위험 분석      |
| 2014년       | NIST CSF           | 핵심 보안 프레임워크          |
| 2017년       | GDPR 시행          | 규제 기반 위험 처리 의무화   |
| 2020년대     | 사이버 보험 급성장 | 랜섬웨어 -> 위험 전가 증가   |
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
위험 식별 -> 위험 분석 (발생가능성×영향도) -> 처리 전략 선택
    v               v                           v
자산 목록       위험 매트릭스             회피/감소/전가/수용
    v
잔여 위험 -> 허용 기준 비교 -> 보험/제로 트러스트
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 위험 처리 4전략은 비가 올 때 대처법이다 — 외출을 안 하기(회피), 우산 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)(감소), 비 피해 보험 들기(전가), 조금 맞아도 괜찮다고 하기(수용).
2. 위험 회피는 폭설에 운전을 안 하는 것이다 — 아무리 좋은 스노우 타이어(통제)도 너무 위험하면, 아예 안 가는 것이 답이다.
3. 심층 방어는 양파 껍질이다 — 한 겹을 뚫어도 다음 겹이 있어서, 결국 공격자가 모든 겹을 다 뚫어야만 성공할 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 34 / 1108

<- **이전**: [위험 대응 전략 (Risk Response Strategies)](/studynote/09_security/01_intro_principles/033_risk_response_strategies/)
**다음**: [035. 위험 전가 (Risk Transfer)](/studynote/09_security/01_intro_principles/035_risk_transfer/) ->

---
