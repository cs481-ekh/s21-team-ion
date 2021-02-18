#!/bin/bash
python test.py $?
if [ $? -ne 0 ]; then
  echo "An error occurred while running tests." >&2
  exit 1
else
  echo "No Errors"
fi
