import logging

from fabric.network import disconnect_all
from fabric.api import execute

# HQ's fabfile
from fab import fabfile


def captain_deploy(deploy):
    try:
        execute(getattr(fabfile, deploy.env))
        execute(fabfile.setup_release)
    except Exception, e:
        logging.exception(e)
        deploy.success = False
    else:
        deploy.success = True
    finally:
        disconnect_all()
        deploy.in_progress = False
        deploy.complete = True
        deploy.save()
