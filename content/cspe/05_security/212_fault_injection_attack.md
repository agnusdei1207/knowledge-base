---
title: "폴트 인젝션 공격 (Fault Injection Attack)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 212
---

# 📖 【암기용】 개념 완전 이해

> 목적: 폴트 인젝션 공격을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 전압·클럭·레이저·전자파로 칩 연산을 일부러 틀리게 만들어 인증 우회나 키 추출을 유도하는 공격
- **왜 필요한가**: Secure Boot, 암호 검증, 권한 체크는 한 번의 비교문 오류만으로 우회될 수 있어 물리적 결함 내성이 필요하다.
- **핵심 직관**: 문지기가 신분증을 확인하는 순간 조명을 깜박여 판단을 건너뛰게 만드는 방식이다.

## 깊이 이해
- **배경·문제의식**: 임베디드 장치는 공격자가 전원선, 클럭, PCB, 패키지에 접근할 수 있다. 소프트웨어 취약점이 없어도 물리 자극으로 CPU 명령 실행, 메모리 읽기, 조건 분기 결과를 교란할 수 있다.
- **작동 원리**: 공격자는 glitch 타이밍을 나노초~마이크로초 단위로 스캔한다. 서명 검증, 부트 단계, 암호 라운드에 결함을 넣어 비교 결과를 바꾸거나 차분 폴트 분석(DFA)으로 키를 복원한다.
- **비유**: 계산기를 두드리는 순간 배터리를 흔들어 한 자릿수만 틀리게 만든 뒤, 틀린 답과 정상 답의 차이로 내부 숫자를 맞히는 과정이다.
- **구체 예시**: RSA-CRT 서명에서 p 또는 q 경로 한쪽에 fault가 발생하면 정상 서명과 오류 서명의 gcd 계산으로 private key 요소가 노출될 수 있다.
- **흔한 오해·주의점**: "디버그 포트를 잠그면 충분"하지 않다. 전압 glitch와 EMFI는 외부 인터페이스를 쓰지 않고도 분기 우회와 secure boot bypass를 노린다.

## 연결 개념
- Secure Boot: 서명 검증 시점이 fault 공격 표적
- Redundancy: 이중 실행·결과 비교로 fault 탐지
- FI Test: voltage/clock/laser/EMFI 조건에서 결함 내성 평가

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 물리 자극 종류보다 공격 지점, 우회 결과, 탐지·복구 통제를 연결해 작성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 폴트 인젝션 공격은 전원·클럭·광·전자파 자극으로 연산 오류를 유도해 검증 우회 또는 키 추출을 수행하는 물리 공격이다.
> 2. **가치**: secure boot, 암호 연산, 권한 체크는 fault 한 번으로 결과가 바뀌므로 이중 검증과 fault sensor가 필요하다.
> 3. **판단 포인트**: 대응은 redundancy, temporal jitter, voltage/clock monitor, fail-secure reset, FI test coverage로 판단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 물리 공격 원리 이해 확인 | voltage/clock glitch, laser, EMFI와 secure boot bypass 연결 | 단순 장애나 전원 불량으로 설명 |
| 내성 설계 역량 확인 | double execution, redundancy, sensor, fail-secure | 재부팅만 대응으로 제시 |
| 검증 절차 확인 | fault campaign, timing window, coverage | 테스트 조건과 합격 기준 누락 |

> 요약: 이 문제는 결함 유발 기술보다 보안 검증 지점의 실패 모드와 내성 설계를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 칩 동작 교란 기반 검증 우회 공격
- 배경: 부트 ROM·암호 가속기·권한 체크는 특정 cycle의 branch skip, instruction corrupt, memory fault로 unsigned firmware 실행이나 키 추출 경로가 열릴 수 있음
- 필요성: 차량 ECU·결제 단말·IoT 게이트웨이는 FI campaign에서 bypass 0건, fault detection 99% 이상을 목표로 결함 내성을 검증해야 함

---

## Ⅱ. 구조 및 구성요소

```text
공격 장비 voltage/clock/laser/EMFI -> 타이밍 탐색
-> 표적 secure boot/crypto/auth check -> fault 발생
-> 우회 또는 오류 출력 수집 -> redundancy/sensor/reset 대응
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 자극 수단 | 전압 강하, clock glitch, laser pulse, EM pulse | ns~us 단위 타이밍 조정 |
| 표적 연산 | 서명 검증, 분기문, 암호 라운드 | branch skip, data corrupt |
| 분석 방법 | 정상/오류 결과 비교, DFA | RSA-CRT, AES round fault |
| 탐지 회로 | voltage monitor, clock monitor, light sensor | 임계 초과 시 reset |
| 소프트웨어 대응 | double execution, control-flow check | 결과 불일치 시 fail-secure |

> 요약: 폴트 인젝션은 자극 수단, 표적 연산, 오류 분석, 탐지 회로, 소프트웨어 대응을 함께 보아야 한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
표적 코드 식별 -> glitch parameter sweep -> fault 주입
-> 분기 우회 또는 오류 암호문 획득 -> 공격 성공 판정
-> 이중 실행/센서/reset 적용 -> FI 재시험
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 부트 로그·전력 trace로 검증 시점 추정 | trigger jitter 범위 산출 |
| 2 | 전압·클럭 폭·지연 값을 sweep | fault success rate 측정 |
| 3 | 서명 검증 skip 또는 암호 round 오류 유도 | unsigned image 실행 여부 |
| 4 | redundancy와 결과 비교로 fault 탐지 | mismatch detection rate |
| 5 | reset, zeroization, lockout 수행 | fail-open 0건 |

> 요약: 공격은 타이밍 탐색과 결함 성공률 최적화로 진행되며, 대응은 탐지 후 fail-secure 상태 전환으로 완성된다.

---

## Ⅳ. 특징

| 구분 | 소프트웨어 공격 | 폴트 인젝션 공격 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 접근 경로 | 네트워크, API | 전원선, 클럭, 패키지, PCB | 물리 접근 수분~수시간 |
| 표적 | 입력 검증, 메모리 버그 | secure boot, branch, crypto round | 단일 cycle fault 가능 |
| 대표 기법 | fuzzing, exploit | voltage/clock glitch, laser, EMFI | ns~us timing sweep |
| 대응 | 패치, 입력 검증 | redundancy, sensor, fault response | fail-open 0건 |

> 요약: 폴트 인젝션은 코드 취약점이 없어도 특정 cycle의 검증 결과를 바꾸므로 물리·논리 대응을 결합해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 검증 경로 | 이중 실행과 결과 비교 | secure boot, key unwrap 등 단일 실패 지점 |
| 비용/성능 | 센서 없음 | voltage/clock/light sensor 추가 | BOM 증가 대비 자산 가치 |
| 운영/위험 | 기능 테스트 | FI campaign 포함 | 공격자 물리 접근 가능성 |

> 요약: 결제·차량·산업 제어처럼 물리 접근 후 피해가 큰 장치는 FI 내성 설계를 기본 요구사항으로 둔다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Secure Boot 우회 | signature check branch skip | 이중 검증, inverted condition check | unsigned boot success 0건 |
| 키 추출 | 암호 round fault, RSA-CRT fault | exponent blinding, recomputation | DFA key recovery 실패율 |
| Fail-open | fault 탐지 후 정상 진행 | reset, zeroization, lockout | fault response latency |

> 요약: 주요 위험은 검증 우회와 키 추출이며, 대응 성공은 fail-open 0건으로 확인한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Fault 탐지율 | fault detection 99% 이상 | voltage/clock/EMFI campaign |
| 우회 방지 | secure boot bypass 0건 | unsigned firmware 주입 시험 |
| 복구 동작 | reset/zeroization 10ms 이내 | logic analyzer, boot log |

> 요약: FI 대응은 탐지율, 우회 성공 건수, 복구 지연을 동시에 측정해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Secure Boot는 서명 검증 2회, hash 재계산, inverted branch check를 적용해 단일 fault로 pass 상태가 되지 않게 설계
2. 하드웨어는 voltage/clock monitor, active shield, light sensor를 배치하고 임계 초과 시 key zeroization과 reset 수행
3. 검증은 voltage glitch, clock glitch, laser, EMFI별 fault campaign을 수행하고 bypass 0건, detection 99% 이상을 합격 기준으로 설정

**결론 (2줄):**
- 기술사 판단: 물리 접근 가능한 보안칩은 secure boot와 key path에 redundancy와 fail-secure response를 필수 통제로 둠
- 향후 방향: 칩렛·엣지 AI 보안 모듈에서도 FI test를 양산 전 보안 평가 항목으로 포함해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "폴트 인젝션 공격을 설명하시오" | 자극 수단, 표적 연산, 우회 흐름 | 소프트웨어 공격과 물리 공격 차이 |
| 요구사항 명시형 | "대응 방안을 제시하시오", "평가하시오" | redundancy, sensor, fail-secure 절차 | FI campaign 기준, 리스크·지표 |

> 요약: 설명형은 공격 원리와 사례, 방안형은 secure boot 내성 설계와 시험 기준을 중심으로 전환한다.
