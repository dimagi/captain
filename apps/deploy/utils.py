from apps.deploy.tasks import captain_deploy as captain_deploy_task


def captain_deploy(env):
    captain_deploy_task.delay(env)
