#! /usr/bin/python3

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/juliettedebono/spodeezer/env/lib/python3.9/site-packages/")
sys.path.insert(0, '/home/juliettedebono/spodeezer')
from spodeezer import app as application
