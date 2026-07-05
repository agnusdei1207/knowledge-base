---
title: "NTN (Non-Terrestrial Network)"
date: "2026-07-05"
tags:
  - "cspe-network"
weight: 43
---

## Ⅰ. 개요
- **정의**: 위성·HAPS·UAV 등 비지상 플랫폼을 3GPP 표준 기반으로 통합한 통신 네트워크임
- **배경/필요성**: 지상망 커버리지 한계(해양·산악·재난)를 해소하고 글로벌 연결성을 확보해야 함
- **비유**: 지상 도로망이 닿지 않는 곳에 헬기 노선을 추가하는 것과 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 5G/6G NTN 표준화 동향 | 3GPP Rel-17 NR-NTN 규격 | LEO 위성통신(042 참조)과의 차이: NTN은 표준 프레임워크 |

> 요약: 3GPP 표준으로 비지상 플랫폼을 셀룰러 네트워크에 통합하는 개념임

## Ⅱ. 구성요소
```text
UE <--NR Uu--> NTN Platform <--Feeder Link--> NTN Gateway <---> 5GC
                  |
         LEO / GEO / HAPS / UAV
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| NTN Platform | 위성·HAPS·UAV 등 공중 중계 노드 | 하늘 위의 기지국 |
| NTN Gateway | 비지상 플랫폼과 5G 코어를 연결하는 지상 관문 | 공항 게이트 |
| Service Link | UE와 NTN 플랫폼 간 NR 무선 구간 | 이용자-헬기 간 통로 |
| Feeder Link | NTN 플랫폼과 Gateway 간 백홀 링크 | 헬기-공항 간 항로 |

> 요약: UE-Service Link-NTN Platform-Feeder Link-Gateway-5GC로 구성됨

## Ⅲ. 절차
```text
UE -> Timing Advance 보정 -> NTN Platform -> Feeder Link -> Gateway -> 5GC
5GC -> Gateway -> NTN Platform -> UE
```
- 1단계: UE가 GNSS 기반 위치·시각 정보로 전파 지연을 사전 보정(pre-compensation)함
- 2단계: 보정된 Timing Advance로 NTN 플랫폼에 NR Uplink를 전송함
- 3단계: NTN 플랫폼이 투명(Transparent) 또는 재생(Regenerative) 모드로 신호를 처리함
- 4단계: Gateway가 5GC에 연결하여 AMF·UPF를 통한 세션 관리를 수행함

> 요약: 전파 지연 보정 후 NR 프로토콜로 비지상 경유 통신을 수행함

## Ⅳ. 문제점
- 높은 전파 지연: LEO 기준 왕복 20~40ms, GEO 기준 약 600ms로 HARQ 타이밍 부적합
- 도플러 편이: 위성 고속 이동으로 주파수 편이가 발생하여 동기 유지 곤란
- 단말 복잡도 증가: GNSS 수신·사전 보정 로직 추가로 저가 IoT 단말 적용 곤란

> 요약: 지연·도플러·단말 복잡도가 NTN 상용화의 핵심 과제임

## Ⅴ. 개선방안
1. 단기: HARQ 비활성화 및 ARQ 계층 대체로 높은 RTT 환경에 적응함
2. 중기: 위성 에페메리스 기반 도플러 사전 보정 알고리즘 적용
3. 장기: RedCap NTN 단말 규격 정의로 저복잡도 IoT 단말 지원 확대

> 요약: HARQ 대체·도플러 보정·경량 단말 규격으로 과제를 해결함

## Ⅵ. 전망
- 발전 방향: 6G 시대 지상-비지상 통합 네트워크(Unified NW)의 핵심 요소로 발전 전망
- 기술사적 판단: D2C 서비스가 NTN의 킬러 유스케이스로 부상 중임
- 기술사 제언: 국내 위성-이동통신 주파수 공동 사용 정책과 로밍 체계 수립이 필요함
