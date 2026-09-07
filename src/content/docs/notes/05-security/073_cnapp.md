---
sidebar:
  order: 73
  label: "073. 클라우드 네이티브 애플리케이션 보호 플랫폼 (Cloud-Native Application Protection Platform, CNAPP)"
  badge:
    text: "미출 · 70%"
    variant: note
title: "코드부터 런타임까지의 전주기 클라우드 보안 통합 : CNAPP (Gartner CNAPP & Attack Path Analysis)"
date: "2026-09-07T14:00:00+09:00"
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

- 정의/개념: Gartner 표준에 기반하여 Shift-Left(IaC/SCA) $\rightarrow$ CSPM(클라우드 형상 관리) $\rightarrow$ CIEM(인프라 권한 관리) $\rightarrow$ CWPP(런타임 워크로드 보호) 를 단일 그래프 모델로 결합하고, **실질적 공격 경로(Attack Path Analysis)** 를 도출하여 치명적 위험의 조치 우선순위를 산출하는 전주기 클라우드 보안 아키텍처
- 배경/필요성: 클라우드 네이티브 환경에서 개발 단계의 소스코드(SAST/SCA), 배포 단계의 코드형 인프라(IaC), 운영 단계의 형상 관리(CSPM), 권한 관리(CIEM), 런타임 워크로드 보호(CWPP)가 파편화된 포인트 솔루션으로 사일로화되어, 보안팀이 매일 수만 건의 단순 취약점 경보 피로(Alert Fatigue)에 매몰되고 실제 침해로 이어지는 유효 공격 경로를 식별하지 못하는 심각한 한계가 존재함에 따라, 개발부터 런타임까지의 전주기(Code-to-Cloud) 텔레메트리를 단일 그래프 데이터베이스로 융합하여 인프라 노출·과다 권한·취약점의 상관관계를 다차원 분석하는 **CNAPP**(Cloud-Native Application Protection Platform)를 도입하여 실질적 공격 경로(Attack Path Analysis) 기반 조치 우선순위화, 경보 노이즈 99% 감축 및 런타임 결함의 원본 IaC 코드 자동 역추적/원복을 달성할 필요

#### 한줄 요약
- CNAPP가 새로 만들어 낸 것은 탐지 능력이 아니라 이미 있던 신호들 사이의 연결이며, 위험의 크기는 개별 결함이 아니라 그것들이 하나로 이어지는지에서 결정된다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **공격 경로 분석(Attack Path Analysis)**: 개별 취약점의 단순 CVSS 점수에 의존하지 않고, 인터넷 노출(CSPM) $\rightarrow$ 취약한 컨테이너(CWPP) $\rightarrow$ 과도한 IAM 역할(CIEM) $\rightarrow$ 핵심 DB 자산으로 연결되는 공격자의 실제 횡적 이동 경로를 그래프 알고리즘으로 모델링하여 조치 우선순위를 지정하는 기법.
- **코드-런타임 역추적성(Code-to-Cloud Traceability)**: 런타임 클라우드에서 발견된 보안 오설정이나 취약점을 배포 파이프라인의 원본 Git 레포지토리 및 Terraform/CloudFormation 코드 라인으로 즉각 매핑하여 개발자 수정을 유도하는 기능.

</details>

- 단일 그래프 데이터베이스 융합 (Graph-based Contextual Engine): 인프라 노드, 네트워크 인바운드 룰, IAM 정책, CVE 취약점 간의 관계망을 다차원 그래프로 시각화
- 경보 피로 99% 감축 (Contextual Prioritization): 수만 건의 단순 경보 중 실제 침해 가능한 1%의 유효 공격 경로에 보안 엔지니어링 역량 집중
- Agentless + In-workload eBPF 하이브리드 가시성: 클라우드 API 기반의 Agentless 스캔으로 신속한 인프라 커버리지를 확보하고, 핵심 워크로드는 eBPF 에이전트로 초정밀 실시간 방어

#### 한줄 요약
- 경보를 1%로 줄였다는 말은 나머지 99%를 안전하다고 판정했다는 뜻이므로, 그래프에서 빠진 자산이 있으면 줄어든 경보가 그대로 사각지대가 된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CNAPP 4대 핵심 통합 컴포넌트**:
  1. **Shift-Left Security (Artifact Scanning)**: SAST, SCA, Secret Scanner, IaC 템플릿 검사.
  2. **CSPM (Cloud Security Posture Management)**: 클라우드 API를 통한 인프라 오설정 및 컴플라이언스 점검.
  3. **CIEM (Cloud Infrastructure Entitlement Management)**: 미사용/과다 IAM 권한 및 최소 권한 위반 탐지.
  4. **CWPP (Cloud Workload Protection Platform)**: eBPF/커널 레벨 실시간 위협 및 컨테이너 이상 행위 차단.

</details>

```text
[CNAPP 아키텍처]
├─ Shift-Left 개발·빌드 계층
│  ├─ 소스코드 및 오픈소스 점검 (SAST·SCA)
│  ├─ 하드코딩 시크릿 스캔 (Secret Detection)
│  └─ 배포 전 인프라 결함 점검 (IaC Scanning)
├─ 멀티 클라우드 태세 및 권한 통제
│  ├─ 클라우드 형상 오설정 감사 (CSPM)
│  └─ 최소 권한 검증 및 과권한 회수 (CIEM)
├─ 런타임 워크로드 보호 계층
│  ├─ 컨테이너·VM 이상 행위 감시 (CWPP)
│  └─ 호스트 커널 패킷 인라인 차단 (eBPF)
└─ 중앙 맥락 그래프 분석 엔진
   ├─ 다차원 자산 관계망 매핑 (Graph DB)
   ├─ 실질적 공격 경로 분석 (Attack Path)
   └─ Git PR 자동 발행 및 코드 역추적
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| Shift-Left 보안 모듈 | 소스코드 취약점, 하드코딩 시크릿, IaC 템플릿 결함을 배포 전 사전에 차단 |
| CSPM (형상 관리) | 클라우드 API를 통해 보안그룹 개방, 스토리지 퍼블릭 노출 등 형상 오설정을 감사 |
| CIEM (권한 관리) | 머신 계정 및 인간 사용자의 실제 사용 이력을 분석하여 과다 IAM 권한을 회수 |
| CWPP (워크로드 보호) | 호스트 커널 eBPF를 통해 프로세스 인젝션, 악성 쉘 실행 등 런타임 공격을 방어 |
| 공격 경로 그래프 엔진 | CSPM, CIEM, CWPP 신호를 결합하여 데이터 유출로 이어지는 실질 경로를 도출 |

#### 한줄 요약
- 네 도구는 그대로 두고 그래프 엔진만 위에 얹은 구조이므로, 통합의 실익은 도구 교체가 아니라 도구 간 신호가 같은 자산 식별자로 묶이는지에 달려 있다.

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

1. 배포 전 정적 검증: IaC·이미지 결함 탐지
2. 런타임 자산 그래프 동기화: 형상·권한·취약점 연결
3. 공격 경로 상관 분석: 악용 가능한 경로 우선순위화
4. 자동화된 다층 조치: 런타임 차단과 코드 수정 병행
5. 단절 검증 및 종결: 그래프 재평가로 경로 소멸 확인

#### 한줄 요약
- 런타임 차단은 경로를 임시로 끊을 뿐이고 원본 IaC를 고쳐야 다음 배포에서 되살아나지 않으므로, 두 조치는 대체재가 아니라 시간차를 둔 짝이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **클라우드 보안 접근법 3대 비교**: 사일로형 개별 솔루션, 단순 통합 대시보드(Aggregated), 차세대 그래프 CNAPP의 비교.

</details>

| 비교 항목 | 사일로형 개별 도구 (Point Solutions) | 단순 통합 대시보드 (Aggregated UI) | 차세대 그래프 CNAPP (Unified CNAPP) |
|:---|:---|:---|:---|
| 도구 아키텍처 | CSPM, CWPP, SAST 별도 솔루션 운영 | 개별 도구 경보를 단일 화면에 나열 | 단일 그래프 DB 기반 데이터 융합 분석 |
| 경보 발생 형태 | 수만 건의 개별 알람 (경보 피로 극심)| 필터링된 알람 목록 나열 | 실제 침해 가능한 1% 공격 경로만 제시 |
| **공격 경로 분석** | 전혀 불가 (도구 간 맥락 연결 단절) | 부분적 (수동 상관 대조 필요) | 완벽 지원 (다차원 노드 연결망 분석) |
| 원인 코드 역추적| 불가 (런타임 알람만 제공) | 수동 조사 필요 | 원본 IaC/Git 코드 라인 즉시 매핑 |
| 운영 오버헤드 | 관리 콘솔 다변화로 비용/인력 낭비 | 벤더 통합으로 비용 일부 절감 | 조치 우선순위 명확화로 보안 생산성 극대화|

#### 한줄 요약
- 개별 도구는 경보 피로와 사일로 결함, 단순 통합은 나열에 불과, CNAPP는 그래프 기반 공격 경로와 원본 코드 수정을 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NIST SP 800-190 (Application Container Security Guide)**: 컨테이너 이미지 취약점, 레지스트리 보안, 오케스트레이터 및 호스트 런타임 격리 통제를 규정한 국제 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수만 개의 단순 취약점(CVE) 및 오설정 알람이 쏟아져 실제 위험한 침해 경로를 놓치고 보안팀이 경보 피로(Alert Fatigue)에 매몰 | 단일 그래프 DB 기반 맥락 인식형 공격 경로 분석(Attack Path Analysis) 엔진 도입 | 무의미한 알람 99% 노이즈 필터링 및 실제 침해 가능한 1% 치명적 위험에 조치 집중 |
| 운영 부서의 성능 저하 및 안정성 우려로 인해 호스트 에이전트 설치가 거부되어 워크로드 가시성 사각지대 발생 | 클라우드 API 기반의 Agentless 스냅샷 스캐닝과 미션 크리티컬 워크로드 대상 경량 eBPF 에이전트 결합 | 서버 가용성 저하 0% 유지 및 전사 클라우드 자산 가시성 100% 확보 |
| 런타임에서 발견된 오설정을 콘솔에서 수동 수정하여 다음 CI/CD 배포 시 취약한 IaC 코드로 인해 오설정이 재발생하는 드리프트 | 런타임 보안 결함을 원본 Git 리포지토리의 IaC 코드 라인으로 역추적하고 자동 Pull Request 발행 | 인프라 드리프트(Drift) 원천 차단 및 개발-보안 협업 기반의 근본적 보안 취약점 해결 |

#### 한줄 요약
- Agentless는 커버리지를 넓히는 대신 런타임 순간의 행위를 놓치므로, 어디까지 스냅샷으로 보고 어디부터 eBPF 에이전트를 심을지가 실무의 실제 결정이 된다.

## Ⅶ. 결론

- 파편화된 개별 포인트 보안 도구들의 사일로를 타파하고 코드부터 클라우드 런타임까지의 전주기 위험을 단일 관제망으로 통합하는 현대 클라우드 네이티브 보안(Gartner CNAPP / DevSecOps)의 최상위 차세대 통합 플랫폼으로 확고히 자리 잡았으며, AI 기반 자동 침해 경로 차단 및 CSPM/CIEM/CWPP/DSPM 융합으로 전면 진화하는 가운데, 실무 CNAPP 플랫폼 구축 시에는 Agentless 스냅샷 스캔과 호스트 eBPF 에이전트를 결합한 하이브리드 가시성 확보, 인터넷 노출-취약점-IAM 과권한을 연결하는 그래프 기반 공격 경로(Attack Path) 분석 엔진 가동, 런타임 결함을 원본 Git 리포지토리의 IaC 코드 라인으로 즉시 역추적하여 자동 Pull Request를 발행하는 DevSecOps 피드백 루프 구축을 결합하여 완벽한 클라우드 전주기 보안성을 완성

#### 한줄 요약
- CNAPP 도입은 도구를 줄이는 선택이라기보다 조치 우선순위를 그래프 판정에 맡기는 선택이므로, 자산 커버리지 검증이 도입의 전제가 된다.
