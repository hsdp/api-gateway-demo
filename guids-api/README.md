# The guids-api test application

This directory contains all the files for creating the guids api for this
demo.  You can generate a docker image to deploy or just deploy with a
buildpack.  The docker images are already generated and referenced in the
vars.yml file in the repo root.  The docker file is included so you can
generate the images yourself if desired.

We have no idea what these guids are used for in our fictional application,
but our regulatory department won't let us deprecate it because it gets two
hits per month from unknown sources.  The guids api provides the following
endpoints: 

* `GET /`: returns a JSON object of guid mappings.

## Deploying guids-api as a standalone application

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
