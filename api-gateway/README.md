# The api-gateway test application

This directory contains all the files for creating the api gateway for this
demo.  You can generate a docker image to deploy or just deploy with a
buildpack.  The docker images are already generated and referenced in the
vars.yml file in the repo root.  The docker file is included so you can
generate the images yourself if desired.

The api gateway used is Krakend (www.krakend.io).  Its a stand alone go
binary with a single JSON file for configuration so it works well as either
a buildpack based deployment or as a docker image based deployment. Krakend
also has a nice designer that will generate the configuration for you
(https://designer.krakend.io). 

The directory is structured so that you can do either a `docker build` or
`cf push` from the root and everything will just work.  The entrypoint
script is used as the start command for both models.

# Deploying the api-gateway as a standalone application

In order to push this application as a standalone app without the rest of
the deployment you will still need to rely on the `vars.yml` file in the
root of the repo for pushing.

To push the deployment with buildpacks, run:
```
cf push -f ./manifest.yml --vars-file ../vars.yml
```
To push the deployment with docker images, run:
```
cf push -f ./manifest-docker.yml --vars-file ../vars.yml
```
