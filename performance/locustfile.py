from locust import HttpUser, between


def hit_showcase(user):
    user.client.get("/aurora-demo/")


class AuroraTopologyUser(HttpUser):
    wait_time = between(0.2, 0.8)
    tasks = [hit_showcase]
