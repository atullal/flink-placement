import os, sys

'''
generate schedulercfg* file for all possible placement plans
Usage: python3 permutation.py q5m_c
'''

ts=sys.argv[1]
if(ts.startswith('q5m')):
    numtasks={    # Query 5-MOD
        'Source: Source -> TimestampAssigner': 1,
        'Transform': 6,
        'SlidingWindow': 4,
        'Sink': 1
    }
elif(ts.startswith('deem')):
    numtasks={    # deem
        'Source: Source -> TimestampAssigner': 1,
        'Transform': 4,
        'Inference': 4,
        'Map': 2,
        'Sink': 1
    }


#workers_ip=['192.168.1.180', '192.168.1.181', '192.168.1.182', '192.168.1.183']
workers_ip=['192.168.1.180', '192.168.1.181', '192.168.1.182']
workers_slot=4
totslot=len(workers_ip)*workers_slot
tottask=0
for tv in numtasks:
    tottask+=numtasks[tv]
if(totslot-tottask>0):      # 'None' means empty slots if total num of tasks < total num of slots
    numtasks['None']=totslot-tottask

walked=set()
allocate=['None' for x in range(totslot)]

def runcmd(cmd):
    print('------------------------------------------------------------')
    print(cmd)
    res=os.popen(cmd).read()
    print('------------------------------------------------------------')
    return(res)

def allocate2set(allocate):
	res=[]
	for i in range(len(workers_ip)):
		ww=[]
		for j in range(workers_slot):
			idx=i*workers_slot+j
			ww.append(allocate[idx])
		ww.sort()
		res.append(tuple(ww))
	res.sort()
	return(tuple(res))

def dfs(allocate, x):
	if(x==totslot):
		walked.add(allocate2set(allocate))
	else:
		for t in numtasks.keys():
			if(numtasks[t]>=1):
				allocate[x]=t
				numtasks[t]-=1
				dfs(allocate, x+1)
				numtasks[t]+=1

def printcfg(wx, fname):
    ff=open(fname, 'w')
    tmp=numtasks.copy()
    for i in range(len(workers_ip)):
        tsklist=list(wx[i])
        for j in range(len(tsklist)):
            tskname=tsklist[j]
            tskno='('+str(tmp[tskname])+'/'+str(numtasks[tskname])+')'
            tsklist[j]=tsklist[j]+' '+tskno
            tmp[tskname]-=1
            if(tskname!='None'):
                ff.write(tsklist[j]+'; '+workers_ip[i]+'\n')
                print(tsklist[j]+'; '+workers_ip[i])
        #print(workers_ip[i])
        #print(tsklist)
    ff.close()


if __name__ == "__main__":
    print(totslot,'slots in total: ',len(workers_ip),' workers * ',workers_slot,' slots')
    cnt=0
    dfs(allocate, 0)
    print(len(walked))
    erootdir='../expresult/'+str(ts)
    edir=erootdir+'/schedulercfg_list'
    print(edir)
    runcmd('mkdir '+erootdir)
    runcmd('mkdir '+edir)
    for wx in walked:
        print(cnt,'---------------------------------')
        #print(wx)
        printcfg(wx, edir+'/schedulercfg_'+str(cnt))
        cnt+=1
    print(cnt)
