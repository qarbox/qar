#!/bin/bash

# Check if root
if [ "$EUID" -ne 0 ]
  then echo "Must run as root"
  exit
fi

rm -rf /usr/local/bin/qar*
rm -rf /usr/local/share/qar/
