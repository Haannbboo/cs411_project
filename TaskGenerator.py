from Task import Task


class Generator:
    # Generate tasks that will be executed by TaskManager
    # Find nearby cities and dates to search from

    def __init__(self):
        self.abc = 1

    def generate(self, C1, C2, T) -> list:
        tasks = [Task(C1, C2, T)]
        return tasks
