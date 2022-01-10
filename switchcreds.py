#!/usr/bin/env python3

import os

creds_answer= input("What credentials would you like to switch into? (personal, cross, vr): ")
userhomedir = os.path.expanduser('~')
os.system("copy {}\.aws\credentials-{} {}\.aws\credentials".format(userhomedir,creds_answer,userhomedir))
os.system("aws sts get-caller-identity")