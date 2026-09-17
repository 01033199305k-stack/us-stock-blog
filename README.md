# 미국주식 데이터랩

미국주식 콘텐츠 + 애드센스 수익화용 정적 사이트. Astro 기반, Cloudflare Pages 무료 호스팅.

## 명령어

```sh
npm run dev      # 로컬 미리보기 http://localhost:4321
npm run build    # dist/ 로 정적 빌드
npm run preview  # 빌드 결과 확인

python scripts/gen_market_post.py             # 오늘 마감 데이터로 초안 생성
python scripts/gen_market_post.py --date 2026-09-14
```

---

## 돈이 되기까지 — 순서대로

### 1단계. 도메인 구입 (필수, 연 1~2만원)

**애드센스는 `.pages.dev` 같은 무료 서브도메인으로는 거의 승인되지 않습니다.** 자기 도메인이 있어야 합니다.

- 추천: [Cloudflare Registrar](https://domains.cloudflare.com) (원가 판매, 갱신가 인상 없음) 또는 가비아
- `.com` 기준 연 12~15,000원
- 주식/투자와 연관된 짧은 영문 이름 권장

구입 후 `src/consts.js`의 `SITE.url`과 `public/robots.txt`의 Sitemap 주소를 실제 도메인으로 바꾸세요.

### 2단계. Cloudflare Pages 배포 (무료)

1. 이 폴더를 GitHub 저장소로 올립니다
2. [Cloudflare Pages](https://pages.cloudflare.com) → Create a project → 저장소 연결
3. 빌드 설정:
   - Framework preset: **Astro**
   - Build command: `npm run build`
   - Build output directory: `dist`
4. 배포 후 Custom domains에서 1단계 도메인 연결

이후 `git push` 할 때마다 자동 재배포됩니다.

### 3단계. 콘텐츠 20~30개 쌓기 (여기가 진짜 일)

애드센스 심사는 **콘텐츠 분량과 질**로 갈립니다. 특히 주식은 구글이 YMYL(돈·건강 관련)로 분류해 일반 주제보다 심사가 깐깐합니다.

- 글 1개당 최소 1,500자 이상, 데이터 표 포함
- `투자기초` 카테고리 글을 먼저 채우는 게 안전합니다 (심사 통과율이 높음)
- **자동 생성 초안을 그대로 대량 발행하면 안 됩니다.** 애드센스 정책상 "스팸성 자동 생성 콘텐츠"에 해당해 계정이 거절·정지될 수 있습니다. `gen_market_post.py`가 `draft: true`로 만드는 이유입니다. `[작성]` 부분에 본인 해석을 채우고 `draft: false`로 바꿔야 발행됩니다.

### 4단계. 구글 서치콘솔 등록

- [Search Console](https://search.google.com/search-console) → 도메인 등록
- `https://도메인/sitemap-index.xml` 제출 (빌드 시 자동 생성됨)
- 색인이 시작돼야 트래픽이 생기고, 트래픽이 있어야 광고 수익이 납니다

### 5단계. 애드센스 신청

1. [AdSense](https://adsense.google.com) 가입 → 사이트 추가
2. 승인되면 게시자 ID(`ca-pub-...`)와 광고 단위 slot ID를 받습니다
3. `src/consts.js`의 `ADSENSE.client`와 `slots`에 넣습니다
4. `public/ads.txt`의 `pub-0000000000000000`도 본인 ID로 교체 (이거 빠지면 수익 제한)
5. `git push` → 광고 자동 노출

심사는 보통 1~2주, 거절되면 콘텐츠 보강 후 재신청할 수 있습니다.

---

## 현실적인 기대치

| 시점 | 상태 |
| --- | --- |
| 1개월 | 글 20~30개, 애드센스 신청 가능. 수익 0원 |
| 3개월 | 색인 안정화, 일 방문자 수십~수백. 월 몇천~몇만원 |
| 6개월+ | 검색 유입이 붙기 시작. 글 수와 거의 비례 |

애드센스 블로그는 **글 개수가 수익을 결정**합니다. 빠른 돈이 아니라 쌓이는 자산 쪽입니다.

## 콘텐츠 작성 원칙 (중요)

**뉴스 사이트는 소재를 찾는 용도로만 씁니다. 기사를 옮겨 쓰지 않습니다.**

애드센스 정책의 `스크랩된 콘텐츠` 항목은 "타 사이트 콘텐츠를 약간 수정해 게시하는 행위"를 금지합니다. 문장을 바꿔 써도 동일하게 걸리고, 이게 애드센스 거절 사유 1위입니다.

### 올바른 순서

1. **소재 탐지** — 뉴스에서 "오늘 시장이 뭘 보고 있나"만 파악
2. **1차 출처에서 직접 검증** — 여기서 얻은 숫자가 글의 근거가 됩니다
   - 주가·지수·금리 → yfinance (`^TNX`, `^GSPC` 등)
   - 국채 금리 → [미 재무부](https://home.treasury.gov/resource-center/data-chart-center/interest-rates), FRED
   - 기업 실적 → 기업 IR 페이지, [SEC EDGAR](https://www.sec.gov/edgar)
3. **독자적 해석을 쓴다** — 검증한 수치에 기준일과 출처를 붙이고, 구조와 분석은 새로 작성

### 소재 고르는 기준

**좋은 소재** — 숫자로 떨어져 원본 검증이 가능하고 금융 광고 단가가 높음
- 금리, 유가, 환율, 지수 움직임, 실적 발표

**피할 소재**
- `(카더라)` 류 미확인 루머 — 검증이 불가능하면 쓰지 않습니다
- 교차 확인 안 된 지정학 뉴스 (특히 분쟁 당사국 국영매체 단독 보도)
- 정치 발언 기사 — 광고 단가가 낮고 심사에도 불리합니다

참고 예시: `src/content/posts/10y-yield-and-stocks.md` — 뉴스에서 "10년물 금리 화제"라는 힌트만 얻고, 시계열은 직접 조회해 검증한 뒤 분석 구조는 새로 쓴 글입니다.

## 구조

```
src/
├── consts.js              # 사이트명·도메인·애드센스 ID (여기만 고치면 됨)
├── content.config.ts      # 글 메타데이터 스키마
├── content/posts/*.md     # 글 (draft: true 면 발행 안 됨)
├── layouts/BaseLayout.astro   # SEO 메타·JSON-LD·애드센스 스크립트
├── components/AdSlot.astro    # 광고 슬롯
└── pages/
    ├── index.astro / posts/   # 목록·본문
    ├── about, contact, privacy, disclaimer   # 애드센스 심사 필수 페이지
    └── rss.xml.js
scripts/gen_market_post.py     # yfinance 마감 데이터 → 초안
public/{robots.txt, ads.txt}
```

## 발행 전 체크리스트

- [ ] `src/consts.js` — 도메인, 사이트명 교체
- [ ] `src/pages/contact.astro` — 이메일 주소 교체 (개인 메일 말고 사이트 전용 권장)
- [ ] `public/robots.txt` — Sitemap 도메인 교체
- [ ] `public/ads.txt` — 애드센스 승인 후 게시자 ID 교체
