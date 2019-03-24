#!/usr/bin/env bash

container_name=recipe_allocation_${USER}

eval "docker run -d -p 5000:5000 ${container_name}"
