#!/bin/bash
pelican
(cd output; python -m pelican.server 8000 0.0.0.0)
