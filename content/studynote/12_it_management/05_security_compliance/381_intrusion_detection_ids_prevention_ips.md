+++
title = "381. 침입 탐지 IDS 침입 방지 IPS 비교 (Intrusion Detection IDS Prevention IPS)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IDS(Intrusion Detection System)는 패킷을 복제(Span/Tap)하여 **탐지(Detection)** 후 경보만 발령하는 Out-of-band 패시브 시스템이며, IPS(Intrusion Prevention System)는 인라인(Inline) 구간에서 페이로드를 **능동 차단(Prevention)**하는 인-라인 액티브 시스템으로, 양자 모두 시그니처(Signature), 이상행위(Anomaly), 상태기반 프로토콜 분석(Stateful Protocol Analysis), 행동 분석(Behavioral) 4대 탐지 엔진을 Snort/Suricata 룰셋, YARA, Zeek 스크립트 등으로 구현한다.
> 2. **가치**: NSS Labs 벤치마크 기준 Inline IPS 적용 시 평균 95.4% 탐지율·0.4% False Positive·50μs 이하 레이턴시 달성이 가능하며, KISA 침해사고 통계상 IDS+IPS+SIEM 3계층 배포 환경에서 MTTD(평균탐지시간) 18.7배, MTTR(평균복구시간) 4.3배 단축이 보고되어 침해사고 피해액을 약 78% 절감한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **(1) 가용성 vs 보안성(Fail-Open/Fail-Closed 정책)**, **(2) 인라인 처리 지연 vs 트래픽 처리량(Throughput: 1G/10G/40G/100G)**, **(3) 시그니처 매칭 속도 vs 암호화 트래픽 가시성(TLS 1.3 가로채기 vs Encrypted Traffic Analysis)**, **(4) 탐지 정확도 vs 운영 오버헤드(룰 튜닝·화이트리스트 관리)** 의 4축이며, 기술사는 조직의 RTO/RPO, CDE(카드데이터환경) 위치, 망 분리(Zone) 정책, 그리고 컴플라이언스(PCI-DSS 11.4, ISMS-P, GDPR Art.32) 요건에 따라 IDS 단독, IPS 단독, 또는 SIEM/SOAR/XDR과 통합한 하이브리드 배치로 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 경계 보안(Perimeter Security)의 핵심이었던 방화벽(Firewall)은 OSI 3·4계층의 IP/Port/Protocol 기반의 **상태추적(Stateful Inspection)**과 L7 애플리케이션 제어(Next-Gen Firewall)로 진화했음에도 불구하고, 시그니처 기반의 알려진 익스플로잇 외에 **제로데이 취약점, 랜섬웨어 C2 통신, 내부자 위협(Insider Threat), 횡적 이동(Lateral Movement), SQLi/XSS/SSRF/RCE 같은 애플리케이션 계층 공격**을 차단하는 데 명백한 한계를 보인다. 2024년 Verizon DBIR(Verizon Data Breach Investigations Report) 기준 웹 애플리케이션 공격이 전체 침해사고의 26.8%, 시스템 침투 19.2%, 사회공학적 약점을 악용한 C2 통신 68.1%가 보고되며, MITRE ATT&CK T1059(명령 및 스크립트 인터프리터), T1486(데이터 암호화), T1027(난독화 파일) 같은 Advanced Persistent Threat(APT) 행위는 1차 방어선을 우회한 후 탐지될 수밖에 없는 특성 때문에 **"탐지(Detect) + 대응(Respond) + 회복(Recover)"** 중심의 2차·3차 방어선이 필수적으로 요구된다.

이러한 패러다임 전환을 주도하는 것이 **IDS(Intrusion Detection System)**와 **IPS(Intrusion Prevention System)**이며, 단순히 두 시스템의 차이를 나열하는 것을 넘어 **"어디에(Inline/Tap), 어떤 방식으로(Signature/Anomaly/Stateful/Behavioral), 어떤 트래픽에(North-South/East-West), 어떤 통합(SIEM/SOAR/XDR) 맥락에서 배치할 것인가"**가 기술사 시험의 핵심 평가 포인트다. 1998년 Marty Roesch의 Snort 1.0 출시 이후 룰 기반 탐지, 2000년대 후반 Anomaly Detection(베이지안 네트워크, HMM), 2010년대 Suricata의 멀티스레딩 NFQ(NFTables) 모드, 2018년 이후 EDR/XDR/MDR/NDR로 확장되는 등 IDS/IPS는 30여 년간 단독 제품에서 **XDR 플랫폼의 한 계층**으로 그 위상이 재정의되고 있다.

```text
+------------------------------------------------------------------+
|          1990s                2010s                2020s~         |
|  +-------------+        +--------------+     +----------------+  |
|  | Firewall(L3) |---->--|IDS(NIDS)단독 |----> |SIEM+SOAR+XDR  |  |
|  | + IDS(이중)  |        |+ IPS(인라인) |     | + NDR(EDA)     |  |
|  +-------------+        +--------------+     +----------------+  |
|      Stateful            Snort/Suricata/      Cloud-native ML    |
|     Inspection             Bro/Zeek            + UEBA + 자동대응  |
|                                                                  |
|  진화 키워드: 1세대 Rule-> 2세대 Anomaly-> 3세대 Behavioral-> 4세대 AI  |
+------------------------------------------------------------------+
```

**구세대(레거시) IDS**: Snort 2.x 단독, 시그니처 한 줄(alert tcp any any -> any 80 msg:"WEB-IIS";) 단위 룰, 일 50만 이벤트 -> 분석가 수작업, 탐지 후 알람만 -> 후속조치 인적 개입
**신세대 NDR/XDR**: Suricata + Zeek + Random Forest + LSTM + Threat Intel(STIX/TAXII) + SOAR 자동 차단, UEBA(User Entity Behavior Analytics) 기반 행위 베이스라인 -> Egress Traffic Baseline, **Encrypted Traffic Analysis(ETA)**로 TLS 1.3 메타데이터(Certificate, JA3/JA3S, Cipher Suites)까지 분석

- **📢 섹션 요약 비유**: IDS는 **CCTV 녹화 기능**과 같다(녹화는 하지만 도둑을 즉시 멈추지는 못함), IPS는 **자동 잠금 장치가 달린 강화 유리문**과 같다(도둑이 깨려고 하면 즉시 잠겨버림). 그러나 강화 유리문은 견딜 수 있는 충격(처리량)과, 평소 문을 두드리는 손님(정상 트래픽)을 가려내는 정밀함(탐지 정확도)이 반드시 뒷받침되어야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IDS/IPS는 **센서(Sensor) -> 분석 엔진(Analysis Engine) -> 저장소(Storage) -> 응답 모듈(Response Module) -> 관리 콘솔(Management Console)**의 5계층으로 구성되며, 각 계층은 데이터 플레인(Data Plane)과 컨트롤 플레인(Control Plane)으로 분리된다. 센서는 NIC(Network Interface Card) 단에서 **libpcap/Cilium/eBPF/XDP**를 통해 패킷 캡처를 수행하며, 인라인(Inline) 모드 IPS의 경우 **Bypass 스위치(Fail-Open Copper/Fiber Bypass, Gigamon Bypass, NetOptics)**가 필수 동반 장비로, 자체 전원/하드웨어 장애 시 **Fail-Open(트래픽 통과) 또는 Fail-Closed(트래픽 차단)** 정책을 정의한다. 분석 엔진은 패킷 디코딩(802.1Q VLAN, MPLS, GRE, VXLAN 터널 캡슐화 해제), TCP 재조립(TCP Reassembly: 64KB 윈도우, 8KB 디폴트 버퍼), IP 단편화(Fragmentation: 8바이트 단위, Teardrop 공격 방어), HTTP 정규화(HTTP Normalization: %uXXXX 인코딩, UTF-8 multi-byte 인코딩), 그리고 프로토콜 디코더(Decoder: HTTP, DNS, SMTP, SMB, TLS 1.2/1.3 핸드셰이크) 단계를 거친다.

탐지 엔진은 크게 4가지 방식이 결합(Ensemble)되어 동작한다. (1) **시그니처 기반(Signature/Pattern Matching)**: Aho-Corasick 멀티패턴 매칭 알고리즘으로 한 번에 수천 개 룰을 O(n+m) 시간 복잡도로 매칭하며, Snort 룰 포맷(Action Proto Src_IP Src_Port Direction Dst_IP Dst_Port (옵션: msg, content, pcre, classtype, sid, rev, reference:cve))을 따른다. (2) **이상행위 탐지(Anomaly Detection)**: 통계 기반(Statistical: 평균, 분산, 카이제곱 거리), 클러스터링(K-means, DBSCAN), 분류(Decision Tree, Random Forest, XGBoost, Isolation Forest), 딥러닝(LSTM, AutoEncoder, GAN) — Suricata 7.0+의 `app-layer-event`, Zeek의 `analyzer` 프레임워크. (3) **상태기반 프로토콜 분석(Stateful Protocol Analysis)**: RFC 793(TCP), RFC 1035(DNS), RFC 2616(HTTP/1.1) 등의 명세를 모델링하여 정상 상태 머신(FSM)에서 벗어나는 비정상 전이(ColdStart, Half-Open, Evasion: TTL/Window Size 조작) 탐지. (4) **행위/위협 인텔리전스 기반(Behavior & TI)**: MITRE ATT&CK TTP(Tactics, Techniques, Procedures) 매핑, STIX 2.1/TAXII 2.1 피드 수신, JA3/JA3S TLS 핑거프린트, p0f OS 핑거프린트, RITA(Rye Imp Threat Analyst) beaconing 탐지.

```text
                          IDS/IPS 처리 파이프라인 (Inline + Tap Hybrid)
+--------+  +--------+  +-------------+  +-------------+  +---------+
| 패킷  |  | NIC    |  | Pre-        |  |  Detection  |  |Response |
| 캡처  |-->| Promisc|-->| processor   |-->|  Engine     |-->| Module  |
|(Copper/|  | Mode   |  | • TCP Reasm |  | • Signature |  | • Reset |
| Fiber  |  | AF_PKT |  | • IP Defrag |  | • Anomaly   |  | • Drop  |
|  Tap)  |  |  + DPDK|  | • HTTP Norm |  | • Stateful  |  | • Block |
+--------+  +--------+  | • TLS Decry |  | • Behavior  |  | • Alert |
                       +-------------+  |   (UEBA/TI) |  +---------+
                                       +------+------+
                                              | IOCs, Events
                                              v
                              +----------------------------+
                              |  Storage & Integration     |
                              |  • Unified2/JSON logs      |
                              |  • Elasticsearch (ELK)     |
                              |  • SIEM (Splunk/QRadar)    |
                              |  • SOAR (Cortex XSOAR)     |
                              |  • XDR (CrowdStrike/SentinelOne)|
                              +----------------------------+
                              ^                            ^
                              |                            |
                       +------------+              +--------------+
                       | Management |              | Bypass Switch|
                       |  Console   |              |  (Fail-Open) |
                       |  (GUI/API) |              |              |
                       +------------+              +--------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Packet Capture (NIC/Tap)** | 인라인(Bump-in-the-wire) 또는 미러링(SPAN/Tap)으로 트래픽 획득 | Intel X520/X710 10G/25G NIC, Napatech NT200A02, Silicom PE310G4i71L Bypass, **DPDK(Data Plane Development Kit) 22.11+**로 제로카피(Zero-Copy) 처리, **AF_XDP(eXpress Data Path)**로 커널 바이패스 |
| **Pre-processor** | 페이로드 정규화·조립·프로토콜 디코딩 | Snort/Suricata `app-layer-parser` 모듈, HTTP URI %-디코딩, IPv4/v6 듀얼스택, DNS-over-HTTPS(DoH, RFC 8484) 메타 추출, **SMBv1/SMBv3 멀티채널다이얼렉트 핸들링** |
| **Detection Engine** | 4대 탐지 로직 실행 | Snort 3.1.65.0(2024 LTS) `ips_action` / `so_proxy` / `event_filter`; Suricata 7.0.5 `threading.detect-thread-ratio` 자동 튜닝; **Hyperscan 5.4.1** SIMD 가속 정규식 매칭, **PF_RING ZC(Zero Copy)** 100Gbps 처리 |
| **Response Module** | 탐지 결과에 따라 액션 수행 | `reject` (TCP RST 송신), `drop` (Silent Drop, TCB 유지), `sdrop` (로그 미생성 Drop), `rejectboth` (양방향 RST+FYN), IPS Inline 시 **`queue` (NFQUEUE) bypass**, `tag`/`react`(클라이언트 차단 페이지 주입) |
| **Storage & Analytics** | 이벤트 저장·상관분석·대응 자동화 | Snort **`u2`** 바이너리 포맷 -> Barnyard2 -> MySQL; **Suricata **`eve.json`****(150+ 필드: flow, alert, http, dns, tls, files, stats) -> Filebeat/Logstash -> ES -> Kibana; Wazuh 4.7 OSSIM, **TIGER Stack(Telegraf+InfluxDB+Grafana)** |
| **Management Console** | 룰 배포·정책 관리·리포팅 | Sourcefire Defense Center(현 Cisco Firepower FMC 7.4), **Snorby**, **Suricata-Update**, **SELKS 7.0**, **EVEBOX**, **Aanval** |

**심화 파라미터**: Snort 3 `latency:{ tolerance: 200, action: alert }`로 패킷 처리 레이턴시 200ms 초과 시 자동 알람, Suricata `stream.reassembly.depth: 1mb`, `stream.midstream: true`로 미드스트림 세션 처리, `defrag.memcap: 512mb`, `flow.memcap: 1gb`. 룰 튜닝에서 `threshold:type both, track by_src, count 5, seconds 60` 형태로 false positive 억제. CVE-2022-22965(Spring4Shell) 대응 룰의 경우 PCRE 기반 `/class\.module\.classLoader\.\*DefaultResourceLoader.*class\.module\.classLoader/Ui` 패턴이 1ms 이내 매칭되어야 한다.

- **📢 섹션 요약 비유**: IDS/IPS의 처리 파이프라인은 **공항 보안 검색대**와 같다. 위층(NIC)에서 승객(패킷)이 도착하면 검색 요원(Pre-processor)이 가방을 열고(HTTP Normalization) 액체류를 분리(TCP Reassembly)한 뒤, 4가지 탐지 요원(시그니처·이상행위·상태기반·위협인텔)이 1) 금속탐지기(Signature) 2) 행동관찰 CCTV(Anomaly) 3) 여권 진위확인(Stateful) 4) 수배자 명단 대조(TI)를 동시에 수행한다. 통과하면(Allow), 위험 판정 시에는 위층(Bypass)으로 보내거나(IDS), 즉시 출국금지(Drop, IPS) 조치한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **IDS (NIDS/HIDS)** | **IPS (NIPS/HIPS)** |
|:---|:---|:---|
| **배치 모드** | Out-of-band (SPAN Port, Optical TAP, ERSPAN) | In-line (Bump-in-the-wire, Transparent Bridge, NFQUEUE) |
| **동작 방식** | 패시브(Passive): 패킷 복제만, **원본 트래픽 변경 금지** | 액티브(Active): TCP RST 송신, 패
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 381 / 800

<- **이전**: [380. 전자서명 디지털 서명 비부인 무결성](/knowledge-base/studynote/12_it_management/05_security_compliance/380_digital_signature_non_repudiation_integrity/)
**다음**: [382. 방화벽 차세대 NGFW 웹 방화벽 WAF](/knowledge-base/studynote/12_it_management/05_security_compliance/382_firewall_ngfw_web_application_firewall_waf/) ->

---
