---
title: "OPC UA 산업 표준 통신 (OPC Unified Architecture)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 329
---

# 📖 【암기용】 개념 완전 이해

> 목적: OPC UA를 제조·설비 데이터를 벤더 중립적으로 교환하기 위한 산업 표준 통신·정보 모델로 이해하게 만든다.

## 한눈에
- **개요**: 산업 장비와 IT 시스템이 데이터를 의미 있는 객체로 교환하는 IEC 62541 기반 표준
- **왜 필요한가**: PLC, 로봇, 센서, SCADA, MES가 제조사별 프로토콜로 분리되면 설비 데이터를 통합하기 어렵다.
- **핵심 직관**: 여러 나라 사람이 공통 언어와 신분증 체계로 대화하듯, 산업 장비가 표준 주소공간과 보안 체계로 데이터를 교환한다.

## 깊이 이해
- **배경·문제의식**: OPC Classic은 Windows COM/DCOM 의존성이 커서 플랫폼 독립성과 인터넷 규모 보안 요구를 만족하기 어려웠다.
- **작동 원리**: OPC UA 서버가 장비 데이터를 Node, Object, Variable, Method 형태의 Address Space로 제공하고, 클라이언트가 인증·암호화 채널로 읽기·쓰기·구독을 수행한다.
- **비유**: 전화번호부에 사람 이름, 부서, 연락처, 권한이 정리되어 있으면 앱이 같은 방식으로 사람을 찾는 것과 같다.
- **구체 예시**: MES가 OPC UA 서버를 통해 CNC 장비의 spindle speed, alarm code, production count를 구독해 생산 실적을 자동 수집한다.
- **흔한 오해·주의점**: OPC UA는 단순 전송 프로토콜만이 아니다. 정보 모델, 서비스, 보안, Client/Server와 PubSub 통신 패턴을 포함한다.

## 연결 개념
- Smart Factory — 설비 데이터를 MES·데이터 플랫폼과 연결
- IIoT — 산업 장비를 네트워크 기반으로 수집·분석
- IEC 62443 — OPC UA 적용 환경의 OT 보안 통제 기준

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: OPC UA는 IEC 62541 기반으로 산업 데이터의 의미 모델, 서비스, 보안을 함께 제공하는 벤더 중립 통신 표준임.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OPC UA는 장비 데이터를 Address Space의 객체·변수·메서드로 표현하고 안전한 채널로 교환하는 산업 상호운용 표준임.
> 2. **가치**: PLC·SCADA·MES·클라우드 간 데이터를 제조사 종속 없이 연결하고 의미 정보까지 전달함.
> 3. **판단 포인트**: 정보 모델, Client/Server, PubSub, X.509 인증서, 암호화 정책, Companion Specification이 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 산업 표준 통신 이해 확인 | IEC 62541, Address Space, Service | MQTT와 같은 메시지 브로커로만 설명 |
| 상호운용성 판단 확인 | 정보 모델, Companion Spec, 벤더 중립 | 단순 데이터 수집 API로 축소 |
| OT 보안 인식 확인 | 인증서, 암호화, 사용자 인증·인가 | 폐쇄망이므로 보안 불필요 서술 |

> 요약: 이 문제는 OPC UA를 전송 기술이 아니라 산업 의미 모델과 보안을 포함한 상호운용 표준으로 설명해야 한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | 산업 장비와 IT 시스템이 데이터를 의미 있는 객체로 교환하는 IEC 62541 기반 표준 | "핵심 기술 요소" |
| **왜 필요한가** | PLC, 로봇, 센서, SCADA, MES가 제조사별 프로토콜로 분리되면 설비 데이터를 통합하기 어렵다 | "핵심 기술 요소" |
| **핵심 직관** | 여러 나라 사람이 공통 언어와 신분증 체계로 대화하듯, 산업 장비가 표준 주소공간과 보안 체계로 데이터를 교환한다 | "핵심 기술 요소" |
| **배경·문제의식** | OPC Classic은 Windows COM/DCOM 의존성이 커서 플랫폼 독립성과 인터넷 규모 보안 요구를 만족하기 어려웠다 | "핵심 기술 요소" |
| **비유** | 전화번호부에 사람 이름, 부서, 연락처, 권한이 정리되어 있으면 앱이 같은 방식으로 사람을 찾는 것과 같다 | "핵심 기술 요소" |
| **구체 예시** | MES가 OPC UA 서버를 통해 CNC 장비의 spindle speed, alarm code, production count를 구독해 생... | "핵심 기술 요소" |
| **흔한 오해·주의점** | OPC UA는 단순 전송 프로토콜만이 아니다 | "핵심 기술 요소" |

---


## Ⅰ. 개요 및 필요성

- 개요: 산업 데이터 상호운용 표준
- 배경: 제조사별 PLC·SCADA·장비 프로토콜이 분리되어 설비 데이터 통합과 의미 해석이 어려움.
- 필요성: IEC 62541 기반 정보 모델과 보안 채널로 OT와 IT 시스템 간 데이터를 표준 방식으로 교환해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Device / PLC -> OPC UA Server -> Address Space / Information Model
Client / MES / SCADA -> Secure Channel -> Read / Write / Subscribe
PubSub -> Broker / UDP / TSN -> Edge / Cloud
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| OPC UA Server | 장비 데이터와 메서드 제공 | node, object, variable |
| OPC UA Client | 데이터 조회·구독·제어 요청 | MES, SCADA, edge |
| Address Space | 데이터 의미와 관계 표현 | namespace, node id |
| Security Model | 인증·암호화·인가 제공 | X.509, secure channel |

> 요약: OPC UA는 서버·클라이언트 통신에 정보 모델과 보안 체계를 결합한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서버 endpoint 발견 -> 인증서 교환 -> Secure Channel 생성
-> Session 생성 -> Node 탐색 -> Read / Write / Subscribe -> Audit
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 클라이언트가 서버 endpoint와 보안 정책을 확인함 | endpoint policy |
| 2 | 인증서를 교환하고 secure channel을 생성함 | certificate trust |
| 3 | session에서 address space를 탐색하고 node를 선택함 | namespace mapping |
| 4 | read/write/subscribe 또는 PubSub로 데이터를 교환함 | latency, audit log |

> 요약: OPC UA 통신은 endpoint 발견, 보안 채널, session, node 접근 순서로 이루어진다.

---

## Ⅳ. 특징

| 구분 | OPC Classic | OPC UA | 판단 기준 |
|:---|:---|:---|:---|
| 플랫폼 | COM/DCOM 의존 | 플랫폼 독립 | Linux·edge 적용 |
| 데이터 | 태그 중심 | 객체·관계 정보 모델 | 의미 상호운용 |
| 통신 | Client/Server 중심 | Client/Server+PubSub | cloud·TSN 연계 |
| 보안 | DCOM 보안 의존 | 인증서·암호화 내장 | OT 보안 요구 |

> 요약: OPC UA는 OPC Classic의 플랫폼 의존성을 줄이고 정보 모델과 보안을 표준에 포함한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 프로토콜 | Modbus 태그 | OPC UA 정보 모델 | 의미 데이터 필요 |
| 메시징 | MQTT payload | OPC UA PubSub | 산업 모델 유지 |
| 보안 | 네트워크 격리 | 인증서·사용자 권한 | 외부 연계 범위 |

> 요약: 단순 센서값 전송은 MQTT도 가능하지만, 산업 의미 모델과 표준 보안이 필요하면 OPC UA가 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 인증서 운영 실패 | trust list·만료 관리 부재 | PKI와 인증서 갱신 절차 | expired cert |
| namespace 불일치 | 장비별 모델 차이 | Companion Spec 적용 | mapping error |
| 제어 위험 | write 권한 과다 | read-only 기본, 역할 기반 인가 | write audit |

> 요약: OPC UA 운영은 인증서, namespace, write 권한을 중점 통제해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 상호운용 | node mapping 오류 추적 | integration test |
| 보안 | 인증서 신뢰·암호화 정책 점검 | certificate audit |
| 운영 | subscribe latency와 drop 관리 | telemetry |

> 요약: OPC UA 적용 성과는 연결 성공이 아니라 의미 매핑, 보안 설정, 통신 품질로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 설비별 태그를 OPC UA Address Space와 namespace로 매핑하고 Companion Specification 적용 가능성을 검토함.
2. 서버·클라이언트 인증서, trust list, 보안 정책, 사용자 권한을 운영 절차로 관리함.
3. MES/SCADA 연계는 read-only 구독부터 적용하고 write 제어는 승인·감사·rollback 절차를 갖춘 뒤 제한적으로 허용함.

**결론 (2줄):**
- 기술사 판단: 의미 모델과 벤더 중립성이 필요한 스마트팩토리는 OPC UA를 우선 검토하고, 단순 telemetry는 MQTT와 병행 가능함.
- 향후 방향: OPC UA는 PubSub, TSN, edge/cloud 연계를 통해 IIoT와 실시간 제조 데이터 통합의 기반으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OPC UA를 설명하시오" | 보안 채널·session·node 접근 흐름 | OPC Classic과 차이 |
| 요구사항 명시형 | "스마트팩토리 통신 표준을 비교하시오" | OPC UA와 MQTT 적용 구분 | 정보 모델·보안·리스크 |

> 요약: 설명형은 IEC 62541 구조를, 비교형은 의미 모델과 메시징의 선택 기준을 중심으로 작성한다.
