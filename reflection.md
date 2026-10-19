# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The initial design included five classes. `Owner` stores the owner's information, available time, and preferences. `Pet` stores the pet's information and manages its care tasks. `CareTask` represents an activity with a duration, priority, category, recurrence, and completion status. `Scheduler` applies constraints and priorities to organize tasks, while `DailyPlan` stores and displays the selected tasks for the day.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. The original UML treated `CareTask` as the main task class, but the final
implementation uses a simpler `Task` class as the primary model. `CareTask`
now extends `Task` and preserves the original UML field names for backward
compatibility. I also added `due_date` and `start_time` to support future tasks,
recurring tasks, and conflict warnings. `Owner` became the single source of
truth for pets and their tasks, so `Scheduler` can plan from the owner's actual
data instead of maintaining a duplicate task collection.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler uses the owner's available minutes as the main capacity
constraint. It orders tasks by priority, skips completed tasks, skips tasks
whose due date is in the future, and skips tasks that do not fit in the
remaining time. It also supports filtering by completion status and pet name,
sorts tasks by duration for review, and reports active tasks with identical
start times. Owner preferences are stored and passed into `Scheduler` as
`owner_constraints`, but the current scheduling algorithm does not yet use
those preferences to include or exclude tasks.

I treated availability and task completion as hard constraints because a daily
plan should not promise more care than the owner can provide or repeat a task
that is already complete. Priority is the next decision factor because it helps
the scheduler choose the most important tasks when the available time is
limited. Due dates and conflict warnings add safety information without
silently changing the owner's task data.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler checks for tasks with the exact same start time rather than detecting every possible overlap between task durations. This approach is simpler to implement and gives the owner a clear warning when two tasks are scheduled at the same time. It is reasonable for this project because the scheduler is intended to provide basic planning support, but a future version could compare each task's start and end times to detect partial overlaps as well.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to brainstorm the system objects, create the UML diagram, generate the class skeleton, review relationships, and add documentation. Prompts that listed the project requirements and asked for concrete attributes, methods, and relationships were the most helpful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The AI suggested that `Owner` should track its pets and that `Scheduler` should use the owner's task collection instead of maintaining a separate source of truth. I accepted those suggestions because they matched the UML relationships, then verified the result by reviewing the code, instantiating the classes, and running the pytest suite. I kept the scheduling logic as a simple priority-and-time filter rather than adding unneeded complexity.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The test suite covers task completion, adding tasks to pets, rejection of
negative durations, required-field validation, sorting by duration, filtering
by pet and completion status, and daily-plan limits. It also tests that plans
exclude completed, future-dated, and over-limit tasks. Recurrence tests verify
that daily tasks create a next-day occurrence, weekly tasks create a next-week
occurrence, and one-time tasks do not create duplicates. Conflict tests verify
that active tasks with the same start time produce a warning while completed
and future tasks are ignored.

These tests are important because they check both ordinary workflows and the
boundary conditions that could make a schedule misleading, such as exceeding
the available time or scheduling work that is not currently due.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident in the core scheduler because the full test suite has 12
passing tests covering the main domain behaviors. I also verified the example
workflow through `main.py` and connected the scheduler methods to the
Streamlit UI. The remaining risk is that the UI has less automated coverage
than the domain classes.

Next, I would test tasks with equal priority and equal duration, invalid or
unexpected priority values, zero available minutes, several conflicts at the
same time, due dates exactly equal to today, and tasks whose durations could
partially overlap even when their start times differ. I would also add a test
for owner preferences once those preferences affect scheduling decisions.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with the separation between the domain model and the
planning algorithm. `Owner` and `Pet` manage relationships, `Task` manages
task state and recurrence, `Scheduler` makes selection decisions, and
`DailyPlan` tracks the resulting time totals. That separation made it easier
to test the scheduler independently and then reuse it in both the CLI example
and the Streamlit UI.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add start and end time calculations so conflict detection could catch
partial overlaps instead of only identical start times. I would also connect
owner preferences to the scheduling algorithm, add UI controls for due dates
and start times, and add a way to mark tasks complete from the Streamlit app.
Finally, I would add Streamlit integration tests so the visible tables and
warnings are verified as well as the backend behavior.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that being the lead architect means deciding which suggestions fit
the system's responsibilities and verifying them in the running code. An AI
coding assistant can propose classes, methods, tests, and documentation very
quickly, but I still need to define the source of truth, keep the public model
coherent, and reject complexity that the requirements do not need.

## AI Strategy

### Effective assistant features

The most effective features were context-aware code review, targeted edits,
test generation and execution, and help tracing relationships between the UML,
Python classes, and Streamlit UI. Asking the assistant to inspect the nearby
implementation before changing it helped keep edits consistent with the
existing APIs. Running the pytest suite after backend changes was especially
useful because it quickly exposed whether a proposed scheduler change matched
the intended behavior.

### A suggestion I modified

I modified the initial task-model suggestion instead of keeping `CareTask` as
the only task type. The final implementation uses `Task` for the scheduler and
keeps `CareTask` as a subclass that supports the original UML names. This kept
the scheduling code simple while preserving compatibility with the earlier
design. I verified the choice by checking the scheduler call sites and running
the tests for sorting, filtering, recurrence, and plan generation.

### Separate chat sessions

Separate sessions for design, backend implementation, UI integration, UML
updates, and documentation helped me keep each phase focused. The design
session established responsibilities and relationships, the implementation
session concentrated on behavior and tests, and the UI and documentation
sessions translated those behaviors into something a user and reviewer could
see. This organization reduced the chance of mixing an early UML assumption
with the final implementation and made it easier to revisit one phase without
losing the overall project goal.

### Lead architect lesson

My main lesson is that AI accelerates implementation, but it does not replace
architectural ownership. I had to choose the source of truth for tasks, decide
which constraints were hard requirements, keep the scheduler understandable,
and verify every important behavior with tests or a runnable example. The lead
architect's job is to provide direction, question convenient suggestions, and
accept changes only when they improve the design and can be explained clearly.
