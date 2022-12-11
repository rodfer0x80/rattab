#!/bin/sh

sudo ls >/dev/null
sudo ./__main__.py >/dev/null 2>&1 &
