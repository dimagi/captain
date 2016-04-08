from apps.deploy.tasks import captain_deploy as captain_deploy_task
from django_rq import enqueue


def captain_deploy(env):
    enqueue(captain_deploy_task, env)
