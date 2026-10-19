from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


owner = Owner("Jordan", available_minutes=60)
mochi = Pet("Mochi", "dog", "mixed breed", 3, owner)
luna = Pet("Luna", "cat", "tabby", 5, owner)

mochi.add_task(Task("Morning walk", 20, "daily", start_time="08:00"))
mochi.add_task(Task("Brush coat", 15, "weekly", start_time="10:00"))
mochi.add_task(Task("Trim nails", 5, "weekly", completed=True))
mochi.add_task(Task("Give medication", 5, "daily", start_time="08:00"))
luna.add_task(Task("Feed breakfast", 10, "daily", start_time="08:00"))

scheduler = Scheduler(owner)

print("Tasks sorted by time")
for task in scheduler.sort_by_time():
    print(f"- {task.description}: {task.time} minutes")

print("\nIncomplete Mochi tasks")
for task in scheduler.filter_tasks(completed=False, pet_name="Mochi"):
    print(f"- {task.description}: {task.time} minutes")

print("\nRecurring task completion")
morning_walk = mochi.list_tasks()[0]
next_walk = scheduler.mark_task_complete(morning_walk, date(2026, 10, 19))
print(f"- Next occurrence: {next_walk.due_date}")

print("\nSchedule conflicts")
for warning in scheduler.detect_conflicts(date(2026, 10, 19)):
    print(warning)

schedule = scheduler.generate_plan()

print("Today's Schedule")
for task in schedule.scheduled_tasks:
    print(f"- {task.description}: {task.time} minutes ({task.frequency})")
print(f"Total scheduled time: {schedule.calculate_total_time()} minutes")
print(f"Remaining time: {schedule.remaining_minutes} minutes")
