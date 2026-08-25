---
sidebar:
  order: 22
  label: "022. NGFW vs WAF vs CASB 비교"
  badge:
    text: "기출 · 50%"
    variant: note
title: "계층별 보안 통제 아키텍처 비교 : NGFW vs WAF vs CASB"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 22
extra:
  question_no: "22"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "네트워크 경계(NGFW/L3-L7 DPI), 웹 애플리케이션(WAF/OWASP Top 10), 클라우드 SaaS 거버넌스(CASB/Shadow IT)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **NGFW vs WAF vs CASB**: 네트워크 전역(NGFW), 웹/API 서버(WAF), 클라우드 SaaS(CASB)를 방어하는 3대 보안 통제 솔루션.
- **Defense-in-Depth (심층 방어)**: 단일 보안 장비에 의존하지 않고 다계층으로 방어선을 구축하여 단일 장애점(SPOF)을 제거하는 보안 원칙.

</details>

- 정의/개념: 네트워크 경계(NGFW), 웹/API 서버(WAF), 클라우드 SaaS(CASB)를 유기적으로 분업 결합하여 **엔드투엔드 위협을 방어하는 다계층 심층 방어 아키텍처**
- 배경/필요성: 단일 방화벽(NGFW)만으로는 해결할 수 없는 **웹 로직 공격(SQLi/XSS) 침투, 비인가 클라우드(Shadow IT) 데이터 유출 및 보안 사각지대 발생**

#### 한줄 요약
- NGFW, WAF, CASB의 다계층 분업을 통해 네트워크, 웹, 클라우드 전 영역의 보안 사각지대를 제거한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Shadow IT (섀도 IT)**: 기업 IT 부서의 승인 없이 임직원이 임의로 사용하는 개인 클라우드 저장소나 협업 도구.
- **OWASP Top 10**: 웹 애플리케이션에서 가장 빈번하고 치명적으로 발생하는 10대 보안 취약점 목록.

</details>

- **영역별 전문화된 심층 검사(Specialized Depth)**: NGFW는 **광범위한 프로토콜 전수 검사, WAF는 L7 웹 정밀 검사, CASB는 SaaS 데이터 DLP 통제**
- **제로 트러스트 기반 접근 통제 연동**: 네트워크 세그멘테이션, **웹 API 스키마 검증, SaaS 테넌트 격리를 연계하여 내부 침해 차단**
- **통합 가시성 및 위협 상관 분석**: 3대 솔루션의 로그를 **SIEM/SOAR로 집결하여 다단계 APT 공격 체인 실시간 가시화**

#### 한줄 요약
- 영역별 특화 심층 검사, 제로 트러스트 연동, 통합 위협 상관 분석을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Reverse Proxy vs Forward Proxy**: 외부에서 내부 웹 서버로 들어오는 트래픽을 중계하는 Reverse Proxy(WAF)와 내부 사용자가 외부 클라우드로 나가는 트래픽을 통제하는 Forward Proxy(CASB).

</details>

```text
[NGFW - WAF - CASB 다계층 보안 방어 토폴로지]
|-- Enterprise Ingress/Egress (전사 트래픽 유입/유출)
`-- 1. NGFW (Network Edge: L3-L7 DPI, App-ID, IPS, C2 차단)
    |-- Inbound Web Traffic -> [ 2. WAF (Web Front: SQLi/XSS 차단, API 스키마 검증) ] -> DMZ Web/API Server
    `-- Outbound SaaS Traffic -> [ 3. CASB (Cloud Broker: Shadow IT 탐지, DLP 차단) ] -> Public SaaS (M365)
`-- Integrated SOC (SIEM / SOAR: 3개 솔루션 이벤트 통합 상관 분석 및 자동 대응)
```

선의 의미: 인입되는 전체 네트워크 트래픽을 NGFW가 1차 정제하고 웹 서버 대상 패킷은 WAF가, 외부 클라우드 접속은 CASB가 정밀 검사하는 계층형 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **차세대 방화벽 (NGFW)** | 엔터프라이즈 네트워크 인프라, **전사 IP 트래픽 L7 DPI 및 IPS 차단** | Palo Alto / Fortinet |
| **웹 방화벽 (WAF)** | 웹 애플리케이션(HTTP/S) 대상 **OWASP Top 10(SQLi, XSS) 정밀 방어** | Imperva / AWS WAF |
| **클라우드 중개 (CASB)**| SaaS 클라우드 대상 **Shadow IT 탐지 및 인라인 DLP 데이터 유출 차단** | Netskope / Prisma |
| **통합 관제 (SIEM/SOAR)**| 3개 솔루션의 보안 이벤트를 **정규화 상관 분석하고 플레이북 자동 대응** | Integrated SOC |

#### 한줄 요약
- NGFW(네트워크 전역), WAF(웹/API 서버), CASB(SaaS 클라우드), SIEM/SOAR(통합 관제)가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **다계층 트래픽 라우팅 파이프라인**: 목적지와 프로토콜에 따라 패킷을 분기하여 검사 오버헤드를 최적화하고 보안을 완성하는 프로세스.

</details>

```text
NGFW 1차 정제, 목적지별 WAF/CASB 분기 검사 및 SIEM 연동 파이프라인
        │
   1. [NGFW 1차 정제] 패킷 인입 시 L3/L4 5-Tuple, L7 App-ID 및 IPS 시그니처 대조 ➔ [정상 통과]
        │
   ├─ [목적지: 사내 DMZ 웹 서버] ──▶ [WAF 계층 이동]
   │     │
   │     ▼
   │   HTTP 요청 정밀 파싱 ➔ SQLi/XSS 공격 패턴 및 API 스키마 검증 ➔ 정상 웹 트래픽만 백엔드 전달
   │
   └─ [목적지: 외부 클라우드 SaaS] ──▶ [CASB 계층 이동]
         │
         ▼
       SaaS 테넌트 인가 확인 ➔ 업로드 파일 내 주민번호/기밀 DLP 검사 ➔ 비인가 시 업로드 즉시 차단
```

#### 한줄 요약
- NGFW 1차 정제 → WAF 웹 취약점 심사 → CASB 클라우드 DLP 통제 → SIEM 통합 관제 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **NGFW** vs **WAF** vs **CASB**.

</details>

| 비교 항목 | 차세대 방화벽 (NGFW) | 웹 애플리케이션 방화벽 (WAF) | 클라우드 접근 보안 중개 (CASB) |
|:---|:---|:---|:---|
| **배치 위치** | **네트워크 경계 및 데이터센터 게이트웨이** | **웹 서버 및 API 게이트웨이 전면 (DMZ)** | **엔드포인트 에이전트, 인터넷 출구, Cloud API**|
| **주요 검사 계층** | **L3 ~ L7 (모든 IP/포트 트래픽 전수)** | **L7 전용 (HTTP, HTTPS, WebSocket, API)** | **L7 SaaS 응용 계층 (M365, Salesforce 등)** |
| **주요 탐지 위협** | **네트워크 침입(IPS), 악성코드 C2, DDoS** | **OWASP Top 10 (SQLi, XSS, SSRF), 웹쉘** | **Shadow IT, 비인가 클라우드 업로드, 계정 탈취**|
| **검사 심도 (Depth)** | 넓은 범위의 트래픽을 얕고 빠르게 검사 | **웹 프로토콜 페이로드를 극도로 깊게 검사**| **클라우드 메타데이터 및 파일 내용(DLP) 검사** |
| **단독 사용 시 한계** | 웹 로직 취약점 및 SaaS 내부 유출 불가 | 웹 외 타 프로토콜(FTP, SSH, RDP) 보호 불가| 온프레미스 네트워크 침입 및 서버 공격 방어 불가|

#### 한줄 요약
- NGFW는 넓은 네트워크 전역 방어, WAF는 깊은 웹 취약점 방어, CASB는 외부 클라우드 데이터 통제에 특화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **WAF False Positive (오탐 장애)**: 정상적인 특수문자 입력이나 API 호출을 WAF가 공격으로 오인하여 정상 결제 트랜잭션을 차단하는 운영 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NGFW를 통과한 정상 HTTP 트래픽 내부의 **SQL Injection 공격으로 인한 DB 탈취** | **DMZ 웹 서버 전면에 `특화 WAF 인라인 배치 및 OWASP Core Rule Set 적용`** | 웹 로직 공격 100% 차단 및 웹 애플리케이션 무결성 보장 |
| 임직원이 개인 클라우드를 사용하여 **사내 핵심 기술 문서를 무단 유출하는 사고** | **`CASB Forward Proxy 연동 및 인라인 DLP(정규식+AI 파일 분류)`** 강제 | 섀도 IT 사용 즉각 적발 및 비인가 외부 업로드 원천 차단 |
| WAF의 과도한 시그니처 매칭으로 인한 **정상 고객 요청 차단(오탐 장애)** | **WAF 룰 적용 전 `모니터링(Detection-Only) 모드 운영 및 예외 화이트리스트`** 정제 | 오탐률 0.1% 이하 억제 및 서비스 비즈니스 연속성 보장 |
| 다중 보안 장비 도입으로 인한 트래픽 지연 및 관리 복잡성 증가 | **단일 클라우드 네이티브 `SASE(Secure Access Service Edge) 플랫폼` 통합** | 검사 지연시간 50% 단축 및 중앙 통합 정책 관리 실현 |

#### 한줄 요약
- WAF로 SQLi를 방어하고, CASB DLP로 섀도 IT 유출을 차단하며, 모니터링 모드로 WAF 오탐을 방지한다.

## Ⅶ. 결론

- 클라우드 전환과 원격 근무 환경에서 경계가 사라진 엔터프라이즈 인프라를 보호하기 위해 **NGFW, WAF, CASB의 계층형 결합 아키텍처는 제로 트러스트 엔터프라이즈 보안의 핵심 뼈대**이며, 실무 구현 시 **NGFW 기반 네트워크 마이크로 세그멘테이션, WAF 기반 웹/API 전용 방어선, CASB 기반 SaaS 거버넌스 및 DLP 연동**을 단일 SASE(Secure Access Service Edge) 프레임워크로 통합 구현하여 무결점 심층 보안 체계 완성

#### 한줄 요약
- NGFW, WAF, CASB를 유기적으로 결합하여 네트워크, 웹, 클라우드를 아우르는 심층 방어 체계를 실현한다.