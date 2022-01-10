#!/usr/bin/env python3

import os

os.system('aws sts assume-role  --role-arn "arn:aws:iam::233105232672:role/SecurityPoCRole" --role-session-name "SecurityPoCRoleSession" --duration-seconds "43200"')
