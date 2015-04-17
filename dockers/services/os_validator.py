#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import argparse
import json
import httplib

__version__ = "0.0.1"

OPERATIONS = [
    {'service': 'rabbitmq', 'oper': 'cluster_size'},
    {'service': 'rabbitmq', 'oper': 'validate_all'},
    {'service': 'galera', 'oper': 'cluster_size'}]


class OSValidator(object):
    '''
    Openstack Services Validator.
    '''
    def __init__(self, **kwargs):
        self.service = kwargs['service']
        self.operation = kwargs['operation']
        self.service_host = kwargs['service_host']
        self.service_username = kwargs['service_username']
        self.operation = kwargs['operation']
        self.monit_host = kwargs['monit_host']
        self.monit_port = kwargs['monit_port']
        self.cluster_size = kwargs['cluster_size']

    def build_url_info(self):
        '''
        Based on the service and operation, but the url path
        and body.
        '''
        method = 'GET'
        path = "/" + self.service + "/"
        body = {}
        body['operation'] = self.operation
        body['username'] = self.service_username
        body['hostname'] = self.service_host
        if self.operation == "validate_all":
            body['cluster_size'] = self.cluster_size
        body = json.dumps(body)

        return (method, path, body)

    def execute_operation(self):
        '''
        Execute the Validation task.
        '''
        conn = httplib.HTTPConnection(self.monit_host,
                                      self.monit_port)
        headers = {"Content-Type": "application/json"}
        (method, path, body) = self.build_url_info()
        print "path: ", path
        print "body: ", body
        try:
            conn.request(method, path, body, headers)
        except socket.error:
            print "Socket Error"
            sys.exit(0)

        resp = conn.getresponse()
        print "status:%s, result%s" % (resp.status, resp.read())

        return resp.read()


def show_usage():
    '''
    Help: show usage.
    '''
    usage = "\n" + "=" * 50 + "\n"
    usage += "Available operations:" + "\n"
    for operation in OPERATIONS:
        usage += " %s  %20s" % (operation['service'], operation['oper']) + "\n"
    return usage


def manage_options():
    '''
    Handling parsing of user input.
    '''
    parser = argparse.ArgumentParser(
        description='Openstack Services Validator V' + __version__,
        usage=show_usage())

    parser.add_argument('-H', '--host', dest='monit_host',
                        action='store',
                        help='IP Address/Hostname for the monitor server.',
                        metavar='<monitor_host>')

    parser.add_argument('-P', '--port', dest='monit_port',
                        action='store',
                        help='Monitor server listen port (Default: 5025)',
                        metavar='<monitor_port>')

    parser.add_argument('-S', '--service', dest='service',
                        action='store',
                        help='Specifiy the service',
                        metavar='<monitor_service>')

    parser.add_argument('-O', '--operation', dest='operation',
                        action='store',
                        help='Operation to perform',
                        metavar='<service_operation>')

    parser.add_argument('-s', '--service_host', dest='service_host',
                        action='store',
                        help='Host/IP Addr for the service',
                        metavar='<service_host>')

    parser.add_argument('-u', '--username', dest='service_username',
                        action='store',
                        help='Username to access the service',
                        metavar='<service_username>')

    parser.add_argument('-c', '--cluster_size', dest='cluster_size',
                        action='store',
                        help='Cluster size expected.',
                        metavar='<cluster_size>')


    (opts, args) = parser.parse_known_args()

    return (opts, args)


def main():
    '''
    Main
    '''
    print "In main"
    (opts, _) = manage_options()

    if not opts.monit_host:
        print "Hostname for monitor server needed"
        print show_usage()
        sys.exit(0)

    if not opts.service:
        print "Service to monitor needed"
        sys.exit(0)

    if not opts.operation:
        print "Operation needed"
        sys.exit(0)

    if not opts.service_host:
        print "service hostname/ip needed"
        sys.exit(0)

    if not opts.service_username:
        print "service username needed"
        sys.exit(0)

    if not opts.monit_port:
        print "Using default port 5025"
        opts.monit_port = 5025

    if not opts.cluster_size:
        print "Using default (3)"
        opts.cluster_size = 3

    kwargs = {}
    kwargs['service'] = opts.service
    kwargs['operation'] = opts.operation
    kwargs['service_host'] = opts.service_host
    kwargs['monit_host'] = opts.monit_host
    kwargs['monit_port'] = opts.monit_port
    kwargs['service_username'] = opts.service_username
    kwargs['operation'] = opts.operation
    kwargs['cluster_size'] = opts.cluster_size

    validator = OSValidator(**kwargs)
    validator.execute_operation()


if __name__ == '__main__':
    main()

