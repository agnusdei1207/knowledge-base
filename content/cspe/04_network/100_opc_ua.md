---
title: "OPC UA 산업 표준 통신 (OPC UA)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 100
---

# 📖 【암기용】 개념 완전 이해

> 목적: OPC UA를 공장 장비 데이터를 표준 정보 모델과 보안 통신으로 연결하는 산업용 상호운용 표준으로 이해하게 만든다.

## 한눈에
- **개요**: 산업 장비와 시스템 간 데이터 의미, 접근 방식, 보안을 표준화한 통신 규격
- **왜 필요한가**: PLC, SCADA, MES, 클라우드가 제조사별 프로토콜로 분리되면 데이터 통합과 보안 통제가 어렵다.
- **핵심 직관**: 공장 장비마다 다른 언어를 쓰더라도 OPC UA라는 공통 사전과 통역 규칙으로 대화하게 만드는 방식이다.

## 깊이 이해
- **배경·문제의식**: 전통 OPC Classic은 Windows COM/DCOM 의존성이 컸다. OPC UA는 플랫폼 독립, 정보 모델, 보안, 확장성을 제공해 OT와 IT 통합에 사용된다.
- **작동 원리**: 서버는 Address Space에 객체, 변수, 메서드, 이벤트를 노드로 표현한다. 클라이언트는 browse, read/write, subscribe로 접근한다. PubSub 모델은 MQTT, UDP, TSN과 결합해 다수 구독자에게 배포한다.
- **비유**: 공장 전체 자산 목록을 표준 지도(Address Space)로 만들고, 각 설비의 온도·속도·상태를 이름과 의미가 있는 표지판으로 제공하는 방식이다.
- **구체 예시**: PLC가 `Machine01/SpindleSpeed` 변수를 OPC UA Server로 노출하고 MES가 subscribe하여 100ms 주기로 변경값을 수신한다.
- **흔한 오해·주의점**: OPC UA는 단순 프로토콜이 아니라 정보 모델, 서비스, 보안, transport를 포함한다. 방화벽 개방만으로 OT 보안이 해결되지 않는다.

## 연결 개념
- IoT Architecture — 산업 데이터 수집 계층의 표준 인터페이스
- MQTT — OPC UA PubSub transport로 활용 가능
- Zero Trust — OT/IT 연계 시 인증서·권한·감사 필요

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: OPC UA 출제 시 정보 모델, 클라이언트/서버, PubSub, 보안, OT/IT 통합 관점을 답안화한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OPC UA는 산업 장비 데이터를 표준 Address Space와 보안 서비스로 표현·교환하는 플랫폼 독립 산업 통신 표준이다.
> 2. **가치**: PLC, SCADA, MES, 클라우드 간 의미 기반 데이터 통합과 인증서 기반 접근통제를 제공한다.
> 3. **판단 포인트**: Client/Server, PubSub, information model, certificate, namespace, sampling interval을 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 산업 통신 표준 이해 확인 | Address Space, Node, Service, Security | 단순 TCP 프로토콜로 설명 |
| OT/IT 통합 판단 확인 | PLC·SCADA·MES·Cloud 연결 | 제조사 독자 프로토콜과 차이 누락 |
| 보안·운영 역량 확인 | certificate, user token, role, audit | OT망 인증서 관리 누락 |

> 요약: 이 문제는 OPC UA의 통신 방식보다 정보 모델과 보안 기반 상호운용성을 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 산업 장비 데이터 통합 표준
- 배경: 공장에는 PLC, HMI, SCADA, MES, 클라우드가 혼재하고 제조사별 프로토콜과 데이터 모델이 다르다.
- 필요성: OPC UA는 정보 모델, 서비스 세트, 인증서 기반 보안으로 OT/IT 데이터를 일관된 방식으로 연결한다.

---

## Ⅱ. 구조 및 구성요소

```text
PLC/Device -> OPC UA Server Address Space
           -> Client/Server Service / PubSub
           -> SCADA / MES / Cloud / Analytics
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Address Space | 객체·변수·메서드·이벤트를 Node로 표현 | namespace, NodeId |
| OPC UA Server | 장비 데이터를 서비스로 제공 | browse, read, write, subscribe |
| OPC UA Client | 데이터 조회·제어·구독 수행 | SCADA, MES, gateway |
| Security Model | 인증서·암호화·권한 통제 | X.509, user token, role |

> 요약: OPC UA는 장비 데이터를 표준 Address Space로 표현하고 클라이언트가 보안 채널로 접근한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Endpoint Discovery -> Secure Channel -> Session 생성
-> Browse/Read/Write/Subscribe -> DataChange/Event 수신 -> Audit 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | endpoint와 security policy 확인 | Basic256Sha256 등 |
| 2 | certificate 교환과 secure channel 생성 | trust list 등록 |
| 3 | session과 user token 인증 | role 기반 권한 |
| 4 | address space browse, read/write, subscribe 수행 | sampling interval 100ms |
| 5 | event·audit log와 연결 상태 관리 | session timeout, reconnect |

> 요약: OPC UA는 endpoint 탐색, 보안 채널, 세션, 서비스 호출, 감사 기록 순서로 동작한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | OPC UA | 수치 컬럼 |
|:---|:---|:---|:---|
| 플랫폼 | OPC Classic DCOM | 플랫폼 독립 | TCP 4840 |
| 데이터 의미 | 태그명 중심 | Address Space 정보 모델 | NodeId, namespace |
| 통신 방식 | polling 중심 | Client/Server, PubSub | sampling 100ms |
| 보안 | 네트워크 격리 의존 | 인증서·암호화·권한 | X.509, Basic256Sha256 |

> 요약: OPC UA는 제조사별 태그를 의미 모델과 보안 채널로 표준화해 OT/IT 통합을 지원한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 표준성 | Modbus, vendor protocol | OPC UA information model | 다벤더 설비 통합 |
| 통신 모델 | Client/Server only | Client/Server + PubSub | 다수 구독자·클라우드 연계 |
| 보안 | 방화벽 중심 | certificate, role, audit | OT/IT 경계 통합 |

> 요약: OPC UA는 다벤더 공장 데이터의 의미 통합과 보안 접근통제가 필요할 때 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 인증서 운영 실패 | 만료·trust list 불일치 | PKI inventory, 만료 30일 전 경보 | expired cert 0건 |
| 모델 불일치 | namespace 설계 부재 | companion spec, naming rule | unknown NodeId 0건 |
| OT망 부하 | 짧은 sampling interval | subscription 튜닝, gateway buffering | server CPU 70% 이하 |

> 요약: OPC UA 운영 리스크는 인증서, 정보 모델, 샘플링 부하를 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 연결 품질 | session reconnect 1분 이내 | OPC UA client log |
| 데이터 품질 | bad quality value 0.1% 이하 | status code 집계 |
| 보안 운영 | 인증서 만료 0건, 감사로그 100% | PKI, audit trail |

> 요약: OPC UA 도입 효과는 연결 복구, 데이터 quality, 인증서·감사 운영으로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 설비별 Address Space와 namespace naming rule을 정의하고 companion specification 적용 여부를 검토
2. X.509 인증서, trust list, Basic256Sha256 security policy, role 기반 권한을 표준 운영 절차로 수립
3. SCADA·MES·Cloud 연계는 OPC UA PubSub 또는 gateway를 사용하고 sampling interval 100ms~1초로 부하를 조정

**결론 (2줄):**
- 기술사 판단: 다벤더 산업 장비를 의미 기반으로 통합하려면 OPC UA를 표준 인터페이스로 채택해야 함
- 향후 방향: OPC UA PubSub over MQTT와 TSN 결합으로 cloud analytics와 deterministic control을 동시에 지원하는 방향

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | endpoint, session, service 호출 흐름 | OPC Classic·Modbus 대비 특성 |
| 요구사항 명시형 | "비교하시오", "방안을 제시하시오", "설계하시오" | 정보 모델·인증서·PubSub 설계 | 인증서·부하·namespace 리스크 대응 |

> 요약: 포괄형은 OPC UA 표준 구조, 요구사항 명시형은 OT/IT 통합 설계와 보안 운영을 중심으로 전환한다.
