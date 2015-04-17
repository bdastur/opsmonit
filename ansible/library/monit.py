#!/usr/bin/env python
# -*- coding: utf-8 -*-

MONITOR_DEPENDENCIES_MET = True
PKG_ERRORS = ""

try:
    import psutil
except ImportError as imperr:
    MONITOR_DEPENDENCIES_MET = False


class Monitor(object):
    '''
    Monitoring Operations on Remote hosts.
    '''
    OPERATIONS = {
        'cpu_usage': 'cpu_usage'}

    def __init__(self, module):
        '''
        Initialize Monitor
        '''
        self.module = module

    def execute_operation(self):
        '''
        Execute operations
        '''
        operation = self.module.params.get('operation', None)
        if not operation:
            self.module.fail_json(failed=True, msg="Invalid Operation")



        func = Monitor.OPERATIONS.get(operation, None)
        if not func:
            self.module.fail_json(failed=True,
                                  msg="Invalid check. Not supported")
        func = getattr(self, func)

        result = {}
        result['params'] = self.module.params
        result['result'] = func()

        if result['result']['status'] == 'PASS':
            self.module.exit_json(changed=False, **result)
        elif result['result']['status'] == 'FAIL':
            self.module.fail_json(failed=True, **result)


    def cpu_usage(self):
        '''
        Get the CPU Usage.
        '''
        result = {}
        result['cpu_percent'] = []
        for _ in range(3):
            cpu_list = psutil.cpu_percent(interval=1, percpu=True)
            result['cpu_percent'].append(cpu_list)

        result['status'] = 'PASS'
        return result


def check_dependencies(module):
    '''
    Check if the required packags are present on the
    host.
    '''
    if not MONITOR_DEPENDENCIES_MET:
        msg = ("Packages Not available on host for Monitor module")
        module.fail_json(failed=True, msg=msg)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            operation=dict(required=True, alias=['args']),
            arguments=dict(aliases=['args'], default=''),
        ),
        supports_check_mode=True
    )

    if module.params['operation'] is None:
        module.fail_json(msg="Operation not specified")

    check_dependencies(module)

    monitor = Monitor(module)
    monitor.execute_operation()



from ansible.module_utils.basic import *
main()

