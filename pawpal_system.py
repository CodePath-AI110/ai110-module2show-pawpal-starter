"""Core PawPal+ domain classes."""


class Owner:
    def __init__(self, name: str, available_minutes: int, preferences: str = "") -> None:
        """Initialize an owner profile and its pet collection."""
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences
        self.pets: list[Pet] = []

    def update_availability(self, minutes: int) -> None:
        """Update the owner's available care time."""
        if minutes < 0:
            raise ValueError("available minutes cannot be negative")
        self.available_minutes = minutes

    def set_preferences(self, preferences: str) -> None:
        """Update the owner's care preferences."""
        self.preferences = preferences

    def add_pet(self, pet: "Pet") -> None:
        """Associate a pet with this owner."""
        if pet not in self.pets:
            self.pets.append(pet)
        pet.owner = self

    def remove_pet(self, pet: "Pet") -> None:
        """Remove a pet from this owner's collection."""
        self.pets.remove(pet)

    def list_pets(self) -> list["Pet"]:
        """Return the owner's pets."""
        return list(self.pets)

    def get_all_tasks(self) -> list["Task"]:
        """Return tasks belonging to all of the owner's pets."""
        return [task for pet in self.pets for task in pet.list_tasks()]


class Pet:
    def __init__(
        self,
        name: str,
        species: str,
        breed: str,
        age: int,
        owner: Owner,
    ) -> None:
        """Initialize a pet and associate it with its owner."""
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.owner = owner
        self.tasks: list[Task] = []
        if self not in owner.pets:
            owner.pets.append(self)

    def add_task(self, task: "Task") -> None:
        """Add a care task to the pet."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        """Remove a care task from the pet."""
        self.tasks.remove(task)

    def list_tasks(self) -> list["Task"]:
        """Return the pet's care tasks."""
        return list(self.tasks)


class Task:
    def __init__(
        self,
        description: str,
        time: int,
        frequency: str,
        completed: bool = False,
    ) -> None:
        """Initialize a care task."""
        if time < 0:
            raise ValueError("task time cannot be negative")
        self.description = description
        self.time = time
        self.frequency = frequency
        self.completed = completed

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def update_details(
        self,
        description: str | None = None,
        time: int | None = None,
        frequency: str | None = None,
    ) -> None:
        """Update the task fields that were provided."""
        if time is not None and time < 0:
            raise ValueError("task time cannot be negative")
        if description is not None:
            self.description = description
        if time is not None:
            self.time = time
        if frequency is not None:
            self.frequency = frequency

    def is_valid(self) -> bool:
        """Return whether the task has valid required fields."""
        return bool(self.description and self.time >= 0 and self.frequency)

    # These aliases keep the names used by the original UML and starter UI usable.
    @property
    def name(self) -> str:
        """Return the task description as its name."""
        return self.description

    @property
    def duration_minutes(self) -> int:
        """Return the task duration in minutes."""
        return self.time

    @property
    def recurrence(self) -> str:
        """Return the task frequency as its recurrence."""
        return self.frequency


class CareTask(Task):
    """Backward-compatible form of the original UML task model."""

    def __init__(
        self,
        name: str,
        duration_minutes: int,
        priority: str,
        category: str,
        recurrence: str,
        completed: bool = False,
    ) -> None:
        """Initialize a task using the original UML field names."""
        super().__init__(name, duration_minutes, recurrence, completed)
        self.priority = priority
        self.category = category


class DailyPlan:
    def __init__(
        self,
        pet: Pet | Owner,
        available_minutes: int,
    ) -> None:
        """Initialize an empty daily plan with a time limit."""
        self.pet = pet
        self.scheduled_tasks: list[Task] = []
        self.available_minutes = available_minutes
        self.remaining_minutes = available_minutes

    def add_task(self, task: Task) -> None:
        """Add a task when it fits within the remaining plan time."""
        if task.time > self.remaining_minutes:
            raise ValueError("task exceeds the plan's remaining time")
        self.scheduled_tasks.append(task)
        self.remaining_minutes -= task.time

    def remove_task(self, task: Task) -> None:
        """Remove a task and restore its time to the plan."""
        self.scheduled_tasks.remove(task)
        self.remaining_minutes += task.time

    def calculate_total_time(self) -> int:
        """Return the total time of scheduled tasks."""
        return sum(task.time for task in self.scheduled_tasks)

    def display_plan(self) -> str:
        """Return a readable summary of the scheduled tasks."""
        return "\n".join(
            f"{task.description} ({task.time} min, {task.frequency})"
            for task in self.scheduled_tasks
        )


class Scheduler:
    def __init__(
        self,
        owner: Owner,
        daily_time_limit: int | None = None,
        owner_constraints: str = "",
    ) -> None:
        """Initialize a scheduler for an owner's pets and time limit."""
        self.owner = owner
        self.owner_constraints = owner_constraints or owner.preferences
        self.daily_time_limit = (
            owner.available_minutes if daily_time_limit is None else daily_time_limit
        )

    def sort_tasks_by_priority(self) -> list[Task]:
        """Return incomplete and complete tasks ordered by priority."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda task: priority_order.get(getattr(task, "priority", "medium"), 1),
        )

    def filter_tasks_by_time(self) -> list[Task]:
        """Return incomplete tasks that fit within the daily limit."""
        selected: list[Task] = []
        remaining = self.daily_time_limit
        for task in self.sort_tasks_by_priority():
            if not task.completed and task.time <= remaining:
                selected.append(task)
                remaining -= task.time
        return selected

    def generate_plan(self) -> DailyPlan:
        """Generate a daily plan from the tasks that fit."""
        plan = DailyPlan(self.owner, self.daily_time_limit)
        for task in self.filter_tasks_by_time():
            plan.add_task(task)
        return plan

    def explain_choices(self) -> str:
        """Explain which tasks were selected for the daily plan."""
        tasks = self.filter_tasks_by_time()
        if not tasks:
            return "No incomplete tasks fit within the available time."
        return "Selected " + ", ".join(task.description for task in tasks) + "."
