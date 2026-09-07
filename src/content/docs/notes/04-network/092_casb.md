---
sidebar:
  order: 92
  label: "092. CASB 클라우드 접근 보안 브로커"
  badge:
    text: "기출 · 70%"
    variant: note
title: "클라우드 가시성 및 데이터 보호 : CASB (Cloud Access Security Broker)"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-network"
weight: 92
extra:
  question_no: "92"
  source_status: "기출"
  source_history: "122회, 137회"
  priority: 70
  priority_note: "Gartner 4대 핵심 축(가시성, 컴플라이언스, 데이터 보안, 위협 방어) 및 Forward/Reverse Proxy, API 연동"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **CASB (Cloud Access Security Broker)**: 사용자 단말과 클라우드 SaaS 사이에 위치하여 가시성, 컴플라이언스, 데이터 보안, 위협 방어를 집행하는 보안 게이트웨이.
- **Shadow IT (섀도우 IT)**: 보안 부서의 승인 없이 임직원이 임의로 업무에 사용하는 비인가 클라우드 서비스로 인한 보안 사각지대.

</details>

- 정의/개념: 사용자와 SaaS 사이에서 통제하는 **클라우드 보안 브로커**
- 배경/필요성: 기업의 업무 환경이 온프레미스에서 클라우드 SaaS(M365, Google Workspace, Salesforce, Slack 등)로 급속히 전환됨에 따라, 보안 부서의 통제를 벗어난 비인가 클라우드 사용(Shadow IT)이 만연해지고 승인되지 않은 외부 공유 링크나 개인 단말(BYOD)을 통한 기밀 데이터 무단 유출 위험이 급증함에도 불구하고 전통적인 사내 경계 보안 장비로는 암호화된 SaaS 트래픽을 가시화하거나 통제할 수 없는 한계를 극복하기 위해, 사용자와 다중 클라우드 SaaS 서비스 접점에 위치하여 가시성(Visibility), 컴플라이언스(Compliance), 데이터 보안(Data Security), 위협 방어(Threat Protection)의 Gartner 4대 핵심 축을 집행하는 클라우드 접근 보안 브로커(CASB)를 도입하여 **섀도우 IT의 완벽한 가시화, 민감정보 유출 방지(DLP) 및 악의적 클라우드 위협 선제 차단**을 달성할 필요

#### 한줄 요약
- Gartner 4대 기둥과 하이브리드 배치 모델을 통해 분산된 클라우드 데이터와 섀도우 IT를 통합 통제한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Gartner 4대 기둥**: 가시성(Visibility), 컴플라이언스(Compliance), 데이터 보안(Data Security), 위협 방어(Threat Protection).
- **UEBA (User and Entity Behavior Analytics)**: 정상 사용자의 접속 시간, 위치, 다운로드 패턴을 학습하여 계정 탈취 및 내부자 유출을 감지하는 이상 행위 분석.

</details>

- **4대 핵심 기능**: 가시성·준수·**DLP·위협 방어** 제공
- **하이브리드 배치**: Forward·Reverse·**API 연동** 지원
- **UEBA**: 대량 다운로드와 동시 접속으로 **계정 도용 탐지**

#### 한줄 요약
- Gartner 4대 기능, 하이브리드 프록시/API 배치, UEBA 기반 이상 행위 탐지를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Forward vs Reverse vs API**: 관리 단말 인라인 통제(Forward), BYOD 인가 앱 통제(Reverse), 클라우드 저장 데이터 사후 감사(API).

</details>

```text
[CASB 아키텍처]
  ├── [인라인 제어] ─────── [Forward Proxy (섀도우 IT)]
  │                           │
  ├── [BYOD 제어] ───────── [Reverse Proxy (접근 통제)]
  │                           │
  ├── [백엔드 감사] ─────── [API 커넥터 (저장 데이터)]
  │                           │
  └── [보안 엔진] ───────── [위험 카탈로그 / DLP 엔진]
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| Forward Proxy | 관리 단말의 **섀도우 IT 차단** |
| Reverse Proxy | 비관리 단말의 **접근·다운로드 통제** |
| API 커넥터 | 저장 데이터 검사와 **공유 링크 회수** |
| 위험 카탈로그 | SaaS의 **위험도 평가** |
| DLP 엔진 | 민감정보 탐지와 **유출 차단** |

#### 한줄 요약
- 프록시가 실시간 경로를 가로채고 API 커넥터가 이미 저장된 데이터를 사후 점검하므로, 인라인에서 놓친 흐름이 저장 시점 검사에서 한 번 더 걸린다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Revoke Public Share (공유 링크 회수)**: 임직원이 대외비 문서를 '전체 공개' 링크로 잘못 설정했을 때 CASB가 API를 통해 이를 감지하고 즉각 비공개로 강제 전환하는 기능.

</details>

```text
사용자 업로드
      |
 1. SaaS 위험도 판정
      |
 2. 클라우드 DLP 검사
      +-- 위반: 차단·경보
      `-- 정상: 3. 파일 업로드 허용
                       |
                  4. 공유 링크 감사
                       |
                    SaaS 저장
```

동작 원리

1. SaaS 위험도 판정
2. 클라우드 DLP 검사
3. 파일 업로드 허용
4. 공유 링크 감사

#### 한줄 요약
- 인라인 차단과 API 사후 회수로 갈리며, 전자는 경로 강제와 지연을, 후자는 노출이 유지되는 시간을 대가로 치른다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Forward Proxy vs Reverse Proxy vs API-Based**: 3대 배치 모델별 장단점 비교.

</details>

| 비교 항목 | 순방향 프록시 (Forward Proxy) | 역방향 프록시 (Reverse Proxy) | API 연동 (API-Based) |
|:---|:---|:---|:---|
| 적용 대상 단말 | **관리 단말** | **비관리 단말** | SaaS **저장소** |
| 통제 대상 서비스 | 모든 SaaS와 **섀도우 IT** | 인가된 **SaaS** | API 지원 SaaS |
| 데이터 검사 시점 | **실시간 인라인** | **실시간 인라인** | **비동기 사후 검사** |
| 핵심 장점 | 섀도우 IT 사전 차단 | 에이전트 없는 **BYOD 통제** | 망 부하 없는 과거 감사 |
| 주요 한계 | 에이전트 배포 부담 | 비인가 SaaS 통제 불가 | 실시간 업로드 차단 불가 |

#### 한줄 요약
- Forward는 섀도우 IT 실시간 통제, Reverse는 BYOD 인가 앱 통제, API는 저장 데이터 사후 감사에 쓰인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Contextual Access (조건부 접근 제어)**: 접속 단말의 신뢰도(관리/비관리 기기), 네트워크 위치, 사용자 역할에 따라 SaaS 내 읽기 전용(View-Only) 강제 등 차등 권한을 부여하는 정책.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 개인 웹하드로 **기밀정보 유출** | **Forward Proxy·DLP**로 미인가 SaaS 차단 | 섀도우 IT 경로 차단 |
| BYOD에서 **문서 다운로드** | **Reverse Proxy**로 읽기 전용 적용 | 비관리 단말 저장 차단 |
| 공개 링크로 **대외비 노출** | **API 커넥터**로 권한 검사·회수 | 비인가 공유 무력화 |
| API 호출 한도로 **감사 지연** | **웹훅·델타 스캔** 적용 | 호출량 절감과 반응성 유지 |

#### 한줄 요약
- Forward 프록시로 섀도우 IT를 막고, Reverse 프록시로 BYOD를 통제하며, API 연동으로 퍼블릭 링크 노출을 방어한다.

## Ⅶ. 결론

- 경계가 사라진 클라우드 중심 환경에서 분산된 SaaS 자산과 데이터를 중앙에서 통합 통제하는 **가장 핵심적인 클라우드 데이터 보안 솔루션이자 SSE(Security Service Edge)의 핵심 컴포넌트**로 확립되었으며, 프라이빗 앱을 보호하는 ZTNA 및 엔드포인트 보안(EDR)과의 융합으로 진화하는 가운데, 실무 CASB 도입 및 운영 시에는 **사내 관리 단말의 섀도우 IT를 실시간 차단하는 Forward Proxy, 에이전트 설치가 불가능한 개인 단말(BYOD)의 다운로드를 제한하는 Reverse Proxy, 이미 저장된 데이터의 악성코드 검사 및 비인가 공개 공유 링크를 즉시 강제 회수하는 API 커넥터 연동의 하이브리드 멀티모드(Multi-Mode) 배치**를 결합하여 완벽한 SaaS 데이터 거버넌스를 완성

#### 한줄 요약
- CASB는 프록시와 API 연동을 통해 섀도우 IT를 가시화하고 클라우드 내 민감 데이터를 보호하는 표준 보안 게이트웨이다.
