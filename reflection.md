# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The initial design included five classes. `Owner` stores the owner's information, available time, and preferences. `Pet` stores the pet's information and manages its care tasks. `CareTask` represents an activity with a duration, priority, category, recurrence, and completion status. `Scheduler` applies constraints and priorities to organize tasks, while `DailyPlan` stores and displays the selected tasks for the day.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

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

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
