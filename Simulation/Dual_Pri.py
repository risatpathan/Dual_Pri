#!/bin/python
import sys;
from Task import *
from  pdb import *
from math import *

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

def rbf(tau_i,tau_j,ts,t):
	if ts<t-tau_i.Di or ts>t:
		raise NameError('not correct ts')
	
# when j<i i.e., tau_j has higher o_priority
	if tau_j.o_prio<tau_i.o_prio:
		return rbf_A(tau_i,tau_j,ts,t)
# when j>i, i.e.,  tau_j has lower o_priority	
	elif tau_j.o_prio>tau_i.o_prio: 
		return rbf_B(tau_i,tau_j,ts,t)
	else:
		print "false prioity assignment"
		raise NameError('no such function')

def rbf_1(tau_i,tau_j,ts,t): # optimization technique  one
# when j<i i.e., tau_j has higher o_priority
	if tau_j.o_prio<tau_i.o_prio:
		return rbf_A_1(tau_i,tau_j,ts,t)
# when j>i, i.e.,  tau_j has lower o_priority	
	elif tau_j.o_prio>tau_i.o_prio: 
		return rbf_B_1(tau_i,tau_j,ts,t)
	
def rbf_2(tau_i,tau_j,ts,t): # optimization technique  two
# when j<i i.e., tau_j has higher o_priority
	if tau_j.o_prio<tau_i.o_prio:
		return rbf_A_2(tau_i,tau_j,ts,t)
# when j>i, i.e.,  tau_j has lower o_priority	
	elif tau_j.o_prio>tau_i.o_prio: 
		return rbf_B_2(tau_i,tau_j,ts,t)
	

def rbf_A(tau_i,tau_j,ts,t): 	# when j<i i.e., tau_j has higher o_priority
	nj,rj,Pj=short_cutj(tau_j,ts)
	ri,Pi=short_cuti(tau_i,t)
	if Pj<=Pi: 
		req=nj*tau_j.Ci+min(tau_j.Ci,ts-rj)
		return	req 
	else:	
		req=nj*tau_j.Ci+min(tau_j.Ci, max(0,ts-rj-(min(ts,Pj)-max(rj,Pi))))
		return	req

def rbf_A_1(tau_i,tau_j,ts,t):
	nj,rj,Pj=short_cutj(tau_j,ts)
	ri,Pi=short_cuti(tau_i,t)
	rjs=floor(ri/tau_j.Ti)*tau_j.Ti
	if Pj<=Pi: 
		if rj<=ri:
			return min(tau_j.Ci,max(0,ts-ri))
		else:
			return min(tau_j.Ci,max(0,ts-rj))+((rj-rjs-tau_j.Ti)/tau_j.Ti)*tau_j.Ci+min(tau_j.Ci, max(0, rjs+tau_j.Di-ri))
	elif Pj>Pi:	
		if ts<Pj and rj<=ri:
			return min(tau_j.Ci,max(0,min(ts,Pi)-ri))
		elif ts<Pj and rj>ri:
			return min(tau_j.Ci,max(0,min(ts,max(rj,Pi))-rj))+((rj-rjs-tau_j.Ti)/tau_j.Ti)*tau_j.Ci+min(tau_j.Ci, max(0, rjs+tau_j.Di-ri))
		elif ts>=Pj and rj<=ri:
			return min(tau_j.Ci, max(0,ts-ri-(Pj-Pi)))
		elif ts>=Pj and rj>ri:
			return min(tau_j.Ci, max(0, ts-rj-(Pj-max(Pi,rj))))+((rj-rjs-tau_j.Ti)/tau_j.Ti)*tau_j.Ci+min(tau_j.Ci, max(0, rjs+tau_j.Di-ri))

def rbf_A_2(tau_i,tau_j,ts,t):
	nj,rj,Pj=short_cutj(tau_j,ts)
	ri,Pi=short_cuti(tau_i,t)
	rjw=floor(Pi/tau_j.Ti)*tau_j.Ti
	if Pj<=Pi: 
		if rj<=Pi:
			return min(tau_j.Ci,max(0,ts-Pi))
		else:
			return  min(tau_j.Ci,max(0,ts-rj))+((rj-rjw-tau_j.Ti)/tau_j.Ti)*tau_j.Ci+min(tau_j.Ci, max(0, rjw+tau_j.Di-Pi))
	elif Pj>Pi:	
		if ts<Pj and rj<=Pi:
			return 0
		elif ts<Pj and rj>Pi:
			return ((rj-rjw-tau_j.Ti)/tau_j.Ti)*tau_j.Ci+min(tau_j.Ci, max(0, rjw+tau_j.Di-Pi))
		elif ts>=Pj and rj<=Pi:
			return min(ts-Pj,tau_j.Ci)
		elif ts>=Pj and rj>Pi:
			return min(tau_j.Ci,max(0,ts-Pj))+((rj-rjw-tau_j.Ti)/tau_j.Ti)*tau_j.Ci+min(tau_j.Ci, max(0, rjw+tau_j.Di-Pi))
	raise NameError('ERROR A2')





def rbf_B(tau_i,tau_j,ts,t): # when ij< i.e., tau_i has higher o_priority
	nj,rj,Pj=short_cutj(tau_j,ts)
	ri,Pi=short_cuti(tau_i,t)
	if Pi<=Pj and rj<=ri: 
		return	nj*tau_j.Ci+min(tau_j.Ci, ri-rj)
	elif Pi<=Pj and rj>ri:
		return	nj*tau_j.Ci
	elif Pi>Pj and rj<=ri:
		return	nj*tau_j.Ci+min(tau_j.Ci, ri-rj+max(0,min(ts,Pi)-max(ri,Pj)))
	elif Pi>Pj and rj>ri:
		return nj*tau_j.Ci+min(tau_j.Ci, max(0, min(ts,Pi)-Pj))
	else:
		raise NameError('Error B')
def rbf_B_1(tau_i,tau_j,ts,t):
	nj,rj,Pj=short_cutj(tau_j,ts)
	ri,Pi=short_cuti(tau_i,t)
	if Pi<=Pj and rj<=ri: 
		return 0
	elif Pi<=Pj and rj>ri:
		return min(tau_j.Ci, max(0,	min(Pi,rj-tau_j.Ti+tau_j.Di)-ri ))
	elif Pi>Pj and rj<=ri:
		return min(tau_j.Ci, max(0, min(ts,Pi)-max(Pj,ri)  ))
	elif Pi>Pj and rj>ri:
		return	min(tau_j.Ci, max(0, min(ts,Pi)-Pj))+min(tau_j.Ci, max(0,rj-tau_j.Ti+tau_j.Di-ri))
	else:
		raise NameError('Error B1')
def rbf_B_2(tau_i,tau_j,ts,t):
	return 0


def fsum(tau_i,tau_rest,ts,t):
	ri,Pi=short_cuti(tau_i,t)
	demand=dbf(tau_i,t)
	L1=max(0,dbf(tau_i,t)-tau_i.Ci)
	R1=tau_i.Ci
	L2=max(0,dbf(tau_i,t)-tau_i.Ci)
	R2=tau_i.Ci
	for tau_j in tau_rest:
		demand+=rbf(tau_i,tau_j,ts,t)
		R1+=rbf_1(tau_i,tau_j,ts,t)
		L1+=rbf(tau_i,tau_j,ts,t)-rbf_1(tau_i,tau_j,ts,t)
		R2+=rbf_2(tau_i,tau_j,ts,t)
		L2+=rbf(tau_i,tau_j,ts,t)-rbf_2(tau_i,tau_j,ts,t)
	A=min(L1,ri)+R1
	B=1000000
	if ts>Pi:
		B=min(L2,Pi)+R2
	# print A,B,demand
	return min(A,B)
	# return demand
	# return A
	# return B

def tbound(tau_i,tau_rest):
	Csum=0
	U=0
	for tau in tau_rest:
		U+=tau.Ci/tau.Ti
		Csum+=tau.Ci
	U+=tau_i.Ci/tau_i.Ti
	# print  Csum, U
	Csum+=tau_i.Di
	return ceil(Csum)/(1-U)



def dual_pri_test_task(tau_i,tau_rest):
	tF=tbound(tau_i,tau_rest)
	# print tF
	# tF=10000
	check_list=[]
	flag=False
	t=tau_i.Di
	check_list.append(t)
	while t<tF:
		t+=1
		check_list.append(t)
	for t in check_list:
		for ts in xrange(int(t-tau_i.Di),int(t)+1):
			# if t>=432 and ts==430:
			# 	pdb.set_trace()
			# 	print tau_i.Ti
			Esum=fsum(tau_i,tau_rest,ts,t)
			if Esum<=ts:
			 	flag=True
			 	# print t,ts,Esum
			 	break
		if flag==False:
			# print t,ts,Esum
			return False
		else:
			flag=False
	return True

def dual_pri_test(taskset):
	flag=True
	empty=False
	while flag==True:
		flag=False
		for tau_i in taskset:
			tau_rest=copy(taskset)
			tau_rest.remove(tau_i)
			if dual_pri_test_task(tau_i,tau_rest)==False:
				if tau_i.pi>2:
					tau_i.pi-=1
					flag=True
					break
				else:
					return False
	return True
	# for tau_i in taskset:
	# 	tau_rest=copy(taskset)
	# 	tau_rest.remove(tau_i)
	# 	if dual_pri_test_task(tau_i,tau_rest)==False:
	# 		return False
	# return True

 


x=0
for i in xrange(0,10):
	taskset=taskset_generator(0.8,10,100,1)
	pri_assign(taskset)
	promotion_set(taskset)
	if dual_pri_test(taskset)==True:
		x+=1
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
# tau_3.pi=38
# read(taskset)
# print dual_pri_test(taskset)

    # C[1]=6;  T[1]=20;  P1[1]=4; P2[1]=1;  O[1]=14;
    # C[2]=10;  T[2]=73; P1[2]=5; P2[2]=2;  O[2]=57;
    # C[3]=47;  T[3]=84; P1[3]=6; P2[3]=3;  O[3]=40;

