import traceback
import logging
from datetime import datetime

from fabric.network import disconnect_all
from fabric.api import execute

# HQ's fabfile
from fab import fabfile

from .exceptions import FailedCaptainDeploy


def captain_deploy(deploy):
    try:
        start = datetime.utcnow()
        if deploy.code_branch:
            fabfile.env.code_branch = deploy.code_branch
        fabfile.env.captain_user = deploy.user
        fabfile.env.abort_exception = FailedCaptainDeploy
        execute(getattr(fabfile, deploy.env))
        execute(fabfile.awesome_deploy, confirm='no')
    except Exception, e:
        logging.exception(e)
        deploy.stacktrace = traceback.format_exc()
        deploy.failure_reason = unicode(e)
        deploy.success = False
    else:
        deploy.success = True
    finally:
        duration = (datetime.utcnow() - start).seconds
        disconnect_all()
        deploy.duration = duration
        deploy.in_progress = False
        deploy.complete = True
        deploy.save()
