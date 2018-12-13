#!/usr/bin/env sh

if [ -f ./vars.yml ]; then
    API_GATEWAY=$(grep 'api_gateway:' vars.yml | awk '{print $2}')
    GUIDS_API=$(grep 'guids_api:' vars.yml | awk '{print $2}')
    PRODUCT_API=$(grep 'product_api:' vars.yml | awk '{print $2}')
    USERS_API=$(grep 'users_api:' vars.yml | awk '{print $2}')
else
    echo "vars.yml does not appear to exist in the current directory!"
    exit 1
fi

CF=$(which cf)

if [ -n "$CF" ]; then
    $CF add-network-policy $API_GATEWAY --destination-app $GUIDS_API --protocol tcp --port 8080
    $CF add-network-policy $API_GATEWAY --destination-app $PRODUCT_API --protocol tcp --port 8080
    $CF add-network-policy $API_GATEWAY --destination-app $USERS_API --protocol tcp --port 8080
else
    echo "Cannot find cf binary in your path, please install the latest cf cli tools."
fi
