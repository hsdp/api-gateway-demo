import os
import sys
import json
from factories.log import create_logger


log = create_logger('users-api-configuration')


class Config(object):

    DEBUG = False
    VCAP_SERVICES = json.loads(os.getenv('VCAP_SERVICES', '{}'))
    REDIS_SERVICE_NAME = os.getenv('REDIS_SERVICE_NAME', 'redis')
    REDIS_HOST = os.getenv('REDIS_HOST', '')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    S3_SERVICE_NAME = os.getenv('S3_SERVICE_NAME', 's3')
    S3_ENDPOINT = os.getenv('S3_ENDPOINT', '')
    S3_SECRET_KEY_ID = os.getenv('S3_SECRET_KEY_ID', '')
    S3_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY_ID', '')
    S3_BUCKET = os.getenv('S3_BUCKET', '')

    @property
    def REDIS_CREDS(cls):
        return {
            'host': cls.REDIS_HOST,
            'port': cls.REDIS_PORT,
            'password': cls.REDIS_PASSWORD
        }


class CloudFoundryConfig(Config):

    def __init__(self):
        self._get_s3_creds()
        self._get_redis_creds()

    def _get_redis_creds(self):
        creds = self._get_vcap_service(self.REDIS_SERVICE_NAME)
        if creds:
            self.REDIS_HOST = creds['host']
            self.REDIS_PORT = creds['port']
            self.REDIS_PASSWORD = creds['password']
        else:
            log.error(
                f"Invalid service instance name for redis: {self.REDIS_SERVICE_NAME}")
            sys.exit(1)

    def _get_s3_creds(self):
        creds = self._get_vcap_service(self.S3_SERVICE_NAME)
        if creds:
            self.S3_ENDPOINT = creds['endpoint']
            self.S3_SECRET_KEY_ID = creds['secret_key']
            self.S3_ACCESS_KEY_ID = creds['api_key']
            self.S3_BUCKET = creds['bucket']
        else:
            log.error(
                f"Invalid service instance name for S3: {self.S3_SERVICE_NAME}")
            sys.exit(1)

    def _get_vcap_service(self, name):
        creds = {}
        for service, instances in self.VCAP_SERVICES.items():
            for instance in instances:
                if name.lower() == instance['name'].lower():
                    creds = instance['credentials']
                    break
        return creds


class DevConfig(Config):

    DEBUG = True

    def __init__(self):
        required_vars = [
            'REDIS_HOST', 'REDIS_PORT', 'S3_ENDPOINT',
            'S3_SECRET_KEY_ID', 'S3_ACCESS_KEY_ID', 'S3_BUCKET'
        ]
        missing = self._missing_vars(required_vars)
        if missing:
            log.error(
                f'Missing required environment variables: {",".join(missing)}')
            sys.exit(1)

    def _missing_vars(self, required_vars):
        return [x for x in required_vars if not getattr(self, x)]


def get_config(config):

    config_map = {
        'dev': DevConfig,
        'production': CloudFoundryConfig,
    }

    if config not in config_map:
        log.error(
            'Invalid value used for configuration type.  Valid values are: '
            f'{", ".join(config_map.keys())}.  Set the environment variable '
            'CONFIG_ENV to one of the valid values.'
        )
        sys.exit(1)

    return config_map[config]()
