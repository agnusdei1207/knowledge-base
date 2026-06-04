+++
title = "596. 위성 인터넷 LEO 저궤도 통신 (Satellite Internet LEO Low Earth Orbit)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LEO(저궤도, 500–1,200km) 위성 군집(Constellation)을 Phased Array 안테나, ISL(Inter-Satellite Link) 레이저 광통신, Doppler·Handover 보상 알고리즘으로 운영하여 GEO 대비 왕복 지연(RTT)을 600ms -> 20~50ms 수준으로 단축하는 차세대 광대역 접속망(Broadband Access) 기술.
> 2. **가치**: 글로벌 커버리지(해상·극지·재난 지역 포함) 확보, 3GPP NTN(Non-Terrestrial Network) Rel-17/18 표준 기반 5G NR 위성 직접통신, Starlink 기준 다운로드 100–200Mbps·Upload 10–20Mbps·지연 25ms 실측, OneWeb·Project Kuiper·한Sat·CAS500 등 다국적 군집 경쟁으로 LEO 단가·용량 지속 하락.
> 3. **판단 포인트**: Handover 빈도(수십 초~수 분)·도플러 편이(±48kHz @Ku-band)·Fade Margin 설계·게이트웨이 분산 배치 vs ISL Mesh 토폴로지·위성 수명(5~7년) 대비 Kessler Syndrome 우주 쓰레기 위험·주파수 간섭(GSO 보호) 규제 준수 여부·보안(재밍·스푸핑·Quantum)·사업자 생태계 선택.

---

## Ⅰ. 개요 및 필요성

기존 위성 인터넷은 정지궤도(GEO, 35,786km) 위성을 이용해 왔으나, 한 홉(Hop) 왕복 지연이 약 600ms에 달해 VoIP·게임·실시간 금융 트레이딩과 같은 지연민감(Delay-sensitive) 서비스에 부적합했다. 또한 고도 36,000km에 따른 자유공간 경로손실(FSPL, Free Space Path Loss)이 약 210dB(@Ka-band)로 커서 단말 안테나口径이 0.6–1.2m 이상 필요했고, 단일 위성 점유 시간(Visibility window)이 길어 슬롯(Slot)·주파수 자원이 희소했다.

반면 5G·메타버스·자율주행·IoT Massive Connectivity 시대에는 "어디서나(universal coverage)" "1Gbps급" "50ms 이하"의 트래픽 요구가 등장했다. 이를 충족하기 위해 2019년 SpaceX Starlink를 시작으로 Amazon Project Kuiper(2027~ 양산), OneWeb(현 Eutelsat-OneWeb, Gen-2 위성 도입), 중국 Guowang(國網)·Qianfan(千帆), 한국의 한Sat·L3SAT·CAS500-2/3 통신탑재체 등이 LEO 군집을 구축 중이다. LEO는 고도가 1/30~1/60 수준이므로 **FSPL이 약 30–35dB 낮고, 왕복 지연은 20–50ms로 약 1/20** 수준이 되며, 위성 자체가 빠르게 이동하므로 **셀(Cell)을 좁고 빔(Beam)을 빠르게 재지향**하여 주파수 재사용 효율을 극대화할 수 있다.

다만 단점도 명확하다. 단일 위성이 지상 점유 시간이 5~10분(Starlink 기준 53° inclination 550km에서 패스 시간 ~4분)에 불과해 빈번한 Handover가 발생하고, 위성 속도 7.5km/s에 따른 도플러 편이(S-band 기준 ±48kHz), 대기항력(Atmospheric Drag)에 의한 궤도 붕괴, 우주 쓰레기·Kessler Syndrome, ITU Radio Regulations 상 GSO 보호(EPFD 한도) 등 신기술·신규제 이슈가 동반된다.

```text
[전통 GEO 위성 인터넷]
   사용자 단말 --► GEO(36,000km) --► 게이트웨이 --► 인터넷 백본
                 <--------- RTT ~600ms --------►
                 안테나 Ø0.6~1.2m, Ku/Ka-band
                 슬롯·주파수 자원이 희소

[차세대 LEO 위성 인터넷 군집]
                  +---+  +---+  +---+
                  |S1 |--|S2 |--|S3 |   (ISL Laser 200Gbps)
                  +-+-+  +-+-+  +-+-+
                     ╲      |      ╱
                      ╲     |     ╱   빔 스티어링(Beam Steering)
                       ╲    |    ╱
                  +---+  +--╧-+  +---+
                  |S4 |--|S5 |--|S6 |
                  +-+-+  +-+-+  +-+-+
                     |      |      |
  +------+    Ku/Ka/V-band    |      |    +----------+
  |  UE  |◄---- 빔 ◄----------+------+----| Gateway  |◄--► IXP/IX
  +------+    (전자식 Phased Array)        +----------+
   RTT 20~50ms
   안테나 Ø0.48m (Starlink Dishy McFlatface)
   Handover 수십 초~수 분 단위
```

추가로, 3GPP는 Rel-17(2022)에서 NTN(Non-Terrestrial Network)을 5G NR 표준에 정식 포함시켰고, Rel-18(2024)에서는 NR-NTN 진화(Evolution) 단계에서 핸드오버·Doppler 사전보상·타이밍 관계(Timing Relation)·HARQ 피드백 지연 대응 등을 규격화했다. 이는 "위성=통신 독립 망"이 아니라 "5G/6G 코어 네트워크의 일종 액세스"로 통합되는 패러다임 전환을 의미한다.

- **📢 섹션 요약 비유**: GEO는 "하늘의 정지 위성"에 의존해 먼 거리를 한 번에 가로지르는 '고속버스'이고, LEO 군집은 "도시 위를 빽빽히 도는 셔틀 여러 대"가 끊임없이接力(릴레이)하면서 짐을 빨리 배달하는 '셔틀 시스템'이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

LEO 위성 인터넷 시스템은 크게 **우주 구간(Space Segment)**, **지상 구간(Ground Segment)**, **제어 구간(Control Segment)**, **단말(User Segment)**의 4 계층으로 구성된다. 핵심 메커니즘은 (1) **빔 스티어링 + 셀 재구성**, (2) **위성 간 광통신(ISL) Mesh**, (3) **게이트웨이/단말 핸드오버**, (4) **Doppler·Timing 사전 보상**의 4축으로 동작한다.

```text
+---------------- Space Segment (LEO Constellation) ----------------+
|  +------+        +------+        +------+        +------+        |
|  |Sat A |-ISL-L-►|Sat B |-ISL-L-►|Sat C |-ISL-L-►|Sat D |  (Laser|
|  | 550km|◄-ISL-L-| 550km|◄-ISL-L-| 550km|◄-ISL-L-| 550km|  100G+) |
|  +--+---+        +--+---+        +--+---+        +--+---+        |
|     |  Ka-Band      |  Ka-Band      |  Ka-Band      |            |
|     |  Downlink     |  Uplink       |  Feeder       |            |
+-----+---------------+---------------+---------------+-------------+
      |               |               |               |
      v               v               v               v
+---------------- Ground Segment (Gateways) -------------------------+
|  +----------+    +----------+    +----------+                       |
|  |GW-Seoul |◄--►|IXP/KIXP  |◄--►|Internet  |   GW-1Gbps~10Gbps    |
|  | Ka feeder|    |          |    | Backbone |   PoP 분산 배치       |
|  +----------+    +----------+    +----------+   (10~30km 간격 권장) |
+----------------------------------------------------------------------+
      ^
      |  Ku-band  (User Link, 12–18GHz)
      |  Ka-band  (User Link, 26.5–40GHz)
      |  V-band   (Starlink Gen2, 37.5–43.5GHz feeder)
+---------------- User Segment (UE/UT) ------------------------------+
|  +----------------------+     +--------------------------+         |
|  | Flat Panel Phased    | ◄-► | Starlink Gen3 / Kuiper  |         |
|  | Array Antenna        |     | Terminal / OneWeb UT     |         |
|  | (GaN MMIC, 1,000+    |     | 100–200Mbps DL           |         |
|  |  elements)           |     | 10–20Mbps UL             |         |
|  +----------------------+     +--------------------------+         |
+---------------------------------------------------------------------+
       ^
       | Tracking/Telemetry/Command (TTC, S-band 2GHz)
+---------------- Control Segment -----------------------------------+
|  MOC(위성관제), TOC(궤도결정), SOC(스케줄링), Anti-jamming SOC     |
|  궤도역학(TLE/SGP4) + 위성 자세제어(Reaction Wheel, Hall Thruster)  |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **LEO 위성(버스)** | 궤도 유지, 자세제어, 전력공급 | 3축 안정화, Solar Array ~25kW(Starlink v2 mini), Hall-effect Thruster(Xenon) 궤도 유지·de-orbit, 위성 수명 5~7년, Mass 260–800kg |
| **탑재 통신체(Comm. Payload)** | 다중빔(Multi-beam) 형성, 주파수 변환, ISL | Ka/Ku/V-band 능동 위상배열(Active Phased Array), 빔 폭 1° 이하(셀 Ø10–50km), ISL Laser 1550nm 100–200Gbps, Digital Channelizer(DSP 빔 형성) |
| **단말(User Terminal)** | 사용자 트래픽 송수신, 빔 자동 추적 | GaN MMIC 기반 평면형 위상배열(Starlink Dishy 0.48m, Kuiper µUT 0.2m), <1° 정확도 추적, 소비전력 50–100W, PoE 공급 |
| **게이트웨이(Gateway/Earth Station)** | 위성↔인터넷 백본 인터페이스, 망 등록·인증 | Ka-band feeder, 5–10m 안테나 다수, 1–10Gbps 백홀, IXP·PoP와 직접 Peering, 양자키분배(QKD) 시험 적용(Korea·EU) |
| **제어·관제(MOC/TTC)** | 궤도·자세·자원·Handover 관리 | TLE·GPS·Star Tracker로 ±10m 위치결정, NSCC·NTN 자원할당, QPSK/8PSK/16APSK/64APSK 적응변조, Doppler 사전보상 0.5ppm 이내 |
| **ISL(위성 간 링크)** | 위성–위성 직접 라우팅, 글로벌 Mesh | 1550nm laser / 1064nm·Free-Space Optical(FSO), 100Gbps+, Optical Head + Acquisition·Tracking·Pointing(ATP) 정렬 <1μrad |
| **NTN 코어 인터페이스** | 5G/6G 코어 연동, IP 라우팅 | 3GPP NTN Rel-17/18, Transparent vs Regenerative Payload, IPSec/MACsec, L3 Satellite Router, SDN/NFV 기반 자원 제어 |
| **스펙트럼·규제 모듈** | 주파수 등록·보호, GSO 공존 | ITU RR Article 22 EPFD 한도, FCC Part 25, 한국 전파법, Ku/Ka 우선, NGSO 간 간섭 조정 |

### 1) 궤도·링크 설계
LEO 고도 h는 **자유공간 경로손실** $L_{fs} = 20\log_{10}(d) + 20\log_{10}(f) + 32.45$ (dB, d[km], f[MHz])로 표현되며, 550km Ku(14GHz)에서 약 163dB, Ka(30GHz)에서 170dB 수준이다. GEO Ka는 210dB 이상이므로 LEO는 30~40dB 링크 이득 여유가 있다. 이를 활용해 **소형 평면형 위상배열 단말**이 가능해진다. 단, elevation angle이 25° 이하로 떨어지면 대기 감쇄·잡음온도 증가로 capacity가 급감하므로, constellation 설계 시 **최소 elevation 25~40°**를 전제로 커버리지를 산정한다.

### 2) 핸드오버(Handover)
LEO 위성 1기의 가시 시간(Visibility)은 평균 4~10분이다. 따라서 다음 두 종류의 핸드오버가 빈번히 발생한다.
- **Intra-satellite handover**: 한 위성이 다중 빔(Multi-beam)을 운용할 때, 단말이 빔 간 경계를 넘어 이동하며 발생(수십 초 단위).
- **Inter-satellite handover**: 위성 1기의 가시 영역을 벗어나 인접 위성으로 인계(수 분 단위).
3GPP NTN Rel-17은 **Conditional Handover(CHO)**, **Dual-Active Protocol Stack(DAPS)**로 **Handover interruption time < 50ms** 목표를 정의한다. 실제 Starlink 측정에서 handover 발생 시 0.5~3초의 throughput dip이 관측된다.

### 3) Doppler·Timing 보상
위성 속도 v ≈ 7.5km/s, 주파수 f_c에서 도플러 편이 $\Delta f = \frac{v}{c} f_c$. Ku-band 14GHz 기준 ±350kHz, Ka 30GHz ±750kHz까지 발생한다. 5G NR NTN에서는 **Pre-compensation offset**을 UE가 기지국(위성)에 보고하고, gNB 측에서 **Timing Advance(TA)**와 **Frequency Pre-correction**을 수행한다. LEO의 시간에 따라 변하는 TA는 1m/s ≈ 3.3ns/s 수준으로, PRACH 접근 시 latency window를 충분히 길게
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 596 / 800

<- **이전**: [595. 6G 비전 테라헤르츠 지능형 네트워크](/knowledge-base/studynote/06_ict_convergence/uncategorized/595_6g_vision_terahertz_intelligent_network/)
**다음**: [597. 양자 통신 양자 키 분배 QKD](/knowledge-base/studynote/06_ict_convergence/uncategorized/597_quantum_communication_quantum_key_distributio/) ->

---
