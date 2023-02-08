#!/bin/bash
BUILD_VERSION=1.0.0
docker build \
-t vibrio-detector:${BUILD_VERSION} \
.