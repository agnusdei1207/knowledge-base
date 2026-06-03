+++
title = "🌐 Quartz를 이용한 사내 위키 웹 사이트 배포 가이드"

[taxonomies]
tags = ["work"]

[extra]
tags = ["work"]
+++

Quartz는 마크다운 저장소를 활용해 초고속 웹 브라우저 뷰어를 만들어주는 최적의 동반자입니다.

[GitHub에서 이 문서 수정](https://github.com/agnusdei1207/knowledge-base/edit/main/content/quartz-deployment.md)

---

## 🛠️ GitHub Actions를 이용한 무상 배포 (정석)

GitHub Pages를 통해 별도의 웹서버를 구축하지 않고도 무료로 실시간 위키 사이트를 배포할 수 있습니다.

1. **레포지토리 설정 변경:** 
   * GitHub 레포지토리 Settings -> Pages 탭 진입
   * Build and deployment -> Source를 <strong>GitHub Actions</strong>로 변경
2. **GitHub Workflow 파일 생성:**
   * `.github/workflows/deploy.yml` 파일 생성 (자동 생성 스크립트 실행 시 셋팅 가능)
3. **배포 확인:**
   * 이제 마크다운 문서를 쓰고 깃허브에 `git push`하기만 하면 약 1분 뒤에 `https://<organization>.github.io/<repository>` 경로에 검색과 인터랙티브 노드 그래프가 연동된 고급 웹 위키가 즉시 배포됩니다!

---

## 🐳 Docker Compose를 이용한 로컬 프리뷰 실행

로컬 서버 또는 사내 가상머신(VM)에서 실시간 그래프와 검색창이 있는 웹 위키를 띄워 테스트하거나 전사에 직접 호스팅할 수 있습니다.

이 방식은 저장소에 Quartz 엔진 소스를 풀어두지 않고, 컨테이너 안에서만 Quartz를 내려받아 실행합니다. 저장소에는 계속 `content/`와 설정 파일만 유지되고, 로컬에 `package.json`이나 `node_modules` 같은 빌드 파일을 남기지 않습니다.

### 1. 로컬 실행 방법
1. 저장소 폴더로 진입합니다.
   ```bash
   cd /home/user/knowledgebase
   ```
2. Docker Compose 명령어를 실행하여 컨테이너를 백그라운드에서 구동합니다.
   ```bash
   docker compose up -d
   ```
3. 도커 컨테이너가 Quartz 소스를 내려받고 컨테이너 내부에서만 의존성을 설치한 뒤 서버를 구동합니다.

### 2. 웹 접속 및 확인
* 브라우저를 열고 다음 주소로 접속합니다.
  ```text
  http://localhost:8080   (또는 http://<사내서버IP>:8080)
  ```
* 마크다운 문서 내용과 오른쪽 그래프 뷰가 연동된 웹 위키를 확인할 수 있습니다.

### 3. 컨테이너 중지 방법
테스트를 마치고 서버를 내리고 싶다면 아래 명령어를 입력하세요.
```bash
docker compose down
```
