#!/bin/bash

case $TIER in
    master)
        ./scripts/$1
        ;;
    staging)
        ./scripts/$1
        ;;
    develop)
        ./scripts/$1
        ;;
    *)
        echo "TIER should be either master  or staging or develop"
        exit -1
        ;;
esac

