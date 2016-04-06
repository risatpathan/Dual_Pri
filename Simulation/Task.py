from random import *
from math import *
import pdb
from copy import *
class Task(object):
	"""docstring for task"""
	def __init__(self,Ci,Di,Ti,pi):     
		super(Task, self).__init__()
		self.Ci=Ci
		self.Di=Di
		self.Ti=Ti	
		self.pi=pi	
		self.o_prio=0	#original priority
		self.p_prio=0	#promoted priority 	 

def pri_assign(taskset):
	'''
	assign priority based on deadlines
	'''
	num=len(taskset)
	i=1
	for tau in taskset:
		tau.o_prio=num+i
		tau.p_prio=i
		i+=1

	
		
def read(taskset):
	for tau in taskset:
		print ' Ci: ',tau.Ci, ' Di: ', tau.Di, ' Ti: ', tau.Ti, 'o_prio',tau.o_prio,'p_prio',tau.p_prio,'pi',tau.pi

def promotion_set(taskset):
	'''
	assume tasks in the list is sorted
	'''
	Csum=0
	for tau_i in taskset:
		Csum+=tau_i.Ci
		tau_i.pi=tau_i.Ti-Csum
	
	
def taskset_generator(Umax,Cmax,Tmax,RD):
	'''
	return taskset sorted by deadlines
	'''
	U=0;
	taskset=[]
	while 1:
		Ci=float((randint(1,Cmax)))
		Ti=randint(ceil(Ci),Tmax)
		Di=ceil(Ci+RD*(Ti-Ci))
		tau_i=Task(Ci,Di,Ti,0)
		taskset.append(tau_i)
		U=U+Ci/Ti
		if  U>=Umax-0.02 and U<=Umax:
			taskset=sorted(taskset, key=lambda task: task.Di)  
			pri_assign(taskset)
			promotion_set(taskset)
			return  taskset
		elif U>Umax :
			U=0
			taskset=[]



# taskset=taskset_generator(0.9,5,25,1)
# read(taskset)


