from Stack.models import task

class taskClass:
    def createTask(self, name, description, lock, reoccuring, time):
        #validateName
        #processLock
        #reoccuringTag
        #timeStamp
        #createTask
        if taskClass.validateName(self, name):
            newTask = task(name, description, lock, reoccuring, time)
            newTask.save()

    def validateName(self, name):
        if name is None:
            raise Exception("Task name may not be left blank!")
