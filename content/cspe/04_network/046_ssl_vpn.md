---
title: "SSL VPN (Secure Sockets Layer VPN)"
date: "2026-07-05"
tags:
  - "cspe-network"
weight: 46
---

## Ⅰ. 개요
- **정의**: TLS/SSL 프로토콜을 이용하여 웹 브라우저 기반으로 원격 접속을 제공하는 VPN 기술임
- **배경/필요성**: 별도 클라이언트 설치 없이 HTTPS 포트(443)만으로 원격 접근이 가능해야 함
- **비유**: 웹 브라우저라는 범용 열쇠 하나로 회사 사무실 문을 여는 것과 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| IPsec VPN(045 참조)과의 비교 | 애플리케이션 계층 동작·Clientless 모드 | SSL VPN도 Full Tunnel 모드 지원 가능 |

> 요약: TLS 기반으로 웹 브라우저만으로 안전한 원격 접속을 제공하는 기술임

## Ⅱ. 구성요소
```text
Browser/Client ---(HTTPS 443)---> SSL VPN Gateway ---> Internal App/Server
                    |                    |
               TLS Handshake       Reverse Proxy / Tunnel
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| SSL VPN Gateway | TLS 종단·인증·접근 제어를 수행하는 관문 장비 | 건물 로비의 안내 데스크 |
| Clientless Mode | 웹 브라우저만으로 웹 애플리케이션에 접근하는 방식 | 손님용 출입증 |
| Thin/Fat Client | 에이전트 설치로 L3 Full Tunnel을 구성하는 방식 | 정직원용 출입 카드 |
| 접근 제어 정책 | 사용자 역할·단말 상태에 따라 접근 범위를 제한하는 규칙 | 층별 출입 권한표 |

> 요약: Gateway 중심으로 Clientless·Tunnel 두 가지 접근 방식을 제공함

## Ⅲ. 절차
```text
User -> HTTPS 접속 -> Gateway -> TLS Handshake -> 인증(MFA)
Gateway -> 접근 정책 적용 -> Reverse Proxy 또는 Tunnel 생성
User -> 암호화 트래픽 -> Gateway -> 복호화 -> 내부 리소스
```
- 1단계: 사용자가 HTTPS(443)로 SSL VPN Gateway에 접속을 요청함
- 2단계: TLS Handshake로 서버 인증서 검증 및 세션 키를 협상함
- 3단계: MFA 등 사용자 인증 후 단말 보안 상태를 검사(Host Checker)함
- 4단계: 정책에 따라 Clientless(Reverse Proxy) 또는 Full Tunnel 모드로 내부 자원 접근을 허용함

> 요약: TLS 핸드셰이크-인증-정책적용-접근허용의 4단계로 동작함

## Ⅳ. 문제점
- Clientless 기능 제한: 웹 기반이므로 RDP·SSH 등 비HTTP 프로토콜 접근이 제한적임
- Gateway 부하 집중: 모든 TLS 종단·복호화가 Gateway에 집중되어 동시 접속 시 병목
- 브라우저 의존성: 브라우저 버전·플러그인 호환성에 따라 기능 차이 발생

> 요약: 프로토콜 제약·게이트웨이 병목·브라우저 의존성이 과제임

## Ⅴ. 개선방안
1. 단기: HTML5 기반 프로토콜 변환(RDP/SSH over WebSocket)으로 Clientless 범위 확대
2. 중기: SSL 오프로딩·로드밸런서 도입으로 Gateway 처리 용량을 수평 확장함
3. 장기: SASE/ZTNA 통합으로 브라우저 비의존적 앱 단위 접근 제어로 전환

> 요약: 프로토콜 변환·부하 분산·ZTNA 전환으로 개선함

## Ⅵ. 전망
- 발전 방향: ZTNA가 SSL VPN의 후속 모델로 부상하며 에이전트 기반 접근 제어로 진화 중임
- 기술사적 판단: 레거시 웹 앱 접근 용도로 SSL VPN은 당분간 병행 운용될 전망
- 기술사 제언: VPN 장비 자체의 취약점(CVE) 관리와 패치 주기 단축이 중요함
