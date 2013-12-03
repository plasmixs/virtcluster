#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import common
from provision import py_libvirt

import inspect
import os
import json
import urlparse

def _prep_commision(dat_dir, fname):
    with open(fname, "w") as f:
        f.write("Initiated")
    key_fname = os.path.join(dat_dir, "host_key")
    common.exec_cmd(["ssh-keygen", "-P", "", "-f", key_fname])
    with open(fname, "w") as f:
        f.write("Done")
    return ((0, "success"))

def _check_commision_prep(dat_dir):
    prep_status=(0, "success")
    try:
        os.mkdir(dat_dir)
    except OSError:
        pass

    fname = os.path.join(dat_dir, "commision.dat")

    if not os.path.isfile(fname):
        prep_status=_prep_commision(dat_dir, fname)

    if prep_status[0] != 0:
        return prep_status

    state="Done"
    with open(fname) as f:
        state=f.readline()

    if state != "Initiated":
        if state != "Done":
            return ((-1, "commision.dat state not valid"))

    return ((0, "success"))

def _do_ssh_config(domain_dir, known_host_fname, id_fname, ip_host):
    ssh_config = os.path.join(domain_dir, "ssh_config")
    with open(ssh_config, "w") as f:
        f.write("Host {0}\n".format(ip_host[0]))
        f.write("  User root\n")
        f.write("  IdentityFile {0}\n".format(id_fname))
        f.write("  UserKnownHostsFile {0}\n".format(known_host_fname))

def _do_ssh_linkup(known_host_fname, id_fname, ip_host):
    ip=ip_host[0]
    common.exec_cmd(["ssh",
                     "-o", "UserKnownHostsFile={0}".format(known_host_fname),
                     "-o", "StrictHostKeyChecking=no",
                     "-i", id_fname,
                     ip,
                     "hostname"])
    return ((0, "success"))

def _exec_remote_cmd(ip_host, config_file, cmd):
    ip=ip_host[0]
    common.exec_cmd(["ssh",
                     "-F", config_file,
                     ip,
                     cmd])
    return ((0, "success"))

def _remote_cp(ip_host, config_file, src, dst):
    ip=ip_host[0]
    common.exec_cmd(["scp",
                     "-F", config_file,
                     src,
                     ip+":"+dst])
    return ((0, "success"))

def _do_pm_config_file(pm_config, arg_d):
    with open(pm_config, "w") as f:
        f.write("[main]\n")
        f.write("   type = rpm-md\n")
        f.write("   baseurl = {0}\n".format(arg_d['pm-url']))
    return ((0, "success"))

def start(comi_dir, arg_d):
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    dat_dir = os.path.join(comi_dir, "dat")

    ck_status = _check_commision_prep(dat_dir)
    if ck_status[0] != 0:
        return ck_status

    known_host_fname = os.path.join(dat_dir, "known_hosts")
    id_fname = os.path.join(dat_dir, "host_key.pub")

    #Proceed with domain specific commision processing.
    ip_host=py_libvirt.get_fabric_ip(arg_d['domain'])

    lk_status=_do_ssh_linkup(known_host_fname, id_fname, ip_host)
    if lk_status[0] != 0:
        return lk_status

    domain_dir = os.path.join(comi_dir, arg_d['domain'])
    try:
        os.mkdir(domain_dir)
    except OSError:
        return ((-1, "Unable to create domain directory"))

    _do_ssh_config(domain_dir, known_host_fname, id_fname, ip_host)

    ssh_config_file = os.path.join(domain_dir, "ssh_config")

    rmt_conf_dir='/opt/x86vm'
    cmd='mkdir -p {0}'.format(rmt_conf_dir)
    exec_status=_exec_remote_cmd(ip_host, ssh_config_file, cmd)
    if exec_status[0] != 0:
        return exec_status

    conf={}
    conf['pkg-mgmt']=arg_d['pkg-mgmt']

    url=urlparse.urlparse(arg_d['pm-url'])
    conf['pm-url-scheme']=url.scheme

    pm_config_fname="pm_config"
    pm_config = os.path.join(domain_dir, pm_config_fname)
    pm_status=_do_pm_config_file(pm_config, arg_d)
    if pm_status[0] != 0:
        return pm_status

    cp_status=_remote_cp(ip_host, ssh_config_file, pm_config, rmt_conf_dir)
    if cp_status[0] != 0:
        return cp_status

    conf['pm-config-file']=os.path.join(rmt_conf_dir, pm_config_fname)

    comm_fname="commision.conf"
    rem_comm_file = os.path.join(rmt_conf_dir, comm_fname)
    comm_conf = os.path.join(domain_dir, comm_fname)
    with open(comm_conf, 'w') as f:
        json.dump(conf, f)

    cp_status=_remote_cp(ip_host, ssh_config_file, comm_conf, rem_comm_file)
    if cp_status[0] != 0:
        return cp_status

    bootstrap_f = os.path.join(comi_dir, "../provision/bootstrap_com.sh")
    cp_status=_remote_cp(ip_host, ssh_config_file, bootstrap_f, rmt_conf_dir)
    if cp_status[0] != 0:
        return cp_status

    cmd="sh -x /opt/x86vm/bootstrap_com.sh {0}".format(rem_comm_file)
    exec_status=_exec_remote_cmd(ip_host, ssh_config_file, cmd)
    if exec_status[0] != 0:
        return exec_status

    return ((0, "success"))
