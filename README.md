# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

PawPal+ is implemented in [`pawpal_system.py`](pawpal_system.py) and connected to
the Streamlit interface in [`app.py`](app.py). Its main features are:

- **Owner and pet profiles:** Create an owner with available care time, add pets,
	and manage each pet's care tasks.
- **Task sorting by time:** `Scheduler.sort_by_time()` orders tasks from shortest
	to longest duration for quick review in the UI.
- **Priority-based scheduling:** `Scheduler.sort_tasks_by_priority()` considers
	high-, medium-, and low-priority tasks when building a daily plan.
- **Task filtering:** `Scheduler.filter_tasks()` filters by completion status and
	pet name. The UI exposes All, Incomplete, and Completed task views.
- **Time-aware daily plans:** `Scheduler.filter_tasks_by_time()` excludes
	completed, future-dated, and over-limit tasks while respecting available time.
- **Conflict warnings:** `Scheduler.detect_conflicts()` identifies active tasks
	with the same start time. The UI names both pets and tasks and suggests
	changing one start time.
- **Daily and weekly recurrence:** Completing a daily or weekly task creates its
	next occurrence one or seven days later.
- **Explainable results:** `Scheduler.explain_choices()` reports which tasks were
	selected, while `DailyPlan` reports total scheduled and remaining minutes.
- **Automated tests:** [`tests/test_pawpal.py`](tests/test_pawpal.py) covers
	validation, sorting, filtering, time limits, recurrence, and conflicts.

The final class relationships and public methods are documented in
[`diagrams/uml_final.mmd`](diagrams/uml_final.mmd).

## Implementation Summary

PawPal+ uses `Owner`, `Pet`, and `Task` objects to store care information. `Owner` manages pets and their tasks, while `Scheduler` sorts tasks by priority and selects incomplete tasks that fit the owner's available time. `DailyPlan` stores the selected tasks, tracks remaining time, and displays the schedule. The `CareTask` class preserves the original UML naming while extending the simpler `Task` model.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py`:

```
Today's Schedule
- Morning walk: 20 minutes (daily)
- Brush coat: 15 minutes (weekly)
- Feed breakfast: 10 minutes (daily)
Total scheduled time: 45 minutes
Remaining time: 15 minutes
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

The test suite covers task validation, sorting and filtering, daily plan limits,
daily and weekly recurring tasks, non-recurring tasks, and conflict detection
for active, completed, and future-dated tasks.

Successful test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.14.6, pytest-9.0.3, pluggy-1.6.0
rootdir: /Project2/ai110-module2show-pawpal-starter
plugins: anyio-4.12.1, Faker-40.39.0
collected 12 items

tests/test_pawpal.py ............                                        [100%]

============================== 12 passed in 0.07s ==============================
```

**Confidence Level:** ★★★★☆ (4/5)

The core scheduling behaviors are covered and all 12 tests pass. Additional
integration and UI testing would be needed for complete system confidence.

## 📐 Smarter Scheduling

PawPal+ includes several algorithms that make daily planning more useful for a
pet owner:

| Feature | Method(s) | Behavior |
|---------|-----------|----------|
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks from shortest to longest duration. The daily plan also uses `Scheduler.sort_tasks_by_priority()` to consider high-, medium-, and low-priority tasks. |
| Filtering | `Scheduler.filter_tasks()` and `Scheduler.filter_tasks_by_time()` | Filters by pet name and completion status, then excludes completed, future-dated, or over-limit tasks from a daily plan. |
| Conflict detection | `Scheduler.detect_conflicts()` | Reports active tasks that share a `start_time`, including the affected pets and tasks, without stopping the program. |
| Recurring tasks | `Task.mark_complete()`, `Pet.mark_task_complete()`, and `Scheduler.mark_task_complete()` | Creates the next occurrence one day later for daily tasks or seven days later for weekly tasks. |

## Demo Walkthrough

### Streamlit UI

Start the interactive app from the project directory:

```bash
streamlit run app.py
```

Then open the local URL printed by Streamlit, normally `http://localhost:8501`.
The main UI workflow is:

1. Enter the owner's name and available care time.
2. Enter a pet's name, species, breed, and age, then select **Add pet**.
3. Choose that pet, enter a task title and duration, select a priority, and
	select **Add task**.
4. Use the task view selector to show all, incomplete, or completed tasks. The
	displayed tasks are sorted from shortest to longest duration.
5. Select **Generate schedule** to build today's plan. The result shows each
	selected task, its pet, duration, priority, frequency, total scheduled time,
	remaining time, and the scheduler's explanation.

The scheduler prioritizes incomplete tasks that fit within the owner's available
minutes. It skips completed tasks, future-dated tasks, and tasks that exceed the
remaining time. If active tasks share a start time, the UI displays a warning
identifying both tasks and pets and recommends changing one start time.

### CLI example

[`main.py`](main.py) demonstrates the same algorithms without Streamlit. Run it
with:

```bash
python main.py
```

Example output:

```text
Tasks sorted by time
- Trim nails: 5 minutes
- Give medication: 5 minutes
- Feed breakfast: 10 minutes
- Brush coat: 15 minutes
- Morning walk: 20 minutes

Incomplete Mochi tasks
- Morning walk: 20 minutes
- Brush coat: 15 minutes
- Give medication: 5 minutes

Recurring task completion
- Next occurrence: 2026-10-20

Schedule conflicts
Warning: Give medication (Mochi) and Feed breakfast (Luna) both start at 08:00.
Today's Schedule
- Brush coat: 15 minutes (weekly)
- Give medication: 5 minutes (daily)
- Feed breakfast: 10 minutes (daily)
Total scheduled time: 30 minutes
Remaining time: 30 minutes
```
