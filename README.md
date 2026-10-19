# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

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
rootdir: /Users/hannarosekellenberger/Documents/CodePath/AI110/Project2/ai110-module2show-pawpal-starter
plugins: anyio-4.12.1, Faker-40.39.0
collected 12 items

tests/test_pawpal.py ............                                        [100%]

============================== 12 passed in 0.07s ==============================
```

**Confidence Level:** ★★★★☆ (4/5)

The core scheduling behaviors are covered and all 12 tests pass. Additional
integration and UI testing would be needed for complete system confidence.

## 📐 Smarter Scheduling

PawPal+ includes several algorithms that make daily planning more useful for a pet owner:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Returns tasks ordered from shortest to longest duration using the task's `time` attribute. The scheduler also uses `Scheduler.sort_tasks_by_priority()` when building a daily plan. |
| Filtering | `Scheduler.filter_tasks()` and `Scheduler.filter_tasks_by_time()` | Filters tasks by pet name and completion status. Daily plan generation also skips completed, future-dated, or over-limit tasks. |
| Conflict detection | `Scheduler.detect_conflicts()` | Returns warning messages when active tasks for the same or different pets have the same `start_time`. It reports warnings instead of stopping the program. |
| Recurring tasks | `Task.mark_complete()`, `Pet.mark_task_complete()`, and `Scheduler.mark_task_complete()` | Completing a daily task creates the next occurrence one day later. Completing a weekly task creates the next occurrence seven days later using `timedelta`. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
