import sys, os

TCMD="/sbin/tc"

def runcmd(cmd):
    print('------------------------------------------------------------')
    print(cmd)
    res=os.popen(cmd).read()
    print('------------------------------------------------------------')
    return(res)

def createtc(NIC, LIMIT):
    DST_CIDR="192.168.1.1/24"
    U32CMD=TCMD+" filter add dev "+NIC+" protocol ip parent 1:0 prio 1 u32"

    runcmd(TCMD+" qdisc add dev "+NIC+" root handle 1:0 htb default 30")
    runcmd(TCMD+" class add dev "+NIC+" parent 1:0 classid 1:1 htb rate "+LIMIT)
    runcmd(U32CMD+" match ip dst "+DST_CIDR+" flowid 1:1")

def cleantc():
    runcmd(TCMD+" qdisc del dev "+NIC+" root")

# usage: python3 tcconfig.py create enp6s0f0 1000mbit

rcmd=sys.argv[1]
NIC=sys.argv[2]
LIMIT=sys.argv[3]
cleantc(NIC)
if(rcmd=='create'):
    createtc(NIC, LIMIT)
