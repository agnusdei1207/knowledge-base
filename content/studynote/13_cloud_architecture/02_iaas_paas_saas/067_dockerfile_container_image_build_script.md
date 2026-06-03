+++
title = "67. 도커 파일 (Dockerfile) - 컨테이너 이미지를 생성(빌드)하기 위한 명령어 명세 스크립트 (IaC 성격)"
date = 2026-04-07

[taxonomies]
tags = ["studynote-cloud"]

[extra]
tags = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Dockerfile은 컨테이너 이미지를 어떻게 만들지 선언하는 빌드 스크립트(Build Script)다. 각 명령어(Instruction)가 읽기 전용 레이어를 하나씩 쌓아 최종 이미지를 만든다.
> 2. **가치**: 이미지 생성 과정을 코드(Code)로 관리함으로써 재현성(Reproducibility)과 자동화를 실현한다. 사람이 수동으로 서버를 설정하는 시대를 끝낸 IaC(Infrastructure as Code)의 컨테이너 버전이다.
> 3. **판단 포인트**: Dockerfile 작성 품질이 이미지 크기, 빌드 속도, 보안 수준을 직접 결정한다. 레이어 순서, 캐시 전략, 멀티 스테이지 빌드, 시크릿 관리를 함께 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

과거에는 새 서버를 준비할 때 관리자가 직접 SSH로 접속해 패키지를 설치하고 설정 파일을 수정했다. 이 과정은 "설치 순서", "패키지 버전", "설정값" 중 어느 하나만 달라져도 완전히 다른 환경이 만들어지는 취약한 방식이었다.

Dockerfile은 이 문제를 해결한다. "베이스 이미지로 무엇을 쓸지", "어떤 패키지를 설치할지", "어떤 파일을 복사할지", "시작 명령어가 무엇인지"를 텍스트 파일에 선언적으로 기술한다. 이 파일만 있으면 누구든, 어떤 환경에서든, `docker build` 한 줄로 동일한 이미지를 생성할 수 있다.

이것이 Dockerfile이 단순한 "셸 스크립트 대체물"이 아닌, <strong>이미지 생성용 IaC(Infrastructure as Code)</strong>라 불리는 이유다. Dockerfile은 Git으로 버전 관리되고, 코드 리뷰를 받으며, CI/CD 파이프라인에서 자동으로 실행되어야 한다.

- **📢 섹션 요약 비유**: 요리사가 바뀌어도 같은 맛을 내려면 레시피 카드가 필요하다. Dockerfile은 이미지를 만드는 정확한 레시피다. 레시피대로 만들면 누가 만들어도 같은 도시락이 나온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 핵심 명령어 (Instructions)

| 명령어 | 용도 | 중요 특성 |
| :--- | :--- | :--- |
| `FROM` | 베이스 이미지 지정 | 첫 번째 명령어. 모든 레이어의 기반 |
| `RUN` | 빌드 시 명령 실행 | 새 레이어 생성. 캐시 대상 |
| `COPY` | 파일/디렉토리 복사 | 새 레이어 생성. ADD보다 권장 |
| `ADD` | 파일 복사 + URL/압축 해제 | 사이드 이펙트 있어 COPY 선호 |
| `WORKDIR` | 작업 디렉토리 설정 | 이후 명령의 기준 경로 |
| `ENV` | 환경변수 설정 | 빌드/실행 시 모두 적용 |
| `ARG` | 빌드 인수 | 빌드 시에만 사용. 이미지에 남지 않음 |
| `EXPOSE` | 포트 문서화 | 실제 개방은 아님. 정보성 선언 |
| `CMD` | 기본 실행 명령 | 컨테이너 시작 시. 오버라이드 가능 |
| `ENTRYPOINT` | 고정 실행 명령 | CMD와 조합 사용. 오버라이드 어려움 |
| `USER` | 실행 사용자 지정 | 보안 강화. non-root 권장 |
| `HEALTHCHECK` | 상태 확인 명령 | 컨테이너 헬스 체크 정의 |
| `VOLUME` | 볼륨 마운트 포인트 | 데이터 영속성 |

### 레이어 생성 흐름



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Dockerfile</div>
<div class="kb-diagram-tree-item" style="--depth:2">FROM python:3.11-slim → Layer 0 (베이스)</div>
<div class="kb-diagram-tree-item" style="--depth:2">WORKDIR /app → Layer 1 (메타)</div>
<div class="kb-diagram-tree-item" style="--depth:2">COPY requirements.txt . → Layer 2 (파일 복사)</div>
<div class="kb-diagram-tree-item" style="--depth:2">RUN pip install -r ... → Layer 3 (패키지 설치)</div>
<div class="kb-diagram-tree-item" style="--depth:2">COPY . . → Layer 4 (소스 코드)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">── CMD</div><div class="kb-diagram-node">"python", "app.py"</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Layer 5 (실행 명령)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">읽기 전용 이미지 = Layer 0 ~ 5 합산</div></div>
<div class="kb-diagram-note">▼ docker run</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">읽기-쓰기 레이어 추가 = 컨테이너</div></div>
</div>
</div>



### 레이어 캐시 전략

캐시는 Dockerfile 위에서부터 순서대로 적용된다. <strong>변경이 발생한 레이어 이후의 모든 레이어는 캐시가 무효화</strong>된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">최적화 전 (나쁜 예):</div>
<div class="kb-diagram-note">COPY . . ← 소스 코드 자주 변경 → 캐시 깨짐</div>
<div class="kb-diagram-note">RUN pip install ... ← 매번 재설치 (불필요한 시간)</div>
<div class="kb-diagram-note">최적화 후 (좋은 예):</div>
<div class="kb-diagram-note">COPY requirements.txt . ← 의존성 파일만 먼저 복사</div>
<div class="kb-diagram-note">RUN pip install ... ← requirements.txt 변경 시에만 재실행</div>
<div class="kb-diagram-note">COPY . . ← 소스 코드 복사 (캐시 깨져도 pip는 OK)</div>
</div>
</div>



### 멀티 스테이지 빌드 (Multi-stage Build)

```dockerfile
# Stage 1: 빌드 스테이지 (컴파일러, 빌드 도구 포함)
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /workspace
COPY pom.xml .
RUN mvn dependency:go-offline  # 의존성 캐시
COPY src/ src/
RUN mvn package -DskipTests

# Stage 2: 실행 스테이지 (JRE만 포함)
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /workspace/target/app.jar app.jar
USER 1000:1000                 # non-root 실행
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget -q --spider http://localhost:8080/health || exit 1
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

결과: Maven + JDK 이미지(700MB) → JRE Alpine 이미지(75MB)로 약 90% 감소

- **📢 섹션 요약 비유**: 케이크를 만들 때 오븐(빌드 환경)은 케이크 가게에 두고, 완성된 케이크(실행 이미지)만 손님에게 배달하는 것과 같다. 오븐째 배달할 필요가 없다.

---

## Ⅲ. 비교 및 연결

### Dockerfile vs 셸 스크립트 vs Ansible

| 항목 | Dockerfile | 셸 스크립트 | Ansible |
| :--- | :--- | :--- | :--- |
| 목적 | 이미지 빌드 | 서버 설정 자동화 | 서버 구성 관리 |
| 재현성 | 이미지로 보장 | 환경 의존적 | 멱등성 보장 |
| 버전 관리 | Git 가능 | Git 가능 | Git 가능 |
| 격리 | 컨테이너로 완전 격리 | 호스트 공유 | 호스트 공유 |
| 배포 방식 | 이미지 push/pull | scp + 실행 | Playbook 실행 |
| 실무 선택 | 클라우드 네이티브 앱 | 단순 초기화 | 레거시 서버 관리 |

### Dockerfile 최적화 기법 비교

| 기법 | 효과 | 적용 시점 |
| :--- | :--- | :--- |
| 최소 베이스 이미지 | 크기 감소, 공격 표면 축소 | 모든 Dockerfile |
| 레이어 병합 (&&) | 임시 파일 레이어 제거 | RUN 명령 최적화 |
| 멀티 스테이지 빌드 | 빌드 도구 최종 이미지 제외 | 컴파일 언어 프로젝트 |
| .dockerignore | 빌드 컨텍스트 최소화 | 모든 프로젝트 |
| 레이어 순서 최적화 | 캐시 히트율 극대화 | CI 빌드 시간 단축 |
| BuildKit 활용 | 병렬 빌드, 시크릿 안전 주입 | 고급 최적화 |

- **📢 섹션 요약 비유**: 좋은 요리 레시피(Dockerfile)는 재료를 낭비하지 않고, 조리 순서가 효율적이며, 음식에 독성 재료(시크릿)를 넣지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Dockerfile 보안 베스트 프랙티스

**1. non-root 사용자 지정**

```dockerfile
# UID:GID 1000:1000 으로 실행 (root 불필요)
RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -H -D appuser
USER appuser
```

**2. 시크릿 안전 주입 (BuildKit Secret)**

```dockerfile
# --mount=type=secret 사용 → 시크릿이 레이어에 남지 않음
RUN --mount=type=secret,id=npm_token \
    npm ci --userconfig=/dev/stdin < /run/secrets/npm_token
```

**3. 읽기 전용 파일시스템 설정**

```dockerfile
# VOLUME 으로 쓰기 필요 경로만 지정
VOLUME ["/app/logs", "/tmp"]
# 나머지는 읽기 전용으로 --read-only 플래그로 실행
```

**4. HEALTHCHECK 정의**

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
```

### 설계 판단 체크리스트

1. 베이스 이미지가 최소화된 공식 이미지인가? (alpine, slim, distroless)
2. 자주 변경되는 레이어가 Dockerfile 아래에 위치하는가? (캐시 효율)
3. 불필요한 패키지/파일을 설치하지 않고, 임시 파일을 정리하는가?
4. 멀티 스테이지 빌드로 빌드 도구가 최종 이미지에 포함되지 않는가?
5. ARG/BuildKit Secret으로 빌드 시크릿을 주입하며, ENV로 시크릿을 설정하지 않는가?
6. USER 명령어로 non-root 사용자를 지정했는가?
7. .dockerignore 파일로 빌드 컨텍스트에서 불필요한 파일을 제외하는가?

### 안티패턴

- <strong><code>RUN apt-get update</code> 레이어 분리</strong>: 업데이트와 설치를 별도 레이어로 나누면, 캐시된 apt 인덱스를 사용하다 패키지를 찾지 못하는 오류가 발생한다. `&&`로 합쳐야 한다.
- **거대한 단일 레이어**: 모든 작업을 하나의 RUN에 때려 넣으면, 부분 변경 시 전체를 다시 실행해야 한다.
- **비밀값(API 키, 비밀번호)을 ENV로 설정**: `docker history`로 모든 레이어가 보이므로 시크릿이 노출된다. ARG + BuildKit Secret 사용.
- **빌드와 런타임 스테이지 미분리**: 최종 이미지에 컴파일러, 테스트 도구가 포함되어 크기가 수 GB가 된다.
- **ENTRYPOINT와 CMD 혼용 오류**: ENTRYPOINT를 셸 형식(`ENTRYPOINT npm start`)으로 쓰면 시그널이 전달되지 않아 컨테이너가 우아하게 종료되지 않는다. exec 형식(`ENTRYPOINT ["node", "app.js"]`) 사용.

- **📢 섹션 요약 비유**: 집을 짓는 설계도(Dockerfile)가 잘못되면, 아무리 좋은 자재(베이스 이미지)를 써도 결과물(이미지)이 나쁘다. 설계도 리뷰가 가장 중요하다.

---

## Ⅴ. 기대효과 및 결론

### 정량적 효과

| 지표 | 최적화 전 | 최적화 후 | 개선율 |
| :--- | :--- | :--- | :--- |
| 이미지 크기 | 1.2GB | 80MB | 93% 감소 |
| 빌드 시간 (캐시 활용) | 8분 | 45초 | 90% 단축 |
| 취약점 수 (CVE) | 120개 | 3개 | 97% 감소 |
| 배포 속도 | 10분 | 1분 | 90% 단축 |

### 정성적 효과

- **일관된 빌드**: "나는 되는데 너는 안 되는" 빌드 환경 불일치 해소
- **협업 개선**: Dockerfile 리뷰로 빌드 방식에 대한 팀 합의 형성
- **보안 기준선 확립**: Dockerfile 작성 표준으로 조직 전체의 보안 수준 일관성 확보
- **CI/CD 통합**: Dockerfile이 있으면 CI/CD 파이프라인에서 자동 빌드·스캔·배포 완성

### 미래 전망

BuildKit(Docker의 차세대 빌드 엔진)은 병렬 레이어 빌드, 시크릿 안전 주입, 캐시 최적화를 제공한다. 또한 <strong>Cloud Native Buildpacks</strong>는 Dockerfile 없이도 애플리케이션 소스를 자동으로 분석하여 최적화된 이미지를 생성하는 방향으로 발전하고 있다. 그러나 세밀한 제어가 필요한 엔터프라이즈 환경에서는 Dockerfile이 당분간 표준 자리를 유지할 것이다.

결론적으로 Dockerfile은 컨테이너 이미지 생성의 선언적 명세이자, 이식 가능하고 재현 가능한 배포를 가능하게 하는 IaC의 핵심이다.

- **📢 섹션 요약 비유**: 레시피 카드(Dockerfile)가 잘 쓰여 있으면, 어느 주방에서도 같은 요리가 나온다. 레시피가 CI/CD 파이프라인이라는 요리 기계를 통과하면 자동으로 도시락(이미지)이 완성되어 배달된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Docker Image](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/068_docker_image_immutable_package/) | Dockerfile 빌드의 산출물 |
| [Layered File System (UnionFS)](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/069_layered_file_system_unionfs/) | 레이어 기반 이미지 구조의 저장 기술 |
| [Container Registry](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/070_container_registry_docker_hub_ecr/) | 빌드된 이미지를 저장·배포하는 저장소 |
| [CI/CD Pipeline](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/166_cicd_pipeline_tools/) | Dockerfile 기반 빌드 자동화 |
| IaC (Infrastructure as Code) | Dockerfile의 설계 철학적 기반 |
| Secret Management | 빌드 시 시크릿 안전 주입 방법론 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">수동 서버 설정</div><div class="kb-diagram-note">SSH + 명령어 직접 실행 (재현 불가)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">설치 스크립트</div><div class="kb-diagram-note">Shell Script (부분 자동화, 환경 의존성 여전)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Dockerfile 등장</div><div class="kb-diagram-note">선언적 이미지 빌드 (2013, Docker 0.1)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">멀티 스테이지 빌드</div><div class="kb-diagram-note">빌드/런타임 분리로 경량화 (Docker 17.05+)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">BuildKit</div><div class="kb-diagram-note">병렬 빌드 + 시크릿 안전 주입 (Docker 18.09+)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Cloud Native Buildpacks</div><div class="kb-diagram-note">Dockerfile 없는 자동 이미지 생성</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">미래</div><div class="kb-diagram-note">AI 기반 Dockerfile 최적화 자동화</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 도커파일은 요리 레시피예요. "먼저 재료를 씻고, 다음에 볶고, 마지막에 담아라"고 순서를 적어 두죠.
2. 레시피가 있으면 어느 요리사도 똑같은 요리를 만들 수 있어요. 컴퓨터도 그 레시피대로 자동으로 이미지를 만들어요.
3. 레시피를 잘 적으면 도시락이 가볍고 맛있어요. 레시피를 못 적으면 무겁고 위험한 도시락이 나와요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 66 / 371

← **이전**: [66. 도커 데몬 (Docker Daemon, dockerd) - 컨테이너 라이프사이클 관리 프로세스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/066_docker_daemon_dockerd/)
**다음**: [68. 도커 이미지 (Docker Image) - 불변(Immutable) 상태의 애플리케이션 실행 패키지 파일](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/068_docker_image_immutable_package/) →

---
