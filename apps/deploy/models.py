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

    @classmethod
    def current_deploys_for_env(cls, env):
        return Deploy.objects.filter(in_progress=True, env=env)

    @classmethod
    def current_deploys(cls):
        deploys = {}
        for env in ENVIRONMENTS:
            deploys[env] = cls.current_deploys_for_env(env)
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
            'machines': [m.as_json() for m in self.machine_set.all()],
            'stages': [s.as_json() for s in self.stage_set.all()],
        }
