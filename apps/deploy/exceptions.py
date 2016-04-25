class DeployAlreadyInProgress(Exception):
    pass


class FailedCaptainDeploy(Exception):
    """Called when a captain deploy has failed"""
