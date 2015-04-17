FROM centos:centos7
MAINTAINER Behzad Dastur <bdastur@cisco.com>

###########################################################
# Yum Packages 
############################################################
RUN yum install -y openssl mariadb

# Enable EPEL Repositories for Juno openstack release.
RUN yum install -y yum-plugin-priorities
RUN yum install -y http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
RUN yum install -y http://rdo.fedorapeople.org/openstack-juno/rdo-release-juno.rpm
RUN yum upgrade -y

RUN yum install -y \
          python-novaclient \
          python-glanceclient \
           python-keystoneclient

RUN yum install -y python-flask
RUN yum clean all 

ADD ./monit_start.sh /monit_start.sh
ADD ./rabbitmqadmin /rabbit/rabbitmqadmin

# Run the ops-monit start script.
CMD ["/monit_start.sh"]

