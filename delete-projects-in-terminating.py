#!/usr/bin/env python
# Script to remove projects stuck in "Deleting" state
# As per solution https://access.redhat.com/solutions/4165791

import json
import sys
import subprocess
import shlex
import os

if not len(sys.argv) == 2:
    print "need name of project as argument"
    sys.exit(1)

project = sys.argv[1]
command = 'oc get project -o json %s' % format(project)

f = subprocess.check_output(shlex.split(command))
j = json.loads(f)

j['spec']['finalizers'] = []
j['apiVersion'] = 'v1'

command = 'curl -k -H "Content-Type: application/json" --cacert /etc/origin/master/ca.crt --key /etc/origin/master/admin.key --cert /etc/origin/master/admin.crt -X PUT --data-binary '+ "'" + json.dumps(j) + "'" + ' https://127.0.0.1:443/api/v1/namespaces/' + project + '/finalize'
print "Deleting project %s" % (project)

os.system(command)
