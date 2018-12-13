# The product-api test application

This directory contains all the files for creating the product api for this
demo.  You can generate a docker image to deploy or just deploy with a
buildpack.  The docker images are already generated and referenced in the
vars.yml file in the repo root.  The docker file is included so you can
generate the images yourself if desired.

Our demo product-api uses Redis to store information about our products.  It
also requires an S3 bucket and can backup the contents of the Redis DB to the
S3 bucket with a Cloud Foundry task.

The product api provides the following endpoints --

* `GET /products`: returns a JSON collection of all product guids.
* `GET /product/((guid))`: returns a JSON object with product details.
* `GET /random/product`: returns a JSON object for a random product.
* `GET /healthcheck`: endpoint used by Cloud Foundry healthcheck.

## Deploying product-api as a standalone application

If you deploy the application from this directory as a standalone application
it will be deployed on a public domain.  When deployed from the root of the
repo as part of the demo it will be deployed as an internal application and
not reachable directly.  See the `vars.yml` file in the repo root to see
the external vs internal domain names.

To deploy the application with a buildpack, run:
```
cf push -f manifest.yml --vars-file ../vars.yml
```
To deploy the application as a docker image, run:
```
cf push -f manifest-docker.yml --vars-file ../vars.yml
```

### Tasks for the product-api application

The product-api ships with some scripts used to perform some bootstrapping
and housekeeping tasks.

**Creating seed data in the Redis DB**
```
cf run-task product-api "application/tasks/redis-seed.py"
```
If you are watching the logs you should see some output like this -
`2018-02-25T07:52:17.28-0800 [APP/TASK/068ea2c7/0] OUT Added 100 records
to redis.`

**Backup data to S3**
```
cf run-task product-api "application/tasks/redis-backup.py"
```
This will backup all the data currently in Redis to the S3 service instance
bound to the application.  You can verify by going to the S3 service dashboard
and inspecting the bucket contents.  If you are watching the logs you should
see a message like this when the backup in complete --
`2018-02-25T08:19:36.19-0800 [APP/TASK/b5a6d8ba/0] OUT Redis backup complete.`

**Flush data from Redis**
```
cf run-task product-api "application/tasks/redis-flush.py"
```
This task should purge all the data currently in the Redis instance.
`2018-02-25T08:21:03.67-0800 [APP/TASK/3bb855da/0] OUT Redis data flushed!`

**Restore data to Redis**
```
cf run-task product-api "application/tasks/redis-restore.py"
```
This will restore the data backup in S3 to the running Redis instance.  You
should see a log message like this when the restore is complete --
`2018-02-25T08:24:21.05-0800 [APP/TASK/889efbb7/0] OUT Redis restore complete.`
