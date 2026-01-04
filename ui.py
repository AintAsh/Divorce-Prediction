import streamlit as st
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import time

# ==================================================
# CONFIG
# ==================================================
API_URL = "https://divorce-prediction-34ru.onrender.com/predict/"  

st.set_page_config(
    page_title="Relationship Insight Analyzer",
    page_icon="💔",
    layout="wide"
)

# ==================================================
# THEME (FROSTED GLASS + NATURAL TONES)
# ==================================================
st.markdown("""
<style>
html, body {
    background: radial-gradient(circle at top, #0f766e, #020617);
    color: #e5e7eb;
}

.glass {
    background: rgba(255,255,255,0.10);
    backdrop-filter: blur(18px);
    border-radius: 24px;
    padding: 26px;
    margin-bottom: 26px;
    border: 1px solid rgba(255,255,255,0.25);
    box-shadow: 0 0 22px rgba(45,212,191,0.28);
}

.metric {
    background: rgba(255,255,255,0.14);
    border-radius: 18px;
    padding: 18px;
    text-align: center;
}

.tip {
    background: rgba(0,0,0,0.35);
    padding: 14px;
    border-left: 4px solid #5eead4;
    border-radius: 12px;
    margin-bottom: 10px;
}

.scale-bar {
    height: 14px;
    border-radius: 10px;
    background: linear-gradient(90deg, #22c55e, #eab308, #ef4444);
}

button[kind="primary"] {
    background: linear-gradient(135deg,#14b8a6,#2dd4bf);
    color: black;
    font-weight: 700;
    border-radius: 18px;
    height: 55px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HERO
# ==================================================
st.markdown("""
<div class="glass">
<h1>💔 Relationship Insight Analyzer</h1>
<p>
A reflective AI tool designed to highlight relationship stress patterns
with care, clarity, and responsibility.
</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR INPUTS (PROGRESSIVE)
# ==================================================
st.sidebar.header("🧾 Relationship Details")

with st.sidebar.expander("👤 Personal", expanded=True):
    age_at_marriage = st.slider("Age at marriage", 18, 60, 25)
    marriage_duration_years = st.slider("Years married", 0, 40, 5)
    num_children = st.slider("Children", 0, 5, 1)
    education_level = st.selectbox("Education", ["High School","Bachelor","Master","PhD"])
    employment_status = st.selectbox("Employment", ["Unemployed","Employed","Self-employed"])
    combined_income = st.number_input("Combined income", min_value=0, value=500000)

with st.sidebar.expander("💬 Communication"):
    communication_score = st.slider("Communication quality", 1, 10, 7)
    conflict_frequency = st.slider("Conflict frequency", 1, 10, 4)
    conflict_resolution_style = st.selectbox("Conflict handling", ["Calm","Aggressive","Avoidant"])

with st.sidebar.expander("❤️ Trust & Stress"):
    trust_score = st.slider("Trust level", 1, 10, 7)
    financial_stress_level = st.slider("Financial stress", 1, 10, 5)
    social_support = st.slider("Social support", 1, 10, 6)
    shared_hobbies_count = st.slider("Shared hobbies", 0, 10, 3)

with st.sidebar.expander("⚠️ Sensitive"):
    religious_compatibility = st.selectbox("Religious compatibility", ["Yes","No"])
    cultural_background_match = st.selectbox("Cultural match", ["Yes","No"])
    mental_health_issues = st.selectbox("Mental health issues", ["Yes","No"])
    infidelity_occurred = st.selectbox("Infidelity history", ["Yes","No"])
    counseling_attended = st.selectbox("Counseling attended", ["Yes","No"])
    marriage_type = st.selectbox("Marriage type", ["Love","Arranged"])
    pre_marital_cohabitation = st.selectbox("Lived together before marriage", ["Yes","No"])
    domestic_violence_history = st.selectbox("Domestic violence history", ["Yes","No"])

data = {
    "age_at_marriage": age_at_marriage,
    "marriage_duration_years": marriage_duration_years,
    "num_children": num_children,
    "education_level": education_level,
    "employment_status": employment_status,
    "combined_income": combined_income,
    "religious_compatibility": religious_compatibility,
    "cultural_background_match": cultural_background_match,
    "communication_score": communication_score,
    "conflict_frequency": conflict_frequency,
    "conflict_resolution_style": conflict_resolution_style,
    "financial_stress_level": financial_stress_level,
    "mental_health_issues": mental_health_issues,
    "infidelity_occurred": infidelity_occurred,
    "counseling_attended": counseling_attended,
    "social_support": social_support,
    "shared_hobbies_count": shared_hobbies_count,
    "marriage_type": marriage_type,
    "pre_marital_cohabitation": pre_marital_cohabitation,
    "domestic_violence_history": domestic_violence_history,
    "trust_score": trust_score
}

# ==================================================
# PREDICT
# ==================================================
if st.button("✨ ANALYZE RELATIONSHIP", use_container_width=True):

    with st.spinner("Analyzing relationship patterns…"):
        time.sleep(0.9)
        response = requests.post(API_URL, json=data)

    result = response.json()

    if "error" in result:
        st.error("API Error")
        st.json(result)
        st.stop()

    prob = result["probability"]
    risk = result["risk_level"]

    # ==================================================
    # RESULT OVERVIEW
    # ==================================================
    st.markdown("<div class='glass'><h2>📊 Result Overview</h2></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div class='metric'><h3>Risk Level</h3><h2>{risk}</h2></div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='metric'><h3>Probability</h3><h2>{prob:.2%}</h2></div>", unsafe_allow_html=True)

    with col3:
        confidence = abs(prob - 0.5) * 2
        st.markdown(
            f"<div class='metric'><h3>Model Confidence</h3><h2>{confidence:.2%}</h2></div>",
            unsafe_allow_html=True
        )

    # ==================================================
    # RISK SCALE
    # ==================================================
    st.markdown("<div class='glass'><h3>Risk Interpretation</h3></div>", unsafe_allow_html=True)
    st.markdown("<div class='scale-bar'></div>", unsafe_allow_html=True)
    st.caption("Low (0–40%) • Moderate (40–70%) • High (70–100%)")

    # ==================================================
    # INTERACTIVE PIE CHART
    # ==================================================
    pie_fig = px.pie(
        values=[prob, 1 - prob],
        names=["Stress Indicators", "Stability Indicators"],
        hole=0.45,
        color_discrete_sequence=["#f97316", "#22c55e"]
    )
    st.plotly_chart(pie_fig, use_container_width=True)

    # ==================================================
    # SMALL BAR CHART (FROSTED STYLE)
    # ==================================================
    # ==================================================
    # ULTRA-INFORMATIVE SMALL FROSTED BAR CHART
    # ==================================================
    st.markdown(
        "<div class='glass'>"
        "<h3 style='margin-bottom:6px'>Key Stress Contributors</h3>"
        "<p style='font-size:12px; opacity:0.8'>"
        "Scores reflect how strongly each factor contributes to relationship stress (0–10)"
        "</p>"
        "</div>",
        unsafe_allow_html=True
    )
    
    _, bar_col, _ = st.columns([1, 1.4, 1])
    
    stress_data = {
        "Comm": 10 - communication_score,
        "Trust": 10 - trust_score,
        "Conflict": conflict_frequency,
        "Finance": financial_stress_level
    }
    
    def severity(val):
        if val <= 3:
            return "Low", "#22c55e"
        elif val <= 6:
            return "Moderate", "#eab308"
        else:
            return "High", "#ef4444"
    
    labels = []
    colors = []
    for v in stress_data.values():
        level, color = severity(v)
        labels.append(level)
        colors.append(color)
    
    with bar_col:
        fig, ax = plt.subplots(figsize=(2.6, 1.9), dpi=140)
    
        # Fully transparent canvas
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
    
        bars = ax.bar(
            stress_data.keys(),
            stress_data.values(),
            color=colors,
            width=0.55
        )
    
        # Value + severity label
        for bar, lvl in zip(bars, labels):
            h = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + 0.15,
                f"{int(h)} • {lvl}",
                ha="center",
                va="bottom",
                fontsize=6.5,
                color="#e5e7eb"
            )
    
        # Axes formatting
        ax.set_ylim(0, 10)
        ax.set_yticks([0, 5, 10])
        ax.tick_params(axis="x", colors="#d1fae5", labelsize=7)
        ax.tick_params(axis="y", colors="#99f6e4", labelsize=6)
    
        for spine in ax.spines.values():
            spine.set_visible(False)
    
        ax.grid(axis="y", linestyle="--", alpha=0.15, color="#99f6e4")
    
        ax.set_title(
            "Stress Intensity Scale",
            fontsize=8,
            color="#e5e7eb",
            pad=4
        )
    
        st.pyplot(fig, use_container_width=False)
    
    # ==================================================
    # MICRO-INSIGHT (THIS IS KEY)
    # ==================================================
    highest_factor = max(stress_data, key=stress_data.get)
    highest_value = stress_data[highest_factor]
    highest_level, _ = severity(highest_value)

    st.markdown(
        f"<div class='tip'>"
        f"🔍 <b>{highest_factor}</b> shows the strongest stress signal "
        f"(<b>{highest_level}</b>). Addressing this area may have the "
        f"greatest positive impact."
        f"</div>",
        unsafe_allow_html=True
    )

    # ==================================================
    # PERSONALIZED INSIGHTS
    # ==================================================
    st.markdown("<div class='glass'><h2>🧠 Personalized Insights</h2></div>", unsafe_allow_html=True)

    insights = []
    if communication_score < trust_score:
        insights.append("Communication appears weaker than trust — strengthening dialogue may help.")
    if financial_stress_level > 6:
        insights.append("Higher financial stress may be affecting emotional balance.")
    if conflict_frequency > 6:
        insights.append("Frequent conflicts can increase long-term relationship strain.")

    if not insights:
        insights.append("Overall balance between trust, communication, and stress appears healthy.")

    for i in insights:
        st.markdown(f"<div class='tip'>🌱 {i}</div>", unsafe_allow_html=True)

    st.caption("ℹ️ This tool provides probabilistic insights, not certainties.")


