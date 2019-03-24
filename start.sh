#!/usr/bin/env bash

container_name=recipe_allocation_${USER}

eval "docker run -v $(pwd):/app -d -p 5000:5000 ${container_name}"
