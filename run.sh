#!/bin/bash
pelican
(cd output; python -m pelican.server 9001)
