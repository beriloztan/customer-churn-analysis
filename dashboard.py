import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

st.set_page_config(page_title="Churn Dashboard", layout="wide")

# Veri ve modeli yükle
df = pd.read_csv('data/customer_summary.csv')
with open('data/churn_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Başlık
st.title("Customer Churn Analysis")
st.markdown("Bu dashboard e-ticaret müşterilerinin churn analizini gösterir.")

# Üst metrikler
col1, col2, col3 = st.columns(3)
col1.metric("Toplam Müşteri", len(df))
col2.metric("Churn Eden", df['churn'].sum())
col3.metric("Churn Oranı", f"%{df['churn'].mean()*100:.1f}")

# Grafikler
col1, col2 = st.columns(2)

with col1:
    fig = px.pie(df, names=df['churn'].map({0: 'Kaldı', 1: 'Gitti'}),
                 title='Churn Dağılımı',
                 color_discrete_sequence=['steelblue', 'tomato'])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.histogram(df, x='toplam_harcama', color=df['churn'].map({0: 'Kaldı', 1: 'Gitti'}),
                        title='Harcama Dağılımı',
                        color_discrete_map={'Kaldı': 'steelblue', 'Gitti': 'tomato'},
                        barmode='overlay', opacity=0.7)
    st.plotly_chart(fig2, use_container_width=True)

# Churn riski yüksek müşteriler
st.subheader("Churn Riski Yüksek Müşteriler")
riskli = df[df['churn'] == 1].sort_values('toplam_harcama', ascending=False).head(10)
st.dataframe(riskli[['Customer ID', 'toplam_siparis', 'toplam_harcama', 'gecen_gun']])

# Churn Tahmin Aracı
st.subheader("Churn Tahmin Aracı")
st.markdown("Bir müşterinin bilgilerini girerek churn riskini tahmin et.")

col1, col2 = st.columns(2)
with col1:
    siparis = st.slider("Sipariş Sayısı", 1, 50, 5)
with col2:
    harcama = st.slider("Toplam Harcama (£)", 0, 10000, 500)

tahmin = model.predict([[siparis, harcama]])[0]
olasilik = model.predict_proba([[siparis, harcama]])[0][1]

if tahmin == 1:
    st.error(f"Yüksek Churn Riski! Olasılık: %{olasilik*100:.1f}")
else:
    st.success(f"Düşük Churn Riski. Olasılık: %{olasilik*100:.1f}")