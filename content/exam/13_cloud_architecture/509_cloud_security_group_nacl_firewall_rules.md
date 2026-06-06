---
title: "Cloud Security Group NACL Firewall Rules"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: **Security Group(SG)**은 ENI(Elastic Network Interface) 레벨에서 동작하는 *Stateful Allow-list* 방화벽이고, **Network ACL(NACL)**은 Subnet 레벨에서 동작하는 *Stateless Allow/Deny-list* 방화벽으로, AWS는 이 둘을 **다층 방화벽(Defense-in-Depth)**으로 분리하여 라우팅·연결 추적·상태 보존 책임을 분담한다.
> 2. **가치**: 단일 VPC 내에서도 (1) 서브넷 단위의 광역 차단(블랙리스트), (2) 인스턴스 단위의 세밀한 허용(화이트리스트)을 분리해 **공격 표면(Attack Surface)을 70~90% 축소**하고, (3) SG 간 참조(SG-to-SG Reference)로 **마이크로서비스 간 동적 화이트리스트**를 자동 구성해 운영 비용을 절감한다.
> 3. **판단 포인트**: 가장 빈번한 장애 원인은 (a) NACL의 Stateless 특성상 **Ephemeral Port(32768~60999) 회신 트래픽 미허용**, (b) SG는 *allow only*이므로 *명시적 deny*가 필요한 공격자 IP 차단은 NACL에서 수행해야 함, (c) SG 규칙은 **순서 무시 전수 평가**인 반면 NACL은 **Rule Number 오름차순**으로 평가되므로 평가 모델 혼동 시 디버깅 실패.

---

## Ⅰ. 개요 및 필요성

클라우드 인프라로 전환하면서 **네트워크 경계(Network Perimeter)**가 물리적 데이터센터에서 가상화되었습니다. 전통적 L3/L4 방화벽(Palo Alto, Fortigate, Cisco ASA 등)은 **물리/가상 어플라이언스 단일 경로**에서 모든 트래픽을 검사했지만, 클라우드에서는 (1) 워크로드가 **수평으로 탄력적 확장**하고, (2) ENI가 **다수의 AZ에 분산**되며, (3) **마이크로서비스 간 동적 IP**가 빈번히 변경됩니다. 이러한 환경에서 단일 방화벽 어플라이언스는 **병목·SPOF(Single Point of Failure)**가 됩니다.

AWS는 이를 해결하기 위해 **Hypervisor(가상화 커널) 내부에 분산 침입 방지 기능을 내장**한 SG와, **VPC 라우터 내부에 stateless 필터**를 수행하는 NACL을 제공합니다. 이 두 메커니즘은 **AWS Nitro System의 ENA(Elastic Network Adapter) 드라이버**와 **VPC Dataplane**에서 각각 패킷을 검사하므로, 추가 어플라이언스 없이 **선형적 성능 저하 없이(Linear Scalability)** 모든 인스턴스에 방화벽 기능을 부여합니다.

```text
+-----------------------------------------------------------------+
|            Public Internet (Untrusted Zone)                      |
+----------------------------+------------------------------------+
                             |  (1) Route 0.0.0.0/0 -> IGW
                             v
        +----------------------------------------+
        |   Internet Gateway (IGW) - VPC 경계    |  ※ 1Gbps+ 대역폭,
        |   (Stateful, BGP 등 라우팅만 수행)     |     stateless 검사 없음
        +----------------+-----------------------+
                         |
                         v
        +----------------------------------------+
        |  Route Table (VPC Router) - L3 라우팅  |
        |  ※ 패킷 페이로드 검사 없음             |
        +----------------+-----------------------+
                         |
        +----------------+--------------------------------+
        |  NACL (Stateless, Subnet 단위)                 | <--- 계층 1
        |  +------------------------------------------+   |
        |  | Rule 100: ALLOW TCP 443 0.0.0.0/0       |   |     평가순서: Rule
        |  | Rule 200: ALLOW TCP 1024-65535 10.0.0/16|   |     Number 오름차순
        |  | Rule *:    DENY  ALL (기본 거부)         |   |     (단, AWS 콘솔은
        |  +------------------------------------------+   |      * Rule을 32767로
        +----------------+--------------------------------+     표시)
                         |  Ephemeral Port 응답 주의!
                         v
        +----------------------------------------+
        |  Security Group (Stateful, ENI 단위)   | <--- 계층 2
        |  +----------------------------------+  |
        |  | IN: ALLOW TCP 443 from 0.0.0.0/0 |  |     평가: 전체 룰셋 동시
        |  | IN: ALLOW TCP 22  from SG:bastion|  |     평가(순서 무관)
        |  | OUT: ALLOW ALL  (기본)           |  |     반환 트래픽 자동 허용
        |  +----------------------------------+  |     (Connection Tracking)
        +----------------+-----------------------+
                         v
        +----------------------------------------+
        |  EC2 Instance (Private IP 10.0.1.50)   |
        |  - App Server (Nginx/Tomcat)            |
        +----------------------------------------+
```

기존에는 **단일 물리 방화벽**에서 ACL을 작성했지만, 클라우드에서는 **네트워크 토폴로지 = 정책(Policy)**이 됩니다. 즉, SG와 NACL을 통해 **인프라 코드(IaC, Terraform/CloudFormation)**로 네트워크 정책을 버전 관리하고, **GitOps**로 변경 이력을 추적할 수 있게 됩니다.

- **📢 섹션 요약 비유**: SG는 **아파트 현관문 도어락(각 집집마다 다름, 자동 잠금/해제 - Stateful)**, NACL는 **아파트 단지 입구 경비실(전체 동 단위, 신분증 검사 후 들어오지만 나가는 사람도 다시 검사 - Stateless)**입니다. 도어락이 정밀하지만 경비실이 1차 필터 역할을 하는 셈입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) 패킷 처리 경로(Packet Path)

```text
[Inbound Traffic Flow - 인바운드 상세]
-------------------------------------------------------------------
Client (1.2.3.4:54321)
   |
   |  ① Internet -> IGW (Stateful, NAT 수행)
   v
IGW --[SourceIP 변환 없음, Destination은 Public IP 또는 Private IP]
   |
   |  ② Route Table Lookup
   v
VPC Router (VPC Dataplane - 100Gbps+ Nitro 기반)
   |  ※ 라우팅만 수행, 패킷 복사/미러링 없음
   |
   |  ③ Subnet 식별 (예: 10.0.1.0/24)
   v
+----------------------------------------------+
|  NACL Inbound Rules (Stateless)              |
|  +----------------------------------------+  |
|  | #100 ALLOW TCP 443 0.0.0.0/0          |  | <--- 매칭
|  | #200 ALLOW TCP 1024-65535 10.0.0.0/16 |  |
|  | *     DENY  ALL                        |  |
|  +----------------------------------------+  |
|  ※ Stateless이므로 Client의 Ephemeral Port를 |
|    정확히 알아야 함. 54321 ∈ 1024-65535 OK   |
+------------+---------------------------------+
             | ④ NACL 통과
             v
+----------------------------------------------+
|  Security Group Inbound Rules (Stateful)     |
|  +----------------------------------------+  |
|  | ALLOW TCP 443 from 0.0.0.0/0           |  | <--- 매칭
|  | ALLOW TCP 22  from sg-bastion          |  |
|  +----------------------------------------+  |
|  ※ Connection Tracking Table에              |
|    {Src=1.2.3.4:54321, Dst=10.0.1.50:443,   |
|     Proto=TCP, State=ESTABLISHED} 기록     |
+------------+---------------------------------+
             | ⑤ SG 통과
             v
       EC2 Instance (Nginx가 SYN-ACK 응답)


[Outbound Traffic Flow - 아웃바운드 회신]
-------------------------------------------------------------------
EC2 (10.0.1.50:443) -> Client (1.2.3.4:54321)
   |
   |  ① SG Outbound 검사
   v
Security Group OUT: ALLOW ALL (default)
   |
   |  ※ Stateful: Connection Tracking에 일치 ->
   |    Inbound Rule이 매칭되었으면 Outbound는 자동 허용
   |    (별도 Outbound Rule 불필요)
   |
   |  ② NACL Outbound 검사 (Stateless!)
   v
+----------------------------------------------+
|  NACL Outbound Rules (Stateless)             |
|  +----------------------------------------+  |
|  | #100 ALLOW TCP 1024-65535 0.0.0.0/0   |  | <--- 서버 응답이 Ephemeral
|  | #200 DENY  TCP 25   0.0.0.0/0 (SMTP)  |  |     Port(32768~60999)로
|  | *     DENY  ALL                        |  |     나가므로 반드시 허용
|  +----------------------------------------+  |
+------------+---------------------------------+
             | ③ NACL OUT 통과
             v
        IGW -> Client
```

### 2) 구성 요소 상세

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Security Group (SG)** | ENI(Elastic Network Interface) 단위 인스턴스 방화벽 | • **Stateful**: Connection Tracking Table(C5.xlarge급 인스턴스 기준 약 1.2M 동시 연결 추적)<br>• **Allow-list only**: 명시적 Deny 룰 불가, "기본 거부(Default Deny) + 화이트리스트" 모델<br>• **순서 무시 전수 평가**: 모든 규칙 평가 후 매칭되는 것이 하나라도 있으면 허용<br>• **SG-to-SG Reference**: `sg-web`이 `sg-db`를 Source로 지정 -> IP 변경에 무관<br>• **Quota**: SG당 최대 60 rules(증설 시 1,000), ENI당 최대 5 SG |
| **Network ACL (NACL)** | Subnet 단위 stateless 필터 | • **Stateless**: 인바운드 허용해도 아웃바운드 별도 허용 필요<br>• **Allow + Deny 명시 가능**: Rule Number 오름차순 평가, 첫 매칭 적용<br>• **Asterisk(*) Rule**: Rule #32767은 변경 불가, 모든 미매칭 트래픽 거부<br>• **Ephemeral Port**: 기본 1024-65535, AL2023부터 32768-60999<br>• **Quota**: NACL당 최대 100 rules, AWS Support 통해 1,000까지 증설 가능 |
| **VPC Router / Dataplane** | 라우팅 + NACL 검사 수행 | • AWS Nitro System 기반 **하드웨어 오프로드**<br>• 트래픽이 워커 호스트 CPU를 거치지 않음 (i3.metal 등 일부 baremetal 제외)<br>• IPv4/IPv6 듀얼스택 지원 |
| **ENI (Elastic Network Interface)** | SG가 attach되는 가상 NIC | • 인스턴스 생성 후에도 detach/attach 가능<br>• **한 ENI에 여러 SG 가능**(5개), 모든 SG 규칙이 OR 결합되어 적용 |

### 3) Stateful vs Stateless 핵심 차이

| 특성 | Security Group (Stateful) | NACL (Stateless) |
| :--- | :--- | :--- |
| 반환 트래픽 처리 | **자동 허용** (Connection Tracking) | **반드시 별도 Rule**로 허용 (Ephemeral Port) |
| Deny Rule | ❌ 불가능 (allow-list only) | ✅ 가능 (`DENY` 명시) |
| 평가 순서 | 전체 동시 평가 | Rule Number 오름차순 |
| 적용 단위 | ENI(인스턴스) | Subnet |
| Source 지정 | CIDR, **다른 SG ID**, Prefix List | CIDR만 가능 |
| 변경 즉시 반영 | ✅ (밀리초 단위) | ✅ (밀리초 단위) |

### 4) Ephemeral Port 문제 — 가장 흔한 장애 원인

Linux 커널은 클라이언트 소켓에 **임의의 Ephemeral Port**를 할당합니다. 이 포트가 NACL Outbound Rule에서 허용되지 않으면 응답이 차단됩니다.

- **Linux/AL2023+ 권장 범위**: `32768 ~ 60999` (1024개)
- **구형 Linux**: `32768 ~ 61000`
- **Windows Server**: `49152 ~ 65535`

**올바른 NACL 설정 예시**:
```
# Web Server가 외부 API를 호출하는 경우
# Inbound (규칙 100번): Client -> Web Server 응답 수신
NACL-IN  #100: ALLOW TCP
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 509 / 800

<- **이전**: [508. 클라우드 서비스 엔드포인트 프라이빗링크](/studynote/13_cloud_architecture/06_exam_summary/508_cloud_service_endpoint_private_link/)
**다음**: [510. 클라우드 리소스 자동화 람다 트리거](/studynote/13_cloud_architecture/06_exam_summary/510_cloud_resource_automation_lambda_trigger/) ->

---
