# 🌐 Knowledgebase Web App

1인 회사를 위한 통합 지식 자산 뷰어. Vercel에 배포.

## 구조

```
web/
├─ app/              Next.js App Router (페이지 + API)
├─ components/       React 컴포넌트
├─ lib/              서버 유틸 (auth, YAML reader)
├─ scripts/          빌드 스크립트 (data 동기화)
└─ data/             ← 빌드 시 자동 생성 (gitignore)
```

`data/` 폴더는 `../data/` (레포 루트)에서 빌드 시 자동 복사됩니다. 원본은 항상 레포 루트 `data/`에 두세요.

## 로컬 개발

```bash
cd web
cp .env.example .env.local
# .env.local 편집 (GITHUB_ID, GITHUB_SECRET, NEXTAUTH_SECRET)
npm install
npm run dev
# → http://localhost:3000
```

## Vercel 배포

1. Vercel에서 GitHub repo import
2. Build Settings:
   - Framework: **Next.js**
   - Root Directory: **`web`**
   - Build/Output/Install: 기본값
3. Environment Variables (Settings → Environment Variables):
   - `GITHUB_ID`, `GITHUB_SECRET`, `NEXTAUTH_SECRET`
   - `NEXTAUTH_URL` = 배포 도메인
4. GitHub OAuth App의 callback URL에 `https://<domain>/api/auth/callback/github` 추가
