from locust import HttpLocust, TaskSequence, seq_task, TaskSet, task


class UserBehavior(TaskSequence):
    @seq_task(1)
    def index(self):
        self.client.get('/')
    @seq_task(2)
    def submitfridge(self):
        self.client.post('/submitted_fridge', {"Ingredient1":"bacon", "Ingredient2":"eggs", "Ingredient3":"Spaghetti"})

class UserIndex(TaskSet):
    @task
    def index(self):
        self.client.get('/')

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
    host = "https://www.emptymyfridge.com"