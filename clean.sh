#!/bin/sh

find . -type d -name "__pycache__" -exec rm -r {} +
return 0;
