import os
import sys
import json
from factories.log import create_logger


log = create_logger('users-api-configuration')


class Config(object):

    CLOUD_FOUNDRY = False
    VCAP_SERVICES = json.loads(os.getenv('VCAP_SERVICES', '{}'))
    JSON_TMP_FILE = os.getenv('JSON_TMP_FILE', 'tmp.json')

    def __init__(self):
        self.deployment_type()

    def deployment_type(self):
        index = os.getenv('CF_INSTANCE_INDEX')
        if index:
            self.CLOUD_FOUNDRY = True
