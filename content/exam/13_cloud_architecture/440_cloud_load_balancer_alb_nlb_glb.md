---
title: "Cloud Load Balancer ALB NLB GLB"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ALB는 OSI 7계층의 리버스 프록시 기반 HTTP/HTTPS/gRPC 라우터(콘텐츠 기반 스위칭), NLB는 L4에서 5-tuple 해시 기반 connection-level pass-through(초저지연·원본 IP 보존), GLB는 GENEVE(UDP 6081) 터널로 투명한 인라인 가상 어플라이언스 체이닝(Firewall/IDS/IPS) — 세 로드밸런서는 L7/L4/L3-투명-인라인이라는 명확한 **계층 분업**으로 한 개의 LB가 모든 트래픽을 처리하던 모놀리식 한계를 해체한 구조다.
> 2. **가치**: 단일 ALB로 100개 이상의 Target Group·마이크로서비스 라우팅·WAF 통합 처리, 단일 NLB로 수백만 RPS·정적 IP·PrivateLink 종단 처리, GLB로 페어 단위(Active-Passive)·3AZ 스패닝으로 어플라이언스 HA/스케일아웃 처리 — 이를 통해 TPS 100배 변동에도 AZ 장애 시 RTO≈0·P95 지연 ms 단위 안정화가 가능하다.
> 3. **판단 포인트**: (a) **프로토콜 종속성**(HTTP/REST->ALB, TCP/UDP·초저지연·EKS NTP->NLB, 트래픽 미러링·차세대 FW->GLB), (b) **클라이언트 IP 보존 필요성**(NLB는 `client_ip preservation` 기본, ALB는 `X-Forwarded-For` 헤더 의존), (c) **TLS 오프로드 vs 패스스루**(ALB는 종단 처리로 백엔드 부담v, NLB는 종단 처리 시 ALB로 위임), (d) **정적 IP/DNS 친화성**(NLB는 EIP 1개당 1 AZ, ALB는 FQDN only), (e) **비용 모델**(ALB는 LCU, NLB는 NLCU+시간, GLB는 GLCU).

---

## Ⅰ. 개요 및 필요성

클라우드 환경으로 워크로드가 이전되면서, 단일 EC2 인스턴스 또는 단일 VM에 L4/L7 처리를 모두 떠안기던 **클래식(HAProxy/Nginx + iptables) 아키텍처**는 다음과 같은 한계에 부딪혔다. (1) 인스턴스 장애 시 DNS TTL 갱신까지 수 분의 다운타임, (2) 컨테이너·마이크로서비스의 **수시 스케일 아웃/인**에 따른 엔드포인트 변동 추적 불가, (3) AZ 간 트래픽 균등 분산 미흡으로 인한 핫스팟, (4) DDoS·L7 공격(예: Slowloris, HTTP Flood) 흡수 기능 부재. AWS는 2009년 **ELB(Classic Load Balancer, CLB)** 로 시작해 2016년 **ALB(L7)·NLB(L4)**, 2020년 **GLB(Gateway Load Balancer)** 를 라인업에 추가하며, **계층별로 책임을 분담**하는 *Specialty LB* 패러다임을 완성했다. 이는 전통적인 F5 LTM/LTM+ASM 단일 어플라이언스 모델과 대비되는데, 컨트롤 플레인(LB의 라우팅 규칙)과 데이터 플레인(실제 트래픽 포워딩)을 API로 완전히 분리해 **DevOps 친화적 선언적 구성(Terraform/CloudFormation/CDK)** 이 가능해졌다.

핵심적으로, ALB/NLB/GLB는 동일한 AWS **Elastic Load Balancing(ELB) 서비스**의 *SKU(Same control plane, different data plane)* 라고 보면 된다. AWS 내부적으로는 모두 **Midoshim(미도시) + Rubix(루빅스)** 라는 Envoy 기반 프록시 위에 올라가지만, **데이터 경로 자체**가 다르다. ALB는 요청 단위로 파싱·라우팅·종단 처리하는 *reverse proxy*, NLB는 SYN을 가로채 트래픽을 그대로 흘려보내는 *flow-based forwarder*, GLB는 패킷을 가로채지 않고 GENEVE 캡슐화로 미러링하는 *transparent inline gateway* 다.

```text
                  [ 클라이언트(브라우저/모바일/IoT) ]
                              |  HTTPS
                              v
        +--------------------------------------------------+
        |  AWS Global Accelerator / Route 53 (Anycast IP)  |  <- 글로벌 GSLB(별도 토픽)
        +--------------------------------------------------+
                              |
        +---------------------+---------------------+
        v                     v                     v
   +---------+           +---------+           +---------+
   |   ALB   |           |   NLB   |           |   GLB   |
   | (L7)    |           | (L4)    |           | (L3-투명)|
   | HTTP/2  |           | TCP/UDP |           | GENEVE  |
   | gRPC/WS |           | TLS     |           | 6081    |
   +----+----+           +----+----+           +----+----+
        |                     |                     |
   +----+----+           +----+----+           +----+----+
   |  ECS/   |           |  EKS/   |           | 3rd-Party|
   | EKS Pod |           | EC2/ALB |           | Firewall|
   | Lambda  |           | RDS Proxy|           | IDS/IPS |
   +---------+           +---------+           +---------+
        |                     |                     |
   +----+---------------------+---------------------+----+
   | VPC 내부 Target Group(Instance | IP | Lambda | ALB)|
   +-----------------------------------------------------+
```

전통적 온프레미스 HAProxy/Nginx+F5 조합과 비교하면, 클라우드 LB는 (1) **API·IaC 완전 통합**, (2) **컨트롤 플레인 무상·자동화**, (3) **리전·AZ 페일오버 자동화**, (4) **WAF·Shield·Cognito·ACM과의 1급 통합**이라는 차이를 가진다. 다만 이 모든 기능을 무료로 누가 주는 것은 아니며, **LCU/NLCU/GLCU**라는 사용량 기반 요금이 발생한다(아래 Ⅴ절에서 정량 분석).

- **📢 섹션 요약 비유**: "은행 창구"에 비유하면, ALB는 **"어떤 업무(예금/대출/신용카드)인지 보고 적절한 담당자에게 배분하는 스마트 안내원"**, NLB는 **"VIP 전용 출입구에서 들어온 손님을 별도 체크 없이 즉시 안내하는 1차 게이트"**, GLB는 **"은행 건물 뒤편의 보안검색대(X-ray·폭발물 탐지)를 투명하게 통과시킨 뒤 본 창구로 보내는 보안 게이트"** 이다. 손님은 GLB의 존재를 의식하지 못한 채 본 창구(ALB/NLB)에 도착한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. ALB(Application Load Balancer) — L7 리버스 프록시

ALB는 클라이언트의 **HTTP/1.1, HTTP/2, gRPC, WebSocket** 요청을 파싱해 Host 헤더, Path, HTTP Method, Query String, Header 값, Source IP, ASNUM 같은 속성을 기반으로 Target Group을 결정한다. **Listener 1개당 1~100개 Rule**을 가질 수 있고, **Priority 순서**대로 평가된다. AWS NLB와 달리 ALB는 **HTTPS 종단(TLS Termination)** 을 LB가 직접 수행한다. 즉, ALB는 자체 ACM 인증서를 부착해 TLS 핸드셰이크를 끝내고, 평문 HTTP로 백엔드에 전달하는 **SSL 오프로드**가 디폴트다. 백엔드까지 TLS로 보호하려면 **Target Group의 `protocol: HTTPS` 지정 + 인증서 설치**로 양방향 TLS(mTLS) 구성이 가능하다.

라우팅 규칙은 **조건부**로 평가된다. `path-pattern`은 `/api/*`, `/static/*` 식의 prefix·exact 매치, `host-header`는 다중 도메인(예: `api.example.com`, `admin.example.com`) 라우팅, `http-header`는 `User-Agent: *Mobile*` 같은 임의 헤더 기반, `query-string`, `http-request-method`는 GET/POST 분기, **Lambda 호출 규칙**(`forward` 액션을 `aws:lambda` 로 지정하면 Target Group 없이 Lambda 동기 호출)까지 지원한다. 가장 강력한 기능은 **`weighted target group`** 으로, `/api/v1`(90%) + `/api/v2`(10%) 형태로 **카나리/블루-그린 배포**가 LB 단 한 곳에서 정의된다. 이때의 트래픽은 Sticky Session(쿠키 기반 `AWSALB`·`AWSALBAPP`)으로 사용자별 일관성 있게 유지할 수 있다.

헬스 체크는 **Active** 방식이다. 지정한 Protocol/Port/Path(예: HTTP 8080 `/health`)에 주기적 GET을 보내 200 OK를 기대하며, 임계값(Healthy/UnhealthyThresholdCount, 기본 2·2), Interval(기본 30s), Timeout(기본 5s)을 조정한다. ECS·EKS 환경에서는 **Dynamic Port Mapping**이 핵심이다. 컨테이너가 임의 포트(32768~60999)로 매핑되어도 ALB는 `instance:port`가 아닌 `ip:port`로 Target을 등록하므로(`target_type=ip`), 노드 재스케줄 시 0-downtime 마이그레이션이 가능하다.

```text
    Client -> ALB(1) -> Target Group A (EC2/ECS)
            |     (2) -> Target Group B (Lambda)
            |     (3) -> Target Group C (EKS IP)
            |
   [Listener :80/:443, Rules]
   1) IF  host = api.x.com  AND path /v1/*   -> TG-A(weight 90)
                                            -> TG-B(weight 10)  [Blue-Green]
   2) IF  host = admin.x.com AND path /*     -> TG-C(EC2 ASG)
   3) DEFAULT                                -> TG-D(Static S3 via Lambda@Edge)
   4) IF  http-header X-Debug = true         -> Fixed-Response 200 "Debug On"
```

성능 최적화 핵심: ALB는 **connection multiplexing**을 수행한다. 클라이언트 ↔ ALB 사이는 6개의 HTTP/2 멀티플렉스드 스트림이지만, ALB ↔ 백엔드 사이는 1:1의 HTTP/1.1 커넥션을 재사용해 백엔드 소켓 자원을 보존한다. 또한 **Cross-Zone Load Balancing**이 ALB는 디폴트로 활성화되어 있어, AZ-A LB 노드가 모든 AZ의 백엔드로 균등 라우팅한다(요금 무료). 보안 측면에서 ALB는 **SG(Security Group)** 부착이 가능해 클라이언트 IP 화이트리스트를 인그레스 단에서 강제할 수 있다(단, 클라이언트 IP는 ALB의 프라이빗 IP이므로 실제 화이트리스트는 X-Forwarded-For 헤더 기반으로 WAF에서 처리).

### 2. NLB(Network Load Balancer) — L4 flow-based forwarder

NLB는 TCP/UDP/TLS 트래픽을 **L4 헤더(5-tuple: src_ip, src_port, dst_ip, dst_port, protocol)** 만 보고 해시 테이블을 조회해 동일 흐름은 동일 백엔드로 **pin** 한다. SYN만 보고 라우팅한 뒤, 그 커넥션의 후속 패킷은 **stateful flow cache**를 통해 동일 백엔드로 직행한다. 이 때문에 **마이크로초 단위 지연**이 가능하며, ALB 대비 10~100배 처리량 확장이 가능하다(NLB 단일 노드 수백만 RPS, ALB 단일 노드 수만 RPS).

NLB의 가장 큰 차별점은 **클라이언트 소스 IP 보존**이다. ALB처럼 `X-Forwarded-For` 헤더에 의존하지 않고, 백엔드가 직접 클라이언트의 진짜 IP를 본다. 이를 위해 (a) **Target Group의 `preserve_client_ip.enabled=true`** 와 (b) **백엔드 ENI의 `src/dst check` 비
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 440 / 800

<- **이전**: [439. 클라우드 VPN 하이브리드 연결 Direct Connect](/studynote/13_cloud_architecture/06_exam_summary/439_cloud_vpn_hybrid_connection_direct_connect/)
**다음**: [441. 클라우드 마이그레이션 6R 전략 방법론](/studynote/13_cloud_architecture/06_exam_summary/441_cloud_migration_6r_strategy_methodology/) ->

---
