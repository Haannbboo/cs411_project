from Task import Task
import random


class TaskManager:
    # contains temporary tasks generated by Generator
    # ensures that all incomplete tasks are completed or report an error code
    # permanent information of a route will be stored in data structure Route

    def __init__(self, CnTn: list):
        self.tasks = CnTn  # incomplete tasks received from Generator
        self.completedTasks: list = []
        self.errorTasks: list = []

    def addTasks(self, CnTn: list) -> None:
        self.tasks.extend(CnTn)

    def dropTasks(self, CnTn: list) -> None:
        for CT in CnTn:
            if CT in self.tasks:
                self.tasks.remove(CT)

    def getTask(self) -> Task:
        # Task might have error, like an error code for errors and exceptions
        # for simplicity status == 0.5 is not considered now
        task = random.choice(self.tasks)
        self.tasks.remove(task)
        return task

    def reportTask(self, processedTask: Task) -> None:
        if processedTask.status == 1:
            self.completedTasks.append(processedTask)
        if processedTask.status == 0:
            self.tasks.append(processedTask)
        if processedTask.status == 0.5:
            if processedTask.errorCount == 1:  # retry 3 times
                self.errorTasks.append(processedTask)
            else:
                self.tasks.append(processedTask)

    def allCompleted(self):

        return len(self.tasks) == 0


'''
t1 = Task('BJS', 'SHA', '2021-8-21')
t2 = Task('BJS', 'SHA', '2021-8-22')
t3 = Task('BJS', 'SHA', '2021-8-23')
t4 = Task('BJS', 'CHX', '2021-8-21')
t5 = Task('BJS', 'CHX', '2021-8-22')
tasks = TaskManager([t1, t2, t3, t4, t5])

t6 = Task('BJS', 'SHA', '2021-8-29')
tasks.addTasks([t6])
assert len(tasks.tasks) == 6
tasks.dropTasks([t2, t3])
assert len(tasks.tasks) == 4

t = tasks.getTask()
print(t)
t.markCompleted()
print(t)
tasks.reportTask(t)
assert len(tasks.completedTasks) == 1

t = tasks.getTask()
print(t)
t.markError(0.5)
print(t)
tasks.reportTask(t)
assert len(tasks.errorTasks) == 1
'''
