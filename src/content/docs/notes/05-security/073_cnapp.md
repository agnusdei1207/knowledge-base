---
sidebar:
  order: 73
  label: "073. 클라우드 네이티브 애플리케이션 보호 플랫폼 (Cloud-Native Application Protection Platform, CNAPP)"
  badge:
    text: "미출 · 70%"
    variant: note
title: "코드부터 런타임까지의 전주기 클라우드 보안 통합 : CNAPP (Gartner CNAPP & Attack Path Analysis)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 73
extra:
  question_no: "073"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "Gartner CNAPP 통합 프레임워크, Shift-Left(IaC/SAST/SCA) + CSPM(형상 관리) + CIEM(권한 관리) + CWPP(워크로드 보호) 융합, 단일 그래프 DB 기반 실질적 공격 경로(Attack Path) 분석"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **CNAPP(Cloud-Native Application Protection Platform / Gartner 표준)**: 소스코드(SAST/SCA), 코드형 인프라(IaC), 멀티 클라우드 오설정(CSPM), 과다 권한(CIEM), 컨테이너/VM 런타임 위협(CWPP)으로 파편화된 개별 보안 도구들을 단일 그래프 데이터베이스로 통합하여, 개발(Build)부터 운영(Runtime)에 이르는 클라우드 전주기(Code-to-Cloud) 위험을 연계 분석하고 조치 우선순위를 제공하는 차세대 통합 클라우드 보안 플랫폼.
- **보안 도구 사일로 및 경보 피로(Alert Fatigue & Disconnected Silos Defect)**: CSPM, CWPP, SAST 등 개별 도구가 수만 건의 독립 경보를 쏟아내지만, 실제 "퍼블릭 인터넷 노출 + 취약한 컨테이너 + 과다 IAM 관리자 권한 + 데이터베이스 접근"이 결합된 실질적 침해 위험 경로(Attack Path)를 파악하지 못해 조치가 지연되는 구조적 결함.

</details>

- 정의/개념: Gartner 표준에 기반하여 **Shift-Left(IaC/SCA) $\rightarrow$ CSPM(클라우드 형상 관리) $\rightarrow$ CIEM(인프라 권한 관리) $\rightarrow$ CWPP(런타임 워크로드 보호)** 를 단일 그래프 모델로 결합하고, **실질적 공격 경로(Attack Path Analysis)** 를 도출하여 치명적 위험의 조치 우선순위를 산출하는 **전주기 클라우드 보안 아키텍처**
- 배경/필요성: 마이크로서비스(MSA), 쿠버네티스, CI/CD 자동화로 배포 주기가 초 단위로 단축됨에 따라, 런타임 발견 결함을 원본 IaC 코드(Git) 라인으로 역추적(Traceability)하여 즉각 수정할 통합 거버넌스 요구

#### 한줄 요약
- 소스코드부터 런타임까지 CSPM, CIEM, CWPP를 그래프 DB로 통합하여 실질적 공격 경로(Attack Path)를 식별하고 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **공격 경로 분석(Attack Path Analysis)**: 개별 취약점의 단순 CVSS 점수에 의존하지 않고, 인터넷 노출(CSPM) $\rightarrow$ 취약한 컨테이너(CWPP) $\rightarrow$ 과도한 IAM 역할(CIEM) $\rightarrow$ 핵심 DB 자산으로 연결되는 공격자의 실제 횡적 이동 경로를 그래프 알고리즘으로 모델링하여 조치 우선순위를 지정하는 기법.
- **코드-런타임 역추적성(Code-to-Cloud Traceability)**: 런타임 클라우드에서 발견된 보안 오설정이나 취약점을 배포 파이프라인의 원본 Git 레포지토리 및 Terraform/CloudFormation 코드 라인으로 즉각 매핑하여 개발자 수정을 유도하는 기능.

</details>

- **단일 그래프 데이터베이스 융합 (Graph-based Contextual Engine)**: 인프라 노드, 네트워크 인바운드 룰, IAM 정책, CVE 취약점 간의 관계망을 다차원 그래프로 시각화
- **경보 피로 99% 감축 (Contextual Prioritization)**: 수만 건의 단순 경보 중 실제 침해 가능한 1%의 유효 공격 경로에 보안 엔지니어링 역량 집중
- **Agentless + In-workload eBPF 하이브리드 가시성**: 클라우드 API 기반의 Agentless 스캔으로 신속한 인프라 커버리지를 확보하고, 핵심 워크로드는 eBPF 에이전트로 초정밀 실시간 방어

#### 한줄 요약
- 단일 그래프 기반 공격 경로 도출, 코드-런타임 역추적, 경보 피로 감축, Agentless/eBPF 하이브리드 가시성을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CNAPP 4대 핵심 통합 컴포넌트**:
  1. **Shift-Left Security (Artifact Scanning)**: SAST, SCA, Secret Scanner, IaC 템플릿 검사.
  2. **CSPM (Cloud Security Posture Management)**: 클라우드 API를 통한 인프라 오설정 및 컴플라이언스 점검.
  3. **CIEM (Cloud Infrastructure Entitlement Management)**: 미사용/과다 IAM 권한 및 최소 권한 위반 탐지.
  4. **CWPP (Cloud Workload Protection Platform)**: eBPF/커널 레벨 실시간 위협 및 컨테이너 이상 행위 차단.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. 개발 및 빌드 계층 (Shift-Left: Artifact & Pipeline Scanning) ]     │
│  ├─ Git Repo: IaC(Terraform) 오설정 및 하드코딩 Secret 검출             │
│  └─ CI/CD Registry: 컨테이너 베이스 이미지 CVE 취약점 사전 차단(SCA)     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (스캔 메타데이터 전송)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. CNAPP 중앙 통합 그래프 분석 엔진 (Context Graph Analytics Engine) ]│
│  ├─ CSPM 신호 융합: "EC2 인스턴스가 0.0.0.0/0 인터넷에 노출됨"           │
│  ├─ CWPP 신호 융합: "해당 EC2 내 컨테이너에 RCE 취약점(Log4j) 존재"       │
│  ├─ CIEM 신호 융합: "해당 EC2에 연결된 IAM 역할이 `AdminAccess` 과권한"  │
│  └─ [ 그래프 분석 ➔ "치명적 공격 경로(Attack Path) 식별" ➔ 최우선 경보] │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (원인 코드 역추적 및 조치 지시)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. 런타임 및 개발자 피드백 계층 (Remediation & Runtime Defense) ]     │
│  ├─ CWPP/eBPF: 런타임 RCE 익스플로잇 실시간 차단 (임시 방어)            │
│  └─ Git Pull Request 자동 생성: Terraform 코드 수정 PR 발급 (근본 해결) │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 개발 파이프라인의 스캔 데이터와 클라우드 런타임의 CSPM/CIEM/CWPP 신호가 중앙 그래프 엔진에서 공격 경로로 융합되어 원본 코드 수정으로 피드백되는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **Shift-Left 보안 모듈** | 소스코드 취약점, 비밀 자격증명(Secret), IaC 템플릿 결함을 배포 전 사전 차단 | Pre-deployment |
| **CSPM (형상 관리)** | 클라우드 API를 통해 인바운드 보안그룹 개방, S3 퍼블릭 노출 등 형상 오설정 감사 | Posture Core |
| **CIEM (권한 관리)** | 머신 계정 및 인간 사용자의 실제 사용 권한을 분석하여 과다 IAM 권한 회수 | Identity Core |
| **CWPP (워크로드 보호)** | 호스트 커널 eBPF를 통해 프로세스 인젝션, 악성 쉘 실행 등 런타임 공격 방어 | Runtime Core |
| **공격 경로 그래프 엔진**| CSPM, CIEM, CWPP 신호를 결합하여 데이터 유출로 이어지는 실질 경로 도출 | Context Engine |

#### 한줄 요약
- Shift-Left 스캐너, CSPM, CIEM, CWPP, 공격 경로 그래프 엔진이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CNAPP 전주기 위협 탐지 및 조치 5단계 프로세스**:
  1. 배포 전 IaC/컨테이너 이미지 정적 검증
  2. 런타임 인프라 형상 및 IAM 권한 그래프 매핑
  3. 실시간 공격 경로(Attack Path) 분석 및 위험 순위화
  4. 런타임 eBPF 즉각 차단 및 담당 개발자 Git 티켓 자동 발행
  5. 원본 IaC 코드 수정 배포 및 공격 경로 단절 검증

</details>

```text
1. [배포 전 정적 검증] 개발자가 Terraform 코드 푸시 ➔ CNAPP IaC 스캐너가 보안 결함 점검
            │
            ▼
2. [런타임 자산 그래프 동기화]
    ├─ CSPM이 퍼블릭 인바운드 오픈(80/443) 상태 수집
    ├─ CIEM이 인스턴스에 부착된 IAM Role의 S3 쓰기/읽기 전체 권한 수집
    └─ CWPP가 워크로드 내부의 패치되지 않은 웹 취약점(RCE) 식별
            │
            ▼
3. [공격 경로(Attack Path) 상관 분석]
    ├─ 그래프 엔진이 [인터넷 노출 ➔ RCE 취약점 ➔ IAM 관리자 권한 ➔ 고객 DB] 연결망 확정
    └─ [수만 개 단순 알람 대신 단 1건의 '치명적 공격 체인(Critical Attack Path)' 경보 생성]
            │
            ▼
4. [자동화된 다층 조치 (Remediation)]
    ├─ 런타임: CWPP가 침투 시도 패킷을 커널 레벨에서 즉시 인라인 차단
    └─ 코드단: CNAPP가 해당 Terraform 파일의 보안그룹 룰을 수정한 Pull Request 자동 생성
            │
            ▼
5. [단절 검증 및 종결] 승인된 PR 머지 및 재배포 후, 그래프 엔진에서 공격 경로가 완전히 소멸되었음을 확인
```

**동작 원리**

1. **상관 관계 기반 위험 평가**: 단편적 취약점 점수가 아닌 실제 공격자의 악용 가능성(Exploitability) 중심 판정
2. **코드-런타임 동기화**: 런타임 콘솔 수동 수정 대신 IaC 코드를 정정하여 인프라 드리프트(Drift) 원천 차단
3. **가용성 저하 없는 전수 감사**: Agentless 방식으로 전사 클라우드 자산을 10분 만에 인벤토리화
4. **즉각적 방어와 근본적 해결의 병행**: CWPP로 런타임 공격을 막는 동안 IaC 코드를 배포하여 보안 부채 청산
5. **폐쇄 루프 검증 (Closed-Loop Verification)**: 조치 후 공격 경로가 사라졌는지 그래프 재평가로 종결

#### 한줄 요약
- 정적 검증, 자산 그래프 동기화, 공격 경로 상관 분석, 다층 조치(코드 PR), 공격 경로 단절 검증 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **클라우드 보안 접근법 3대 비교**: 사일로형 개별 솔루션, 단순 통합 대시보드(Aggregated), 차세대 그래프 CNAPP의 비교.

</details>

| 비교 항목 | 사일로형 개별 도구 (Point Solutions) | 단순 통합 대시보드 (Aggregated UI) | 차세대 그래프 CNAPP (Unified CNAPP) |
|:---|:---|:---|:---|
| **도구 아키텍처** | CSPM, CWPP, SAST 별도 솔루션 운영 | 개별 도구 경보를 단일 화면에 나열 | **단일 그래프 DB 기반 데이터 융합 분석** |
| **경보 발생 형태** | **수만 건의 개별 알람 (경보 피로 극심)**| 필터링된 알람 목록 나열 | **실제 침해 가능한 1% 공격 경로만 제시** |
| **공격 경로 분석** | **전혀 불가 (도구 간 맥락 연결 단절)** | 부분적 (수동 상관 대조 필요) | **완벽 지원 (다차원 노드 연결망 분석)** |
| **원인 코드 역추적**| 불가 (런타임 알람만 제공) | 수동 조사 필요 | **원본 IaC/Git 코드 라인 즉시 매핑** |
| **운영 오버헤드** | 관리 콘솔 다변화로 비용/인력 낭비 | 벤더 통합으로 비용 일부 절감 | **조치 우선순위 명확화로 보안 생산성 극대화**|

#### 한줄 요약
- 개별 도구는 경보 피로와 사일로 결함, 단순 통합은 나열에 불과, CNAPP는 그래프 기반 공격 경로와 원본 코드 수정을 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NIST SP 800-190 (Application Container Security Guide)**: 컨테이너 이미지 취약점, 레지스트리 보안, 오케스트레이터 및 호스트 런타임 격리 통제를 규정한 국제 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수만 개의 단순 취약점(CVE) 및 오설정 알람이 쏟아져 **실제 위험한 침해 경로를 놓치고 보안팀이 경보 피로(Alert Fatigue)에 매몰** | **단일 그래프 DB 기반 맥락 인식형 공격 경로 분석(Attack Path Analysis) 엔진 도입** | 무의미한 알람 99% 노이즈 필터링 및 실제 침해 가능한 1% 치명적 위험에 조치 집중 |
| 운영 부서의 성능 저하 및 안정성 우려로 인해 **호스트 에이전트 설치가 거부되어 워크로드 가시성 사각지대 발생** | **클라우드 API 기반의 Agentless 스냅샷 스캐닝과 미션 크리티컬 워크로드 대상 경량 eBPF 에이전트 결합** | 서버 가용성 저하 0% 유지 및 전사 클라우드 자산 가시성 100% 확보 |
| 런타임에서 발견된 오설정을 콘솔에서 수동 수정하여 **다음 CI/CD 배포 시 취약한 IaC 코드로 인해 오설정이 재발생하는 드리프트** | **런타임 보안 결함을 원본 Git 리포지토리의 IaC 코드 라인으로 역추적하고 자동 Pull Request 발행** | 인프라 드리프트(Drift) 원천 차단 및 개발-보안 협업 기반의 근본적 보안 취약점 해결 |

#### 한줄 요약
- 공격 경로 분석으로 경보 피로를 해소하고, Agentless로 가시성을 확보하며, IaC 역추적으로 드리프트를 방지한다.

## Ⅶ. 결론

- 클라우드 네이티브 환경의 보안 사일로와 경보 피로를 근원적으로 해결하는 **CNAPP 아키텍처**는 미래 클라우드 보안의 표준 플랫폼이며, 실무 구현 시 **Shift-Left(IaC/SCA)와 CSPM, CIEM, CWPP의 단일 데이터 모델 융합**, **그래프 기반 실질적 공격 경로(Attack Path) 도출**, **Agentless와 eBPF 결합 가시성**, **IaC 코드 라인 자동 역추적(Traceability)** 을 통합 구축하여 클라우드 전주기에 걸친 완벽한 보안 레질리언스를 완성

#### 한줄 요약
- 코드부터 런타임까지 단일 그래프 DB 기반으로 공격 경로를 식별하고 IaC 코드를 자동 정정하여 전주기 보안을 완성한다.
