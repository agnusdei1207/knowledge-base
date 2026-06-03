---
title: 333. CNAPP 클라우드 통합 보안 플랫폼 (CNAPP Cloud Native Application Protection Platform
  CSPM CWPP Risk Graph Wiz Agentless)
date: '2026-05-09'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[256_cnapp_cloud_native_application_protection|CNAPP]] ([[199_cloud_native_architecture_msa_cicd_devops|Cloud Native]] Application [[571_protection_vs_security|Protection]] Platform, [[531_cloud_native_architecture|클라우드 네이티브]] 애플리케이션 [[571_protection_vs_security|보호]] 플랫폼)은 [[780_cspm_cloud_security_posture_management|CSPM]] + [[332_cwpp|CWPP]] + [[793_iac_idempotency_template|IaC]] 보안 스캔 + [[513_container_security|컨테이너 보안]]을 단일 플랫폼으로 통합한 클라우드 보안 솔루션이다. Gartner가 2021년 명명했다.
> 2. **[[096_risk_non_risk_architecture_evaluation_flaws|Risk]] Graph의 혁신**: Wiz가 개척한 [[096_risk_non_risk_architecture_evaluation_flaws|Risk]] Graph는 개별 취약점을 단독으로 평가하는 대신, 취약점 A + 퍼블릭 노출 B + 과도한 권한 C 가 조합될 때만 실제 공격 경로가 형성된다는 것을 [[070_graph_datastructure|그래프]]로 [[003_bigdata_7v|시각화]]한다. 소음(False Positive)을 줄이고 실제 위험에 집중한다.
> 3. **판단 포인트**: Agentless 방식([[022_snapshot_backup_architecture|스냅샷]] 스캔)은 프로덕션 무영향이 장점이고, Agent 방식은 런타임 실시간 탐지가 장점이다. CNAPP은 두 방식을 결합해 정적+동적 보안을 함께 제공한다.

---

## Ⅰ. 개요 및 필요성

클라우드 환경에서는 인프라([[793_iac_idempotency_template|IaC]]), [[561_container_based_deployment|컨테이너]] 이미지, 실행 중인 워크로드, 클라우드 [[009_config|설정]]이 모두 별개의 보안 도구로 관리되었다. 운영자는 Prisma Cloud ([[780_cspm_cloud_security_posture_management|CSPM]]), Aqua [[283_security_tactics|Security]] ([[332_cwpp|CWPP]]), Checkov ([[793_iac_idempotency_template|IaC]]) 등 여러 콘솔을 동시에 운영해야 했다.

CNAPP은 이 [[136_variance|분산]]된 보안 도구를 단일 플랫폼으로 통합하고, 전체 클라우드 환경의 보안 상태를 하나의 [[070_graph_datastructure|그래프]]로 이해할 수 있게 한다. Gartner Market Guide 2021에서 CNAPP을 클라우드 보안의 미래 방향으로 제시했다.

> 📢 **섹션 요약 비유**: [[256_cnapp_cloud_native_application_protection|CNAPP]] 이전은 경보 시스템(침입), 잠금장치 상태([[009_config|설정]]), [[933_cctv|CCTV]](런타임)를 각기 다른 앱으로 관리하는 것이다. CNAPP은 이 모든 것을 하나의 스마트홈 앱으로 통합한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+--------------------------------------------------------------+
|                    CNAPP 통합 구조                            |
+--------------------------------------------------------------+
|                                                              |
|  +----------------------------------------------------------+ |
|  |                    Risk Graph                            | |
|  |  (취약점 + 노출도 + 권한 조합 -> 실제 공격 경로 시각화) | |
|  +----------------------------------------------------------+ |
|               |                                             |
|    +----------+----------+                                  |
|    v          v          v                                  |
|  CSPM       CWPP       IaC 보안                             |
|  (설정 오류) (런타임)  (Terraform)                          |
|    |          |          |                                  |
|    +----------+----------+                                  |
|               v                                             |
|  Agentless (스냅샷) + Agent (런타임) 복합 탐지              |
+--------------------------------------------------------------+
```

| 구성 요소 | 역할 |
|:---|:---|
| [[780_cspm_cloud_security_posture_management|CSPM]] | 클라우드 계정 [[009_config|설정]] [[040_error_detection|오류 탐지]] (CIS [[149_benchmark|Benchmark]]) |
| [[332_cwpp|CWPP]] | [[561_container_based_deployment|컨테이너]]/[[598_vm_migration_nic|VM]] 런타임 [[571_protection_vs_security|보호]], 이상 행동 탐지 |
| [[793_iac_idempotency_template|IaC]] 보안 | [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]]/CloudFormation 코드 스캔 |
| [[096_risk_non_risk_architecture_evaluation_flaws|Risk]] [[104_graph|Graph]] | 취약점 조합 기반 실제 공격 경로 우선순위화 |

> 📢 **섹션 요약 비유**: [[096_risk_non_risk_architecture_evaluation_flaws|Risk]] Graph는 질병 예측 모델이다. 고혈압(취약점) 하나가 아니라 고혈압 + 흡연 + 비만의 조합이 심장마비(공격 성공) 위험을 만든다.

---

## Ⅲ. 비교 및 연결

| 항목 | [[780_cspm_cloud_security_posture_management|CSPM]] 단독 | [[332_cwpp|CWPP]] 단독 | [[256_cnapp_cloud_native_application_protection|CNAPP]] 통합 |
|:---|:---|:---|:---|
| 커버리지 | 클라우드 [[009_config|설정]] | 런타임 워크로드 | 전체 [[057_stack|스택]] 통합 |
| 공격 경로 분석 | 제한적 | 제한적 | [[096_risk_non_risk_architecture_evaluation_flaws|Risk]] Graph로 통합 |
| 오탐 | 많음 | 많음 | 조합 분석으로 감소 |
| 콘솔 수 | 별도 | 별도 | 단일 통합 |

Wiz vs Prisma Cloud:
- **Wiz**: Agentless [[022_snapshot_backup_architecture|스냅샷]] 기반, [[096_risk_non_risk_architecture_evaluation_flaws|Risk]] [[104_graph|Graph]], 빠른 도입
- **Prisma Cloud**: Agent+Agentless 혼합, 상세 런타임 제어, 엔터프라이즈

> 📢 **섹션 요약 비유**: CSPM만 있으면 잠금장치 상태만 알고, CWPP만 있으면 침입자 움직임만 안다. CNAPP은 잠금장치가 열려 있는데 침입자가 이미 안에 있다는 상황을 한눈에 보여준다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[256_cnapp_cloud_native_application_protection|CNAPP]] 도입 로드맵

1. **현황 파악**: 기존 [[780_cspm_cloud_security_posture_management|CSPM]]/[[332_cwpp|CWPP]] 도구 인벤토리 및 커버리지 갭 분석
2. **Agentless 스캔 도입**: 프로덕션 영향 없이 클라우드 계정 전체 스캔
3. **[[096_risk_non_risk_architecture_evaluation_flaws|Risk]] [[104_graph|Graph]] 구성**: 고위험 공격 경로 [[655_ir_detection_analysis|식별]] 및 우선순위화
4. **Agent 확장**: 중요 워크로드에 런타임 탐지 에이전트 추가

### [[435_checklist_based_testing|체크리스트]]

1. 멀티클라우드(AWS, Azure, GCP) 환경을 단일 CNAPP으로 통합 관리하는가?
2. [[096_risk_non_risk_architecture_evaluation_flaws|Risk]] Graph에서 퍼블릭 노출 + 고위험 취약점 + 과도한 권한 조합을 24시간 내 감지하는가?
3. [[793_iac_idempotency_template|IaC]] 코드 변경이 [[256_cnapp_cloud_native_application_protection|CNAPP]] [[793_iac_idempotency_template|IaC]] 스캔을 [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인에서 통과한 후 배포되는가?

> 📢 **섹션 요약 비유**: [[256_cnapp_cloud_native_application_protection|CNAPP]] 도입은 마치 도시 전체의 CCTV를 AI로 연결하는 것이다. 개별 CCTV보다 용의자가 A지점에서 B지점을 거쳐 C에 도달했다는 경로 분석이 중요하다.

---

## Ⅴ. 기대효과 및 결론

[[256_cnapp_cloud_native_application_protection|CNAPP]] 도입으로 보안 도구 수를 줄이고 통합 가시성을 확보한다. [[096_risk_non_risk_architecture_evaluation_flaws|Risk]] [[104_graph|Graph]] 기반 우선순위화로 보안 팀이 실제 위험에 집중하고, 오탐으로 인한 피로감(Alert Fatigue)이 감소한다.

CNAPP의 핵심 가치는 **"개별 취약점이 아니라 공격 경로(Attack Path) 단위로 보안을 관리하는 것"**이다. 취약점 수가 수천 개여도 실제 익스플로잇 가능한 경로는 소수이며, 그것에 집중해야 한다.

> 📢 **섹션 요약 비유**: 1만 개의 경보가 울리는 것보다 지금 당장 문을 잠가야 할 1개를 정확히 알려주는 것이 CNAPP의 가치다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[256_cnapp_cloud_native_application_protection|CNAPP]] ([[199_cloud_native_architecture_msa_cicd_devops|Cloud Native]] Application [[571_protection_vs_security|Protection]] Platform) | [[780_cspm_cloud_security_posture_management|CSPM]] + [[332_cwpp|CWPP]] + [[793_iac_idempotency_template|IaC]] 보안 통합 |
| [[096_risk_non_risk_architecture_evaluation_flaws|Risk]] [[104_graph|Graph]] | 취약점 조합 기반 공격 경로 [[003_bigdata_7v|시각화]] |
| Agentless 스캔 | [[022_snapshot_backup_architecture|스냅샷]] 기반, 프로덕션 무영향 |
| Wiz | Agentless [[256_cnapp_cloud_native_application_protection|CNAPP]] 선도 솔루션 |
| Alert Fatigue | 과도한 오탐으로 인한 보안 팀 피로 |

### 📈 관련 키워드 및 발전 흐름도

```text
분리된 보안 도구              CNAPP 등장                현대 CNAPP
------------------   --------------------------   ------------------------
CSPM 별도           ->  Gartner CNAPP 정의(2021)  ->  Risk Graph 중심
CWPP 별도                Wiz Agentless 혁신           AI 기반 공격 예측
IaC 스캐너 별도            멀티클라우드 통합             Supply Chain 통합
Alert Fatigue              Risk Graph 우선순위화         SBOM + CNAPP 연동
```

### 👶 어린이를 위한 3줄 비유 설명

1. CNAPP은 집 전체를 지키는 스마트홈 보안 시스템이에요. 문잠금([[780_cspm_cloud_security_posture_management|CSPM]]), 방범카메라([[332_cwpp|CWPP]]), 건축설계 점검([[793_iac_idempotency_template|IaC]])을 하나의 앱으로 관리해요.
2. [[096_risk_non_risk_architecture_evaluation_flaws|Risk]] Graph는 문이 열려 있고, 창문도 열려 있고, 경보도 꺼져 있다는 세 가지가 동시에 일어날 때만 위험 경보를 울려요.
3. 하나씩 경보가 울리면 너무 많아서 무시하게 되지만, 진짜 위험한 조합만 골라서 알려주니까 더 안전해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 333 / 373

← **이전**: [[332_cwpp|332. CWPP 런타임 워크로드 보호 (CWPP Cloud Workload Protection Platform Falco eBPF seccomp]]
**다음**: [[334_opa_gatekeeper_rego|334. Policy as Code OPA Gatekeeper Rego (OPA Open Policy Agent Gatekeeper Rego]] →

---
