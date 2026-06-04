---
title: "481. SD-WAN 소프트웨어 정의 광역 네트워크 (SD-WAN Software Defined Wide Area Network)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SD-WAN은 MPLS·광케이블·인터넷·LTE/5G 등 이기종(異機種) Underlay 전송 매체를 추상화하고, 중앙 오케스트레이터가 **IPsec/GRE/VXLAN-EVPN 오버레이 터널** 위에서 **Application-Aware Routing(AAR)**, **SLA 기반 동적 경로 선택**, **DPI/L7 애플리케이션 식별**, **제로터치 프로비저닝(ZTP)**을 오케스트레이션하는 SDN(Software Defined Networking) 기반 WAN 아키텍처이다.
> 2. **가치**: Gartner/Cisco 다수 사례에서 MPLS 전용 회선 대비 **WAN 총소유비용(TCO) 50~70% 절감**, 신규 지점 구축 기간 **수주 -> 수십 분**, 회선 장애 시 **200~500ms 이내 BFD-driven 페일오버**로 99.99% 가용성 확보, SaaS 트래픽의 **Cloud Onramp(Direct Cloud Breakout)**로 Microsoft 365/Zoom 응답시간 **20~40% 개선**이 입증되었다.
> 3. **판단 포인트**: 핵심 의사결정 축은 ① 보안 통합 방식(내장 NGFW vs 외부 **SSE/SASE** 연동—Gartner 2023 이후 SSE 분리를 권장), ② 오케스트레이터 배치(온프레미스 vManage/Director vs 클라우드 SaaS), ③ 트래픽 스티어링(중앙 집중 vs 로컬 브레이크아웃), ④ 단계적 마이그레이션(파일럿 -> Hybrid MPLS+SD-WAN -> 풀 SD-WAN), ⑤ 멀티클라우드(EKS/AKS/GKE·ExpressRoute·Interconnect) 및 **ZTNA 2.0** 연계 전략이다.

---

## Ⅰ. 개요 및 필요성

전통적 엔터프라이즈 WAN은 **Hub-and-Spoke MPLS** 구조로 본사/IDC에 트래픽을 집중시키는 **백홀링(backhauling)** 방식이었으며, 이는 ① **고비용**(국내 T1/E1급 MPLS 회선 월 100~300만원, 100Mbps MPLS 월 수백만원), ② **장기 구축 기간**(신규 지점 회선 개통 4~12주), ③ **낮은 트럭팩터 활용률**(평균 30% 이하), ④ **클라우드/SaaS 트래픽 폭증 시 비효율**(IDC 경유로 인한 latency 30~80ms 추가), ⑤ **정적 라우팅 기반의 회선 장애 대응 지연**(수 분~수십 분)이라는 구조적 한계를 가졌다.

2010년대 들어 **SaaS(MS 365·Salesforce·Zoom)·IaaS(AWS·Azure)·원격근무(Work From Anywhere)**가 보편화되면서, WAN 트래픽의 **70~85%가 DC가 아닌 인터넷/클라우드 종단**으로 향하는 **East-West -> North-South 전환**이 발생했다. 이 패러다임 변화는 2014년 **Viptela**(현 Cisco SD-WAN, IOS-XE 기반 vEdge/ISR/ASR), **VeloCloud**(현 VMware VeloCloud SD-WAN, 2017 VMware 인수), **Silver Peak**(현 HPE Aruba EdgeConnect), **Versa Networks**, **Cato Networks** 같은 전문 벤더 등장을 촉발했고, 2017년 **Gartner Magic Quadrant for SD-WAN**이 발표되면서 SD-WAN이 엔터프라이즈 WAN의 표준으로 자리매김했다. 이후 2019년 **Gartner가 SASE(Secure Access Service Edge)** 개념을, 2021년 **SSE(Security Service Edge)**를 분리 정의하면서, SD-WAN은 SASE의 WAN 컴포넌트 역할을 수행하며 진화 중이다.

국내에서는 2020년 이후 **공공기관 클라우드 전환**, **재택근무常态化**, **마이데이터·오픈뱅킹** 등 금융권 디지털 전환 가속으로 SD-WAN 도입이 폭증했으며, 통신 3사(SKT·KT·LG U+)가 **Managed SD-WAN** 서비스를, 네이버·카페24 같은 CSP가 **Cloud-Native SD-WAN**을 제공 중이다.

```text
[기존 MPLS Hub-Spoke (Hairpin Bottleneck)]

  [Branch-A]                  [Branch-B]
      \                            /
       \        MPLS L2/L3 VPN     /
        \          (Hub)           /
         \         |              /
          \   [HQ DataCenter] ----+   <- 트래픽이 무조건 본사 경유
           \    /        \         \
            \  /          \         \
       [Internet]      [SaaS/Cloud]  <- IDC 백홀링으로 latency 30~80ms 추가
       (직접접속 불가)   (응답지연)

------------------------------------------------------------

[SD-WAN Overlay 아키텍처]

            +--------------------------------------+
            |  SD-WAN Orchestrator (vManage)       |
            |  • 정책/템플릿/분석/ZTP              |
            |  • 멀티테넌트, RBAC                  |
            +----------------+---------------------+
                             |NETCONF/RESTCONF/TLS
       +---------------------+-------------------------+
       |                     |                         |
   [vBond] ---------- 인증서/제로터치 ------------------|
       |                     |                         |
   +---+----+         +------+------+           +------+------+
   | vSmart |◄-OMP--►|  Branch CPE |           |  DC CPE    |
   |Control |        |  vEdge/ISR  |           |  cEdge/ASR |
   | Plane  |        +------+------+           +------+------+
   +--------+               |                          |
                            |IPsec/GRE/VXLAN Overlay  |
              +-------------+--------------+           |
              |             |              |           |
         [Internet]      [MPLS]        [LTE/5G]    [Internet]
              |             |              |           |
              +--------+----+------+-------+-----------+
                       |             |
              [Cloud Gateway(VeloCloud GW / Versa Cloud)]
                       |
              +--------+---------+
              |        |         |
         [AWS DX] [Azure ER] [GCP Partner]   [MS 365 / Zoom / SaaS]
         (Direct Cloud Onramp)                  (Local Breakout)
```

**기존 vs 신규 패러다임 핵심 비교**

| 항목 | 기존 MPLS WAN | SD-WAN |
|---|---|---|
| 신규 지점 구축 | 4~12주 (회선 개통) | 30분~2시간 (ZTP) |
| 회선 장애 대응 | 수 분~수십 분 (수동) | 200~500ms (BFD 자동) |
| SaaS 응답 시간 | 100~300ms (IDC 백홀) | 30~80ms (Direct Breakout) |
| 월 회선비 (10지점 기준) | 1,500~3,000만원 | 400~900만원 |
| 트럭팩터 활용률 | 20~35% | 70~90% (앱 기반 다이내믹) |
| 보안 통합 | 별도 NGFW/UTM | 인라인 FW/ZTNA 또는 SSE 연동 |

- **📢 섹션 요약 비유**: 기존 MPLS WAN이 "지하철 2호선만 타고 본사까지 우회해서 출근하는 것"이라면, SD
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 481 / 800

<- **이전**: [480. VxLAN 오버레이 네트워크 멀티 테넌트](/studynote/13_cloud_architecture/06_exam_summary/480_vxlan_overlay_network_multi_tenant/)
**다음**: [482. 클라우드 인터커넥트 전용 연결 피어링](/studynote/13_cloud_architecture/06_exam_summary/482_cloud_interconnect_dedicated_connection_peeri/) ->

---
