## Overview

This repo demonstrates how its possible to implement a application on HSDP
using an API gateway.  Several new features of HSDP are used to make this
a fully functional demo.  The most important new feature is container to
container networking with internal DNS for service discovery.  This allows 
for the deployment of completely private services in Cloud Foundry.  Each
environment also has a special internal DNS domain that private apps are
deployment into: `apps.internal`.  When applications are deployed to this
domain they will be unreachable externally or internally.  Its not possible
to make these apps reachable from outside the environment.  Policies can be
be defined and applied that allow for internal traffic between applications.

When communicating via the overlay network internal traffic bypasses the
gorouter which is typically responsible for load-balancing traffic across
multiple application instances.  Round Robin DNS is used for load balancing
traffic internally between applications.  This is effectively the same (albeit
less sophisticated) function as the gorouter serves for external traffic.

Internal services are also not restricted to HTTP only.  Any TCP/UDP port
can be defined as allowed in the networking policies. 

The API gateway used in this demo is Krakend.  The Krakend API gateway is a
lightweight API gateway that consists of a single go binary and single JSON
configuration file (https://www.krakend.io/).

All other applications are simple Python web applications with some basic
services provided from HSDP infrastructure services.

Each application with complete source is stored its own directory and can be 
deployed individually or in a single deployment.  They can also be deployed
either as a buildpack based application or as a docker image.  Dockerfiles, 
manifests, and full application source are stored in each applications
directory.

**Deploying the demo**

The demo repo has manifests for deploying the api-gateway as either buildpack 
based applications or docker based applications.  Either way you will need to
ensure the backing services are created before you attempt to deploy the apps.
You can run the `create-services.sh` script in the root of the repo to create
the needed backing services for the applications.

You will need to wait for the services to fully provision before you can
continue.  You can check the output of the services with the `cf services` 
command.  Once all the services are in the `create succeeded` state you can
continue.

After the services are all in the `create succeeded` state you can deploy the
applications.  Each application can also be deployed in a standalone manner as
well from the manifest files in the projects directory.  See the README files
there for more details for deploying standalone.

To deploy the demo with buildpacks, run:

```
cf push -f manifest.yml --vars-file ./vars.yml
```

To deploy the demo with docker images, run:

```
cf push -f ./manifest-docker.yml --vars-file ./vars.yml
```

If you want to change any parameters for deployment like app names or service
instance names just edit the `vars.yml` file.  Do not edit the manifest files
directly.

Once all the applications are in the running state you will need to apply the
networking policies before the any of the internal applications deployed to
the `apps.internal` domain will reachable by the api-gateway application.

You can test this by attempting to hit one of these endpoints before applying
the security policies --

```
https://((api-gateway)).((external_domain))/guids
https://((api-gateway)).((external_domain))/products
https://((api-gateway)).((external_domain))/product/((guid))
https://((api-gateway)).((external_domain))/users
https://((api-gateway)).((external_domain))/user/comments/((username))
https://((api-gateway)).((external_domain))/random/product
https://((api-gateway)).((external_domain))/random/user
```

Any of those URLs should return a 500 at this point.

Before applying the network policies to enable traffic from the gateway to the
internal APIs we need to do a minor bootstrapping step to seed some data.  The
user-api will automatically detect it has an empty database and generate demo
data on startup.  Likewise the guids-api will automatically generate its own
data.  The product-api does require us to run a task.  All the tooling to
generate data (as well as backup to S3 and restore) are pushed with the
application.  To seed demo data in product-api run this command --

```
cf run-task product-api "application/tasks/redis-seed.py"
```

If you changed the name of the service from the default of `product-api` you
will need to update the above command to reflect that change.

Next apply the network policies that allow the  api-gateway to talk to our
private APIs by running the `create-network-policies.sh` script in the root of
the repo.

You should be able to get a response from any of those API endpoints now.  The
`/guids` endpoint will just return a _very large_ list of guids.  The
`/products` endpoint will return a collection of all product guids.  And the
`/users` endpoint will return a collection of all user names.  You can use any
of the values returned here to further query one of the APIs listed above.  Or
for the lazy you can just hit the `/random/user` or `/random/product`
endpoints to get random product descriptions or user comments.

**Caveats**

Cloud Foundry does not support the switching of an application life cycle after
an application is deployed.  What this mean is that if you deploy the demo as
a buildpack based deployment, you cannot redeploy it as a docker based
deployment.  You will need to delete all the applications before changed the
life cycle of the deployment with `cf delete ((app_name))`.

If an application fails to deploy after a successful deployment or if an
application is deleted with `cf delete` the network policies will be destroyed
as well.  You will need to re-run the `create-network-policies.sh` script if
this happens.
