---
title: "네트워크 슬라이싱 가상화 자원 관리 (Network Slice Resource Management)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 95
---

# 📖 【암기용】 개념 완전 이해

> 목적: 네트워크 슬라이싱을 하나의 물리망을 서비스별 논리망으로 나누고 CPU·무선·전송·코어 자원을 배정하는 관리 문제로 이해하게 만든다.

## 한눈에
- **개요**: 공통 물리 인프라 위에 eMBB, URLLC, mMTC 등 서비스별 논리 네트워크를 생성·운영하는 기술
- **왜 필요한가**: 자율주행, 스마트공장, 대용량 영상은 지연, 대역폭, 연결 수 요구가 서로 다르다.
- **핵심 직관**: 한 고속도로를 구급차 전용 차선, 화물 차선, 일반 차선으로 나누고 각 차선의 규칙을 다르게 적용하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 5G망은 다양한 산업 서비스를 같은 인프라에서 제공해야 한다. 모든 서비스에 같은 QoS를 적용하면 URLLC는 지연 목표를 못 맞추고, mMTC는 연결 수를 확보하지 못한다.
- **작동 원리**: 슬라이스는 S-NSSAI(SST+SD)로 식별되고 RAN, transport, 5G Core, MEC 자원을 서비스 요구에 맞춰 할당한다. 오케스트레이터가 생성, 확장, 축소, 폐기를 수행한다.
- **비유**: 같은 클라우드 서버에서 금융 시스템과 배치 작업을 별도 namespace와 quota로 운영하는 것과 같다.
- **구체 예시**: 스마트공장 URLLC slice는 latency 10ms 이하, packet loss 0.001% 이하를 목표로 MEC와 전용 QoS flow를 사용한다.
- **흔한 오해·주의점**: 슬라이스는 VLAN만 나누는 기능이 아니다. RAN PRB, UPF, QoS flow, 보안 정책, 관측 지표가 함께 묶인 end-to-end 자원 단위다.

## 연결 개념
- 5G SLA Slicing — 슬라이스별 SLA 보장
- NFV·SDN — 가상 네트워크 기능과 경로 제어 기반
- MEC — 지연 민감 슬라이스의 compute 위치

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 네트워크 슬라이싱 출제 시 식별자, 자원 할당, 오케스트레이션, SLA 지표를 중심으로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Network Slice Resource Management는 물리 네트워크를 S-NSSAI 기반 논리 슬라이스로 나누고 RAN·전송·코어 자원을 배정하는 기술이다.
> 2. **가치**: eMBB, URLLC, mMTC별 latency, bandwidth, connection density, isolation 요구를 같은 인프라에서 충족한다.
> 3. **판단 포인트**: slice isolation, admission control, QoS flow, lifecycle orchestration, SLA monitoring을 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 슬라이싱 구조 이해 확인 | S-NSSAI, NSSAI, RAN/Transport/Core slice | VLAN·VPN 수준 분리로 축소 |
| 자원 관리 역량 확인 | PRB, bandwidth, UPF, MEC, QoS flow 배정 | 무선·코어 자원 중 하나만 설명 |
| 운영 판단 확인 | isolation, SLA, lifecycle, admission control | 생성 후 모니터링·폐기 누락 |

> 요약: 이 문제는 논리망 분리보다 end-to-end 자원 보장과 수명주기 관리가 핵심이다.

---

## Ⅰ. 개요 및 필요성

- 개요: 5G 인프라의 논리망 분할
- 배경: 산업 서비스는 지연, 대역폭, 연결 수, 격리 요구가 달라 동일 best-effort망으로 SLA를 보장하기 어렵다.
- 필요성: 슬라이스 자원 관리는 생성, 확장, 축소, 폐기 단계에서 RAN·전송·코어 자원을 SLA 기준으로 배분한다.

---

## Ⅱ. 구조 및 구성요소

```text
Service Requirement -> Slice Template -> S-NSSAI
                    -> RAN Resource / Transport Path / 5GC NFs / MEC
                    -> SLA Monitor -> Orchestrator
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| S-NSSAI | 슬라이스 식별 | SST, SD 조합 |
| Slice Template | 서비스 요구와 자원 정책 정의 | latency, bandwidth, isolation |
| RAN/Transport/Core | 무선·전송·코어 자원 할당 | PRB, QoS flow, UPF |
| Orchestrator | 생성·변경·폐기 자동화 | ETSI NFV MANO, SDN controller |

> 요약: 슬라이스 관리는 요구사항을 템플릿으로 바꾸고 RAN부터 코어까지 자원을 연결한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 요청 -> SLA 요구 해석 -> Slice Template 선택
-> 자원 승인 -> RAN/Transport/Core 배치 -> SLA 측정 -> 조정/해제
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서비스 요구에서 latency, bandwidth, device count 추출 | 요구사항 누락 0건 |
| 2 | S-NSSAI와 slice template 매핑 | SST 값 일치 |
| 3 | RAN PRB, transport bandwidth, UPF/MEC 자원 승인 | admission success rate |
| 4 | QoS flow와 정책 배포 | 5QI, ARP, GBR 설정 |
| 5 | SLA 측정 후 scale-out 또는 해제 | latency 10ms, loss 0.001% |

> 요약: 슬라이스는 요구 해석, 자원 승인, 정책 배포, SLA 측정, 수명주기 조정으로 동작한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | Network Slice | 수치 컬럼 |
|:---|:---|:---|:---|
| 서비스 분리 | VLAN·VPN | S-NSSAI 기반 E2E 논리망 | SST 1/2/3 등 |
| 자원 보장 | best-effort | PRB, QoS flow, UPF 자원 할당 | 5QI, GBR |
| 운영 방식 | 수동 회선 구성 | template 기반 자동 생성 | 생성 시간 분 단위 |
| 한계 | 단순 구조 | cross-domain orchestration 필요 | RAN·Transport·Core 연동 |

> 요약: 네트워크 슬라이스는 단순 경로 분리가 아니라 자원·정책·SLA를 묶은 서비스 단위다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 분리 방식 | VPN, APN | 5G S-NSSAI slice | 산업별 SLA와 격리 요구 |
| 자원 관리 | 정적 대역폭 | 동적 admission·scale | 트래픽 변동, URLLC 요구 |
| 운영 모델 | 장비별 설정 | orchestrator 기반 E2E 제어 | RAN·코어 다벤더 환경 |

> 요약: 슬라이싱은 서비스별 SLA와 자원 격리가 모두 필요한 5G 산업망에 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| SLA 위반 | 과다 수용·혼잡 | admission control, quota | latency p95, PRB usage |
| 격리 실패 | 공유 UPF·정책 오류 | slice isolation test, RBAC | cross-slice leakage 0건 |
| 운영 복잡도 | RAN·Transport·Core 도메인 분리 | closed-loop automation | 변경 성공률 99% |

> 요약: 슬라이스 리스크는 과다 수용, 격리 실패, 도메인 복잡도이므로 자동 검증이 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| SLA | URLLC latency 10ms 이하, loss 0.001% 이하 | probe, UPF metric |
| 자원 사용 | PRB·UPF CPU 70% 이하 | RAN/5GC telemetry |
| 수명주기 | slice 생성 5분 이하, 변경 성공률 99% | orchestrator log |

> 요약: 도입 효과는 SLA 준수, 자원 사용률, 수명주기 자동화 지표로 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 서비스 유형별 SST, latency, bandwidth, isolation 요구를 slice template으로 정의
2. RAN PRB, transport QoS, UPF/MEC 자원을 admission control과 quota로 배정
3. p95 latency, packet loss, PRB usage를 closed-loop로 수집해 scale-out·scale-in 자동화

**결론 (2줄):**
- 기술사 판단: SLA와 격리 요구가 명확한 산업망은 S-NSSAI 기반 E2E slice로 설계해야 함
- 향후 방향: AI 기반 closed-loop orchestration으로 트래픽 예측과 자원 재배치를 자동 수행하는 방향

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | slice 생성·자원 배정 흐름 | VPN 대비 E2E 자원 보장 |
| 요구사항 명시형 | "비교하시오", "방안을 제시하시오", "설계하시오" | SLA 요구를 template·admission으로 변환 | 격리·과다 수용·자동화 대응 |

> 요약: 포괄형은 구조와 원리, 요구사항 명시형은 SLA 기반 자원 설계를 중심으로 답안을 전환한다.
