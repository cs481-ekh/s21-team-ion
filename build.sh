#!/bin/bash
pylint main.py $?
if [ $? -ne 0 ]; then
  echo "An error occurred while running pylint." >&2
  exit 1
else
  echo "no errors"
fi
