#!/usr/bin/env python3
import os
import sys
import argparse
from uuid import uuid4
from random_words import LoremIpsum
import redis


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


from config import get_config
from factories.log import create_logger


config = get_config(os.getenv('CONFIG_ENV', 'dev'))
log = create_logger('product-api-tasks')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--redis-tag',
        dest='redis_tag',
        default=None
    )
    return parser.parse_args()


def main():
    args = parse_args()
    r = redis.Redis(**config.REDIS_CREDS)
    li = LoremIpsum()
    sentences = [li.get_sentences(10) for i in range(100)]
    for sentence in sentences:
        r.set(str(uuid4()), sentence)
    log.info("Seeded 100 records to redis.")


if __name__ == '__main__':
    main()
