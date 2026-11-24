
import streamlit as st
import pandas as pd
from pathlib import Path
DATA_FILE = Path("mistakes.csv")
TOPICS = {
    "Maths": ["Algebra", "Advanced Math", "Geometry", "Trigonometry", "Data Analysis"],
    "Reading and Writing": ["Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"]
}

st.title("ExamPulse")
test_name = st.text_input("Test name")
subject = st.selectbox ("Subject", ["Maths", "Reading and Writing"])

with st.form("mistake_form", clear_on_submit=True):
    topic = st.selectbox("Topic", TOPICS[subject])
    category = st.selectbox("Mistake category", ["Conceptual Gap","Careless Calculation","Time Crunch"])
    fix = st.text_area("The fix (what did you miss?)")
    submitted = st.form_submit_button("Save Mistake")
if submitted:
    new_row = pd.DataFrame([{
        "Test": test_name,
        "Subject": subject,
        "Topic": topic,
        "Category": category,
        "Fix": fix,
    }])
    if DATA_FILE.exists():
        old_data = pd.read_csv(DATA_FILE)
        combined = pd.concat([old_data, new_row], ignore_index =True)
    else:
        combined= new_row
    combined.to_csv(DATA_FILE, index=False)
    st.success("Saved!")

st.divider()
st.subheader("Your saved mistakes")

if DATA_FILE.exists():
    saved= pd.read_csv(DATA_FILE)
    filter_subject = st.selectbox("Filter by subject", ["All", "Maths", "Reading and Writing"])
    filter_category = st.selectbox("Filter by category", ["All", "Conceptual Gap", "Careless Calculation", "Time Crunch"])

    filtered = saved
    if filter_subject != "All":
        filtered = filtered[filtered["Subject"] == filter_subject]
    if filter_category != "All":
        filtered = filtered[filtered["Category"] == filter_category]

    st.write("Showing", len(filtered), "of", len(saved), "mistakes")
    st.dataframe(filtered, width="stretch", hide_index=True)

    st.divider()
    st.subheader("Where you lose marks")
    counts = saved["Category"].value_counts()
    st.bar_chart(counts)
    top_category = counts.index[0]
    top_count = counts.iloc[0]
    percent = round(top_count / len(saved)*100)
    st.info(f"{percent}% of your mistakes are: {top_category}")

    st.divider()
    st.subheader("Your weakest topics")
    topic_counts = saved["Topic"].value_counts().head(5)
    st.bar_chart(topic_counts)

    st.divider()
    st.subheader("Re-solve mode")

    if len(filtered) == 0:
        st.info("No mistakes match your filters")
    else:
        if "position" not in st.session_state:
            st.session_state.position = 0

        number = st.session_state.position % len(filtered)
        row = filtered.iloc[number]

        st.write("Test:", row["Test"])
        st.write("Topic:", row["Topic"])
        st.write("Type:", row["Category"])

        with st.expander(f"Show the fix for mistake {number + 1} of {len(filtered)}"):
            st.write(row["Fix"])

        if st.button("Next mistake"):
            st.session_state.position += 1
            st.rerun()
else:
    st.info("No mistakes saved yet.")

