import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Pet Care Planner")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input(
    "Available care time (minutes)", min_value=0, max_value=1440, value=60
)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
breed = st.text_input("Breed", value="mixed breed")
age = st.number_input("Age", min_value=0, max_value=100, value=3)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name, int(available_minutes))

owner = st.session_state.owner
owner.name = owner_name
owner.update_availability(int(available_minutes))

if st.button("Add pet"):
    if any(pet.name == pet_name for pet in owner.list_pets()):
        st.warning("That pet is already in the owner's profile.")
    else:
        owner.add_pet(Pet(pet_name, species, breed, int(age), owner))
        st.success(f"Added {pet_name} to {owner.name}'s pets.")

if owner.list_pets():
    st.write("Pets:", ", ".join(pet.name for pet in owner.list_pets()))

st.markdown("### Tasks")
st.caption("Add tasks to a pet, then generate a plan from the owner's available time.")

if not owner.list_pets():
    st.info("Add a pet before adding care tasks.")
    task_pet = None
else:
    task_pet = st.selectbox("Pet for this task", owner.list_pets(), format_func=lambda pet: pet.name)

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task") and task_pet is not None:
    task = Task(task_title, int(duration), "daily")
    task.priority = priority
    task_pet.add_task(task)

tasks = owner.get_all_tasks()
if tasks:
    scheduler = Scheduler(owner)
    task_view = st.selectbox(
        "Show tasks",
        ["All", "Incomplete", "Completed"],
    )
    completion_filter = {
        "All": None,
        "Incomplete": False,
        "Completed": True,
    }[task_view]
    visible_tasks = scheduler.sort_by_time(
        scheduler.filter_tasks(completed=completion_filter)
    )

    st.write(f"{task_view} tasks:")
    if visible_tasks:
        st.table(
            [
                {
                    "pet": next(
                        pet.name
                        for pet in owner.list_pets()
                        if task in pet.list_tasks()
                    ),
                    "task": task.description,
                    "duration_minutes": task.time,
                    "priority": getattr(task, "priority", "medium"),
                    "status": "complete" if task.completed else "incomplete",
                }
                for task in visible_tasks
            ]
        )
    else:
        st.info(f"No {task_view.lower()} tasks.")

    conflicts = scheduler.detect_conflicts()
    for conflict in conflicts:
        st.warning(conflict + " Consider changing one task's start time.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("The scheduler selects incomplete tasks by priority while respecting available time.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()
    st.write("Today's schedule:")
    if plan.scheduled_tasks:
        st.table(
            [
                {
                    "pet": next(
                        pet.name
                        for pet in owner.list_pets()
                        if task in pet.list_tasks()
                    ),
                    "task": task.description,
                    "duration_minutes": task.time,
                    "priority": getattr(task, "priority", "medium"),
                    "frequency": task.frequency,
                }
                for task in plan.scheduled_tasks
            ]
        )
        st.success(
            f"Scheduled {plan.calculate_total_time()} minutes. "
            f"{plan.remaining_minutes} minutes remain."
        )
        st.caption(scheduler.explain_choices())
    else:
        st.info("No incomplete tasks fit within the available time.")
