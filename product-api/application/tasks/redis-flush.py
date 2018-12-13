#!/usr/bin/env python3
import os
import sys
from redis import Redis


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


from config import get_config
from factories.log import create_logger


config = get_config(os.getenv('CONFIG_ENV', 'dev'))
log = create_logger('product-api-tasks')


def main():
    r = Redis(**config.REDIS_CREDS)
    r.flushall()
    log.info("Redis data flushed!")


if __name__ == '__main__':
    main()
