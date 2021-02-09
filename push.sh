#!/bin/bash
set -e
TIME=$(date "+%Y%m%D%H%M")
git add .
git commit -m "${TIME}"
git push
