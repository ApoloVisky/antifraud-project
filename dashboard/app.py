import streamlit as st
import pandas as pd
import time
import plotly.express as px

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🚨",
    layout="wide"
)

# CSS customizado
st.markdown("""
<style>
body {
    background-color: #0E1117;
}

.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
}

.metric-title {
    font-size: 18px;
    color: #AAAAAA;
}

.metric-value {
    font-size: 36px;
    font-weight: bold;
    color: white;
}

.header {
    font-size: 36px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">🚨 Real-Time Fraud Detection Dashboard</div>', unsafe_allow_html=True)
st.write("Pipeline Streaming + Machine Learning")

placeholder = st.empty()

while True:
    try:
        df = pd.read_csv("stream_results.csv")

        total = len(df)
        frauds = df["fraud_prediction"].sum()
        fraud_rate = round((frauds / total) * 100, 2) if total > 0 else 0

        with placeholder.container():

            col1, col2, col3 = st.columns(3)

            col1.markdown(f"""
            <div class="card">
                <div class="metric-title">Total de Transações</div>
                <div class="metric-value">{total}</div>
            </div>
            """, unsafe_allow_html=True)

            col2.markdown(f"""
            <div class="card">
                <div class="metric-title">Fraudes Detectadas</div>
                <div class="metric-value">{int(frauds)}</div>
            </div>
            """, unsafe_allow_html=True)

            col3.markdown(f"""
            <div class="card">
                <div class="metric-title">Taxa de Fraude (%)</div>
                <div class="metric-value">{fraud_rate}%</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            fig = px.histogram(
                df,
                x="fraud_prediction",
                color="fraud_prediction",
                title="Distribuição de Transações (0 = Normal | 1 = Fraude)",
                nbins=2
            )

            fig.update_layout(
                plot_bgcolor="#1c1f26",
                paper_bgcolor="#1c1f26",
                font_color="white"
            )

            st.plotly_chart(fig, use_container_width=True)

            st.markdown("### 📋 Últimas Transações Processadas")

            st.dataframe(
                df.tail(15),
                use_container_width=True,
                height=400
            )

        time.sleep(2)

    except Exception as e:
        st.warning("⏳ Aguardando dados do pipeline...")
        time.sleep(2)
