---
title: "IPsec (Internet Protocol Security)"
date: "2026-07-05"
tags:
  - "cspe-network"
weight: 45
---

## Ⅰ. 개요
- **정의**: IP 계층에서 패킷 단위로 인증·무결성·기밀성을 제공하는 보안 프로토콜 모음임
- **배경/필요성**: IP 프로토콜 자체에 보안 기능이 없으므로 네트워크 계층에서 투명한 보호가 필요함
- **비유**: 모든 택배 상자에 봉인 테이프(AH)와 잠금 장치(ESP)를 부착하는 것과 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| AH vs ESP, Transport vs Tunnel 모드 비교 | IKE 2단계 협상 과정 | AH는 기밀성 미제공, NAT 환경에서 AH 사용 불가 |

> 요약: IP 계층에서 AH·ESP 프로토콜과 IKE 키 교환으로 보안을 구현하는 기술임

## Ⅱ. 구성요소
```text
Host A -> [IP Header][AH/ESP Header][Payload] -> Host B
                          |
                    IKE (UDP 500)
                   SA / SPD / SAD
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| AH (Authentication Header) | 패킷 무결성·출처 인증을 제공하나 암호화는 미수행 | 봉인 테이프(변조 감지) |
| ESP (Encapsulating Security Payload) | 패킷 암호화+무결성+인증을 모두 제공함 | 잠금 상자(내용 은닉) |
| IKE (Internet Key Exchange) | SA 협상 및 키 교환을 수행하는 프로토콜 | 비밀 열쇠 교환 의식 |
| SA/SPD/SAD | 보안 정책(SPD)과 보안 연관(SA)을 저장·관리하는 데이터베이스 | 출입 허가 명부 |

> 요약: AH/ESP로 패킷을 보호하고 IKE로 키를 협상하는 구조임

## Ⅲ. 절차
```text
Initiator -> IKE Phase 1 (SA, DH) -> Responder
Initiator -> IKE Phase 2 (IPsec SA) -> Responder
Initiator -> ESP/AH 적용 패킷 전송 -> Responder
Responder -> 복호화/검증 -> Application
```
- 1단계: IKE Phase 1에서 ISAKMP SA를 수립하고 DH 키 교환으로 보안 채널을 생성함
- 2단계: IKE Phase 2에서 IPsec SA(암호 알고리즘·SPI·수명)를 협상함
- 3단계: 협상된 SA에 따라 원본 패킷에 AH 또는 ESP 헤더를 적용하여 전송함
- 4단계: 수신 측이 SAD에서 SPI로 SA를 조회하여 복호화·무결성 검증을 수행함

> 요약: IKE 2단계 협상 후 SA 기반으로 패킷별 보안 처리를 수행함

## Ⅳ. 문제점
- NAT 비호환: AH가 IP 헤더 전체를 인증하므로 NAT 주소 변환 시 무결성 검증 실패
- 설정 복잡도: SA·SPD·라우팅·방화벽 규칙을 모두 정합시켜야 하여 운용 부담 증가
- 성능 오버헤드: 패킷마다 암호화·HMAC 연산이 수행되어 고속 환경에서 처리량 저하

> 요약: NAT 충돌·설정 복잡도·연산 부하가 주요 과제임

## Ⅴ. 개선방안
1. 단기: NAT-Traversal(UDP 4500 캡슐화) 적용으로 NAT 환경 호환성 확보
2. 중기: IKEv2 기반 자동 SA 관리 및 정책 템플릿으로 설정 복잡도 감소
3. 장기: 하드웨어 암호 가속기·인라인 IPsec NIC 도입으로 100Gbps급 처리 달성

> 요약: NAT-T·IKEv2 자동화·HW 가속으로 한계를 극복함

## Ⅵ. 전망
- 발전 방향: WireGuard 등 경량 VPN 프로토콜과의 공존·보완 추세임
- 기술사적 판단: Site-to-Site VPN(044 참조)에서 IPsec은 사실상 표준 지위를 유지함
- 기술사 제언: 포스트 양자 암호(PQC) 키 교환 알고리즘 적용 로드맵 수립이 필요함
