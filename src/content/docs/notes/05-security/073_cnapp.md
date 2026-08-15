---
sidebar:
  order: 73
  label: "073. 클라우드 네이티브 애플리케이션 보호 플랫폼 (Cloud-Native Application Protection Platform, CNAPP)"
  badge:
    text: "미출제 • 70%"
    variant: note
title: "클라우드 네이티브 애플리케이션 보호 플랫폼 (Cloud-Native Application Protection Platform, CNAPP)"
date: "2026-08-13T20:28:00+09:00"
tags:
  - "notes-security"
weight: 73
extra:
  question_no: "073"
  source_status: "미출제"
  source_history: ""
  priority: 70
  priority_note: "클라우드 보안 도구군을 통합하는 코드-런타임 우산임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **클라우드 네이티브 애플리케이션 보호 플랫폼(Cloud-Native Application Protection Platform, CNAPP)**: 소스코드, IaC, 멀티 클라우드 오설정, 과도한 권한 및 런타임 위협을 연계 분석하는 통합 클라우드 보안 아키텍처이다.
- **클라우드 네이티브(Cloud Native)**: 컨테이너, 마이크로서비스, 쿠버네티스, CI/CD 자동화를 통해 클라우드 환경에 최적화하여 애플리케이션을 구축•운영하는 방식이다.

</details>

- 정의/개념: 코드부터 런타임까지 통합 보호하는 **CNAPP**
- 배경/필요성: 도구 사일로는 **경보 피로•공격 경로 단절** 유발

#### 한줄 요약

- 소스코드 빌드부터 런타임 운영까지 보안 도구를 단일 그래프 기반으로 통합해 치명적 침해 경로의 우선순위를 해결하는 플랫폼이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **코드형 인프라(Infrastructure as Code, IaC)**: Terraform, CloudFormation 등을 사용하여 클라우드 인프라 구성을 코드로 선언•배포하는 방식이다.
- **컨테이너 이미지(Container Image)**: 애플리케이션 구동에 필요한 라이브러리, 바이너리를 패키징한 실행 바이너리 레이어이다.
- **런타임(Runtime)**: 쿠버네티스 노드, EC2, ECS 등에서 실제 애플리케이션 세션이 구동 중인 상태이다.
- **클라우드 보안 형상 관리(Cloud Security Posture Management, CSPM)**: 멀티 클라우드 자산의 퍼블릭 노출, 오설정, 컴플라이언스 위반을 실시간 스캐닝하는 모듈이다.
- **클라우드 인프라 권한 관리(Cloud Infrastructure Entitlement Management, CIEM)**: 과도하게 부여된 IAM 기계/사용자 계정의 최소 권한 위반을 탐지하는 모듈이다.
- **클라우드 워크로드 보호 플랫폼(Cloud Workload Protection Platform, CWPP)**: VM, 컨테이너, 서벌리스 워크로드 내부의 커널 수준 위협 및 취약점을 보호하는 모듈이다.

</details>

- **IaC**, 소스코드, **컨테이너 이미지**, **런타임** 상태를 전주기(Code-to-Cloud) 통제선으로 결합한다.
- 자산(CSPM), 과도한 권한(CIEM), 런타임 위협(CWPP)의 취약점을 단일 자산 그래프 DB로 연관 분석한다.
- 개별 취약점 단독 심각도가 아닌, 퍼블릭 노출과 과권한이 결합된 실제 침해 가용 경로(Attack Path) 위주로 조치 우선순위를 부여한다.

#### 한줄 요약

- CSPM, CIEM, CWPP를 통합하여 퍼블릭 노출, 과권한, 취약점이 조합된 고위험 침해 경로(Attack Path)의 조치 순위를 도출한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **자산 관계 그래프(Asset Relationship Graph / Graph DB)**: 자산, 네트워크 인바운드, IAM 권한, CVE 취약점을 3D 그래프 노드로 시각 매핑하는 데이터베이스 모듈이다.
- **공격 경로(Attack Path / Attack Graph)**: 퍼블릭 인터넷 노출 지점부터 비인가 관리자 권한을 거쳐 DB 데이터 유출로 이어지는 침해 시나리오 경로이다.
- **원본 코드 연계(Source Code Traceability / Shift-left Traceability)**: 런타임에 발견된 보안 오설정을 배포 파이프라인 상의 특정 IaC 소스 코드 라인으로 추적해 정정 조치를 유도하는 기능이다.

</details>

```text
                         [자산 관계 그래프]
                      /          |          \
         [코드·IaC·이미지]  [CSPM·CIEM]  [CWPP]
                      \          |          /
                    [소유자·파이프라인 연계]
```

선의 의미: 빌드 산출물, 형상/권한(CSPM/CIEM), 런타임 보호(CWPP)의 분석 결과를 자산 관계 그래프로 융합하고 원본 소스 및 개발자 파이프라인으로 연결하는 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 코드·IaC·이미지 | SAST/SCA/IaC 스캐닝 및 컨테이너 베이스 이미지 내 하드코딩된 Secret 및 취약점 검출 |
| CSPM·CIEM | **CSPM** 기반 퍼블릭 암호화/네트워크 오설정 탐지 및 **CIEM** 기반 과도한 IAM 권한 가시화 |
| CWPP | eBPF/에이전트 기반 커널 위협, 프로세스 인젝션, 컨테이너 이상 행동 실시간 런타임 방어 |
| 자산 관계 그래프 | **자산 관계 그래프**를 통한 맥락 정보 융합 및 실질적 침해 가능 **공격 경로** 도출 |
| 소유자·파이프라인 연계 | 런타임 노출 결함을 **원본 코드 연계** 기술로 담당 개발자의 Git 레포지토리/IaC 라인으로 자동 할당 |

#### 한줄 요약

- 자산 관계 그래프가 CSPM, CIEM, CWPP 신호를 융합해 공격 경로를 도출하고, 런타임 결함을 원본 IaC 코드 조치로 피드백한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **운영 드리프트(Operational Drift / Configuration Drift)**: 승인된 IaC 템플릿과 실제 클라우드 콘솔 수동 조작으로 인해 발생한 런타임 인프라 설정 간의 불일치 상태이다.
- **공격 경로 단절 검증(Attack Path Severance Verification)**: 코드 조치 및 재배포 실행 후, 그래프 분석을 재실행하여 공격 가용 경로의 차단 여부를 검증하는 절차이다.
- **배포 전 발견 정규화(Pre-deployment Discovery Normalization)**: CI/CD 파이프라인 상의 빌드 보안 결과 데이터를 표준 보안 자산 스키마로 가공하는 단계이다.
- **코드•런타임 자산 상관(Code & Runtime Asset Correlation)**: 개발 배포 아티팩트와 런타임에 가동 중인 자산 객체를 1:1 매핑하는 단계이다.
- **공격 경로•위험 우선순위 계산(Attack Path & Risk Prioritization Calculation)**: 그래프 DB를 실행하여 실질적인 자산 침해 도달 경로 및 위협 점수를 산출하는 단계이다.
- **원본 수정•재배포(Source Remediation & Re-deployment)**: 개발자가 깃허브 PR을 통해 IaC 소스를 수정하고 CI/CD로 자동 재배포하는 단계이다.

</details>

```text
[CNAPP 입력]
      |
      +-- 코드·IaC·이미지 발견
      `-- 형상·권한·행위 상태
                  |
                  v
1. 배포 전 발견 정규화
                  |
                  v
2. 코드·런타임 자산 상관
                  |
                  v
3. 공격 경로·위험 우선순위 계산
                  |
                  `-- 공격 경로·원인 근거
                              |
                              v
[자산 소유자·개발 파이프라인]
                  |
                  v
4. 원본 수정·재배포
                  |
                  v
5. 공격 경로 단절 검증
                  |
                  v
[검증된 위험 제거 결과]
```

### 동작 원리

1. **배포 전 발견 정규화**: 코드•IaC•이미지 결과 통일
2. **코드•런타임 자산 상관**: 보안 신호를 자산 그래프로 결속
3. **공격 경로•위험 우선순위 계산**: 실제 도달 경로별 조치 순위 산출
4. **원본 수정•재배포**: IaC•파이프라인 수정•반영
5. **공격 경로 단절 검증**: 드리프트•잔여 경로 재평가

#### 한줄 요약

- 배포 전 스캔 및 런타임 파이프라인 상관 분석, 공격 경로 산출, 원본 IaC 수정 및 공격 경로 단절 검증으로 보안을 수립한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **개별 보안 도구(Siloed Point Security Tools)**: CSPM, CWPP, SAST 등 특정 영역에 특화되었으나 상호 간 신호 연동이 불가능한 파편화 솔루션이다.
- **단순 통합 제품군(Aggregated Dashboard Suite)**: 개별 툴의 경보를 단순 수집하여 단순 리스트 형태 뷰만 제공하는 전통적 대시보드이다.

</details>

| 클라우드 보호 솔루션 | 통합 CNAPP 체계 | 개별 보안 도구 (Point Solution) | 단순 통합 제품군 (Aggregated SIEM) |
|:---|:---|:---|:---|
| 적용 기준 | 멀티 클라우드 개발-운영 통합 보안 | 특정 단일 보안 영역(예: CWPP) 집중 심화 | 다수 보안 도구 경보 단순 중앙 집계 |
| 핵심 특징 | **CNAPP** 기반 단일 그래프 맥락 및 공격 경로 분석 | 특정 영역 스캐닝에 특화된 개별 솔루션 | 개별 툴 알람을 1개 UI 대시보드로 수집 |
| 한계 | 통합 인프라 구축 및 벤더 데이터 호환성 고려 | 도구 파편화, **경보 피로**, **공격 경로** 분석 불가 | 독립 경보 수집에 불과하며 미시적 맥락 연결 한계 |

#### 한줄 요약

- 개별 솔루션의 경보 파편화 한계를 극복하고, 소스코드부터 런타임까지 연관 분석을 수행하는 통합 CNAPP로 전환한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NIST SP 800-190**: 컨테이너 아키텍처(이미지, 레지스트리, 오케스트레이터, 호스트 OS) 전주기 보안 지침 가이드라인이다.
- **NIST SSDF 1.1 (Secure Software Development Framework 1.1)**: 안전한 소프트웨어 개발 생태계 조성을 위한 NIST 프레임워크 표준이다.
- **센서 공백(Sensor Blind Spot / Coverage Gap)**: 에이전트 미설치 노드나 섀도우 클라우드 계정 등으로 인해 CNAPP 가시성에 포함되지 않는 보안 구멍이다.
- **이식성(Portability)**: 특정 벤더 CNAPP 솔루션에 락인(Lock-in)되지 않고 멀티 클라우드 간 보안 정책을 이전에 수용하는 능력이다.
- **애플리케이션 프로그래밍 인터페이스(Application Programming Interface, API)**: 클라우드 서비스 및 보안 도구 간 데이터 연동 접점이다.
- **신원•접근 관리(Identity and Access Management, IAM)**: 사용자/기계 계정의 자원 접근 권한을 제어하는 프레임워크이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 컨테이너 및 오케스트레이터 위험 | **NIST SP 800-190** 표준 통제 준용 | 컨테이너 이미지, K8s, 런타임 노드 전주기 보안 강화 |
| 개발 공급망 보안 취약점 | **NIST SSDF 1.1** 프레임워크 연계 | CI/CD 빌드 파이프라인부터 Shift-left 통합 통제 수립 |
| 에이전트 미설치 및 벤더 락인 | Agentless 스캐닝 결합 및 개방형 **API** 기반 정책 이식 | **센서 공백** 근본 제거 및 멀티 클라우드 간 **이식성** 확보 |

#### 한줄 요약

- NIST SP 800-190/SSDF 표준을 반영하고 Agentless 기술을 결합해 센서 공백 없이 멀티 클라우드 공격 경로를 무력화한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **위험 우선순위화(Risk Prioritization / Contextual Risk Ranking)**: 1만 개의 취약점 중에서 실제 퍼블릭에 노출되어 데이터 유출로 이어지는 1%의 치명적 공격 경로를 골라내는 분석 능력이다.

</details>

- **위험 우선순위화**에 입각하여 전체 멀티 클라우드 위험은 **CNAPP**, 단일 포인트 런타임 제어는 **CWPP** 체계를 선택적으로 결합한다.

#### 한줄 요약

- 멀티 클라우드는 **CNAPP**, 단일 런타임은 **CWPP** 적용
