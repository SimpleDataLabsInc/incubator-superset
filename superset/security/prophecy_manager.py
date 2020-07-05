from flask_appbuilder.security.sqla.models import User

from superset import SupersetSecurityManager
from superset.security.metagraph_client import MetagraphClient
from superset.views.prophecy import ProphecyRemoteUserView


class ProphecySecurityManager(SupersetSecurityManager):
    authremoteuserview = ProphecyRemoteUserView
    user_model = User

    def __init__(self, appbuilder):
        super(ProphecySecurityManager, self).__init__(appbuilder)
        self.client = MetagraphClient(self)

    def find_user(self, username=None, email=None):
        return self.client.query(username)
