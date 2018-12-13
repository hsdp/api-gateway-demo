#!/usr/bin/env python3
import os
import sys
import argparse
import boto3
import redisdl
from boto3.session import Session


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


from config import get_config
from factories.log import create_logger


config = get_config(os.getenv('CONFIG_ENV', 'dev'))
log = create_logger('product-api-tasks')


def redis_restore(tempfile):
    with open(tempfile, 'r') as f:
        redisdl.load(
            f,
            host=config.REDIS_HOST,
            password=config.REDIS_PASSWORD
        )


def copy_from_s3(s3_key, tempfile):
    session = Session(
        aws_access_key_id=config.S3_ACCESS_KEY_ID,
        aws_secret_access_key=config.S3_SECRET_KEY_ID
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(config.S3_BUCKET)
    bucket.download_file(s3_key, tempfile)


def remove_file(tempfile):
    if os.path.exists(tempfile):
        os.remove(tempfile)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--tempfile',
        dest='tempfile',
        default='/tmp/redis.bak'
    )
    parser.add_argument(
        '-k',
        '--s3-key',
        dest='s3_key',
        default='redis.bak'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    copy_from_s3(args.s3_key, args.tempfile)
    redis_restore(args.tempfile)
    remove_file(args.tempfile)
    log.info("Redis restore complete.")


if __name__ == '__main__':
    main()
