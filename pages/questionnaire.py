import streamlit as st
from utils.db_utils import save_questionnaire

# Ensure user is registered before accessing questionnaire
if "username" not in st.session_state or st.session_state.username is None:
    st.warning("You need to register first.")
    st.stop()

st.title("PHQ-9 and GAD-7 Questionnaire")

# PHQ-9 Questions
phq9_score = 0
st.subheader("PHQ-9: Depression Assessment")
phq9_questions = [
    "Little interest or pleasure in doing things?",
    "Feeling down, depressed, or hopeless?",
    "Trouble falling or staying asleep, or sleeping too much?",
    "Feeling tired or having little energy?",
    "Poor appetite or overeating?",
    "Feeling bad about yourself — or that you are a failure?",
    "Trouble concentrating on things, such as reading the newspaper?",
    "Moving or speaking so slowly that others have noticed?",
    "Thoughts that you would be better off dead or hurting yourself?"
]

for i, question in enumerate(phq9_questions, 1):
    selected_option = st.radio(
        f"Q{i}: {question}",
        ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        index=0,
        key=f"phq9_q{i}"  # ✅ Fix duplicate ID issue
    )
    phq9_score += ["Not at all", "Several days", "More than half the days", "Nearly every day"].index(selected_option)

# GAD-7 Questions
gad7_score = 0
st.subheader("GAD-7: Anxiety Assessment")
gad7_questions = [
    "Feeling nervous, anxious, or on edge?",
    "Not being able to stop or control worrying?",
    "Worrying too much about different things?",
    "Trouble relaxing?",
    "Being so restless that it is hard to sit still?",
    "Becoming easily annoyed or irritable?",
    "Feeling afraid as if something awful might happen?"
]

for i, question in enumerate(gad7_questions, 1):
    selected_option = st.radio(
        f"Q{i}: {question}",
        ["Not at all", "Several days", "More than half the days", "Nearly every day"],
        index=0,
        key=f"gad7_q{i}"  # ✅ Fix duplicate ID issue
    )
    gad7_score += ["Not at all", "Several days", "More than half the days", "Nearly every day"].index(selected_option)

if st.button("Submit"):
    save_questionnaire(st.session_state.username, phq9_score, gad7_score)
    st.success("Questionnaire submitted successfully! Redirecting to dashboard...")
    st.session_state.completed_survey = True
    st.switch_page("pages/dashboard.py")  
