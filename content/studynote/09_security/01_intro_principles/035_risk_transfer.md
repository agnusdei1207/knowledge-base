+++
title = "035. 위험 전가 (Risk Transfer)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-security"]

[extra]
tags = ["studynote-security"]
+++

> **핵심 인사이트**
> 1. [위험 전가](/knowledge-base/studynote/09_security/01_intro_principles/051_risk_transfer/)([Risk Transfer](/knowledge-base/studynote/09_security/01_intro_principles/051_risk_transfer/))는 조직이 특정 위험의 재정적 결과를 보험, 계약, 아웃소싱 등을 통해 제3자에게 이전하는 위험 처리([Risk Response](/knowledge-base/studynote/04_software_engineering/01_overview_principles/042_risk_response_strategies/)) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
> 2. 위험 자체가 사라지는 게 아니라 재정적 책임만 이전되므로, [잔여 위험](/knowledge-base/studynote/09_security/01_intro_principles/038_residual_risk/)([Residual Risk](/knowledge-base/studynote/09_security/01_intro_principles/038_residual_risk/))과 이전 비용(보험료, 계약 비용)을 반드시 고려해야 한다.
> 3. 사이버보험([Cyber Insurance](/knowledge-base/studynote/09_security/20_extra_exam_prep/1027_cyber_insurance/))은 [위험 전가](/knowledge-base/studynote/09_security/01_intro_principles/051_risk_transfer/)의 현대적 형태로, [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/)·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 침해 시 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 비용과 법적 비용을 보장한다.

---

## I. 위험 처리 4대 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">위험 식별 완료</div>
<div class="kb-diagram-note">v</div>
<div class="kb-diagram-note">+---&gt; 위험 수용 (Accept) &lt;- 낮은 위험, 비용&gt;이익</div>
<div class="kb-diagram-note">위험 회피 (Avoid) &lt;- 매우 높은 위험, 활동 중단</div>
<div class="kb-diagram-note">위험 경감 (Mitigate) &lt;- 통제로 확률/영향 감소</div>
<div class="kb-diagram-note">+---&gt; 위험 전가 (Transfer) &lt;- 제3자에게 재정 책임 이전</div>
</div>
</div>



| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)     | 위험 제거 | 비용    | 적합 상황              |
|---------|---------|---------|----------------------|
| 수용     | 없음    | 없음    | 낮은 영향/[확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)         |
| 회피     | 완전    | 높음    | 치명적 위험            |
| 경감     | 부분    | 중간    | 기술적 대응 가능       |
| **전가** | 재정적  | 보험료  | 재정 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/), 전문 영역 |

> 📢 **섹션 요약 비유**: 불이 났을 때 혼자 감당하기 힘들면 화재보험 — 위험 자체는 사라지지 않지만 손실 부담을 나눈다.

---

## II. [위험 전가](/knowledge-base/studynote/09_security/01_intro_principles/051_risk_transfer/) 수단

```
위험 전가 방법
+-- 보험 (Insurance)
|   +-- 사이버보험 (Cyber Liability Insurance)
|   +-- 전문직 배상보험 (E&O)
|   +-- 임원배상보험 (D&O)
|
+-- 계약 조항 (Contractual Transfer)
|   +-- 면책 조항 (Indemnification Clause)
|   +-- SLA 패널티 전가
|   +-- 손해배상 한도 조항
|
+-- 아웃소싱 (Outsourcing)
    +-- 클라우드 위탁 (SaaS/IaaS)
    +-- 보안 운영 위탁 (MSSP)
    +-- 데이터 처리 위탁 (책임 계약 포함)
```

> 📢 **섹션 요약 비유**: 집을 지키는 경비원을 직접 고용하든, 경비회사에 맡기든 — 사고 책임을 누가 지느냐가 전가의 핵심이다.

---

## III. 사이버보험 ([Cyber Insurance](/knowledge-base/studynote/09_security/20_extra_exam_prep/1027_cyber_insurance/)) 심화

```
보장 범위:
+-- 1차 손실 (First-Party)
|   +-- 데이터 복구 비용
|   +-- 사업 중단 손실 (BII)
|   +-- 랜섬웨어 몸값 (일부 정책)
|   +-- 사이버 포렌식 비용
|
+-- 3차 손실 (Third-Party / Liability)
    +-- 개인정보 침해 피해자 배상
    +-- 규제 과징금 (GDPR, CCPA)
    +-- 소송 방어 비용
```

| 항목            | 내용                              |
|----------------|----------------------------------|
| 보험료 결정 요소 | 매출, 산업, 보안 성숙도, 청구 이력  |
| 언더라이팅     | [MFA](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/) 필수, [EDR](/knowledge-base/studynote/09_security/04_endpoint_security/325_edr/), [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)       |
| 제외 사항       | 국가 주도 공격([War](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/226_war/) exclusion), 내부 부정 |
| 지급 조건       | 인시던트 응답 절차 준수 여부        |

> 📢 **섹션 요약 비유**: 사이버보험은 해커가 침입하더라도 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)비용을 보험사가 낸다는 계약 — 단, 문단속([MFA](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/)·[백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/))을 안 했으면 보장 안 된다.

---

## [IV](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). 아웃소싱을 통한 [위험 전가](/knowledge-base/studynote/09_security/01_intro_principles/051_risk_transfer/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">On-Premise Cloud (IaaS/PaaS/SaaS)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">보안 책임 전부</div><div class="kb-diagram-node">공유 책임 모델</div></div>
<div class="kb-diagram-note">사용자 부담 -&gt; 물리 보안, 네트워크: CSP</div>
<div class="kb-diagram-note">OS, 앱, 데이터: 사용자</div>
<div class="kb-diagram-note">MSSP (Managed Security Service Provider)</div>
<div class="kb-diagram-note">SOC 운영, 위협 탐지, 인시던트 대응 위탁</div>
<div class="kb-diagram-tree-item" style="--depth:0">보안 전문 인력 부담 전가</div>
</div>
</div>



| 아웃소싱 유형 | 전가 대상 위험          | 주의점               |
|-------------|------------------------|---------------------|
| [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 이용    | 인프라·앱 취약점        | [데이터 주권](/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/) 이슈     |
| MSSP 위탁    | 보안 운영·탐지 실패     | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 검토, 의존성     |
| 클라우드     | 하드웨어 장애, 재해     | 공유 책임 범위 명확화|

> 📢 **섹션 요약 비유**: 요리는 직접 하되, 식재료 보관과 화재 예방은 전문 주방 업체에 맡기는 것 — 역할 분리가 책임 분리다.

---

## V. 실무 시나리오 — [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 대비

| 구분         | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)              | 세부 내용                          |
|-------------|------------------|-----------------------------------|
| 예방         | [위험 경감](/knowledge-base/studynote/09_security/01_intro_principles/036_risk_mitigation/)         | [EDR](/knowledge-base/studynote/09_security/04_endpoint_security/325_edr/), 패치, [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), [MFA](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/)               |
| 보험         | [위험 전가](/knowledge-base/studynote/09_security/01_intro_principles/051_risk_transfer/)         | 사이버보험 ([랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 대응 특약)    |
| 지불 결정    | [위험 수용](/knowledge-base/studynote/09_security/01_intro_principles/037_risk_acceptance/)/전가     | 보험사·법무팀과 협의, FBI 신고     |
| [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)         | [위험 경감](/knowledge-base/studynote/09_security/01_intro_principles/036_risk_mitigation/)+전가     | [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 복원 + 포렌식 비용 보험 청구  |
| 재발 방지    | [위험 경감](/knowledge-base/studynote/09_security/01_intro_principles/036_risk_mitigation/)         | 취약점 패치, [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 전환    |

> 📢 **섹션 요약 비유**: [랜섬웨어](/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/)는 예방(경감) + 보험(전가) + [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)(경감)의 3중 안전망으로 대비 — 하나만으로는 부족하다.

---

## 📌 관련 개념 맵

```
위험 전가 (Risk Transfer)
+-- 목적: 재정적 결과를 제3자에게 이전
+-- 수단
|   +-- 사이버보험 (1st/3rd Party)
|   +-- 계약 조항 (면책, SLA 패널티)
|   +-- 아웃소싱 (MSSP, 클라우드)
+-- 관련 개념
|   +-- 잔여 위험 (Residual Risk)
|   +-- 공유 책임 모델 (CSP)
|   +-- SLA (Service Level Agreement)
+-- 위험 처리 4전략
    +-- 수용 / 회피 / 경감 / 전가
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[전통 위험 관리]
보험 = 재해·화재 중심, 사이버 없음
      |
      v
[IT 아웃소싱 시대 (1990s~)]
계약 통한 IT 위험 전가 일반화
      |
      v
[클라우드 공유 책임 모델 (2006~)]
AWS IaaS: 물리/네트워크 위험 CSP 전가
      |
      v
[사이버보험 본격화 (2014~)]
대형 침해 사고 후 수요 급증 (Target, Sony)
      |
      v
[현재: 언더라이팅 강화]
MFA, EDR, 백업 미비시 보험 거절/보험료 상승
랜섬웨어 지급 제한 정책 확산
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [위험 전가](/knowledge-base/studynote/09_security/01_intro_principles/051_risk_transfer/)는 사고가 났을 때의 돈 걱정을 보험회사에 넘기는 거예요.
2. 해킹 당했을 때 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 비용을 사이버보험이 대신 내주는 것도 같은 원리예요.
3. 하지만 문단속(보안)을 안 했으면 보험도 안 나오니까, 예방이 먼저예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 35 / 1108

← **이전**: [위험 회피 전략 심화 (Risk Avoidance & Treatment)](/knowledge-base/studynote/09_security/01_intro_principles/034_risk_avoidance/)
**다음**: [036. 위험 경감 (Risk Mitigation)](/knowledge-base/studynote/09_security/01_intro_principles/036_risk_mitigation/) →

---
