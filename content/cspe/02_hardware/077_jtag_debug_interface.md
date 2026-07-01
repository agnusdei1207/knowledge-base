---
title: "JTAG 디버깅 인터페이스 (JTAG)"
date: "2026-07-01"
tags:
  - "cspe-hardware"
weight: 77
---

# 📖 【암기용】 개념 완전 이해

> 목적: JTAG를 처음 봐도 왜 4개 핀만으로 칩 내부를 검사하고 디버깅까지 하는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: TCK·TMS·TDI·TDO 4선으로 칩 내부 레지스터와 핀 상태를 직렬로 읽고 쓰는 IEEE 1149.1 표준 테스트·디버그 인터페이스
- **왜 필요한가**: PCB에 물리 프로브를 꽂을 공간이 없는 고밀도 실장 보드에서 칩 간 배선 결함을 검사하고, 부팅 소프트웨어가 없는 상태에서도 펌웨어를 플래시하고 브레이크포인트를 걸어야 한다.
- **핵심 직관**: 자물쇠를 열지 않고 4개 구멍으로 내부 톱니바퀴 위치를 하나씩 확인하고 조정하는 구조다.

## 깊이 이해
- **배경·문제의식**: 표면실장(SMT) 밀도가 올라가면서 핀 간격이 좁아져 오실로스코프나 로직 프로브를 물리적으로 접촉하기 어려워졌다.
- **배경·문제의식**: IEEE는 이 문제를 해결하려고 1990년 IEEE 1149.1(JTAG)로 boundary-scan 표준을 제정해, 칩 내부에 핀마다 shift register 셀을 심고 직렬 신호로 접점 상태를 확인하게 했다.
- **작동 원리**: TAP(Test Access Port)는 TCK(clock), TMS(mode select), TDI(data in), TDO(data out) 4개 필수 신호와 선택적 TRST(비동기 reset)로 구성된다.
- **작동 원리**: TAP Controller는 TMS 비트열로 상태를 전이하는 16-state 유한 상태 기계(FSM)이며, Shift-IR 상태에서 명령어를, Shift-DR 상태에서 데이터를 boundary-scan chain을 통해 TDI에서 TDO로 직렬 이동시킨다.
- **작동 원리**: boundary-scan 모드는 각 핀에 연결된 shift register 셀로 실제 배선의 open·short·냉납을 물리 프로브 없이 검출하고, on-chip debug 모드는 같은 TAP을 통해 CPU 코어 레지스터·메모리에 접근해 breakpoint 설정과 single-step 실행을 수행한다.
- **비유**: boundary-scan은 자물쇠를 분해하지 않고 4개 구멍으로 톱니 위치를 하나씩 읽어 배선이 끊겼는지 확인하는 방식이고, on-chip debug는 같은 구멍으로 자물쇠 내부 톱니를 직접 멈추고 한 칸씩 돌리는 방식이다.
- **구체 예시**: 부트로더가 없는 신규 보드에서 J-Link·ST-Link·OpenOCD로 TAP FSM을 제어하면 flash controller 접근, 부트로더 플래시, GDB breakpoint와 레지스터 덤프가 가능하다.
- **구체 예시**: PCB 양산 검사에서는 다이지 체인으로 묶은 여러 칩의 boundary-scan chain에 테스트 벡터를 흘려 모든 solder joint의 open·short 여부를 한 번에 스캔한다.
- **흔한 오해·주의점**: JTAG 핀이 존재한다고 항상 디버그가 가능한 것은 아니며, 제조사가 debug access port를 fuse나 보안 설정으로 잠가둔 경우 TAP은 응답해도 CPU 코어 레지스터 접근은 거부된다.
- **흔한 오해·주의점**: TRST 핀은 필수 4핀에 포함되지 않는 선택 신호이므로, TRST가 없는 보드는 TMS 시퀀스만으로 Test-Logic-Reset 상태에 진입해야 한다.
- **흔한 오해·주의점**: JTAG와 SWD(Serial Wire Debug)는 다른 인터페이스이며, SWD는 ARM이 정의한 2선(SWDIO, SWCLK) 디버그 전용 프로토콜로 boundary-scan 기능이 없다.

## 연결 개념
- IEEE 1149.1 Boundary-Scan — JTAG의 원 표준과 PCB 결함 검사 목적
- SWD(Serial Wire Debug) — ARM 코어의 2핀 디버그 대안, 핀 수 감소가 목적
- OpenOCD·GDB — TAP FSM을 제어해 소스 레벨 디버깅을 제공하는 소프트웨어 스택

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: JTAG 답안은 TAP 4핀 구성, 16-state FSM, boundary-scan과 on-chip debug 두 용도, 데이지 체인, SWD 대비 선택 기준을 함께 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: JTAG는 IEEE 1149.1 표준에 따라 TCK·TMS·TDI·TDO 4선으로 칩 내부 shift register chain을 직렬 제어하는 테스트·디버그 인터페이스이다.
> 2. **가치**: 물리 프로브 없이 PCB 배선 결함을 검출하고, 소프트웨어가 없는 상태에서도 부트로더·펌웨어를 플래시하며 breakpoint 기반 디버깅을 지원한다.
> 3. **판단 포인트**: 핀 수 제약이 있는 소형 보드는 SWD, 다중 칩 배선 검사와 범용 디버그가 필요한 보드는 JTAG를 선택 기준으로 삼는다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| TAP 구조 이해 확인 | TCK/TMS/TDI/TDO 4핀 + 선택적 TRST, 16-state FSM | 신호선 개수·명칭 오류, FSM 상태 수 누락 |
| 용도 구분 역량 확인 | boundary-scan 시험 vs on-chip debug 용도 차이 | 두 용도를 하나로 뭉뚱그려 설명 |
| 비교 판단 역량 확인 | SWD 대비 핀 수·기능 차이 | JTAG와 SWD를 같은 프로토콜로 혼동 |

> 요약: 이 문제는 TAP 신호 구조 암기보다 boundary-scan과 on-chip debug 두 용도를 구분하고 SWD 대비 선택 근거를 보여야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: TAP 4선으로 칩 내부를 직렬 제어하는 IEEE 1149.1 표준 인터페이스
- 배경: SMT 고밀도 실장으로 물리 프로브 접촉이 어려워지면서 1990년 IEEE 1149.1 boundary-scan 표준이 제정됨
- 필요성: PCB 배선 결함 검사와 부트 이전 펌웨어 플래시·디버깅을 동일 TAP으로 처리해야 개발·양산 비용을 낮춘다

---

## Ⅱ. 구조 및 구성요소

```text
Host PC/Debug Probe(J-Link, ST-Link, OpenOCD)
  -> TAP: TCK/TMS/TDI/TDO(+TRST optional)
  -> TAP Controller(16-state FSM)
  -> IR/DR Shift Register Chain
  -> Target Chip 1 -> Target Chip 2(Daisy-Chain TDO->TDI)
  -> Boundary-Scan Cell / CPU Core Register
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| TCK | shift 동작 기준 clock | 외부 공급, 주파수 가변 |
| TMS | TAP FSM 상태 전이 결정 | 매 clock마다 1비트 샘플링 |
| TDI/TDO | 명령·데이터 직렬 입출력 | 칩 간 daisy-chain 연결(TDO->TDI) |
| TRST(optional) | 비동기 TAP reset | 미존재 시 TMS 시퀀스로 대체 |
| TAP Controller | IR/DR 접근 제어 | 16-state FSM |
| Boundary-Scan Chain | 각 핀에 연결된 shift register | open·short 검출, CPU 레지스터 접근 겸용 |

> 요약: JTAG는 TAP 4선과 16-state FSM으로 다중 칩의 boundary-scan chain을 직렬 제어하는 구조다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Host TMS Sequence -> TAP FSM State Transition
  -> Shift-IR(명령어 로드) -> Update-IR
  -> Shift-DR(데이터 이동) -> Update-DR
  -> TDO 결과 출력 -> Host 판정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | TMS로 Test-Logic-Reset 진입 후 Run-Test/Idle 이동 | 초기 상태 확인 |
| 2 | Shift-IR 상태에서 TDI로 명령어(BYPASS, SAMPLE/PRELOAD, EXTEST 등) 입력 | 명령 코드 일치 여부 |
| 3 | Shift-DR 상태에서 boundary-scan chain을 통해 핀 또는 레지스터 데이터 이동 | open·short 여부, 레지스터 값 일치 |
| 4 | Update-DR/IR에서 결과 반영 후 TDO로 출력 확인 | 스캔 결과값과 기대값 비교 |

> 요약: JTAG 동작은 TMS로 FSM 상태를 옮기고 IR로 명령을, DR로 데이터를 순차 이동시켜 결과를 TDO로 회수하는 순서다.

---

## Ⅳ. 특징

| 구분 | Boundary-Scan 모드 | On-Chip Debug 모드 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 목적 | PCB 배선 결함(open·short) 검출 | breakpoint, single-step, 레지스터 조작 | IEEE 1149.1 |
| 대상 | 핀 간 물리 배선 | CPU 코어 레지스터, 메모리 | Shift-DR, Shift-IR |
| 필요 조건 | 물리 프로브 불필요, 양산 라인 테스트 | 부트로더·OS 유무 무관, 부트 전 플래시 가능 | Test Access Port |
| 도구 예 | ATE(Automated Test Equipment), boundary-scan 벡터 | J-Link, ST-Link, OpenOCD, GDB | TAP FSM 16-state |

> 요약: 같은 TAP을 boundary-scan은 배선 검사에, on-chip debug는 코어 제어에 사용하며 목적에 따라 접근 레지스터가 다르다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | JTAG | SWD | 선택 기준 |
|:---|:---|:---|:---|
| 핀 수 | TCK/TMS/TDI/TDO(+TRST) 4~5핀 | SWDIO/SWCLK 2핀 | 핀 여유 없는 소형 ARM 보드는 SWD |
| 기능 범위 | boundary-scan + on-chip debug + 다중 칩 daisy-chain | on-chip debug 전용, boundary-scan 미지원 | PCB 배선 검사 필요 시 JTAG 필수 |
| 표준·적용처 | IEEE 1149.1, 범용 MCU·FPGA·ASIC | ARM CoreSight 기반 Cortex-M/A 계열 | 대상 코어가 ARM 전용이면 SWD로 핀 절감 |

> 요약: 배선 검사와 다중 칩 디버깅은 JTAG, 핀 수 제약이 큰 ARM 단일 코어 보드는 SWD를 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 디버그 접근 차단 | 제조사가 fuse·보안 설정으로 debug access port 잠금 | 개발 단계 디버그 인증서·키 관리 정책 수립 | TAP 응답 여부, DAP 잠금 상태 로그 |
| daisy-chain 오결선 | TDO->TDI 연결 순서 오류로 IR 길이 불일치 | boundary-scan description language(BSDL) 파일로 chain 길이 검증 | scan chain length 일치 여부 |
| 신호 무결성 저하 | 긴 케이블·고주파 TCK에서 신호 왜곡 | TCK 주파수 하향, 임피던스 매칭 커넥터 사용 | 스캔 오류율, TCK 주파수 상한 테스트 |

> 요약: JTAG 운영은 디버그 접근 권한 관리, chain 길이 검증, 신호 무결성 점검으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| chain 무결성 | scan chain 길이와 IR 코드 일치 | BSDL 파일 대조, boundary-scan 벡터 테스트 |
| 디버그 가용성 | TAP 응답률, DAP 잠금 여부 | 디버그 프로브 연결 로그 |
| 신호 품질 | TCK 주파수 상한에서 스캔 오류율 0 | 로직 분석기, 스캔 재시도 카운트 |

> 요약: 도입 후 성공 여부는 chain 무결성, 디버그 가용성, TCK 신호 품질 지표로 판단한다.

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 신규 보드 양산 전 단계에서는 boundary-scan 벡터로 daisy-chain 전체의 open·short를 검사하고 chain 길이를 BSDL 기준으로 검증함
2. 부트로더가 없는 초기 개발 단계에서는 J-Link·ST-Link·OpenOCD로 TAP과 flash controller 레지스터에 접근해 부트로더를 플래시함
3. 핀 수가 제한된 ARM Cortex 기반 소형 보드는 JTAG 대신 SWD 2핀 구성으로 전환하고 디버그 접근 권한을 별도 인증 체계로 관리함

**결론 (2줄):**
- 기술사 판단: 다중 칩 배선 검사와 범용 디버그가 필요하면 JTAG, ARM 단일 코어에서 핀 절감이 우선이면 SWD를 선택함
- 향후 방향: 보안 강화를 위해 디버그 접근을 인증 기반으로 제한하는 debug authentication 체계와 표준화된 BSDL 검증 자동화가 확대되어야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "JTAG를 설명하시오" | TAP 4핀, 16-state FSM, IR/DR shift 흐름 | boundary-scan과 on-chip debug 용도 차이 |
| 비교형 | "JTAG와 SWD를 비교하시오" | daisy-chain vs 2핀 직결 구조 차이 | 핀 수, 기능 범위, 적용 대상 비교 |

> 요약: 설명형은 TAP FSM 동작 원리, 비교형은 SWD 대비 핀 수·기능 차이 중심으로 답안 축을 바꾼다.
