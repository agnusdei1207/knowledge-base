---
title: "496. IoT 시스템 감리 연결성 보안 평가 (IoT System Audit Connectivity Security)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IoT 시스템 감리 연결성 보안 평가는 MQTT/CoAP/AMQP 등 경량 프로토콜, BLE/Zigbee/LoRaWAN/NB-IoT 등 다중 무선 인터페이스, DTLS/TLS 1.3/mTLS 기반 상호인증, X.509/PKI·OAuth 2.0·JWT 토큰, 그리고 Zero Trust·NAC·마이크로세그멘테이션을 통합적으로 진단하여 디바이스-게이트웨이-플랫폼-애플리케이션 4계층 전 구간의 취약점을 정량화하는 감리 기법이다.
> 2. **가치**: OWASP IoT Top 10(2022), NIST IR 8259B, ISO/IEC 27400:2022, ETSI EN 303 645 v2.1.1, KISA IoT 보안 인증 기준을 통합 매핑함으로써 감리 시 평균 60~80개 점검항목을 자동 스코어카드로 환산하고, 미흡 항목별 CVSS v3.1 기반 위험도(0.0~10.0)를 산출하여 발주처·시공사·사업자 간 책임 소재를 분기별로 가시화한다.
> 3. **판단 포인트**: 트레이드오프는 (a) 디바이스 제약(CPU/RAM/전력)으로 인한 경량 암호(ChaCha20-Poly1305 vs AES-256-GCM) 선택, (b) NB-IoT/Cat-M1의 SIM·eSIM vs LoRaWAN의 OTAA/ABP 인증, (c) MQTT 브로커 중앙화 vs EMQX/Mosquitto 클러스터링, (d) OTA 펌웨어 무결성 검증(서명+RSA-4096 vs Ed25519)인데, 기술사는 “프로토콜 스택 ↔ 위협 모델 ↔ 컴플라이언스” 3축 매트릭스로 우선순위를 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

IoT 시스템은 전통적인 3-tier IT 시스템과 달리 **Edge(센서/액추에이터) -> Fog(게이트웨이) -> Cloud(플랫폼) -> Application**의 4-tier 분산 아키텍처를 가지며, 동일 시스템 내에서 MQTT(대역폭 50~200B/메시지), CoAP(UDP 기반 4~16B 헤더), HTTP/HTTPS, LwM2M, AMQP 1.0이 혼재 운용된다. 2024년 기준 한국정보보호산업협회(KIIS) 통계에 따르면 IoT 도입 사업장 중 **연결성 보안 감리를 수행한 비율은 약 23%**에 불과하며, K-ISMS 인증 심사에서 IoT 연결성 항목이 부적합 판정을 받는 비율은 **34.2%**로 일반 IT 대비 2.4배 높다. 이는 IoT 디바이스의 평균 수명(8~15년)이 TLS 인증서 유효기간(1~3년)보다 길고, OTA 업데이트 미적용률이 중소형 사업장에서 60%를 초과하기 때문이다.

특히 한국 환경에서는 **지능형 홈·빌딩, 스마트팩토리, 자율주행 V2X, 에너지 HEMS, 의료 IoMT** 등 도메인별로 별도 규제(주택법, 에너지이용합리화법, 의료기기법, 자동차관리법)가 적용되어 단일 표준 매핑만으로는 감리가 불가능하다. 따라서 기술사는 **IEC 62443(산업자동화) + ISO/IEC 27001:2022(정보보안) + ISO/SAE 21434(차량보안) + ISO/IEC 30141(IoT 참조모델)**의 하이브리드 통제항목을 발주처 SLA에 맞춰 가중치 적용해야 한다.

```text
[IoT 시스템 감리 연결성 보안 4-tier 참조 모델]

  +--------------------------------------------------------------+
  |  4. Application Tier (SaaS / BSS / 분석 / 대시보드)          |
  |     - OAuth 2.0 / OIDC, RBAC/ABAC, FAPI 2.0                  |
  |     - 감사 로그: WORM(Write Once Read Many) 스토리지          |
  +--------------------------------------------------------------+
  |  3. Cloud Platform Tier (IoT Hub / Broker / DB)              |
  |     - MQTT 5.0 Broker (EMQX 5.x / HiveMQ CE / Mosquitto)     |
  |     - CoAP Server (Eclipse Californium / aiocoap)             |
  |     - LwM2M (Leshan) / AMQP 1.0 (RabbitMQ / Apache Qpid)     |
  |     - TLS 1.3, mTLS, X.509, OCSP Stapling, CRL               |
  +--------------------------------------------------------------+
  |  2. Fog / Gateway Tier (Edge GW / 라우터 / NVR)               |
  |     - 프로토콜 변환: Modbus/OPC-UA -> MQTT                     |
  |     - 로컬 캐시, 데이터 정규화, EDR/XDR, TPM 2.0              |
  |     - NAC(802.1X), VPN/IPsec, WireGuard                       |
  +--------------------------------------------------------------+
  |  1. Edge / Device Tier (센서·액추에이터·MCU)                   |
  |     - 무선: Wi-Fi 6/6E, BLE 5.4 Mesh, Zigbee 3.0, Thread,    |
  |             Z-Wave 800, LoRaWAN 1.0.4, NB-IoT/Cat-M1,         |
  |             Wi-SUN, IEEE 802.15.4g                           |
  |     - 유선: Ethernet/IP, RS-485/Modbus RTU, CAN, BACnet       |
  |     - 보안: Secure Boot, HW Root-of-Trust, TrustZone-M,       |
  |             OPTIGA(TPM), SE050C, ATECC608B, MAXQ1065          |
  +--------------------------------------------------------------+
                ^ 감리 연결성 보안 평가는 1->4 전 구간 점검
```

기존 IT 감리는 ①네트워크 ②시스템 ③어플리케이션 ④데이터 ⑤물리 5개 영역에 한정되었으나, IoT는 여기에 ⑥디바이스 펌웨어 ⑦무선 전파 ⑧전력/배터리 ⑨안전(Safety·Security 공존) ⑩개인정보(영상·생체·위치) 5개 영역이 추가되어 총 10개 영역을 통합 평가해야 한다. **NIST SP 800-183**(네트워크스-of-디바이스) 모델과 **oneM2M TR-0051**(감리 가이드)이 이를 뒷받침한다.

- **📢 섹션 요약 비유**: IoT 감리는 “4층짜리 아파트의 수도관·전기·가스·소방·통신·CCTV를 동시에 점검하는 종합 안전진단”과 같다. 위층 한 곳만 점검해서는 안 되며, 1층 누수가 4층 단말까지 영향을 주듯 디바이스 한 곳의 취약점이 클라우드까지 전파된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IoT 연결성 보안 감리는 **P-A-D-A** 4단계 프로세스로 수행된다: **Plan(계획) -> Assess(평가) -> Defend(방어) -> Audit(감사)**. 각 단계별로 점검 도구와 기준이 다르며, 기술사는 감리 착수 2주 전 발주처·사업자·운영사와 Kick-off를 통해 다음 7개 항목을 확정한다.

| 구분 | 단계 | 주요 산출물 | 도구 예시 |
|:---|:---|:---|:---|
| 1 | 자산 식별 | 디바이스 인벤토리(모델·시리얼·펌웨어), 네트워크 토폴로지 | NetBox, Device42, Axonius, Armis |
| 2 | 위협 모델링 | STRIDE/LINDDUN 기반 DFD | Microsoft Threat Modeling Tool, OWASP pytm |
| 3 | 정적/동적 분석 | 펌웨어 바이너리 분석, 무선 캡처 | binwalk, Ghidra, Firmadyne, Wireshark, Ubertooth, HackRF |
| 4 | 침투 테스트 | PoC 익스플로잇, CVSS 스코어링 | Burp Suite, MQTT-PWN, Nmap NSE, bettercap, KillerBee |
| 5 | 컴플라이언스 매핑 | 통제항목 갭 분석 | OWASP IoT Top 10 매퍼, CIS IoT Benchmark v1.0 |
| 6 | 보고서 작성 | 위험 대장, 시정 권고, 잔여 위험 | KISA 양식, OWASP ASVS Level 2/3 |
| 7 | 후속 감리 | 재평가, SLA 검증, ISMS-P 연계 | K-ISMS-P 인증심사 기준, ISO 27005 |

### 핵심 프로토콜별 보안 메커니즘

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **MQTT 5.0 Broker (EMQX 5.x)** | 디바이스-플랫폼 경량 메시지 버스 (QoS 0/1/2, Topic 와일드카드) | - TLS 1.3 + mTLS: 클라이언트 X.509 인증서 SHA-384 ECDSA P-256<br>- CONNECT 패킷 username/password 또는 JWT(HS256/RS256)<br>- Topic ACL: `${clientid}/+/cmd` 패턴 매칭<br>- Broker 자체 TLS 1.3 cipher suite: `TLS_AES_256_GCM_SHA384`<br>- Backpressure: `Receive-Maximum` 속성으로 흐름 제어 |
| **CoAP (RFC 7252 + RFC 9175)** | UDP 5683/5684 기반 constrained 프로토콜 | - DTLS 1.2/1.3 (TinyDTLS, WolfSSL)<br>- 4가지 보안 모드: NoSec/PreSharedKey/RawPublicKey/Certificate<br>- Block-wise Transfer(1024B 블록) + Observe 패턴(2048)<br>- OSCORE(객체 보안, RFC 8613) – 메시지 본문 단위 암호화 |
| **LwM2M 1.2 (OMA SpecWorks)** | 디바이스 관리 + 원격 펌웨어 업데이트 | - CoAP/DTLS 기반, Bootstrap 절차(BS 서버)<br>- 객체 모델: /3/0/9 (배터리), /3/0/16 (메모리), /5/0/3 (펌웨어)<br>- MASA(Mobile Application Soft-tile Auth) – 진본 검증 |
| **LoRaWAN 1.0.4 (LR-FHSS, RP2-1.0.3)** | LPWAN, NwkSKey·AppSKey·DevAddr 32-bit | - OTAA(Over-The-Air Activation): JoinEUI/AppKey/AppNonce<br>- DevNonce 16-bit 재사용 감지 -> MIC 차단<br>- Frame Counter 32-bit (uplink/downlink)로 리플레이 방지<br>- Adaptive Data Rate(ADR) + Duty Cycle(1%) 준수 |
| **NB-IoT / Cat-M1 (3GPP Rel-17)** | 이동통신망, LTE-M 1.4MHz / NB-IoT 200kHz | - USIM/eSIM (GSMA SGP.22 RSP)<br>- SUPI/SUCI 암호화 (ECIES-X25519, profile A/B)<br>- AKA 인증 + NAS 보안 (EPS-AKA, 5G-AKA')<br>- Non-IP Data Delivery (NIDD) – UDP/IP 헤더 제거 |
| **Zigbee 3.0 / Thread 1.3 / Matter 1.3** | 메쉬 홈·빌딩 자동화 | - Zigbee: APS layer `Install Code + Trust Center Link Key`<br>- Thread: 6LoWPAN + DTLS, CoAP 기반, Mesh Link Establishment<br>- Matter: 운영체제 agnostic, Fabric ID + CASE/PASE 인증, SPAKE2+ |
| **게이트웨이 NAC (802.1X)** | 단말 인증·인가, VLAN 분리 | - EAP-TLS / EAP-TTLS, RADIUS(FreeRADIUS 3.2)<br>- MACsec(802.1AE) – L2 암호화, AES-GCM-128<br>- MAB(MAC Authentication Bypass) 폴백 정책 |
| **Zero Trust Broker (ZTA)** | 정책 결정·강제(PDP/PEP) | - BeyondCorp, OpenZiti, Twingate, Cloudflare Tunnel<br>- SDP 게이트웨이, mTLS device posture check<br>- 마이크로세그멘테이션: eBPF 기반 Cilium 1.15 |

### 무선 스펙트럼 보안 점검 항목

```text
[무선 구간 위협 시나리오 흐름도 - 7단계 공격 체인]

  ① 재밍(Jamming)          ->  채널 스캔: HackRF One + gr-rds / SDRangel
  |  +- 1.1.4GHz / 2.4GHz / 868MHz / 920MHz
  v
  ② 도청(Eavesdropping)     ->  Wireshark + 802.11 모니터 모드
  |  +- WPA3-Personal SAE / WPA3-Enterprise 192-bit Suite-B
  v
  ③ 스푸핑(Spoofing)        ->  ARP spoof, DNS spoof, MAC clone
  |  +- 802.1X + MAB 포트 시큐리티
  v
  ④ 리플레이(Replay)        ->  LoRaWAN Frame Counter / Zigbee NWK Key
  |  +- NTP 시간 동기화(NTS) + 단조 시계
  v
  ⑤ MITM(중간자)            ->  mTLS + Certificate Pinning (HPKP 대체)
  |  +- OCSP Stapling, CRL 검증
  v
  ⑥ 디바이스 탈취            ->  Secure Boot 실패 시 Brick
  |  +- 디버그 포트(JTAG/SWD/UART) 폐쇄
  v
  ⑦ 데이터 변조              ->  디지털 서명 (Ed25519 / ECDSA P-256)
     +- 블록체인 앵커링 (옵션)
```

### 암호 스위트 & 키 관리 결정 매트릭스

| 디바이스 클래스 | RAM/Flash | 권장 암호 스위트 | 키 저장소 | 인증서 주기 |
|:---|:---|:---|:---|:---|
| Class 0 (C0, < 50KB) | < 32KB / < 256KB | PSK (AES-128-CCM) | TrustZone, eFuse | 5~10년 |
| Class 1 (C1) | ~64KB / 256~512KB | DTLS 1.2 + ECC P-256 | OPTIGA Trust M, ATECC608B | 3~5년 |
| Class 2 (C2) | ~256KB+ / 1MB+ | TLS 1.3 + X.509 ECDSA | TPM 2.0, SE050C | 1~3년 |
| 게이트웨이 | 512MB+ | TLS 1.3 + RSA-4096 / Ed25519 | HSM(옵션), TPM | 90일~1년 |
| 서버/클라우드 | 무제한 | TLS 1.3 + PQC (Kyber-1024) | HSM(YubiHSM2, AWS CloudHSM) | 90일 자동 갱신 |

- **📢 섹션 요약 비유**: IoT 연결성 보안 감리는 “국제공항의 7중 보안검색”과 같다. 위층부터 터미널 검색(애플리케이션), 출국장(클라우드), 환승 구간(게이트웨이), 탑승구(디바이스), 활주로(무선)까지 한 곳도
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 496 / 600

<- **이전**: [495. 서버리스 감리 이벤트 드리븐 분석](/studynote/11_design_supervision/06_exam_summary/496_serverless_audit_event_driven_analysis/)
**다음**: [497. 블록체인 감리 스마트 계약 검증](/studynote/11_design_supervision/06_exam_summary/497_blockchain_audit_smart_contract_verifica/) ->

---
