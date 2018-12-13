#!/usr/bin/env python3
import os
import sys
import logging
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


def backup_redis(outfile):
    with open(outfile, 'w') as f:
        redisdl.dump(
            f,
            host=config.REDIS_HOST,
            password=config.REDIS_PASSWORD,
        )


def copy_to_s3(outfile, s3_key):
    session = Session(
        aws_access_key_id=config.S3_ACCESS_KEY_ID,
        aws_secret_access_key=config.S3_SECRET_KEY_ID
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(config.S3_BUCKET)
    data = open(outfile, 'rb')
    bucket.put_object(Key=s3_key, Body=data)


def remove_file(outfile):
    if os.path.exists(outfile):
        os.remove(outfile)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--s3-tag',
        dest='s3_tag',
        default=None
    )
    parser.add_argument(
        '--redis-tag',
        dest='redis_tag',
        default=None
    )
    parser.add_argument(
        '-f',
        '--outfile',
        dest='outfile',
        default='/tmp/redis.bak'
    )
    parser.add_argument(
        '-s',
        '--s3-key',
        dest='s3_key',
        default='redis.bak'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    backup_redis(args.outfile)
    copy_to_s3(args.outfile, args.s3_key)
    remove_file(args.outfile)
    log.info("Redis backup complete.")


if __name__ == '__main__':
    main()
