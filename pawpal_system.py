"""Core PawPal+ domain classes."""


class Owner:
    def __init__(self, name: str, available_minutes: int, preferences: str = "") -> None:
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences

    def update_availability(self, minutes: int) -> None:
        pass

    def set_preferences(self, preferences: str) -> None:
        pass


class Pet:
    def __init__(
        self,
        name: str,
        species: str,
        breed: str,
        age: int,
        owner: Owner,
    ) -> None:
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.owner = owner
        self.tasks: list[CareTask] = []

    def add_task(self, task: "CareTask") -> None:
        pass

    def remove_task(self, task: "CareTask") -> None:
        pass

    def list_tasks(self) -> list["CareTask"]:
        pass


class CareTask:
    def __init__(
        self,
        name: str,
        duration_minutes: int,
        priority: str,
        category: str,
        recurrence: str,
        completed: bool = False,
    ) -> None:
        self.name = name
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.recurrence = recurrence
        self.completed = completed

    def mark_complete(self) -> None:
        pass

    def update_details(self) -> None:
        pass

    def is_valid(self) -> bool:
        pass


class DailyPlan:
    def __init__(
        self,
        pet: Pet,
        available_minutes: int,
    ) -> None:
        self.pet = pet
        self.scheduled_tasks: list[CareTask] = []
        self.available_minutes = available_minutes
        self.remaining_minutes = available_minutes

    def add_task(self, task: CareTask) -> None:
        pass

    def remove_task(self, task: CareTask) -> None:
        pass

    def calculate_total_time(self) -> int:
        pass

    def display_plan(self) -> str:
        pass


class Scheduler:
    def __init__(
        self,
        tasks: list[CareTask],
        owner_constraints: str,
        pet: Pet,
        daily_time_limit: int,
    ) -> None:
        self.tasks = tasks
        self.owner_constraints = owner_constraints
        self.pet = pet
        self.daily_time_limit = daily_time_limit

    def sort_tasks_by_priority(self) -> list[CareTask]:
        pass

    def filter_tasks_by_time(self) -> list[CareTask]:
        pass

    def generate_plan(self) -> DailyPlan:
        pass

    def explain_choices(self) -> str:
        pass
