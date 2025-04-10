import pandas as pd
import streamlit as st

def calculate_arbitrage_profit(price_binance, price_okx, qty, rate_binance, rate_okx, days, fee_binance=0.0, fee_okx=0.0):
    data = {
        "平台": ["币安（多单）", "OKX（空单）"],
        "方向": ["开多", "开空"],
        "价格（USDT）": [price_binance, price_okx],
        "数量（BABY）": [qty, qty],
        "资金费率（年化）": [rate_binance, rate_okx],
        "持仓天数": [days, days],
        "手续费率": [fee_binance, fee_okx]
    }

    df = pd.DataFrame(data)
    df["每日资金费率收益（USDT）"] = df["价格（USDT）"] * df["数量（BABY）"] * (df["资金费率（年化）"] / 365)
    df["总资金费率收益（USDT）"] = df["每日资金费率收益（USDT）"] * df["持仓天数"]
    df["手续费成本（USDT）"] = df["价格（USDT）"] * df["数量（BABY）"] * df["手续费率"]
    df["总收益（USDT）"] = df["总资金费率收益（USDT）"] - df["手续费成本（USDT）"]
    total_profit = df["总收益（USDT）"].sum()

    return df, total_profit

# Streamlit UI
st.title("跨平台套利收益计算器")

price_binance = st.number_input("币安价格 (USDT)", value=0.084, step=0.001)
price_okx = st.number_input("OKX价格 (USDT)", value=0.083, step=0.001)
qty = st.number_input("开仓数量（BABY）", value=540000)
days = st.number_input("持仓天数", value=1)
rate_binance = st.number_input("币安资金费率（年化）", value=0.02)
rate_okx = st.number_input("OKX资金费率（年化）", value=-0.005)
fee_binance = st.number_input("币安手续费率", value=0.0002)  # 0.02%
fee_okx = st.number_input("OKX手续费率", value=0.0005)  # 0.05%

if st.button("计算套利利润"):
    df_result, total_profit = calculate_arbitrage_profit(
        price_binance, price_okx, qty,
        rate_binance, rate_okx, days,
        fee_binance, fee_okx
    )
    st.dataframe(df_result)
    st.success(f"总套利利润：{total_profit:.2f} USDT")
