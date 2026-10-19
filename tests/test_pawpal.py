from pawpal_system import Owner, Pet, Task


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
