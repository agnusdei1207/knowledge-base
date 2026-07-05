---
title: I/O 가상화 — SR-IOV (I/O Virtualization)
date: 2026-07-05
tags: [cspe-hardware]
weight: 73
---

## Ⅰ. 개요
- 정의: 하나의 물리적 PCI 장치를 여러 개의 가상 장치로 분할하여 VM에 직접 할당하는 기술
- 배경: 소프트웨어 기반 I/O 가상화의 CPU 부하 및 네트워크 병목 현상 해결
- 출제 의도: PF(Physical Function)와 VF(Virtual Function)의 역할 및 통신 구조 이해

## Ⅱ. 구성요소
- ASCII 구조도
  [ VM 1 ] [ VM 2 ] [ VM 3 ] (Guest)
     |        |        |
  [ VF 1 ] [ VF 2 ] [ VF 3 ] (Virtual Functions)
  ---------------------------
  [      Physical NIC      ] (PF: Physical Function)

- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| PF | 장치 설정 및 자원 관리를 담당하는 풀 기능 PCI 장치 | 건물 관리인 |
| VF | 실제 데이터 전송만 담당하는 경량화된 가상 장치 | 개별 사무실 |
| Direct I/O | 하이퍼바이저 개입 없이 VM이 HW에 직접 접근 | 전용 출입문 |

- > 요약: 하이퍼바이저를 거치지 않는 패스스루(Pass-through) 방식의 확장형

## Ⅲ. 절차
- ASCII 흐름도
  [PF 활성화] -> [VF 생성] -> [VM 할당] -> [Direct DMA 전송]

1. Capability 설정: NIC 펌웨어에서 SR-IOV 기능 및 가상화 개수 지정
2. VF 인스턴스화: 호스트 OS에서 필요한 개수만큼 가상 기능(VF) 생성
3. 장치 바인딩: 하이퍼바이저가 특정 VF를 특정 VM의 PCI 슬롯에 맵핑
4. 데이터 전송: VM 내 드라이버가 VF와 직접 통신하여 데이터 송수신

- > 요약: 소프트웨어 브릿지를 생략하여 베어메탈에 근접한 I/O 성능 달성

## Ⅳ. 문제점
- Migration 제약: 특정 HW에 종속되어 VM 실시간 이동(Live Migration) 어려움
- 하드웨어 한계: NIC 하드웨어가 지원하는 VF 개수의 물리적 제한

## Ⅴ. 개선방안
- Bonding/Failover: 가상 브릿지와 SR-IOV를 결합하여 가용성 및 이동성 확보
- Virtio-forwarding: 가상화 표준 인터페이스와 SR-IOV의 성능 결합 시도

## Ⅵ. 전망
- 로드맵: SmartNIC/DPU와 결합하여 고성능 클라우드 네트워크 인프라의 표준화
- CSF: 하드웨어 독립적인 추상화 기술(VDPA)과의 연동을 통한 유연성 확보 필수
