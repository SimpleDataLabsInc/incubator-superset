import json
import time
import datetime

from flask_appbuilder.security.sqla.models import User
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface


class MetagraphClient(ModelView):
    datamodel = SQLAInterface(User)

    def __init__(self, manager):
        self.user_model = manager.user_model if manager else User
        from superset import conf
        self.manager = manager
        metagraph_transport = RequestsHTTPTransport(
            url=conf["METAGRAPH_URL"],
            verify=False,
            retries=3,
        )
        self.client = Client(
            transport=metagraph_transport,
            fetch_schema_from_transport=True,
        )

    def to_formatted(self, date):
        print(datetime.datetime.fromtimestamp(date / 1000.0).strftime('%c'))
        return date


    def query(self, token):
        query = gql('''{
          User(token: "%s") {
          _id
          firstName
          lastName
          email
            aspects(aspect: [Info]) {
              AspectName
              AspectValue
              schema
            }
          }
        }''' % token)
        print(dir(MetagraphClient.datamodel))
        try:
            value = self.client.execute(query)
            user = value["User"]
            info = [v for v in user["aspects"] if v["AspectName"] == "Info"]
            token = json.loads(info[0]["AspectValue"])["token"]
            token, expires = token["token"], token["expires"]
            now = int(time.time() * 1000)
            if expires > now:
                if self.manager:
                    self.manager.log.info("Valid User Found")
                return User(id = user["_id"], username = token, email = user["email"], first_name = user["firstName"], last_name = user["lastName"], active = True)
            else:
                if self.manager:
                    self.manager.log.info("User Token Expired")
                return None
        except Exception as e:
            print(e)
            return None
