"""미국 증시 마감 데이터를 받아 글 초안(draft)을 만든다.

초안만 만든다. 해석·코멘트는 사람이 채워 넣고 draft: false 로 바꿔야 발행된다.
자동 생성 글을 그대로 대량 발행하면 애드센스 정책(스팸성 자동 생성 콘텐츠) 위반이다.

사용법:
    python scripts/gen_market_post.py
    python scripts/gen_market_post.py --date 2026-09-14
"""

import argparse
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    sys.exit("yfinance가 필요합니다:  pip install yfinance pandas")

OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "posts"

INDICES = [
    ("^GSPC", "S&P 500"),
    ("^IXIC", "나스닥 종합"),
    ("^DJI", "다우존스"),
    ("^RUT", "러셀 2000"),
    ("^VIX", "VIX 변동성지수"),
]

SECTORS = [
    ("XLK", "기술"),
    ("XLF", "금융"),
    ("XLE", "에너지"),
    ("XLV", "헬스케어"),
    ("XLY", "경기소비재"),
    ("XLP", "필수소비재"),
    ("XLI", "산업재"),
    ("XLU", "유틸리티"),
]

MEGA_CAPS = [
    ("AAPL", "애플"),
    ("MSFT", "마이크로소프트"),
    ("NVDA", "엔비디아"),
    ("GOOGL", "알파벳"),
    ("AMZN", "아마존"),
    ("META", "메타"),
    ("TSLA", "테슬라"),
    ("AVGO", "브로드컴"),
]


def fetch(tickers, period="5d"):
    """종가와 전일 대비 변동률을 반환. 실패한 티커는 건너뛴다."""
    rows = {}
    data = yf.download(
        tickers, period=period, interval="1d", progress=False, auto_adjust=False
    )
    if data.empty:
        return rows

    close = data["Close"]
    if hasattr(close, "columns"):
        cols = list(close.columns)
    else:
        cols = tickers[:1]
        close = close.to_frame(cols[0])

    for tk in cols:
        series = close[tk].dropna()
        if len(series) < 2:
            continue
        last, prev = float(series.iloc[-1]), float(series.iloc[-2])
        rows[tk] = {
            "close": last,
            "chg_pct": (last - prev) / prev * 100 if prev else 0.0,
            "asof": series.index[-1].date(),
        }
    return rows


def table(pairs, quotes, name_label="지표"):
    lines = [f"| {name_label} | 종가 | 전일 대비 |", "| --- | ---: | ---: |"]
    for tk, name in pairs:
        q = quotes.get(tk)
        if not q:
            continue
        sign = "+" if q["chg_pct"] >= 0 else ""
        lines.append(
            f"| {name} ({tk}) | {q['close']:,.2f} | {sign}{q['chg_pct']:.2f}% |"
        )
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="발행일 YYYY-MM-DD (기본: 오늘)")
    args = ap.parse_args()

    pub = (
        datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else date.today()
    )

    print("데이터 수집 중...")
    idx = fetch([t for t, _ in INDICES])
    sec = fetch([t for t, _ in SECTORS])
    mega = fetch([t for t, _ in MEGA_CAPS])

    if not idx:
        sys.exit("데이터를 받지 못했습니다. 네트워크 또는 티커를 확인하세요.")

    asof = max(q["asof"] for q in idx.values())

    movers = sorted(mega.items(), key=lambda kv: kv[1]["chg_pct"], reverse=True)
    gainers = [(tk, tk) for tk, _ in movers[:3]]
    losers = [(tk, tk) for tk, _ in movers[-3:]]

    spx = idx.get("^GSPC", {})
    direction = "상승" if spx.get("chg_pct", 0) >= 0 else "하락"

    body = f"""---
title: '[초안] {asof:%Y년 %m월 %d일} 미국 증시 마감 — S&P 500 {direction} 마감'
description: '{asof:%m월 %d일} 미국 증시 마감 데이터. 주요 지수, 섹터 ETF, 대형주 등락률을 정리했습니다.'
pubDate: {pub:%Y-%m-%d}
category: '시황'
tickers: [{', '.join(f"'{t}'" for t, _ in gainers + losers)}]
tags: ['시황', '마감']
draft: true
---

<!--
  자동 생성된 데이터 초안입니다. 발행 전에 반드시:
  1. 아래 [작성] 표시된 곳에 본인의 해석을 채워 넣으세요
  2. 제목에서 '[초안]'을 지우세요
  3. draft: true 를 false 로 바꾸세요
  데이터만 있는 글은 검색에서도 애드센스 심사에서도 가치를 인정받지 못합니다.
-->

## 주요 지수

{table(INDICES, idx)}

*기준일: {asof:%Y년 %m월 %d일} 미국 증시 정규장 마감 종가 · 출처: Yahoo Finance*

[작성] 지수가 왜 이렇게 움직였는지 한 문단. 그날의 경제지표 발표, 연준 발언, 실적 등 확인 가능한 사실만 적습니다.

## 섹터별 흐름

{table(SECTORS, sec, name_label="섹터")}

*섹터 ETF(SPDR Select Sector) 기준*

[작성] 가장 강했던 섹터와 약했던 섹터를 짚고, 그 배경을 적습니다.

## 대형 기술주

{table(MEGA_CAPS, mega, name_label="종목")}

[작성] 개별 종목 중 특이한 움직임이 있었다면 그 이유를 적습니다. 이유를 확인하지 못했다면 "확인되지 않았다"고 쓰는 편이 낫습니다.

## 오늘 확인할 것

[작성] 다음 거래일에 예정된 지표 발표나 실적 일정.
"""

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{asof:%Y-%m-%d}-market.md"
    path.write_text(body, encoding="utf-8")
    print(f"초안 생성: {path}")
    print("→ [작성] 부분을 채우고 draft: false 로 바꾸면 발행됩니다.")


if __name__ == "__main__":
    main()
