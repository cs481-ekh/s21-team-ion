#!/bin/bash
<<<<<<< HEAD
py -m pylint main.py || pylint-exit $?
if [ $? -ne 0 ]; then
  echo "An error occurred while running pylint." >&2
  exit 1
fi
=======
py -m pylint main.py
>>>>>>> 60fbc7296f1d4fb8cb8dbd04962b019520da2a15
