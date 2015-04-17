#!/bin/bash
# -----------------------------------------------
# OPSMONITOR: Utility To monitor openstack cloud
# 
# Source this file to pull dependencies like
# ansible and setup pythonpath.
# -----------------------------------------------

setup_logs="/tmp/setup.log_"`date +"%b%d%y_%H%M%S"`
curdir=`pwd`
cur_root=${curdir%/*}
old_pythonpath=${PYTHONPATH}
pythonpath="${curdir}:${rex_path}"

function git_pull () 
{
    gitrepo=$1
    localgitrepo=$2
    echo -n "pulling repo: [$gitrepo]  "
    if [[ ! -d $localgitrepo ]]; then 
        echo "Pulling $gitrepo" >> $setup_logs 2>&1
        git clone $gitrepo $localgitrepo >>  $setup_logs 2>&1
    fi

    if [[ -d $localgitrepo ]]; then
        echo " ---> [DONE]"
    else
        echo " ---> [FAILED]";echo
        echo "Error logs: $setup_logs"
    fi
}

# Add ansible git repository.
git_pull http://github.com/ansible/ansible.git ../ansible 

# Add the Ansible submodules
cd ../ansible
git submodule update --init --recursive >> $setup_logs 2>&1
cd ../opsmonit

################################################
# Set the pythonpath.
################################################
export PYTHONPATH=${pythonpath}

echo "================================================="
echo "New PYTHONPATH: '${PYTHONPATH}'"
echo "Old PYTHONPATH: '${old_pythonpath}'"
echo "================================================="

################################################
# Source the Ansible environment.
################################################
source ../ansible/hacking/env-setup


