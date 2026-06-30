---
title: "다중화 (Multiplexing)"
date: "2026-06-30"
weight: 6
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 하나의 물리 전송로(매체)를 여러 신호가 공유하도록 주파수·시간·파장 등의 자원으로 분할하여 동시 전송하는 기술이다.

## Ⅱ. 구성요소 / 원리
- FDM(Frequency Division Multiplexing): 대역폭을 주파수 채널로 분할, 가드밴드로 간섭 방지(아날로그 방송)
- TDM(Time Division Multiplexing): 시간을 타임슬롯으로 분할, 동기식/통계식(STDM)으로 구분
- WDM(Wavelength Division Multiplexing): 광섬유에 서로 다른 파장(λ)을 동시 전송(DWDM/CWDM)
- OFDM(Orthogonal Frequency Division Multiplexing): 직교 부반송파로 주파수 효율 향상·다중경로 강건
- 송신측 MUX로 합성, 수신측 DEMUX로 분리하여 원신호 복원

## Ⅲ. 흐름도 / 구조
```text
  ch1 ─┐                          ┌─ ch1
  ch2 ─┤→[MUX]→ 단일 전송로 →[DEMUX]┤─ ch2
  ch3 ─┘   (주파수/시간/파장 분할)  └─ ch3
 FDM:주파수 | TDM:시간 | WDM:파장 | OFDM:직교 부반송파
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 단일 매체 자원을 분할 공유하여 전송 효율·경제성 향상 |
| 장점 | 회선 수 절감, WDM은 광섬유당 수십 Tbps급 대용량 실현 |
| 한계 | FDM은 가드밴드 낭비·간섭, 동기식 TDM은 빈 슬롯 낭비 발생 |

## Ⅴ. 기술사적 적용
- 광 백본망은 DWDM으로 단일 광섬유에 수십~수백 파장 다중화
- 4G/5G·Wi-Fi·DSL은 OFDM(A) 기반으로 고속·간섭 강건 전송 구현
- 통계식 TDM은 트래픽 가변성에 맞춰 패킷 교환망 효율을 높임
