#!/bin/bash
(cd output; git add *; git commit -m "updated"; git push -f -u origin master)
