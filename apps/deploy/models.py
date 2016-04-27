from django.db import models
from apps.deploy.tasks import captain_deploy
from django_rq import enqueue

from .exceptions import DeployAlreadyInProgress
from .const import ENVIRONMENTS


class Deploy(models.Model):
    """
    A Deploy represents a single deploy from Chief
    """
    in_progress = models.BooleanField(default=False, db_index=True)
    success = models.BooleanField(default=False, db_index=True)
    complete = models.BooleanField(default=False, db_index=True)
    log_file = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    env = models.CharField(max_length=255)
    code_branch = models.CharField(max_length=255)
    user = models.CharField(max_length=255, default='')
    failure_reason = models.CharField(max_length=255, null=True)
    duration = models.IntegerField(null=True)  # Duration in seconds

    @classmethod
    def current_deploys_for_env(cls, env):
        return Deploy.objects.filter(in_progress=True, env=env)

    @classmethod
    def previous_deploy_for_env(cls, env):
        try:
            return Deploy.objects.filter(
                in_progress=False,
                env=env,
                complete=True
            ).latest('date_created')
        except Deploy.DoesNotExist:
            return None

    @classmethod
    def current_deploys(cls):
        deploys = {}
        for env in ENVIRONMENTS:
            deploys[env] = cls.current_deploys_for_env(env)
        return deploys

    @classmethod
    def previous_deploys(cls):
        deploys = {}
        for env in ENVIRONMENTS:
            deploys[env] = cls.previous_deploy_for_env(env)
        return deploys

    def deploy(self):
        deploys_in_progress = Deploy.objects.filter(
            in_progress=True, env=self.env
        ).count()

        if deploys_in_progress:
            raise DeployAlreadyInProgress

        self.in_progress = True
        self.save()
        enqueue(captain_deploy, self)

    def as_json(self):
        return {
            'in_progress': self.in_progress,
            'success': self.success,
            'date_created': self.date_created,
            'env': self.env,
        }
