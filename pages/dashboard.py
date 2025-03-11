import streamlit as st
import plotly.graph_objects as go
import random
from utils.db_utils import get_questionnaire_scores

st.title("Dashboard")

# Ensure user is logged in
if "username" not in st.session_state:
    st.error("You need to log in first.")
    st.stop()

username = st.session_state.username

# Fetch questionnaire scores
scores = get_questionnaire_scores(username)
if scores:
    phq9_score, gad7_score = scores

    # Maximum possible scores
    max_phq9 = 27  # PHQ-9 max score
    max_gad7 = 21  # GAD-7 max score

    # Generate a random "Miscellaneous Emotions" score (for now)
    misc_emotions_score = random.randint(0, 15)  

    # Function to interpret PHQ-9 scores
    def interpret_phq9(score):
        if score >= 20:
            return "Severe depression 😞"
        elif score >= 15:
            return "Moderately severe depression 😟"
        elif score >= 10:
            return "Moderate depression 😕"
        elif score >= 5:
            return "Mild depression 🙂"
        else:
            return "Minimal or no depression 😃"

    # Function to interpret GAD-7 scores
    def interpret_gad7(score):
        if score >= 15:
            return "Severe anxiety 😨"
        elif score >= 10:
            return "Moderate anxiety 😟"
        elif score >= 5:
            return "Mild anxiety 🙂"
        else:
            return "Minimal or no anxiety 😃"

    st.subheader("Your Mental Health Scores")
    st.write(f"**PHQ-9 Score:** {phq9_score} / 27 → {interpret_phq9(phq9_score)}")
    st.write(f"**GAD-7 Score:** {gad7_score} / 21 → {interpret_gad7(gad7_score)}")
    st.write(f"**Miscellaneous Emotions Score:** {misc_emotions_score} / 15 🌀")

    # PHQ-9 Donut Chart
    fig1 = go.Figure(data=[go.Pie(
        labels=["PHQ-9 Score", "Remaining"],
        values=[phq9_score, max_phq9 - phq9_score],
        hole=0.5,
        marker=dict(colors=["#FF9999", "#DDDDDD"]),
    )])
    fig1.update_layout(title_text="PHQ-9 Score Distribution (Out of 27)")

    # GAD-7 Donut Chart
    fig2 = go.Figure(data=[go.Pie(
        labels=["GAD-7 Score", "Remaining"],
        values=[gad7_score, max_gad7 - gad7_score],
        hole=0.5,
        marker=dict(colors=["#66B3FF", "#DDDDDD"]),
    )])
    fig2.update_layout(title_text="GAD-7 Score Distribution (Out of 21)")

    # PHQ-9 vs GAD-7 Donut Chart
    fig3 = go.Figure(data=[go.Pie(
        labels=["PHQ-9 (Depression)", "GAD-7 (Anxiety)"],
        values=[phq9_score, gad7_score],
        hole=0.5,
        marker=dict(colors=["#FF9999", "#66B3FF"]),
    )])
    fig3.update_layout(title_text="Mental Health Score Comparison")

    # Mental Health Bar Chart
    fig4 = go.Figure(data=[go.Bar(
        x=["Depression (PHQ-9)", "Anxiety (GAD-7)", "Miscellaneous Emotions"],
        y=[phq9_score, gad7_score, misc_emotions_score],
        marker=dict(color=["#FF9999", "#66B3FF", "#FFD700"])
    )])
    fig4.update_layout(
        title_text="Mental Health Scores Comparison",
        xaxis_title="Categories",
        yaxis_title="Scores",
        yaxis=dict(range=[0, max(max_phq9, max_gad7, 15)])  # Set max range dynamically
    )

    # Display charts
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
    with col2:
        st.plotly_chart(fig3)
        st.plotly_chart(fig4)  # Bar graph on the right column

else:
    st.warning("No questionnaire data found. Please complete the questionnaire.")
