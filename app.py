import streamlit as st
from datetime import date

# -------------------------------
# App Config
# -------------------------------
st.set_page_config(
    page_title="Taskora",
    layout="wide"
)
st.title("📝 Taskora – Smart Task Manager")

# -------------------------------
# Session State Initialization
# -------------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "new_task" not in st.session_state:
    st.session_state.new_task = ""

if "due_date" not in st.session_state:
    st.session_state.due_date = None

# -------------------------------
# Callback: Add Task
# -------------------------------
def add_task():
    if st.session_state.new_task.strip():
        st.session_state.tasks.append({
            "text": st.session_state.new_task,
            "done": False,
            "due": st.session_state.due_date
        })
        # Clear input safely
        st.session_state.new_task = ""
        st.session_state.due_date = None

# -------------------------------
# Input Section
# -------------------------------
st.markdown("### ➕ Add a New Task")

col1, col2 = st.columns([3, 2])

with col1:
    st.text_input(
        "📝 Task description",
        key="new_task"
    )

with col2:
    st.date_input(
        "📅 Due date (optional)",
        key="due_date"
    )

st.button("Add Task", on_click=add_task)

st.divider()

# -------------------------------
# Categorize Tasks
# -------------------------------
today = []
upcoming = []
someday = []

today_date = date.today()

for task in st.session_state.tasks:
    if task["done"]:
        continue

    if task["due"] is None:
        someday.append(task)
    elif task["due"] == today_date:
        today.append(task)
    else:
        upcoming.append(task)

# -------------------------------
# Display Function
# -------------------------------
def display_tasks(title, tasks, section_key, empty_msg):
    st.subheader(title)

    if not tasks:
        st.info(empty_msg)
        return

    for i, task in enumerate(tasks):
        task["done"] = st.checkbox(
            f"{task['text']}"
            + (f" (due {task['due']})" if task["due"] else ""),
            value=task["done"],
            key=f"{section_key}_{i}"
        )

# -------------------------------
# Display Sections
# -------------------------------
display_tasks("📌 Today", today, "today", "Nothing scheduled for today.")
display_tasks("⏳ Upcoming", upcoming, "upcoming", "No upcoming tasks.")
display_tasks("🌙 Someday", someday, "someday", "No someday tasks.")
