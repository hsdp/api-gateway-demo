# The users-api test application

This directory contains all the files for creating the users api for this
demo.  You can generate a docker image to deploy or just deploy with a
buildpack.  The docker images are already generated and referenced in the
vars.yml file in the repo root.  The docker file is included so you can
generate the images yourself if desired.

Our demo users-api application uses postgres for its database.  When the
application starts it will detect if the database has data.  If it does not
it will automatically seed it with generated test data so that the demo is
functional.

The users api provides the following endpoints: 

* `GET /users`: returns a JSON collection of all usernames.
* `GET /user/comments/((name))`: returns a JSON object with all user comments.
* `GET /random/user`: returns a JSON object for a random users comments.
* `GET /healthcheck`: endpoint used by Cloud Foundry healthcheck.

## Deploying users-api as a standalone application

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
