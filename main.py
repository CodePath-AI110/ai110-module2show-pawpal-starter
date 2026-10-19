pifrom pawpal_system import Owner, Pet, Scheduler, Task


owner = Owner("Jordan", available_minutes=60)
mochi = Pet("Mochi", "dog", "mixed breed", 3, owner)
luna = Pet("Luna", "cat", "tabby", 5, owner)

mochi.add_task(Task("Morning walk", 20, "daily"))
mochi.add_task(Task("Brush coat", 15, "weekly"))
luna.add_task(Task("Feed breakfast", 10, "daily"))

schedule = Scheduler(owner).generate_plan()

print("Today's Schedule")
for task in schedule.scheduled_tasks:
    print(f"- {task.description}: {task.time} minutes ({task.frequency})")
print(f"Total scheduled time: {schedule.calculate_total_time()} minutes")
print(f"Remaining time: {schedule.remaining_minutes} minutes")
