import sys
from plugin.actions import actions


actions = actions()
if len(sys.argv) >= 3:
    if 'register' in sys.argv[1]:
        result = actions.register(sys.argv[2])
        if result:
            sys.exit(0)
        else:
            sys.exit(1)
response = actions.analyze()
if not response:
    print 'Sorry, but it\'s not a linux server'
else:
    print '[+] - Total Vulnerables packages: %d' % len(response['data']['packages'])
    print '[+] - Total Vulnerabilities: %d' % len(response['data']['vulnerabilities'])
    print '[+] - Packages'
    print '\n'.join(response['data']['packages'])
