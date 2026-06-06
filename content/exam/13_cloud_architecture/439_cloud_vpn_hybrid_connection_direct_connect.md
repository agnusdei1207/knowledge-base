---
title: "Cloud VPN Hybrid Connection Direct Connect"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 VPN과 Direct Connect는 공용 인터넷(Public Internet) 기반의 암호화 터널(SSL/IPsec)과 통신사업자 전용 회선(Private Peering/BGP)을 통해 On-Premise 데이터센터와 CSP(Cloud Service Provider) VPC/VNet을 L2/L3 레이어에서 결정론적으로 연결하는 하이브리드 네트워킹 패러다임으로, AWS DX, Azure ExpressRoute, GCP Dedicated Interconnect가 대표적 구현체이다.
> 2. **가치**: 일반 인터넷 대비 지연시간(Latency)을 20~40ms에서 5ms 이하로 단축하고, 대역폭을 예측 가능(Deterministic)하게 만들며, Jitter와 Packet Loss를 0.01% 미만 수준으로 안정화하여 실시간 트랜잭션, 대용량 데이터 마이그레이션, SAP/Oracle 워크로드의 SLA를 99.99% 이상으로 보장한다.
> 3. **판단 포인트**: 초기 비용(포트 비용 + 회선 비용 + 크로스 커넥트) ↔ TCO(Total Cost of Ownership), 암호화 보안성(IPsec/IKEv2) ↔ 성능 오버헤드(MTU/Encryption CPU), Active-Active 이중화 ↔ 운영 복잡도(BGP ASN/VRF 설계) 사이의 트레이드오프를 워크로드 특성(OLTP/배치/스트리밍)과 컴플라이언스 요건(데이터 레지던시/암호화)으로 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈의 디지털 전환(DX) 과정에서 사설 데이터센터에 머물던 트랜잭션·데이터베이스·레거시 시스템(AS400, Mainframe, SAP ECC 등)은 클라우드로의 점진적 이전이 필요해졌으나, 일시에 모든 워크로드를 클라우드로 Lift & Shift할 경우 발생하는 다운타임·리스크·비용을 감수하기 어렵다. 이에 따라 **하이브리드 클라우드(Hybrid Cloud)** 아키텍처가 표준으로 자리 잡았으며, 이의 근간이 되는 두 가지 핵심 연결 방식이 바로 **Site-to-Site VPN**과 **Direct Connect(전용 회선)** 이다.

기존의 "클라우드 = 인터넷을 통한 원격 접속"이라는 인식은 한계가 명확하다. 일반 인터넷은 Best-Effort 전달 모델로, SDN 가상화 오버헤드, ISP 간 Transit Path, 글로벌 라우팅 변동 등으로 인해 지연시간이 예측 불가능하며, 금융권(전자금융감독규정), 의료(HIPAA·개인정보보호법), 공공(클라우드 보안인증), 게임·실시간 서비스에서는 50ms 이상의 지터와 패킷 손실이 SLO(Service Level Objective)를 위반시킨다. 또한 공개된 IP 경로로 트래픽이 노출되므로 GDPR, PCI-DSS 등 규제 환경에서 데이터 평문(Plain Text) 노출 리스크가 존재한다.

이에 CSP들은 ① 7계층(Application) VPN 터널(예: Client VPN, WireGuard, OpenVPN Access Server) ② 3계층(IPsec/IKEv2) Site-to-Site VPN ③ L2/L1 전용 회선(Direct Connect/ExpressRoute/Interconnect) ④ SD-WAN Overlay(Cisco Viptela, Velocloud, Prisma) 등 4단계의 연결 옵션을 제공하며, 기술사 시험에서는 각 방식의 **토폴로지, BGP/ASN, MTU, 암호화 알고리즘, 장애 대비 이중화** 측면의 설계 판단을 묻는 문제가 빈출한다.

```text
[ 하이브리드 클라우드 연결 아키텍처 - 4-Tier Connectivity Model ]

                          +------------------------------------------+
                          |   CSP Region (예: AWS ap-northeast-2)    |
                          |  +------------------------------------+  |
                          |  |  VPC 10.0.0.0/16                   |  |
                          |  |  +---------+    +--------------+  |  |
                          |  |  | Private |    |  Public      |  |  |
                          |  |  | Subnet  |    |  Subnet      |  |  |
                          |  |  |(Web/App)|    |  (NAT/IGW)   |  |  |
                          |  |  +----+----+    +------+-------+  |  |
                          |  |       |                |          |  |
                          |  |  +----+----------------+------+   |  |
                          |  |  |  Virtual Private Gateway    |   |  |
                          |  |  |  (VGW) / Transit Gateway    |   |  |
                          |  |  +--+-------------------+------+   |  |
                          |  +-----+-------------------+----------+  |
                          +--------+-------------------+-------------+
                                   |                   |
        +--------------------------+                   +----------------------+
        | TIER 3: 전용 회선                                       | TIER 2: IPsec VPN
        | (Direct Connect)                                       | (Site-to-Site VPN)
+-------+----------+                                    +--------+--------------+
| AWS Direct       |                                    | Customer Gateway(CGW) |
| Connect Location |                                    | + VGW = IPsec Tunnel |
| (DX LoA,         |                                    | IKEv2 / AES-256-GCM  |
|  Cross-Connect)  |                                    | ESP Tunnel MTU=1437  |
+-------+----------+                                    +------------+----------+
        | 802.1Q VLAN                                              | UDP/500, UDP/4500
        | BGP (Public/Private VIF)                                 | ESP(AH/ESP)
+-------+----------+                                    +------------+----------+
| On-Premise DC    |◄---------- Active/Active --------►| On-Premise DC         |
| BGP ASN 65000    |                                    | Firewall / VPN Router |
| CPE (CSR 1000v,  |                                    | (ASA, FortiGate,      |
|  MX, vMX)        |                                    |  StrongSwan)          |
+------------------+                                    +-----------------------+
        ^                                                            ^
        |                                                            |
        |            +---------------------------------+              |
        +------------| TIER 4: SD-WAN Overlay          +--------------+
                     | (Cisco Viptela, Fortinet,         |
                     |  Prisma Access, Cato)             |
                     |  Application-Aware Path Steering |
                     +---------------------------------+
```

- **📢 섹션 요약 비유**: VPN은 "터널 도시에 뚫린 자동차 전용 도로(고속도로, 표지판이 암호화됨)"이고, Direct Connect는 "도심과 도심을 직선으로 잇는 고속철도(KTX) 전용 트랙"입니다. 택배(데이터)를 한 번에 많이 보내려면 기차(DX)가, 빠르고 가끔 보내야 한다면 자동차(VPN)가 효율적입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Site-to-Site VPN (IPsec/IKEv2) 의 8단계 핸드셰이크

Site-to-Site VPN은 **IKEv2(Internet Key Exchange v2, RFC 7296)** 와 **ESP(Encapsulating Security Payload, RFC 4303)** 를 기반으로 양단 라우터(CGW ↔ VGW) 간 보안 연결(SA: Security Association)을 수립한다. ESP는 AH(Authentication Header)와 달리 **기밀성(Encryption)** 까지 제공하며, 페이로드 무결성(Integrity)과 재전송 방지(Anti-Replay Window)를 함께 보장한다.

```text
[ IKEv2 2-Phase 핸드셰이크 + ESP 데이터 플로우 ]

 On-Premise CGW                                          Cloud VGW/VPN GW
 (203.0.113.1)                                          (52.x.x.x)
      |                                                       |
      |  [Phase 1: IKE_SA_INIT]                               |
      | -- IKE_SA_INIT (HDR, SAi, KEi, Ni) ----------------► |  <- 암호 알고리즘/DH그룹 협상
      | ◄-- IKE_SA_INIT (HDR, SAr, KEr, Nr) ---------------- |  <- AES-256-GCM / DH-14(2048bit)
      |                                                       |
      |  [Phase 1.5: IKE_AUTH]                                |
      | -- IKE_AUTH (IDi, AUTH, SAi2, TSi, TSr) -----------► |  <- PSK or X.509v3 인증
      | ◄-- IKE_AUTH (IDr, AUTH, SAr2, TSr, TSi) ------------ |  <- Child SA(ESP) 생성
      |                                                       |
      |  ======= ESP Encrypted Tunnel (SPI: 0xCAFE1234) ======|
      | -- [ESP HDR | IV | Enc(Payload) | ICV] --------------► |  <- Mode: Tunnel (IP-in-IP)
      | ◄-- [ESP HDR | IV | Enc(Payload) | ICV] -------------- |  <- Anti-Replay: 32bit Seq
      |                                                       |
      |  [Phase 2: Rekey / DPD (Dead Peer Detection)]         |
      | -- INFORMATIONAL (DPD Request) ---------------------► |  <- 10s 주기 keepalive
      |                                                       |
      |  [Dead Peer Detection Timeout = 30s]                  |
      |  -> IKE_SA 삭제, IPSec SA 무효화                      |
      |  -> BGP Hold-Down(180s) -> Failover 트리거              |
```

**핵심 파라미터 & 고려사항:**
- **MTU 산정**: 인터넷 MTU 1500 - IPsec Overhead(50~57 bytes for ESP+AH+NAT-T) = **1420~1437 byte** 권장, MSS Clamping = MTU - 40 - 40 = **1379 byte**
- **DPD (Dead Peer Detection)**: BFD(Bidirectional Forwarding Detection, 50ms×3 = 150ms)가 더 빠르므로 VPN over SD-WAN에서는 DPD 대신 BFD 사용
- **Perfect Forward Secrecy (PFS)**: DH Group 14(2048bit) 또는 DH Group 15(3072bit) — Phase 2 PFS 활성화 시키지 않으면 키 재협상 시 동일 Pre-master Key 사용으로 취약
- **Encryption Algorithm**: AES-256-GCM(권장, 인증+암호화 동시) / AES-256-CBC(레거시 호환) / ChaCha20-Poly1305(ARM 모바일 환경)

### 2. Direct Connect (전용 회선) 아키텍처

Direct Connect는 CSP의 **DX Location**(예: AWS: Equinix IC1~IC11, KDDI, LG U+)에서 **Cross-Connect(LOA-CFA: Letter of Authorization and Connecting Facility Assignment)** 절차를 거쳐 On-Premise CPE 라우터와 CSP 라우터를 물리적으로 1G/10G/100G Single Mode Fiber로 직접 연결한다. 이후 **802.1Q VLAN** 태깅과 **BGP(Border Gateway Protocol, RFC 4271)** 로 경로를 교환한다.

```text
[ AWS Direct Connect 3-Tier Architecture (Public + Private VIF) ]

+-------------------------------------------------------------------------+
|                    AWS Direct Connect Location                         |
|                   (예: Equinix SL1, Seoul)                             |
|  +-------------------+         +-------------------+                  |
|  | AWS DX Endpoint   |         | Customer Router   |                  |
|  | (10G/100G LR4)    |◄--CX--►| (Cisco ASR9k,     |                  |
|  | + VLAN Tag 0x64   |  1G/10G|  Juniper MX,       |                  |
|  | + BGP AS 64512    | Fiber  |  Arista 7280)      |                  |
|  +---------+---------+         +---------+---------+                  |
+------------+-------------------------------+----------------------------+
             |                               |
             |  VIF (Virtual Interface)      |
             |  +----------+----------+      |
             |  | Private  | Public   | Transit
             |  | VIF      | VIF      | VIF
             |  |(RFC1918) |(AWS 공인)|(TGW)
             |  +----+-----+----+-----+---+------+
             |       |          |          |      |
     +-------+-------+------+   |   +------+------+------+
     |  Virtual Private     |   |   |   Transit Gateway   |
     |  Gateway (VGW)       |   |   |  (Inter-Region TGW) |
     |  -> VPC 10.0.0.0/16   |   |   |  -> 50+ VPCs          |
     +----------------------+   |   +---------------------+
                                |
                          +-----+----------+
                          | AWS Public     |
                          | Services       |
                          | (S3, DynamoDB, |
                          |  API Gateway)  |
                          +----------------+

      BGP Configuration Example:
      -------------------------------------
      router bgp 65000                   # On-Prem ASN
       neighbor 169.254.0.1 remote-as 64512   # AWS ASN
       neighbor 169.254.0.1 password 7 xxx
       address-family ipv4 unicast
        network 10.10.0.0 mask 255.255.0.0
        network 192.168.0.0 mask 255.255.0.0
        neighbor 169.254.0.1 activate
        neighbor 169.254.0.1 soft-reconfiguration inbound
        maximum-paths 2            # ECMP Active-Active
      !
      ip route 169.254.0.0 255.255.255.252 Serial0/0
```

### 3. 핵심 구성요소 비교표

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Customer Gateway (CGW)** | On-Premise 측 VPN/DX 종단 라우터의 논리적 표현(CSP에 등록) | BGP ASN, Public IP 등록, IPsec Pre-shared Key 또는 PKI 인증서, IKEv2 정책(IKE Cryptographic Suite) |
| **Virtual Private Gateway (VGW)** | AWS VPC 종단 게이트웨이 (Region 단위, ASN 자동 할당 64512/64513) | Site-to-Site VPN Attachment + Direct Connect VIF 연결, ASN은 커스터마이즈 가능, AWS-Classic 또는 VPN-CloudHub으로 다중 CGW 허브 연결 |
| **Transit Gateway (TGW)** | Region/Account 간 라우팅 허브 (50Gbps/Attachment, 최대 5,000 VPC) | BGP Route Reflector 역할, RAM(Resource Access Manager)으로 멀티 계정 공유, Inter-Region Peering, Multicast Support |
| **Direct Connect Gateway (DXGW)** | Global DX Aggregation Point (모든 Region의 VGW/TGW 연결 가능) | 1개의 DXGW = 10개 VIF 지원, VXLAN/EVPN 기반 L2 Extension은 DxCloud Wan으로 분리 구현 |
| **Customer Premises Equipment (CPE)** | 물리 라우터 (Cisco C8000v, Juniper vMX, VyOS, FRRouting) | BGP-4, IPsec, VxLAN, EVPN, MACsec (802.1AE) — 100Gbps 인터페이스는 Cisco 8000/RFC 8214 |
| **Cloud Router (Azure) / Partner Interconnect (GCP)** | CSP 별 전용 회선 종단 가상 어플라이언스 | Azure: Microsoft Peering + Private Peering, GCP: 10G/100G Partner Interconnect (Megaport, Equinix Fabric) |

### 4. BGP를 통한 하이브리드 라우팅 동작

Direct Connect와 VPN 모두 **BGP(EBGP/IBGP)** 로 경로를 교환한다. CSP는 **AS_PATH** Prepending, **Multi-Exit Discriminator(MED, RFC 4451)**, **BGP Local Preference**, **Communities** 속성을 통해 트래픽 엔지니어링(TE)을 지원한다. 이중화 구성에서 핵심은 **Active-Active(ECMP) vs Active-Passive(Primary/Backup)** 구분이다.

- **Active-Active (ECMP)**: 양단 BGP Session에 `maximum-paths 2` +
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 439 / 800

<- **이전**: [438. 클라우드 VPC 네트워크 분리 보안 그룹](/studynote/13_cloud_architecture/06_exam_summary/438_cloud_vpc_network_isolation_security_group/)
**다음**: [440. 클라우드 로드밸런서 ALB NLB GLB](/studynote/13_cloud_architecture/06_exam_summary/440_cloud_load_balancer_alb_nlb_glb/) ->

---
