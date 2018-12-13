import os
import sys
import json
from factories.log import create_logger


log = create_logger('users-api-configuration')


class Config(object):

    INITDB = False
    DB_URI = os.getenv('DB_URI')
    CLOUD_FOUNDRY = False
    VCAP_SERVICES = json.loads(os.getenv('VCAP_SERVICES', '{}'))

    def __init__(self):
        self.deployment_type()
        if self.CLOUD_FOUNDRY:
            self.get_vcap_db()
        else:
            if not self.DB_URI:
               log.error("DB_URI is required in non cloud foundry environments")
               sys.exit(127)

    def deployment_type(self):
        index = os.getenv('CF_INSTANCE_INDEX')
        if index:
            self.CLOUD_FOUNDRY = True
            if index == "0":
                self.INITDB = True
        else:
            if os.getenv('INITDB'):
                self.INITDB = True

    def get_vcap_db(self):
        for service, instances in self.VCAP_SERVICES.items():
            for instance in instances:
                if 'postgresql' in [x.lower() for x in instance['tags']]:
                    self.DB_URI = instance['credentials']['uri']
                    break
        if not self.DB_URI:
            log.error("Cannot find any postgresql database instances in VCAP_SERVICES!")
            sys.exit(127)
