from datetime import date, timedelta

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status() -> None:
	task = Task("Feed cat", 10, "daily")

	assert task.completed is False

	task.mark_complete()

	assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
	owner = Owner("Alex", 30)
	pet = Pet("Milo", "cat", "tabby", 3, owner)
	task = Task("Feed cat", 10, "daily")
	initial_task_count = len(pet.list_tasks())

	pet.add_task(task)

	assert len(pet.list_tasks()) == initial_task_count + 1


def test_negative_task_duration_is_rejected() -> None:
	with pytest.raises(ValueError):
		Task("Walk dog", -1, "daily")


def test_required_task_fields_are_validated() -> None:
	assert Task("Zero-minute check", 0, "daily").is_valid() is True
	assert Task("", 10, "daily").is_valid() is False
	assert Task("Feed cat", 10, "").is_valid() is False


def test_scheduler_sorts_tasks_from_shortest_to_longest() -> None:
	owner = Owner("Alex", 60)
	pet = Pet("Milo", "cat", "tabby", 3, owner)
	long_task = Task("Long task", 30, "daily")
	short_task = Task("Short task", 5, "daily")
	pet.add_task(long_task)
	pet.add_task(short_task)

	assert Scheduler(owner).sort_by_time() == [short_task, long_task]


def test_scheduler_filters_by_pet_name_and_completion_status() -> None:
	owner = Owner("Alex", 60)
	milo = Pet("Milo", "cat", "tabby", 3, owner)
	luna = Pet("Luna", "dog", "lab", 4, owner)
	milo_incomplete = Task("Feed Milo", 10, "daily")
	milo_complete = Task("Brush Milo", 10, "weekly", completed=True)
	luna_task = Task("Walk Luna", 20, "daily")
	milo.add_task(milo_incomplete)
	milo.add_task(milo_complete)
	luna.add_task(luna_task)

	assert Scheduler(owner).filter_tasks(completed=False, pet_name="mIlO") == [
		milo_incomplete
	]
	assert Scheduler(owner).filter_tasks(completed=True) == [milo_complete]


def test_daily_plan_excludes_completed_future_and_over_limit_tasks() -> None:
	owner = Owner("Alex", 30)
	pet = Pet("Milo", "cat", "tabby", 3, owner)
	completed = Task("Completed", 1, "daily", completed=True)
	future = Task(
		"Future", 1, "daily", due_date=date.today() + timedelta(days=1)
	)
	too_long = Task("Too long", 40, "daily")
	fits_after_long_task = Task("Fits", 10, "daily")
	for task in (completed, future, too_long, fits_after_long_task):
		pet.add_task(task)

	plan = Scheduler(owner).generate_plan()

	assert plan.scheduled_tasks == [fits_after_long_task]
	assert plan.remaining_minutes == 20


def test_completing_daily_task_creates_next_day_occurrence() -> None:
	owner = Owner("Alex", 60)
	pet = Pet("Milo", "cat", "tabby", 3, owner)
	task = Task("Feed cat", 10, "daily", due_date=date(2026, 10, 19))
	pet.add_task(task)

	next_task = Scheduler(owner).mark_task_complete(task)

	assert task.completed is True
	assert next_task is not None
	assert next_task.due_date == date(2026, 10, 20)
	assert pet.list_tasks() == [task, next_task]


def test_completing_weekly_task_creates_next_week_occurrence() -> None:
	owner = Owner("Alex", 60)
	pet = Pet("Milo", "cat", "tabby", 3, owner)
	task = Task("Brush coat", 15, "weekly", due_date=date(2026, 10, 19))
	pet.add_task(task)

	next_task = Scheduler(owner).mark_task_complete(task)

	assert next_task is not None
	assert next_task.due_date == date(2026, 10, 26)


def test_completing_non_recurring_task_does_not_add_duplicate() -> None:
	owner = Owner("Alex", 60)
	pet = Pet("Milo", "cat", "tabby", 3, owner)
	task = Task("One-time vet visit", 30, "once")
	pet.add_task(task)

	assert Scheduler(owner).mark_task_complete(task) is None
	assert pet.list_tasks() == [task]


def test_conflicts_warn_for_active_tasks_with_same_start_time() -> None:
	owner = Owner("Alex", 60)
	milo = Pet("Milo", "cat", "tabby", 3, owner)
	luna = Pet("Luna", "dog", "lab", 4, owner)
	milo.add_task(Task("Feed Milo", 10, "daily", start_time="08:00"))
	luna.add_task(Task("Walk Luna", 20, "daily", start_time="08:00"))

	warnings = Scheduler(owner).detect_conflicts()

	assert len(warnings) == 1
	assert "Feed Milo" in warnings[0]
	assert "Walk Luna" in warnings[0]


def test_conflicts_ignore_completed_and_future_tasks() -> None:
	owner = Owner("Alex", 60)
	pet = Pet("Milo", "cat", "tabby", 3, owner)
	pet.add_task(
		Task("Completed", 10, "daily", completed=True, start_time="08:00")
	)
	pet.add_task(
		Task(
			"Future",
			10,
			"daily",
			due_date=date.today() + timedelta(days=1),
			start_time="08:00",
		)
	)

	assert Scheduler(owner).detect_conflicts(as_of=date.today()) == []
