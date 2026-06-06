---
title: "Edge Computing MEC Distributed Processing IoT"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드-중심 컴퓨팅을 무선 기지국(DU/CU), MEC 호스트, 게이트웨이 측으로 분산 배치하여, 3GPP TS 23.558의 AF( Application Function)와 ETSI MEC ISG 표준 기반의 1ms 이하 Ultra-Low Latency ULL 서비스를 구현하는 **5G-Edge Native** 아키텍처이다.
> 2. **가치**: V2X(20ms 이하), 원격 수술·산업용 HMI(≤10ms), 모바일 AR/VR(≤20ms), 비전 검사(≤50ms) 등 결정적 지연시간(latency-critical) 워크로드를 가능케 하며, 5G UPF의 Uplink Classifier / Branching Point / Local Breakout 을 통해 백홀 트래픽을 **60~90%** 절감한다.
> 3. **판단 포인트**: "Where to compute(어디서 연산할 것인가)"의 결정—단말(On-Device AI) ↔ On-Premise Edge ↔ MEC(5G RAN) ↔ Region Cloud ↔ Hyperscale Cloud—을 데이터 주권, 지연시간, 비용(TCO), 상태 유지(Stateful/Stateless), 동기·비동기 비율, **5G 네트워크 슬라이스(URLLC/eMBB/mMTC)** 매핑 기준으로 트레이드오프 한다.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅은 **집중화된 자원 풀**을 통한 경제성과 확장성을 제공했지만, 4G LTE 시대의 모바일 트래픽 폭증, IoT 디바이스의 **N x 100B(Billion)** 스케일, 그리고 5G URLLC·XR·자율주행 등 **latency-bound** 워크로드 등장으로 **물리적 한계**가 노출되었다. 일반적인 클라우드 RTT는 30~80ms이며, 이는 인간의 반응시간(150~300ms)에는 충분하지만, 산업용 협동로봇(≤1ms), V2X CAM 메시지(≤20ms), 클라우드 게임(≤10ms), Haptic Feedback(≤5ms)에는 부적합하다. 또한 영상·LiDAR·센서 데이터의 폭증으로 인해 **백홀/코어 네트워크 대역폭 비용**이 기하급수적으로 증가하면서, **데이터를 발생地点에서 처리**하는 패러다임 전환이 요구되었다.

ETSI(European Telecommunications Standards Institute)는 2014년 Mobile Edge Computing을, 2017년 5G·Wi-Fi·고정 액세스를 모두 포괄하는 **Multi-access Edge Computing(MEC)**으로 명칭을 변경하고, ISG(Industry Specification Group)를 통해 참조 아키텍처(ETSI GS MEC 003), 프레임워크(GS MEC 010), API(GS MEC 011~029) 표준을 제정했다. 3GPP는 **TS 23.558(Architecture for enabling Edge Applications)**, **TS 23.501/23.502(System Architecture for 5G System)**에서 Edge Application Server(EAS), Edge Enabler Server(EES), UPF의 Traffic Steering 규칙(TSC/URR)을 정의하여 MEC가 **5G 코어 네이티브**로 동작하도록 통합했다.

```text
[클라우드-중심 모델 vs 엣지-중심 모델]

   (기존) 중앙 집중형                    (신) 엣지 분산형
   +----------+                          +------------------+
   | IoT Device|-센서데이터(100%)--►|   | IoT Device      |
   +----------+                          |  + 임베디드 AI --+|
        |                                 |     (TFLite/    ||
        | LTE/5G                          |      ONNX)      ||
        v                                 +------+----------+
   +----------+                                  | 전처리(10%)
   |  EPC/5GC |                                  v
   +----+-----+                          +------------------+
        |                                 | Edge Gateway     |
        v                                 | (K3s/KubeEdge)   |
   +----------+  지연 50ms+                 |  + 프로토콜 변환 |
   |  Cloud   |  비용 $$$                  |  + 로컬 캐시    |
   |(Hyperscale|                          |  + 스트림 분석  |
   |   DC)    |◄-전체 원본                 +------+----------+
   |  + 분석  |                                       | 요약/이벤트(1%)
   |  + AI    |                                       v
   |  + 저장  |                                  +----------+
   +----+-----+                                  | 5G UPF   |
        |                                         |Local Breakout
        v                                         v
   +----------+                              +----------+
   | User/Client|                              | MEC Host|
   +----------+                              | +AKSAWS  |
                                              | Greengrass|
                                              +----+-----+
                                                   | 정책/메타데이터
                                                   v
                                              +----------+
                                              | Region   |
                                              | Cloud    |
                                              +----------+
```

- **📢 섹션 요약 비유**: "택배 기사가 모든 화물을 중앙 물류센터로만 보내던 방식"에서 "**동네 허브(Edge Hub)**에서 1차 분류·처리하고, 전국 본부(Cloud)에는 핵심 화물만 보내는 방식"으로 전환한 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ETSI MEC 참조 아키텍처는 **3계층(Host Level / System Level / External Level)**으로 구성된다. 핵심 컴포넌트는 MEC Host(MEC Platform + MEC Apps + Virtualisation Infrastructure), MEC Orchestrator(MEO), Multi-access Orchestrator(MEAO), OSS/BSS, 그리고 User Equipment 측의 **MEC App + UE App**이다. 3GPP는 이를 5G 코어와 통합하면서 AF(Application Function) 기반의 **EES(Edge Enabler Server) ↔ EEC(Edge Enabler Client)** 구조로 매핑한다.

```text
[ETSI MEC + 3GPP 5G 통합 참조 아키텍처]

  +------------------------------------------------------------+
  |                  External Level (Level 3)                  |
  |  +----------+  +----------+  +----------+  +----------+    |
  |  | OSS/BSS  |  |  MEAO    |  |  MEO     |  |  CAP     |    |
  |  |(Operations|  |(Multi-   |  |(MEC      |  |(Charging|    |
  |  | Support) |  | access   |  | Orchestr.)|  |  System) |    |
  |  +----^-----+  +----^-----+  +----^-----+  +----------+    |
  |       | Mp1/Mp3   | Mm1       | Mm4/Mm5                    |
  +-------+-----------+-----------+----------------------------+
  |       |  System Level (Level 2: MEC Framework)              |
  |  +----+------------------------------+                     |
  |  |   MEC Platform Service           |  Mp2/Mm2             |
  |  |   - Traffic Rule Control          |                     |
  |  |   - DNS, Location, Bandwidth Mgr  |                     |
  |  |   - MEC Service Registry          |                     |
  |  +------------+---------------------+                     |
  +---------------+--------------------------------------------+
  |               |  Host Level (Level 1)                      |
  |  +------------v-----------------------------------------+  |
  |  |            MEC Host  (e.g. 기지국/Regional DC)         |  |
  |  |  +-----------------------------------------------+   |  |
  |  |  | Virtualisation Infrastructure (VM/K8s/K3s)   |   |  |
  |  |  |  +----------+  +----------+  +----------+    |   |  |
  |  |  |  | MEC App  |  | MEC App  |  | MEC App  |    |   |  |
  |  |  |  |  (V2X)   |  | (AR/VR)  |  |(Video   |    |   |  |
  |  |  |  |          |  |          |  | Analytics)|    |   |  |
  |  |  |  +----------+  +----------+  +----------+    |   |  |
  |  |  +-----------------------------------------------+   |  |
  |  +------------------------------------------------------+  |
  +------------------------------------------------------------+
        ^                          ^                  ^
        | N6 (Traffic)             | N33 (NEF/PCF)   | N6
   +----+----+               +-----+----+      +-----+----+
   | 5G UPF  |               |  PCF     |      | Data Net|
   | + AF    |               |  + EES   |      | (Internet/IMS)|
   +----+----+               +----------+      +----------+
        | N3
   +----+----+
   | (R)AN   | gNB-DU / CU
   +----+----+
        | Uu (Radio)
   +----+----+
   |   UE    | EEC + UE App
   +---------+
```

**3GPP TS 23.558의 Edge Application 키 플로우**는 다음과 같다:
1. UE가 EEC를 통해 EES에 **EDN(Edge Data Network) Discovery** 요청
2. EES가 DNS/Local Cache 또는 NRF 조회로 가장 가까운 EDN 식별
3. AF(예: MEC App)가 EES에 **App Context** 등록, EES가 UE에게 **Edge Application Server Info** 통지
4. SMF가 UPF에 **URR(Usage Reporting Rule)** + **TSC(Traffic Steering Control)** 설치 -> UPF가 **Local Breakout**으로 트래픽을 MEC 호스트로 라우팅
5. UE ↔ MEC App 간 **Direct Communication** 성립, 지연시간은 5~15ms 수준

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **UE / IoT Device** | 데이터 발생, EEC(Edge Enabler Client) 내장 | 임베디드 AI(TensorFlow Lite, ONNX Runtime, TVM), NPU(Neural Processing Unit: Apple ANE, Qualcomm Hexagon, Jetson Orin Nano), LwM2M·MQTT·CoAP 클라이언트, OPC UA Pub/Sub |
| **Edge Gateway / IoT Hub** | 프로토콜 변환, 로컬 스트림 처리, 펌웨어 OTA | K3s/KubeEdge/OpenYurt/KubeFed, eKuiper/Apache NiFi(스트림 처리), Node-RED(시각적 플로우), EMQX/Mosquitto(MQTT Broker), InfluxDB/TimescaleDB(시계열) |
| **MEC Host (ETSI)** | 5G RAN 측·Region DC 내 가상화 플랫폼 | OpenStack/VMware VIO/裸 Metal Kubernetes, DPDK/SR-IOV/CPU Pinning, DPDK-Accelerated vSwitch(OVS), GPU Pool(NVIDIA A30/L4), CNI: Multus+Cilium |
| **5G UPF + AF** | Traffic Steering, 정책 적용, 데이터 평면 분기 | Uplink Classifier / Branching Point / Local Breakout, N6 인터페이스, 5G LBO(Local Breakout), LADN(Local Area Data Network) |
| **MEC Orchestrator(MEO)** | MEC 앱 라이프사이클, 자원 할당, FM | MEC013(앱 패키징·라이프사이클), TOSCA/SAREF 온톨로지, GitOps(Argo CD/Flux) |
| **Cloud (Region/Hyperscale)** | 장기 보관, Heavy-Training, Cross-Region 분석 | 데이터 레이크(S3/HDFS), 분산 학습(Ray/DeepSpeed/FSDP), Feature Store, MLOps(MLflow/Kubeflow) |
| **Security Fabric** | Zero-Trust, mTLS, Attestation | SPIFFE/SPIRE 워크로드 ID, TPM 2.0 / SEV-SNP / TrustZone, WireGuard/NetBird 메시 VPN, OPA(Open Policy Agent), Vault 시크릿 관리 |

**핵심 알고리즘·파라미터**
- **Where-to-Compute Decision**: 입력 = (D: 데이터 크기, L_req: 요구 지연시간, C_edge: 엣지 가용자원, Cost_net: 네트워크 비용). 출력 = 데이터 처리 위치. 휴리스틱: `if (D > Threshold or L_req < 10ms) -> Edge / Device`.
- **Traffic Steering Rule(TSC)**: SMF가 PCF·AF로부터 N5/N33 API로 받음. 구조: `{(UE_IP, App_ID, QFI, Bitrate, Latency_Budget) -> Action(redirect/clone/buffer)}`.
- **KubeEdge의 EdgeMesh**: 클라우드-엣지 분리 시 Kube-API Server 단절에도 로컬 kubelet이 Pod를 계속 운영, MQTT/LibP2P 기반 동기화.
- **AI 모델 분할(Split Inference)**: `partition_point` 기준으로 CNN 초반부(Edge)와 후반부(Cloud)를 분할. 계산 부하·전송량 트레이드오프 최적화. **Bottleneck Layer**(파라미터 1MB, FLOPs 80%)를 분할점으로 선정하는 것이 일반적.
- **Coded Edge Computing**: [BGA18] Lyapunov Optimization 기반 1-bit ADC + Compute-and-Forward로 **Energy Efficiency 4~7×** 향상.

- **📢 섹션 요약 비유**: MEC는 "**공항의 출국장**"과 같다—여권심사·탑승수속(Edge), 최종 목적지 안내(Cloud), 그리고 **기내식·면세점은 지역 특화 서비스(MEC App)**로 승객이 기내에서 즉시 이용하는 구조.

---

## Ⅲ. 비교 및 연결

| 구분 | **Cloud Computing** | **Fog Computing (Cisco, 2012)** | **MEC (ETSI/3GPP)** | **On-Device Edge AI** |
| :--- | :--- | :--- | :--- | :--- |
| **컴퓨팅 위치** | Region/Hyperscale DC | 디바이스~Cloud 사이 계층, 주로 LAN/On-Prem | 5G RAN·기지국·Aggregation Point | 단말 칩셋·임베디드 MCU |
| **표준화** | 사실상 표준 없음(NIST 모델) | OpenFog Consortium(2015, IEEE로 이관)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 471 / 800

<- **이전**: [470. 클라우드 성능 최적화 레이턴시 처리량](/studynote/13_cloud_architecture/06_exam_summary/470_cloud_performance_optimization_latency_throug/)
**다음**: [472. 엣지 AI 추론 최적화 온디바이스](/studynote/13_cloud_architecture/06_exam_summary/472_edge_ai_inference_optimization_on_device/) ->

---
