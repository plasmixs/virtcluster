
from common import common
from common import cli_fmwk
from utils import grc
import cmd
import inspect
import socket
import struct

class l2_cli(cli_fmwk.VCCli):
    def __init__(self, d):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Layer 2 packet definitions",
                                prompt="(cpackgen:L2)")
        self.l2_dict=d

    def do_ethernet(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        grc.debug("Ethernet define args {0}".format(args))
        j={}
        arg_lst=args.split()
        if len(arg_lst) < 3:
            self.help_ethernet()
            return
        arg_d = dict(zip(arg_lst[::2],
                         [arg_lst[i] for i in range(1, len(arg_lst), 2)]))

        j['smac']=arg_d['smac']
        j['dmac']=arg_d['dmac']
        if 'ethertype' in arg_d:
            j['ethertype']=int(arg_d['ethertype'], 16)
        if 'payload' in arg_d:
            j['payload']=arg_d['payload']
        self.l2_dict['ethernet']=j

    def help_ethernet(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("Ethernet packet definitions")
        print ("  ethernet smac <source mac> dmac <destination mac> [ethertype <ethertype [in hex]> payload <payload value>]")

class l3_cli(cli_fmwk.VCCli):
    def __init__(self, d):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Layer 3 packet definitions",
                                prompt="(cpackgen:L3)")
        self.l3_dict=d

    def do_ipv4(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        grc.debug("IPv4 define args {0}".format(args))
        j={}
        arg_lst=args.split()
        if len(arg_lst) < 2:
            self.help_ipv4()
            return
        arg_d = dict(zip(arg_lst[::2],
                         [arg_lst[i] for i in range(1, len(arg_lst), 2)]))

        j['sip']=struct.unpack("@i",
                               socket.inet_pton(socket.AF_INET,
                                                arg_d['sip']))[0]
        j['dip']=struct.unpack("@i",
                               socket.inet_pton(socket.AF_INET,
                                                arg_d['dip']))[0]
        if 'ttl' in arg_d:
            j['ttl']=int(arg_d['ttl'])
        if 'protocol' in arg_d:
            j['protocol']=int(arg_d['protocol'])
        if 'payload' in arg_d:
            j['payload']=arg_d['payload']
        if 'dscp' in arg_d:
            j['dscp']=int(arg_d['dscp'])
        self.l3_dict['ipv4']=j

    def help_ipv4(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("IPv4 packet definitions")
        print ("  ipv4 sip <source ip> dip <destination ip> [protocol <next protocol number> payload <payload value> ttl <ttl value> dscp <dscp value>]")

class l4_cli(cli_fmwk.VCCli):
    def __init__(self, d):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Layer 4 packet definitions",
                                prompt="(cpackgen:L4)")
        self.l4_dict=d

    def do_udp(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        grc.debug("UDP define args {0}".format(args))
        j={}
        arg_lst=args.split()
        if len(arg_lst) < 2:
            self.help_udp()
            return
        arg_d = dict(zip(arg_lst[::2],
                         [arg_lst[i] for i in range(1, len(arg_lst), 2)]))

        j['sport']=int(arg_d['sport'])
        j['dport']=int(arg_d['dport'])
        self.l4_dict['udp']=j

    def help_udp(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("UDP packet definitions")
        print ("  udp sport <source port> dport <destination port>")

    def do_tcp(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        grc.debug("TCP define args {0}".format(args))
        j={}
        arg_lst=args.split()
        if len(arg_lst) < 2:
            self.help_tcp()
            return
        arg_d = dict(zip(arg_lst[::2],
                         [arg_lst[i] for i in range(1, len(arg_lst), 2)]))

        j['sport']=int(arg_d['sport'])
        j['dport']=int(arg_d['dport'])
        self.l4_dict['tcp']=j

    def help_tcp(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("TCP packet definitions")
        print ("  tcp sport <source port> dport <destination port>")

class l7_cli(cli_fmwk.VCCli):
    def __init__(self, d):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Layer 7 packet definitions",
                                prompt="(cpackgen:L7)")
        self.l7_dict=d

    def do_payload(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        grc.debug("Payload define args {0}".format(args))
        j={}
        arg_lst=args.split()
        if len(arg_lst) < 2:
            self.help_payload()
            return
        arg_d = dict(zip(arg_lst[::2],
                         [arg_lst[i] for i in range(1, len(arg_lst), 2)]))

        if 'increment' == arg_d['value']:
            j['value_type']=1
            if 'step' in arg_d:
                j['step']=int(arg_d['step'])
        elif 'random' == arg_d['value']:
            j['value_type']=2
        else:
            j['value']=arg_d['value']
            j['value_type']=0
        if 'size' in arg_d:
            j['size']=int(arg_d['size'])

        self.l7_dict['payload']=j

    def help_payload(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("Payload packet definitions")
        print ("  payload value <fixed value>")
        print ("  payload value increment step <step value> size <size value>")
        print ("  payload value ramdom size <size value>")

class customPkt_cli(cli_fmwk.VCCli):
    def __init__(self, d):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Custom packet definitions",
                                prompt="(cpackgen:Custom Packet)")
        self.custom_dict=d
