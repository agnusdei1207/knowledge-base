---
title: "SOAP vs REST"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-software"
weight: 199
---

## 핵심 인사이트 (3줄 요약)
- 서로 다른 컴퓨터끼리 대화(API)하기 위한 두 가지 핵심 철학. **SOAP는 "엄격한 편지 봉투 규격과 서명 도장까지 완벽해야만 통신하는 무거운 공문서"**이고, **REST는 "웹의 기본 주소(URL)와 HTTP 메서드(GET, POST)를 그대로 활용하는 가벼운 엽서"**임.
- SOAP는 XML이라는 단일 언어만 쓰고 융통성이 없어 멸망의 길을 걸었으나, 보안과 트랜잭션 보장이 절대적인 금융권이나 기업 간(B2B) 레거시 시스템에서는 아직도 굳건히 살아있음.
- 모바일과 클라우드 시대가 도래하면서, 가벼운 JSON을 휙휙 던지는 **REST가 현대 웹 API(오픈 API, 마이크로서비스)의 절대적인 글로벌 표준**으로 천하를 통일함.
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | 분산 시스템 간의 정보 교환을 위한 통신 프로토콜/아키텍처 스타일 | "이 개념의 핵심" |
| **필요성** | A 회사의 Java 서버와 B 회사의 C++ 서버가 통신해야 함 | "이 개념의 핵심" |
| **1. SOAP (엄격한 프로토콜)** | - **프로토콜(규칙) 그 자체** | "서비스 분업" |
| **WSDL (Web Services Description Language)** | "이 API를 쓰려면 이런 모양으로 보내라"는 사용 설명서를 XML로 자동 생성해 줌 | "식당 메뉴판" |
| **2. REST (가벼운 아키텍처 스타일)** | - 프로토콜이 아니라 **설계 가이드라인(스타일)** | "표준 주문 방식" |
| **명사 중심의 자원(Resource)** | 모든 데이터를 URL로 표현함 | "이 개념의 핵심" |
| **동사 중심의 HTTP 메서드** | 데이터를 어떻게 할지는 HTTP의 기본 동작(`GET`(조회), `POST`(생성), `PUT`(수정), `DELETE`(삭제))에 맡겨버림 | "이 개념의 핵심" |

---


## Ⅰ. 개요 및 필요성
- **개요**: 분산 시스템 간의 정보 교환을 위한 통신 프로토콜/아키텍처 스타일. (SOAP: Simple Object Access Protocol, REST: REpresentational State Transfer).
- **필요성**: A 회사의 Java 서버와 B 회사의 C++ 서버가 통신해야 함. 언어가 다르니 데이터를 주고받을 공통 언어가 필요했음. "엄청나게 깐깐한 규칙을 만들어서 절대 에러가 안 나게 하자!" ➡️ **SOAP** 탄생. 근데 막상 써보니 설정 파일(WSDL)만 수백 줄이라 개발자들이 너무 고통받음. **"아니, 그냥 우리가 매일 쓰는 인터넷 웹브라우저(HTTP) 기술을 그대로 이용해서 주소창에 `GET /users` 치면 가볍게 데이터(JSON) 주게 만들면 안 돼?"** ➡️ **REST**의 탄생.
---
## Ⅱ. 아키텍처 및 핵심 원리
- **1. SOAP (엄격한 프로토콜)**:
  - **프로토콜(규칙) 그 자체**. 편지를 보낼 때 봉투(Envelope), 머리말(Header), 본문(Body)의 XML 태그 위치가 단 1글자라도 틀리면 가차 없이 에러를 뱉음.
  - **WSDL (Web Services Description Language)**: "이 API를 쓰려면 이런 모양으로 보내라"는 사용 설명서를 XML로 자동 생성해 줌. (기계끼리 통신 세팅하기 좋음).
  - WS-Security, WS-ReliableMessaging 등 '전송 보장'과 '보안'을 위한 내장 기능이 엄청나게 강력함.
- **2. REST (가벼운 아키텍처 스타일)**:
  - 프로토콜이 아니라 **설계 가이드라인(스타일)**. 
  - **명사 중심의 자원(Resource)**: 모든 데이터를 URL로 표현함. (예: `http://api.com/users/123`)
  - **동사 중심의 HTTP 메서드**: 데이터를 어떻게 할지는 HTTP의 기본 동작(`GET`(조회), `POST`(생성), `PUT`(수정), `DELETE`(삭제))에 맡겨버림.
  - 무겁고 긴 XML 대신, 가볍고 괄호 `{ }`로 이루어진 **JSON 포맷**을 대세로 채택하여 모바일 통신 속도를 극대화함.

```text
[ "123번 유저의 이름(John)을 변경해 줘!" API 요청 비교 ]

 ✉️ [ SOAP의 방식 (무거운 공문서 - XML) ]
 POST /UserService HTTP/1.1
 <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header/>
    <soapenv:Body>
       <UpdateUserRequest>
          <UserID>123</UserID>
          <NewName>John</NewName>
       </UpdateUserRequest>
    </soapenv:Body>
 </soapenv:Envelope>
 * ❗ 결과: 태그 쓰다 지침. 데이터보다 껍데기(Envelope) 용량이 더 큼.

 🚀 [ REST의 방식 (가벼운 엽서 - JSON) ]
 PUT /users/123 HTTP/1.1
 {
    "name": "John"
 }
 * 💡 결과: URL과 HTTP 메서드(PUT)로 뜻을 명확히 전달. 데이터(JSON)가 엄청 작고 직관적임!
```
---
## Ⅲ. 비교 및 연결
| 구분 | SOAP | REST |
|---|---|---|
| **본질** | 엄격한 **프로토콜 (Protocol)** | 유연한 **아키텍처 스타일 (Style)** |
| **데이터 포맷** | 오직 **XML**만 허용 | JSON, XML, Plain Text 등 **다양함 (JSON 대세)** |
| **상태 유지** | 상태 유지(Stateful) 기능 지원 | 무조건 **무상태 (Stateless)** |
| **보안 및 신뢰성** | WS-Security (봉투 자체 암호화) <br> 빌트인 에러 처리 완벽 | SSL/TLS(HTTPS)에 의존 <br> 에러는 HTTP 상태 코드(404 등)로 퉁침 |
| **사용처** | **보수적 금융망, 레거시 결제 시스템, B2B** | **모바일 앱, 오픈 API, 마이크로서비스(MSA)** |
---
## Ⅳ. 실무 적용 및 기술사 판단
- **REST 성숙도 모델 (Richardson Maturity Model)**: 대다수 주니어 개발자는 URL만 `/getUsers`로 파놓고 무조건 POST로 던지면서 "나 REST API 만들었다"고 착각함. 기술사는 REST 성숙도 모델을 기준으로, URL은 행위(동사)가 아닌 자원(명사, `/users`)으로 식별하고, HTTP 메서드(GET/POST/PUT/DELETE)를 목적에 맞게 엄격히 사용(Level 2)하며, 궁극적으로 응답 데이터 안에 다음 행동을 할 수 있는 링크(HATEOAS)까지 포함(Level 3)하는 '진정한 RESTful API' 설계를 강제해야 함.
- **GraphQL 및 gRPC와의 진화 연결**: 현대 클라우드 네이티브에서 REST의 한계(JSON 오버헤드, 수많은 URL 엔드포인트 관리)가 드러나고 있음. 기술사는 외부 클라이언트(프론트엔드)용으로는 딱 원하는 데이터만 쿼리해 가는 **GraphQL**을 채택하고, 내부 마이크로서비스 간의 초고속 백엔드 통신(B2B)에는 REST를 버리고 바이너리 압축 기술인 **gRPC**를 도입하는 차세대 API 아키텍처 진화 방향을 짚어야 함.
---
## Ⅴ. 기대효과 및 결론
- SOAP는 분산 시스템 간의 신뢰성 있는 이종(Heterogeneous) 통신 시대를 열어준 훌륭한 개척자였으나, 웹의 폭발적 성장에 따른 '가벼움'의 요구를 맞추지 못함.
- REST는 웹의 본질(HTTP)을 가장 우아하게 활용한 설계 철학으로, 오늘날 우리가 쓰는 스마트폰 앱과 클라우드 생태계를 지탱하는 글로벌 데이터 혈관망을 완성함.
---
### 📌 관련 개념 맵
- API (Application Programming Interface) ➡️ SOAP / WSDL ➡️ RESTful Architecture ➡️ JSON ➡️ GraphQL / gRPC (차세대)

### 📈 관련 키워드 및 발전 흐름도
- 기업 내 EAI/ESB(통합 버스) 기반 SOAP 시대 ➡️ Roy Fielding의 REST 논문 발표(2000) ➡️ 모바일 시대 개막(적은 데이터량 요구) ➡️ 트위터/페이스북의 REST 기반 Open API 대유행 ➡️ SOA에서 MSA로 진화하며 REST가 완전히 천하통일

### 👶 어린이를 위한 3줄 비유 설명
1. **SOAP**는 '엄격한 법원 공문서'예요. 봉투 크기, 우표 위치, 빨간 도장까지 규정대로 안 찍히면 우체국에서 아예 안 받아줘요. (안전하지만 너무 힘들어요).
2. **REST**는 '가벼운 포스트잇 엽서'예요. 
3. "받는 사람: 회원 123번, 할 일: 지우기(DELETE)"라고만 쓱 적어서 보내면 알아서 다 처리해 주니까, 스마트폰처럼 빠르고 가벼운 통신에 최고랍니다!
