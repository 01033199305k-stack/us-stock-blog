// 사이트 전역 설정. 도메인/애드센스 ID를 받으면 이 파일만 고치면 됩니다.

export const SITE = {
  // TODO: 도메인 구입 후 실제 주소로 교체 (애드센스 심사 전 반드시 변경)
  url: 'https://us-stock-blog.pages.dev',
  title: '미국주식 데이터랩',
  tagline: '데이터로 먼저 확인하는 미국주식',
  description:
    '미국주식 시황과 종목을 지표 데이터로 검증해 정리합니다. 밸류에이션, 수급, 실적 추이를 매일 업데이트합니다.',
  author: '강민혁',
  locale: 'ko_KR',
  lang: 'ko',
};

export const ADSENSE = {
  // 게시자 ID (승인 완료 후 광고 슬롯 ID는 아래 slots에 추가)
  client: 'ca-pub-9852386681125742',
  slots: {
    inArticle: '',
    belowTitle: '',
    footer: '',
  },
};

export const NAV = [
  { href: '/', label: '홈' },
  { href: '/posts', label: '전체 글' },
  { href: '/about', label: '소개' },
  { href: '/contact', label: '문의' },
];
