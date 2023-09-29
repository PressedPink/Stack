from Stack.models import task

class taskClass:
    def createTask(self, name, description, lock, recurring, time, user):
        #validateName
        #processLock
        #reoccuringTag
        #timeStamp
        #createTask
        print("in taskClass")

        if taskClass.validateName(self, name):
            newTask = task(name = name, description = description, lock = lock, recurring = recurring, time = time, user = user)
            newTask.save()

    def validateName(self, name):
        if name is None:
            raise Exception("Task name may not be left blank!")
        else:
            return True
