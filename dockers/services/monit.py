#!/usr/bin/env python

'''
Most basic flask application:

Initialization:
* All Flask applications must create an application instance.
* The webserver passes all requests from clients to this object for handling
  using WSGI (Web Server Gateway Interface)

Routes and View Functions:
* Clients such as web browsers send requests to the web server, which in turn
  sends them to the flask app.
* Flask keeps a mapping of URL to python functions. This association is called a
  route
'''

import json
import rabbitmqadmin
from flask import Flask, request
app = Flask(__name__)

options = None


def rabbitmqadmin_init(request_data):
    global options
    if not options:
        (options, args) = rabbitmqadmin.make_configuration()
    options.username = request_data['username']
    options.hostname = request_data['hostname']
    options.port = "15672"
    print "username: %s, hostname: %s " % (options.username, options.hostname)


@app.route("/")
def index():
    return "<h1>Openstack Services Monitoring Console</h1>"


@app.route("/rabbitmq/", methods=['GET', 'POST'])
def rabbit_operations():
    if request.headers['Content-Type'] == "application/json":
        print "BRD: application/json"
        request_data = request.json
    else:
        print "Request content should be application/json"
        return 400

    rabbitmqadmin_init(request_data)

    operation = request_data['operation']
    print "operation: ", operation

    args = ["list", "nodes", "name"]
    mgmt = rabbitmqadmin.Management(options, args[1:])
    cols = args[1:]
    (uri, obj_info) = mgmt.list_show_uri(rabbitmqadmin.LISTABLE,
                                         'list', cols)
    print "uri: ", uri
    nodes_list = mgmt.get(uri).split(",")

    if operation == "cluster_size":
        print "nodes: ", nodes_list
        len_nodes = len(nodes_list)
        print "Cluzter size: ", len_nodes
        return str(len_nodes)
    elif operation == "validate_all":
        #Check cluster size.
        expected_size = int(request_data.get('cluster_size', 3))
        len_nodes = len(nodes_list)
        print "Expected size: %d, Nodes cnt: %d" % (expected_size, len_nodes)
        if expected_size == len_nodes:
            return json.dumps({'STATUS': 'STATUS_OK'})
        else:
            return json.dumps({'STATUS': 'STATUS_FAIL'})
    else:
        return "other oper"


@app.route("/rabbit/cluster_status")
def rabbit_clusterstatus():
    global options
    if not options:
        (options, args) = rabbitmqadmin.make_configuration()
    options.username = 'guest'
    options.hostname = "172.22.191.199"
    options.port = "15672"
    args = ["list", "nodes", "name"]
    mgmt = rabbitmqadmin.Management(options, args[1:])
    cols = args[1:]
    (uri, obj_info) = mgmt.list_show_uri(rabbitmqadmin.LISTABLE, 'list', cols)
    print "uri: ", uri
    return mgmt.get(uri)


@app.route("/user/<name>")
def user(name):
    return "<h1> Hello %s! </h1>" % name


'''
The applciation instance has a run method, that launches Flask's integrated
development web server.
'''
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5025, debug = True)


