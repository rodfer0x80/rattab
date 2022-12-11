#!/bin/sh

pgrep -f "sudo ./__main__.py" | xargs kill
rm -rf ./debug.log
