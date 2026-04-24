# Customer Churn Analysis & Prediction

## Problem
E-ticaret şirketleri müşteri kaybını (churn) genellikle geç fark eder. Bu proje, 
bir e-ticaret şirketinin satış verisini kullanarak hangi müşterilerin churn riski 
taşıdığını önceden tespit etmeyi ve aksiyon önerileri sunmayı amaçlar.

## Dataset
- **Kaynak:** UCI Machine Learning Repository – Online Retail II
- **Kapsam:** 2009-2010 yılları arası gerçek e-ticaret satış verisi
- **Boyut:** 525.000+ işlem, 4.314 benzersiz müşteri

## Yaklaşım

### 1. Veri Temizleme & Keşif (EDA)
- İade işlemleri ve müşteri ID'si olmayan kayıtlar temizlendi
- Müşteri bazında sipariş sayısı, toplam harcama ve aktiflik süresi hesaplandı

### 2. Churn Tanımı
Son 90 gün içinde alışveriş yapmayan müşteriler "churn etmiş" olarak etiketlendi.
- Churn eden müşteri: **1.429 (%33.1)**
- Aktif müşteri: **2.885 (%66.9)**

### 3. Churn Tahmini
Logistic Regression modeli ile churn tahmini yapıldı.
- **Doğruluk:** %73
- Az harcayan ve az sipariş veren müşterilerin churn riski belirgin şekilde yüksek

### 4. Aksiyon Önerileri
| Segment | Durum | Öneri |
|---|---|---|
| Yüksek harcama + churn riski | 34.000£ harcayıp 267 gündür gelmiyor | Kişisel indirim kampanyası |
| Düşük sipariş sayısı | 1-2 sipariş sonrası kaybediliyor | Onboarding e-mail serisi |
| Orta segment | Düzenli ama az harcıyor | Loyalty programı |

### 4. Model Interpretability (SHAP)
- Used SHAP LinearExplainer to explain model decisions
- **toplam_siparis** is the dominant feature — low order count strongly increases churn probability
- Individual customer explanations show exactly why the model flagged each customer as high risk
- Key insight: Order frequency matters more than total spending for churn prediction

## Sonuç
Modelin tespit ettiği yüksek riskli müşterilere yönelik proaktif kampanyalar 
yapılsaydı, müşteri kaybının önemli bir kısmı önlenebilirdi.

## Kurulum

```bash
pip install -r requirements.txt
streamlit run dashboard.py
Proje Yapısı
customer-churn-analysis/
├── data/
│   ├── online_retail.xlsx
│   └── customer_summary.csv
├── notebooks/
│   ├── 1_EDA.ipynb
│   └── 2_Churn_Model.ipynb
├── dashboard.py
└── README.md
Araçlar
Python • pandas • scikit-learn • Streamlit • Plotly