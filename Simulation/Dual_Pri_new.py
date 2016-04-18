#!/bin/python
import sys;
from Task import *
from  pdb import *
from math import *

odec=2
dec=2

def dbf(tau_i,t):
	'''
	demand bound function of tau_i
	'''
	return	(floor((t-tau_i.Di)/tau_i.Ti)+1)*tau_i.Ci


def short_cutj(tau_j,ts):
	nj=floor(ts/tau_j.Ti)
	rj=nj*tau_j.Ti
	Pj=rj+tau_j.pi
	return nj,rj,Pj

def short_cuti(tau_i,t):
	Pi=t-tau_i.Di+tau_i.pi
	ri=t-tau_i.Di
	return ri,Pi

def f(tau_i,tau_j,ts,t):
	if ts<t-tau_i.Di or ts>t:
		raise NameError('not correct ts')
# when j<i i.e., tau_j has higher o_priority
	if tau_j.o_prio<tau_i.o_prio:
		return f_A(tau_i,tau_j,ts,t)
# when j>i, i.e.,  tau_j has lower o_priority	
	elif tau_j.o_prio>tau_i.o_prio: 
		return f_B(tau_i,tau_j,ts,t)
	else:
		print "false prioity assignment"
		raise NameError('no such function')


	
def f_2(tau_i,tau_j,ts,t): # optimization technique  
# when j<i i.e., tau_j has higher o_priority
	if tau_j.o_prio<tau_i.o_prio:
		return f_A_2(tau_i,tau_j,ts,t)
# when j>i, i.e.,  tau_j has lower o_priority	
	elif tau_j.o_prio>tau_i.o_prio: 
		return f_B_2(tau_i,tau_j,ts,t)
	

def f_A(tau_i,tau_j,ts,t): 
# when j<i i.e., tau_j has higher o_priority
	nj,rj,Pj=short_cutj(tau_j,ts)
	ri,Pi=short_cuti(tau_i,t)
	global dec
	if Pj<=Pi: 
		if Pi-Pj>0:
			dec=min(dec,Pi-Pj)
		req=nj*tau_j.Ci+min(tau_j.Ci,ts-rj)
		return	req 
	else:	
		req=nj*tau_j.Ci+min(tau_j.Ci, ts-rj-max(0,(min(ts,Pj)-max(rj,Pi))))
		return	req



def f_A_2(tau_i,tau_j,ts,t):
	rix,Pix=short_cuti(tau_i,t)
	if tau_j.Di-tau_j.pi>=tau_j.Ci:
		rjys=max(0,Pix+tau_j.Ci-tau_j.Di)
		rjy=rjys+ floor((ts-rjys)/tau_j.Ti)*tau_j.Ti
		Pjy=rjy+tau_j.pi
		if rjy==rjys:
			return min(tau_j.Ci,ts-Pix)
		else:
			return tau_j.Ci+(rjy-rjys-tau_j.Ti)*tau_j.Ci/tau_j.Ti+min(tau_j.Ci, max(0,ts-Pjy))

	elif tau_j.Di-tau_j.pi<tau_j.Ci:
		rjys=max(0,Pix-tau_j.pi)
		rjy=rjys+ floor((ts-rjys)/tau_j.Ti)*tau_j.Ti
		Pjy=rjy+tau_j.pi
		if rjy==rjys:
			return min(tau_j.Di-tau_j.pi,ts-Pix)
		else:
			return tau_j.Di-tau_j.pi+(rjy-rjys-tau_j.Ti)*(tau_j.Di-tau_j.pi)/tau_j.Ti+min(tau_j.Di-tau_j.pi, max(0,ts-Pjy))
	raise NameError('ERROR A2')





def f_B(tau_i,tau_j,ts,t): # when ij< i.e., tau_i has higher o_priority
	nj,rj,Pj=short_cutj(tau_j,ts)
	ri,Pi=short_cuti(tau_i,t)
	global dec
	if Pi<=Pj and rj<=ri: 
		return	nj*tau_j.Ci+min(tau_j.Ci, ri-rj)
	elif Pi<=Pj and rj>ri:
		return	nj*tau_j.Ci
	elif Pi>Pj and rj<=ri:
		if Pi-Pj>0:
			dec=min(dec,Pi-Pj)
		return	nj*tau_j.Ci+min(tau_j.Ci, ri-rj+max(0,min(ts,Pi)-max(ri,Pj)))
	elif Pi>Pj and rj>ri:
		if Pi-Pj>0:
			dec=min(dec,Pi-Pj)
		return nj*tau_j.Ci+min(tau_j.Ci, max(0, min(ts,Pi)-Pj))
	else:
		raise NameError('Error B')
def f_B_2(tau_i,tau_j,ts,t):
	return 0


def fsum(tau_i,tau_rest,ts,t):
	ri,Pi=short_cuti(tau_i,t)
	demand=dbf(tau_i,t)
	L2=max(0,dbf(tau_i,t)-tau_i.Ci)
	R2=min(dbf(tau_i,t),tau_i.Ci)
	for tau_j in tau_rest:
		demand+=f(tau_i,tau_j,ts,t)
		R2+=f_2(tau_i,tau_j,ts,t)
		L2+=f(tau_i,tau_j,ts,t)-f_2(tau_i,tau_j,ts,t)
	B=100000000
	if ts>Pi:
		B=min(L2,Pi)+R2
	return min(B,demand)

def tbound(tau_i,tau_rest):
	Csum=0
	U=0
	for tau_j in tau_rest:
		U+=tau_j.Ci/tau_j.Ti
		Csum+=tau_j.Ci
	U+=tau_i.Ci/tau_i.Ti
	Csum+=tau_i.Di
	Csum+=tau_i.Ci
	return ceil(Csum)/(1-U)



def dual_pri_test_task(tau_i,tau_rest):
	tF=tbound(tau_i,tau_rest)
	# print tF
	# tF=500
	check_list=[]
	flag=False
	t=tau_i.Di
	check_list.append(t)
	while t<tF:
		t+=1
		check_list.append(t)
	for t in check_list:
		mindif=10000
		global dec
		dec=10000
		for ts in xrange(int(t-tau_i.Di+tau_i.pi),int(t)+1):
			Esum=fsum(tau_i,tau_rest,ts,t)
			if Esum<=ts:
			 	flag=True
			 	break
		if flag==False:
			mindif=min(mindif,Esum-ts)
			print 'mindif:', mindif
			return False
		else:
			flag=False
	return True

def dual_pri_test(taskset):
	global dec
	global odec
	flag=True
	empty=False
	while flag==True:
		flag=False
		for tau_i in taskset:
			tau_rest=copy(taskset)
			tau_rest.remove(tau_i)
			result=dual_pri_test_task(tau_i,tau_rest)
			dec
			if result==False:
				print 'dec', dec
				dec=min(5,max(odec,dec))
				if tau_i.pi>dec:
					print tau_i.pi, dec
					tau_i.pi-=dec
					flag=True
					break
				else:
					return False
	return True

def dual_pri_test_nt(taskset):
	for tau_i in taskset:
		tau_rest=copy(taskset)
		tau_rest.remove(tau_i)
		if dual_pri_test_task(tau_i,tau_rest)==False:
			return False
	return True

 


x=0
y=0
for i in xrange(0,100):
	taskset=taskset_generator(0.97,5,100,1)
	pri_assign(taskset)
	promotion_set(taskset)
	# read(taskset)
	if dual_pri_test(taskset)==True:
		print 1
		# print dual_pri_test(taskset)
		x+=1
		# read(taskset)
	else:
		print 0
print x

# fsum(tau_2,[tau_1,tau_3],432,432)
# tau_1.pi=5
# tau_2.pi=24
# tau_3.pi=20
# pdb.set_trace()
# print dual_pri_test_task(tau_2,[tau_1,tau_3])
# print dual_pri_test(taskset)

# tau_1=Task(2.0,8.0,8.0,0)
# tau_2=Task(9.0,36.0,36.0,0)
# tau_3=Task(31.0,62.0,62.0,0)

# taskset=[tau_1,tau_2,tau_3]
# pri_assign(taskset)
# promotion_set(taskset)
# # tau_2.pi=23
# read(taskset)
# print dual_pri_test(taskset)

    # C[1]=6;  T[1]=20;  P1[1]=4; P2[1]=1;  O[1]=14;
    # C[2]=10;  T[2]=73; P1[2]=5; P2[2]=2;  O[2]=57;
    # C[3]=47;  T[3]=84; P1[3]=6; P2[3]=3;  O[3]=40;

