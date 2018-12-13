#!/usr/bin/env sh

if [ -f ./vars.yml ]; then
    S3_INSTANCE_NAME=$(grep 's3_instance_name:' vars.yml | awk '{print $2}')
    POSTGRES_INSTANCE_NAME=$(grep 'postgres_instance_name:' vars.yml | awk '{print $2}')
    REDIS_INSTANCE_NAME=$(grep 'redis_instance_name:' vars.yml | awk '{print $2}')
else
    echo "vars.yml does not appear to exist in the current directory!"
    exit 1
fi

CF=$(which cf)

if [ -n "$CF" ]; then
    $CF create-service hsdp-s3 s3_bucket $S3_INSTANCE_NAME
    $CF create-service hsdp-rds postgres-micro-dev $POSTGRES_INSTANCE_NAME
    $CF create-service hsdp-redis-sentinel redis-development $REDIS_INSTANCE_NAME
else
    echo "Cannot find cf binary in your path, please install the latest cf cli tools."
    exit 1
fi
