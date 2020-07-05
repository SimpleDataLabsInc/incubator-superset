from superset import SupersetSecurityManager
from superset.security.metagraph_client import MetagraphClient
from superset.views.prophecy import ProphecyRemoteUserView


class ProphecySecurityManager(SupersetSecurityManager):
    authremoteuserview = ProphecyRemoteUserView

    def __init__(self, appbuilder):
        super(ProphecySecurityManager, self).__init__(appbuilder)
        self.client = MetagraphClient()

    def find_user(self, username=None, email=None):
        return self.client.query(username)
