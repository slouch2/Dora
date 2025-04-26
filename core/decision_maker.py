# core/decision_maker.py

import openai
from config import OPENAI_API_KEY
from utils.data_collector import collect_data

openai.api_key = OPENAI_API_KEY

# 전략 설명
strategy_context = """
[전략 1: RSI + MACD + 스토캐스틱 + 거래량]
- 스토캐스틱: %K Length=14, %K Smoothing=3, %D Smoothing=3
- K선이 D선을 상향 돌파 시 매수 신호, 하향 돌파 시 매도 신호
- RSI가 중간선(50) 위면 상승 추세 매수 / 아래면 하락 추세 매도
- MACD 파란선이 주황선 위로 교차하면 매수
- 거래량이 30MA 위로 상승해야 매수
- 스토캐스틱 과매도(20)이후 RSI 상승 → MACD 교차 → 거래량 증가 순서 충족시 매수
- 스토캐스틱 K선이 과매수(80) 넘기 전에 조건 성립해야 유효
- 손절: 전 저점 / 익절: 손절가 대비 1.5배

[전략 2: 장기 추세 + 중기 조정 + 단기 진입 통합 전략]
- 200MA 우상향 시 매수 신호 고려, 하향 시 매매 회피
- RSI 40~50 부근 반등 + 스토캐스틱 과매도(20) 후 상향 돌파 시 매수 신호
- MACD 골든크로스, 20EMA>50EMA 상향 돌파, 볼린저 하단 이탈 후 복귀 패턴 매수
- 20일 평균 거래량 대비 1.5배 이상 거래량 터질 때만 신호 인정
- 극단적 공포(Fear) 구간 매수 강화
- 진입 시 손익비 1.5 이상 자리만 / 5% 수익 발생시 절반 익절 후 나머지 트레일링 스탑 운영
- 리스크는 전체 자산 대비 1~2% 이내 고정, 추세 붕괴 시 강제 청산
"""

# 투자 철학 설명
investment_philosophy = """
- 상장 5년 이상 경과한 코인만 거래한다.
- 변동성이 높더라도 승률이 유지되면 매매할 수 있다.
- 손실을 감수할 준비가 없는 자리에는 매매하지 않는다.
- 확신 없는 경우 절대 매매하지 않는다.
- 수수료 및 OpenAI 비용까지 고려했을 때 순수익 가능성이 충분히 높을 경우에만 매매한다.
- 시장 컨디션 악화 시 매매를 전면 중단할 수 있다.
- 일시적 변동성에 흔들리지 않는다.
- 총 자산 대비 특정 종목에 과도한 비율을 베팅하지 않는다.
- 매매하지 않는 것도 적극적 전략이다.
- 매매 이유는 간결히 보고하되 내부적으로 깊이 분석한다.
"""

async def make_decision(coin, _):
    # 1. 데이터 수집
    strategy_data = collect_data(coin)

    # 2. 프롬프트 작성
    prompt = f"""
You're an expert in coin investing. 
Based on the following strategies, market data, and investment philosophy, analyze and tell us whether to BUY, SELL, or HOLD the given coin.

Rules:
- Provide a SHORT and LOGICAL reason (1-3 sentences maximum).
- Only recommend BUY if the probability of making a profit is significantly high, even after considering transaction fees and API costs.
- If the conditions are not ideal for a profitable trade, recommend HOLD instead of forcing a trade.

Strategy:
{strategy_context}

Investment Philosophy:
{investment_philosophy}

Coin: {coin}
Data: {strategy_data}
"""

    # 3. OpenAI 요청
    response = openai.ChatCompletion.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {"role": "system", "content": "You are a professional cryptocurrency investor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    reply = response['choices'][0]['message']['content'].lower()

    # 4. 결과 파싱
    if "buy" in reply:
        return "buy", reply
    elif "sell" in reply:
        return "sell", reply
    else:
        return "hold", reply
