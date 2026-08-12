---
sidebar:
  order: 75
  label: "075. 클라우드 CSAP 보안 인증 등급제(Cloud Security Assurance Program)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "클라우드 CSAP 보안 인증 등급제(Cloud Security Assurance Program)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-security"
weight: 75
extra:
  question_no: "075"
  source_status: "기출"
  source_history: "128회, 132회, 138회"
  priority: 85
  priority_note: "128•132•138회 반복, 공공 클라우드 인증 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **클라우드 보안인증(Cloud Security Assurance Program, CSAP)**: 공공기관에 클라우드 서비스를 제공하려는 민간 클라우드 서비스 제공자(CSP)의 보안 조치 이행 여부를 종합 평가하여 안전성을 인증하는 법정 제도이다.
- **공공 보안인증(Public Cloud Security Certification)**: 공공기관 정보자산의 중요도와 서비스 경계에 맞춰 적절한 보증 수준을 검증하는 제도적 보안 통제 체계이다.

</details>

- 정의/개념: **CSAP**는 공공기관이 안심하고 민간 클라우드 서비스를 이용할 수 있도록 서비스의 정보보호 수준과 인증 관리 체계의 적합성을 독립 평가하여 발급하는 보안인증 제도이다.
- 배경/필요성: 공공 시스템의 클라우드 전환 확대에 따른 국가 데이터 보안 확보 요구와 함께, 민간 CSP의 서비스 경계 및 정보 중요도별 맞춤형 보안 통제 검증 절차가 필수적으로 요구된다.

#### 한줄 요약

- CSAP는 공공기관 이용 클라우드 서비스의 법적 보안 기준 적합성을 독립적으로 평가 및 보증하는 공공 클라우드 보안 인증 체계이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **서비스형 인프라(Infrastructure as a Service, IaaS)**: 서버, 저장소, 네트워크 등 컴퓨팅 자원을 클라우드로 제공하는 서비스 모델이다.
- **서비스형 소프트웨어(Software as a Service, SaaS)**: 클라우드 기반의 완제 애플리케이션을 사용자에게 제공하는 서비스 모델이다.
- **서비스형 데스크톱(Desktop as a Service, DaaS)**: 가상 데스크톱 환경(VDI)을 클라우드 기반 서비스로 제공하는 기술 형태이다.
- **인증 유형(Certification Type)**: IaaS, SaaS, DaaS 등 제공하는 클라우드 서비스의 기술적 구조와 운영 모델에 따른 구분이다.
- **인증 등급(Certification Level)**: 취급하는 공공 정보의 민감도와 중요도에 따라 상, 중, 하 등급으로 체계화된 보안 통제 요구 수준이다.
- **사후평가(Surveillance Evaluation)**: 인증 취득 후 연 1회 이상 운영 현황과 매년 보안 기준을 지속해서 충족하고 있는지 점검하는 평가이다.
- **갱신평가(Renewal Evaluation)**: 3년의 인증 유효기간 만료 전 유효성 연장을 위해 이행하는 종합 재평가 절차이다.

</details>

- **IaaS(Infrastructure as a Service)**·**SaaS(Software as a Service)**·**DaaS(Desktop as a Service)** 등 **인증 유형(Certification Type)**에 따라 맞춤형 보안 통제 항목을 적용한다.
- 취급 정보의 민감도 및 국가 보안 등급에 맞추어 상·중·하 **인증 등급(Certification Level)** 제도를 연계 운영한다.
- **사후평가(Surveillance Evaluation)** 및 **갱신평가(Renewal Evaluation)**를 통해 최초 인증 이후의 형상 변화와 취약점을 주기적으로 관리한다.

#### 한줄 요약

- 서비스 구성과 데이터 중요도에 따라 유형별·등급별로 분리 평가하고 사후점검으로 상시 안전성을 확보하는 가변적 평가 구조이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **인증기관(Certification Body)**: CSAP 제도를 총괄 관리하고 평가 결과를 종합 검토하여 최종 인증서 발급 및 취소를 결정하는 주체이다.
- **평가기관(Evaluation Body)**: 신청 서비스를 대상으로 서면 평가, 현장 실사, 기술적 취약점 진단을 수행하는 전문 점검 기관이다.
- **인증위원회(Certification Committee)**: 평가기관의 진단 결과와 신청 CSP의 보완 조치 증적을 독립 심의하는 최종 의결 기구이다.
- **인증 범위(Scope of Certification)**: 인증서가 물리적, 논리적으로 효력을 미치는 자산, 조직, 시설 및 서비스의 경계이다.

</details>

```text
                  [신청자] ----- [평가기관] ----- [인증위원회]
                                    /                 \
                         [정책•인증기관] ----- [이용기관]
```

선의 의미: 신청자·평가기관·인증위원회는 인증 평가 책임 경계를 이루고, 정책·인증기관은 평가기관과 심의 결과를 관리하며 이용기관에 유효한 인증 범위를 제공하는 정적 제도 구조를 뜻한다.

| 구성요소 | 책임 |
|:---|:---|
| 정책·인증기관 | **인증기관(Certification Body)**의 제도 운영·인증 결정·사후관리 |
| 평가기관 | **평가기관(Evaluation Body)**의 서면·현장·취약점 평가 |
| 신청자 | **인증 범위(Scope of Certification)**·통제·운영 증적 준비 |
| 인증위원회 | **인증위원회(Certification Committee)**의 평가결과·보완증적 심의 |
| 이용기관 | 인증서의 서비스명·유형·등급·범위·유효기간 확인 |

#### 한줄 요약

- 평가기관의 진단, 인증위원회의 독립 심의, 인증기관의 통제 관리가 상호 연계되어 인증 신뢰성을 다층 보증하는 운영 구조이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **보완 증적(Corrective Proof)**: 평가 단계에서 발출된 부적합 사항을 시정 완료했음을 입증하는 기술 및 정책 증빙 자료이다.
- **인증 결정(Certification Decision)**: 평가 심의 결과를 바탕으로 인증 부여, 조건부 승인, 부적격 등을 확정하는 행정 절차이다.
- **서면•현장•취약점 평가(Documentary, On-site & Vulnerability Evaluation)**: 관련 서류 검토, 데이터센터 현장 검증, 모의침투 및 보안 설정 진단을 통합 이행하는 단계이다.
- **부적합 시정•보완증적 생성(Non-conformity Correction & Evidence Generation)**: 진단된 문제점을 개선하고 이행 내역을 증빙화하는 단계이다.
- **보완 이행•최종 결과 검증(Corrective Implementation & Final Verification)**: 시정 조치사항의 실효성과 남아있는 부적합 요소를 재검증하는 단계이다.
- **인증기준 적합성 심의(Certification Criteria Compliance Deliberation)**: 종합 진단 보고서와 보완 증적이 인증 기준을 충족하는지 종합 심의하는 단계이다.
- **유형•등급•범위 인증 결정(Type, Level & Scope Certification Decision)**: 서비스 유형, 인증 등급, 보호 경계 및 유효기간을 포함해 최종 인증서 발급을 의결하는 단계이다.

</details>

```text
[신청인] -- 인증 신청
      |
      v
[인증기관] -- 평가 의뢰
      |
      v
[평가기관]
      |
      v
1. 서면•현장•취약점 평가
      |
      `-- 평가 결과•부적합 사항
                  |
                  v
[신청인]
      |
      v
2. 부적합 시정•보완증적 생성
      |
      `-- 보완증적
             |
             v
[평가기관]
      |
      v
3. 보완 이행•최종 결과 검증
      |
      v
[인증위원회]
      |
      v
4. 인증기준 적합성 심의
      |
      v
[인증기관]
      |
      v
5. 유형•등급•범위 인증 결정
      |
      `-- 인증 결과 ----> [신청인]

[인증 유지기간] -- 사후•갱신평가
```

### 동작 원리

1. **서면·현장·취약점 평가(Documentary, On-site & Vulnerability Evaluation)**: 신청 서비스의 정책 문서, 물리 데이터센터, 기술적 취약점을 정밀 진단한다.
2. **부적합 시정·보완증적 생성(Non-conformity Correction & Evidence Generation)**: 파악된 결함 및 미비점을 시정 조치하고 이를 증빙할 **보완 증적(Corrective Proof)**을 수집한다.
3. **보완 이행·최종 결과 검증(Corrective Implementation & Final Verification)**: 시정 조치가 실효성 있게 적용되었는지 최종 평가기관이 현장 및 기술적 재검증을 실행한다.
4. **인증기준 적합성 심의(Certification Criteria Compliance Deliberation)**: 평가 결과서와 보완 이행 결과를 인증위원회에 제출하여 객관적 적합성을 심의한다.
5. **유형·등급·범위 인증 결정(Type, Level & Scope Certification Decision)**: 최종 인증 승인을 확정하고 **인증 결정(Certification Decision)** 사항을 공표 및 수여한다.

#### 한줄 요약

- 진단-시정-재검증-심의-의결의 단계별 정밀 평가 프로세스와 사후·갱신 평가를 통한 지속적 이행 관리 순환 체계이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **최초평가(Initial Evaluation)**: 서비스가 신규로 CSAP 인증을 취득하기 위해 전체 통제 항목을 대상으로 이행하는 심사이다.
- **운영 드리프트(Operational Drift)**: 시간 경과에 따라 클라우드 구성, IAM 권한, 인프라 상태가 최초 인증 시점과 달라지는 편차 현상이다.

</details>

| CSAP 평가 유형 | 최초평가 | 사후평가 | 갱신평가 |
|:---|:---|:---|:---|
| 적용 시점 | 최초 인증 신청 시 | 인증 후 유지기간 중 | 유효기간 만료 전 |
| 평가 목적 | **최초평가(Initial Evaluation)**의 최초 적합성 확인 | **사후평가(Surveillance Evaluation)**의 운영 기준 준수 확인 | **갱신평가(Renewal Evaluation)**의 연장 적합성 확인 |
| 주요 범위 | 서면·현장·취약점 전체 평가 | 변경·운영 상태와 부적합 조치 | 전체 기준과 누적 변경사항 재평가 |
| 결과 | 서비스 유형·등급·범위 인증 | 인증 유지·시정 등 사후조치 | 인증 갱신·종료 결정 |

#### 한줄 요약

- 신규 진입을 위한 최초평가, **운영 드리프트(Operational Drift)** 방지를 위한 사후평가, 지속성을 검증하는 갱신평가로 분목화하여 관리한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **클라우드컴퓨팅법 제23조의2(Cloud Computing Act Article 23-2)**: 공공기관 클라우드 도입 시 보안인증을 획득한 서비스를 사용하도록 법적으로 강제한 조항이다.
- **인증서 대조(Certificate Cross-check)**: 조달·도입하려는 서비스 범위와 실제 발급된 CSAP 인증서의 명칭, 등급, 유효기간 일치 여부를 대조 검증하는 절차이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 법적 근거를 확인하지 않으면 인증 대상·절차 오판 | **클라우드컴퓨팅법 제23조의2(Cloud Computing Act Article 23-2)** 준수 | 인증 대상과 절차 적법성 확보 |
| 제도 전환을 놓치면 조달·검증 절차 혼선 | 2027 통합 검증 전환과 기존 인증 유효성 확인 | 중복 검증·도입 지연 방지 |
| 인증서와 도입 조건이 다르면 범위 밖 서비스 사용 | **인증서 대조(Certificate Cross-check)** 수행 | 미인증·만료 서비스의 공공 도입 방지 |

#### 한줄 요약

- 계약 시 서비스명, 물리 데이터센터 구역, 인증 유효기간이 실제로 이용하려는 사양과 일치하는지 정밀 대조 통제를 이행해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **도입 적합 조건(Compliance Condition for Adoption)**: 도입 대상 클라우드가 CSAP 법정 등급, 인증 범위, 유효기간을 만족하여 법적 도입 요구를 충족하는 상태이다.

</details>

- **도입 적합 조건(Compliance Condition for Adoption)**에 따라 인증서의 서비스명·유형·등급·범위·유효기간이 모두 일치할 때만 도입을 최종 승인한다.

#### 한줄 요약

- CSAP 인증 범위와 법정 등급 준수 여부를 엄격히 심사하고 운영 주기 전반의 지속적인 사후점검 체계를 구축하여 공공 클라우드 안심 환경 조성.

