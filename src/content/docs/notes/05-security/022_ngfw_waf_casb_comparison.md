---
sidebar:
  order: 22
  label: "022. NGFW vs WAF vs CASB 비교"
  badge:
    text: "기출 · 50%"
    variant: note
title: "계층별 보안 통제 아키텍처 비교 : NGFW vs WAF vs CASB"
date: "2026-08-26T14:25:39+09:00"
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

- 정의/개념: NGFW·WAF·CASB를 결합한 **다계층 심층 방어**
- 배경/필요성: NGFW만으로는 **웹 로직·SaaS 유출 통제 불가**

#### 한줄 요약
- NGFW, WAF, CASB의 다계층 분업을 통해 네트워크, 웹, 클라우드 전 영역의 보안 사각지대를 제거한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Shadow IT (섀도 IT)**: 기업 IT 부서의 승인 없이 임직원이 임의로 사용하는 개인 클라우드 저장소나 협업 도구.
- **OWASP Top 10**: 웹 애플리케이션에서 가장 빈번하고 치명적으로 발생하는 10대 보안 취약점 목록.

</details>

- **영역별 심층 검사**: NGFW·WAF·**CASB DLP** 분업
- **제로 트러스트 연동**: 망 분리·API 검증·**테넌트 격리**
- **통합 가시성**: 로그를 **SIEM/SOAR**에서 상관 분석

#### 한줄 요약
- 영역별 특화 심층 검사, 제로 트러스트 연동, 통합 위협 상관 분석을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Reverse Proxy vs Forward Proxy**: 외부에서 내부 웹 서버로 들어오는 트래픽을 중계하는 Reverse Proxy(WAF)와 내부 사용자가 외부 클라우드로 나가는 트래픽을 통제하는 Forward Proxy(CASB).

</details>

```text
[다계층 보안 통제]
|-- NGFW       : 네트워크 경계·DPI 통제
|-- WAF        : 웹·API 공격 통제
|-- CASB       : SaaS 접근·DLP 통제
`-- SIEM/SOAR  : 이벤트 상관·대응
```

선의 의미: 인입되는 전체 네트워크 트래픽을 NGFW가 1차 정제하고 웹 서버 대상 패킷은 WAF가, 외부 클라우드 접속은 CASB가 정밀 검사하는 계층형 구조

| 구성요소 | 책임 |
|:---|:---|
| NGFW | 전사 IP 트래픽의 **DPI·IPS 통제** |
| WAF | **OWASP Top 10·API** 공격 방어 |
| CASB | **Shadow IT·DLP** 통제 |
| SIEM/SOAR | 이벤트 **상관 분석·자동 대응** |

#### 한줄 요약
- NGFW(네트워크 전역), WAF(웹/API 서버), CASB(SaaS 클라우드), SIEM/SOAR(통합 관제)가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **다계층 트래픽 라우팅 파이프라인**: 목적지와 프로토콜에 따라 패킷을 분기하여 검사 오버헤드를 최적화하고 보안을 완성하는 프로세스.

</details>

```text
사용자·외부 트래픽
         |
      NGFW 정제
         |
     목적지·서비스
       /       \
 웹·API         SaaS
   |             |
 WAF 검사      CASB DLP
   |             |
 웹 서버       클라우드 서비스
       \       /
       SIEM/SOAR
```

#### 한줄 요약
- NGFW 1차 정제 → WAF 웹 취약점 심사 → CASB 클라우드 DLP 통제 → SIEM 통합 관제 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **NGFW** vs **WAF** vs **CASB**.

</details>

| 비교 항목 | 차세대 방화벽 (NGFW) | 웹 애플리케이션 방화벽 (WAF) | 클라우드 접근 보안 중개 (CASB) |
|:---|:---|:---|:---|
| 배치 위치 | 네트워크 경계 | 웹·API 전면 | 엔드포인트·출구·Cloud API |
| 주요 검사 계층 | **L3~L7 IP 트래픽** | **L7 HTTP·API** | **L7 SaaS** |
| 주요 탐지 위협 | 침입·C2·DDoS | **SQLi·XSS·SSRF** | **Shadow IT·데이터 유출** |
| 검사 심도 | 넓고 빠른 검사 | 웹 페이로드 심층 검사 | 메타데이터·파일 DLP |
| 단독 사용 한계 | 웹 로직·SaaS 유출 | 비웹 프로토콜 | 온프레미스 침입 |

#### 한줄 요약
- NGFW는 넓은 네트워크 전역 방어, WAF는 깊은 웹 취약점 방어, CASB는 외부 클라우드 데이터 통제에 특화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **WAF False Positive (오탐 장애)**: 정상적인 특수문자 입력이나 API 호출을 WAF가 공격으로 오인하여 정상 결제 트랜잭션을 차단하는 운영 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| HTTP 내부 **SQL 삽입·DB 탈취** | **WAF·OWASP CRS** 적용 | 웹 로직 공격 차단 |
| 개인 SaaS로 **기밀정보 유출** | **CASB Forward Proxy·DLP** | 섀도 IT 업로드 차단 |
| WAF 오탐으로 **정상 요청 차단** | **감사 모드·허용 목록** 튜닝 | 서비스 연속성 확보 |
| 다중 장비로 **지연·관리 복잡성** | **SASE 통합** | 중앙 정책과 검사 효율 확보 |

#### 한줄 요약
- WAF로 SQLi를 방어하고, CASB DLP로 섀도 IT 유출을 차단하며, 모니터링 모드로 WAF 오탐을 방지한다.

## Ⅶ. 결론

- 네트워크는 **NGFW**, 웹·API는 **WAF**, SaaS는 CASB 선택

#### 한줄 요약
- NGFW, WAF, CASB를 유기적으로 결합하여 네트워크, 웹, 클라우드를 아우르는 심층 방어 체계를 실현한다.
