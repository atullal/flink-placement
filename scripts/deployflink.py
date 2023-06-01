import sys,os

FLINKROOT=os.path.dirname(os.path.dirname(os.getcwd()))
print(FLINKROOT)

localip=os.popen("hostname -I").read()
print(localip)

iplist=[]

def stopflink():
    print(os.popen("cp "+FLINKROOT+"/scripts/local/* "+FLINKROOT+"/flink-dist/target/flink-1.14.0-bin/flink-1.14.0/conf/").read())
    print("stopping flink...")
    print(os.popen("cd "+FLINKROOT+"/flink-dist/target/flink-1.14.0-bin/flink-1.14.0/bin/ ; ./stop-cluster.sh").read())
    print(os.popen("rm "+FLINKROOT+"/flink-dist/target/flink-1.14.0-bin/flink-1.14.0/log/*").read())
    print(os.popen("rm -rf "+FLINKROOT+"/flinkstate/*").read())
    print("stopped flink")


def startflink():
    print("starting flink...")
    print(os.popen("cd "+FLINKROOT+"/scripts/local/").read())

    for ip in open('workers','r').readlines():
        iplist.append(ip.replace("\n",""))
    for ip in open('masters','r').readlines():
        iplist.append(ip.replace("\n","").replace(':8081',''))

    for ip in iplist:
        print(os.popen("cp flink-conf.yaml flink-conf.yaml"+ip.replace('.','')).read())
        ff=open('flink-conf.yaml'+ip.replace('.',''), 'r').read().replace('WORKERIP',ip)
        wf=open('flink-conf.yaml'+ip.replace('.',''), 'w').write(ff)

    print(os.popen("cp "+FLINKROOT+"/scripts/local/* "+FLINKROOT+"/flink-dist/target/flink-1.14.0-bin/flink-1.14.0/conf/").read())

    for ip in iplist:
        if not (ip in localip):
            print('-----------------------------------------------------')
            print(ip)
            print(os.popen('ssh '+ip+' "rm -rf '+FLINKROOT+'/flink-dist/target"').read())
            print(os.popen('ssh '+ip+' "rm -rf '+FLINKROOT+'/flinkstate/"').read())
            print(os.popen('ssh '+ip+' "mkdir '+FLINKROOT+'/"').read())
            print(os.popen('ssh '+ip+' "mkdir '+FLINKROOT+'/scripts/"').read())
            print(os.popen('ssh '+ip+' "mkdir '+FLINKROOT+'/flinkstate/"').read())
            print(os.popen('ssh '+ip+' "mkdir '+FLINKROOT+'/flink-dist"').read())
            print(os.popen('ssh '+ip+' "mkdir '+FLINKROOT+'/flink-dist/target"').read())
            print(os.popen('scp -r '+FLINKROOT+'/flink-dist/target/flink-1.14.0-bin/ '+ip+':'+FLINKROOT+'/flink-dist/target/').read())

    for ip in iplist:
        print(ip)
        print(os.popen('ssh '+ip+' "cd '+FLINKROOT+'/flink-dist/target/flink-1.14.0-bin/flink-1.14.0/conf ; mv flink-conf.yaml'+ip.replace('.','')+' flink-conf.yaml"').read())
        print(os.popen('ssh '+ip+' "cp '+FLINKROOT+'/flink-dist/target/flink-1.14.0-bin/flink-1.14.0/conf/flink-conf.yaml '+FLINKROOT+'/scripts/flink-conf.yaml"').read())    # customscheduler need to read it

    for ip in iplist:
        print(os.popen("rm flink-conf.yaml"+ip.replace('.','')).read())

    print('-----------------------------------------------------')
    print(os.popen('cd '+FLINKROOT+'/flink-dist/target/flink-1.14.0-bin/flink-1.14.0/bin ; ./start-cluster.sh').read())
    print("started flink")


ts=sys.argv[1]
stopflink()
if(ts=='start'):
    startflink()


