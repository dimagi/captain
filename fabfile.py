from fabric.api import sudo, cd, env, task, execute
from fabric.colors import red, white, green

# the user to use for the remote commands
env.sudo_user = 'cchq'
# the servers where the commands are executed
env.hosts = ['hqcaptain0.internal.commcarehq.org']
env.code_root = '/home/cchq/captain/src'
env.venv = '/home/cchq/captain/python_env'


def update_code():
    with cd(env.code_root):
        sudo('git remote prune origin')
        sudo('git pull origin master')
        sudo('git submodule sync')
        sudo('git submodule update --init --recursive -q')
        # remove all untracked files, including submodules
        sudo("git clean -ffd")
        sudo("find . -name '*.pyc' -delete")


def staticfiles():
    with cd(env.code_root):
        sudo('{}/bin/python manage.py collectstatic --noinput -v 0'.format(env.venv))


def install_deps():
    cmd_prefix = 'export HOME=/home/{} && source {}/bin/activate && '.format(env.sudo_user, env.venv)
    with cd(env.code_root):
        sudo('export HOME=/home/{} && bower update --production --config.interactive=false'.format(env.sudo_user))
        sudo('{} pip install -r requirements.txt'.format(cmd_prefix))


def migrate():
    with cd(env.code_root):
        sudo('{}/bin/python manage.py migrate --noinput'.format(env.venv))


@task
def restart_services():
    sudo('sudo supervisorctl restart captain-django', user='cchq')
    sudo('sudo supervisorctl restart captain-rq', user='cchq')
    sudo('sudo supervisorctl restart captain-rtail', user='cchq')
    sudo('sudo supervisorctl restart captain-rtail-server', user='cchq')


@task
def deploy():
    print green('''
      ___ __ _ _ __ | |_ __ _(_)_ __
     / __/ _` | '_ \| __/ _` | | '_ \\
    | (_| (_| | |_) | || (_| | | | | |
     \___\__,_| .__/ \__\__,_|_|_| |_|
              |_|
    ''')
    print white('You are now deploying Captain!!')
    try:
        execute(update_code)
        execute(install_deps)
        execute(staticfiles)
        execute(migrate)
        execute(restart_services)
    except Exception, e:
        print e
        print red('Captain has failed to deploy')
