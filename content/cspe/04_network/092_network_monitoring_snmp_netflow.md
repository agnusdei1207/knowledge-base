---
title: "네트워크 모니터링 SNMP NetFlow (Network Monitoring SNMP NetFlow)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 92
---

# 📖 【암기용】 개념 완전 이해

> 목적: SNMP·NetFlow·sFlow를 장비 감시, 트래픽 흐름 분석, 샘플링 관측으로 구분해 이해하게 만든다.

## 한눈에
- **개요**: 네트워크 장비와 트래픽 상태를 수집해 장애·용량·보안을 판단하는 관측 체계
- **왜 필요한가**: 인터페이스 사용률은 SNMP로 보지만, 어떤 IP와 애플리케이션이 회선을 쓰는지는 NetFlow v9/IPFIX나 sFlow가 필요하다.
- **핵심 직관**: SNMP는 계기판, NetFlow는 통행 기록, sFlow는 표본 교통 조사다.

## 깊이 이해
- **배경·문제의식**: 네트워크는 여러 장비를 거쳐 통신하므로 한 장비의 CPU, 포트 drop, 특정 플로우 폭증을 함께 봐야 한다. 모니터링이 없으면 회선 증설과 장애 원인 분석이 민원 기반으로 흐른다.
- **작동 원리**: SNMP는 OID 기반 MIB 값을 polling 또는 trap으로 수집한다. NetFlow v9/IPFIX는 5-tuple, 바이트, 패킷, 시작·종료 시각을 flow record로 내보낸다. sFlow는 패킷을 1:N으로 샘플링해 대용량 스위치에 적용한다.
- **비유**: 건물 관리에서 전기계량기(SNMP), 출입기록(NetFlow), CCTV 표본 분석(sFlow)을 함께 보는 방식이다.
- **구체 예시**: SNMP ifHCInOctets로 10Gbps 포트 사용률 85%를 감지하고, IPFIX에서 특정 백업 서버가 6Gbps를 점유함을 확인한다.
- **흔한 오해·주의점**: SNMP만으로 애플리케이션별 트래픽 원인을 알 수 없다. NetFlow는 payload를 저장하지 않으므로 패킷 내용 분석은 packet capture가 필요하다.

## 연결 개념
- Network KPI — 모니터링 데이터의 판단 기준
- NMS — 수집·시각화·알림을 통합하는 운영 시스템
- SIEM — NetFlow와 보안 로그를 상관 분석

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 모니터링 도구 나열이 아니라 지표 수집 목적별 기술 선택을 답안화한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 네트워크 모니터링은 SNMP OID, NetFlow v9/IPFIX, sFlow를 이용해 장비 상태와 트래픽 흐름을 수집·분석하는 체계다.
> 2. **가치**: 포트 사용률, packet drop, top talker, flow duration을 기반으로 장애 원인과 용량 증설 시점을 수치로 판단한다.
> 3. **판단 포인트**: 장비 상태는 SNMP, 세션 흐름은 NetFlow/IPFIX, 대용량 표본 관측은 sFlow를 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 관측 기술 구분 확인 | SNMP polling/trap, NetFlow v9/IPFIX, sFlow sampling | SNMP와 NetFlow를 같은 로그 수집으로 서술 |
| 장애 분석 흐름 확인 | interface counter와 flow record 상관 분석 | 사용률만 보고 원인 단정 |
| 운영 설계 역량 확인 | 수집 주기, 보존 기간, 알림 임계치, 보안 통제 | SNMP v2c community 노출 누락 |

> 요약: 이 문제는 어떤 데이터를 어떤 프로토콜로 수집하고 장애 판단에 연결하는지 묻는다.

---

## Ⅰ. 개요 및 필요성

네트워크 모니터링은 장비 상태와 트래픽 흐름을 지속 수집하는 운영 체계다. SNMP는 OID 기반 카운터를, NetFlow v9/IPFIX는 flow record를, sFlow는 샘플 패킷을 제공한다. SLA 준수와 장애 원인 분석을 위해 수집 주기·보존·경보 기준을 함께 설계해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Router/Switch -> SNMP Agent / Flow Exporter / sFlow Agent
              -> Collector -> Time Series DB -> Dashboard / Alert / Report
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| SNMP | OID·MIB 기반 장비 상태 수집 | ifHCInOctets, ifInErrors, CPU |
| NetFlow/IPFIX | 5-tuple 단위 흐름 기록 수집 | NetFlow v9, IPFIX RFC 7011 |
| sFlow | 패킷·카운터 샘플링 수집 | 1:1000 등 sampling rate |
| Collector | 수집·정규화·저장 | 중복 제거, 시간 동기화 |

> 요약: 모니터링 구조는 장비 에이전트, 플로우 내보내기, 수집기, 저장소, 대시보드로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
장비 계측 -> SNMP Polling/Trap 또는 Flow Export
-> Collector 수신 -> 지표 정규화 -> 임계치 비교 -> 경보/분석
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 장비별 SNMP OID와 flow exporter 설정 | SNMP v3, UDP 161/162 |
| 2 | 1분 polling, active timeout 60초로 수집 | 수집 누락률 1% 이하 |
| 3 | ifIndex, device, interface, 5-tuple 정규화 | 장비명·시간 동기화 |
| 4 | top talker, drop, error, utilization 산출 | 포트 사용률 70%, error 0.1% |
| 5 | 경보 발행과 원인 drill-down 수행 | 티켓·대시보드 연계 |

> 요약: 수집 체계는 장비 계측값을 정규화해 임계치와 비교하고, 포트 지표와 플로우 지표를 상관 분석한다.

---

## Ⅳ. 특징

| 구분 | SNMP | NetFlow/IPFIX | sFlow |
|:---|:---|:---|:---|
| 수집 대상 | 장비·인터페이스 카운터 | IP 흐름 메타데이터 | 샘플 패킷·카운터 |
| 표준/포트 | SNMP v3, UDP 161/162 | IPFIX RFC 7011, UDP 4739 | sFlow v5, UDP 6343 |
| 장점 | CPU·메모리·포트 상태 확인 | top talker, 애플리케이션 추정 | 100Gbps 이상 대용량 표본 |
| 한계 | 세션 원인 분석 제한 | exporter CPU·저장 용량 부담 | 샘플링 오차 존재 |

> 요약: SNMP는 상태, NetFlow/IPFIX는 흐름, sFlow는 대용량 표본 관측에 맞춘다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 장애 감지 | Ping alive check | SNMP interface·CPU·error 수집 | 장비 상태 장애 중심 |
| 트래픽 분석 | Packet capture | NetFlow/IPFIX flow record | 장기 보존·상위 사용자 분석 |
| 대용량 관측 | Full flow export | sFlow sampling | 40/100Gbps 스위치 부담 절감 |

> 요약: 장애 감지는 SNMP, 원인 추적은 NetFlow/IPFIX, 대용량 코어는 sFlow를 조합한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 인증정보 노출 | SNMP v2c community 사용 | SNMP v3 authPriv 적용 | v2c 장비 0대 |
| 수집기 병목 | flow export 폭증 | sampling, active timeout 조정 | collector drop 1% 이하 |
| 시간 불일치 | NTP 미동기 | NTP stratum 점검 | timestamp skew 1초 이하 |

> 요약: 모니터링 리스크는 인증, 수집 병목, 시간 동기화로 나뉘며 수집 신뢰도를 지표화해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 수집 완전성 | 장비 수집 성공률 99% 이상 | collector heartbeat |
| 분석 정확도 | top talker 95% 이상 식별 | NetFlow/IPFIX 대시보드 |
| 운영 반응 | 경보 후 티켓 생성 1분 이내 | NMS·ITSM 연동 로그 |

> 요약: 모니터링 성공 여부는 수집 성공률, 분석 식별률, 경보 처리 시간으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. SNMP v3 authPriv로 ifHCInOctets, ifInErrors, CPU, memory OID를 1분 주기로 수집
2. 경계 라우터에 NetFlow v9/IPFIX exporter를 설정하고 active timeout 60초, inactive timeout 15초 적용
3. 코어 스위치 100Gbps 구간은 sFlow 1:1000 샘플링으로 collector drop 1% 이하 유지

**결론 (2줄):**
- 기술사 판단: 장비 상태 장애는 SNMP, 트래픽 원인 분석은 NetFlow/IPFIX, 대용량 코어 관측은 sFlow가 적합함
- 향후 방향: Telemetry gNMI와 time-series DB를 결합해 10초 단위 지표 수집과 자동 원인 분석으로 확장

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | 수집·정규화·경보 흐름 | SNMP·NetFlow·sFlow 차이 |
| 요구사항 명시형 | "비교하시오", "방안을 제시하시오", "설계하시오" | 대상망별 수집 주기·collector 설계 | 보안·병목·시간 동기화 대응 |

> 요약: 포괄형은 관측 기술 구분, 요구사항 명시형은 운영 설계와 보안 통제를 중심으로 전환한다.
