 #!/usr/bin/python
 # -*- coding: utf8 -*-
'''
	This file is part of WFRP Battle Simulator.
	WFRP Battle Simulator is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	WFRP Battle Simulator is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.
	You should have received a copy of the GNU General Public License
	along with WFRP Battle Simulator.  If not, see <http://www.gnu.org/licenses/>.

	@author DangerBlack
	@version 1.0

''' 
 
 
import random
import copy
from config import *
from multiprocessing import Pool
import multiprocessing

#Funzioni utili sempre

def debug_print(s):
	pass #print(s)
def d10():
	return int(random.random()*10)+1;
	
def d100():
	return int(random.random()*100)+1;

def sword(bf):
	return bf
	
def arrow(bf):
	return 3

def knife(bf):
	return bf-3
	
def hands(bf):
	return bf-4

def magicDart(me,target,fighters):
	dif=6
	ndice=int(dif/5-me.mag/5)
	print('lancio incantesimo usando: '+str(max(me.mag,ndice))+' dadi')
	print('ndice: '+str(ndice))
	print('me.mag: '+str(me.mag))
	value=tzeentchCurse(ndice,fighters)
	if(value>=dif):
		target.wound(3+self.fury())
			
	
def load_pg_from_file(filename):
	config = load_yaml_file(filename)
	a=weapon(config['weapon'][0],config['weapon'][1],config['weapon'][2],config['weapon'][3])
	f=pg().buildFromAttribute(config['name'],config['primary'],config['secondary'],a,config['armor'],config['faction'],config['skill'])
	return f
	
def load_fighter(folder="fighters/*"):
	fighters=[]
	for f in glob.glob(folder):
		fighter=load_pg_from_file(f)
		print(fighter)
		fighters.append(fighter)
	return fighters

def pN(n):
	if(n<10):
		return '  '+str(n)
	if(n<100):
		return ' '+str(n)
	return ''+str(n)

#definizione delle classi delle armi e dei personaggi
class weapon:
	def __init__(self,name,kind,strength,reloadTime=0):
		self.name=name
		self.kind=kind
		self.strength=eval(strength)		
		self.reloadTime=reloadTime
		self.reloadMax=reloadTime

class pg:
	status=0
	
	#variabili d'ambiente
	posizione=0 #0 mischia 1 distante 2 riparato distante
	mira=False #true o false se ha mirato
	schivata=False #ha già schivato in questo round
	cantDodge=True #non so schivare?
	parata=0 #numero di parate fatte nel round
	maxFend=0 #può parare?
	nemico=-1
	sharpshooter=10
	hasChanneling=True
	channelingTime=0
	
	
	
	def resetRoundStatus(self):
		self.mira=False
		self.schivata=self.cantDodge
		self.parata=0
		
	def __init__(self,nome=None,ac=0,ab=0,f=0,r=0,ag=0,i=0,vol=0,sim=0,a=0,fe=0,bf=0,br=0,m=0,mag=0,fol=0,pf=0,arma=weapon('sword','sword','sword'),armatura=0,fazione=0):
		self.nome=nome
		self.ab=(ab)
		self.ac=(ac)
		self.f=(f)
		self.r=(r)
		self.ag=(ag)
		self.i=(i)
		self.vol=(vol)
		self.sim=(sim)
		self.a=(a)
		self.fe=(fe)
		self.bf=(bf)
		self.br=(br)
		self.m=(m)
		self.mag=(mag)
		self.fol=(fol)
		self.pf=(pf)
		self.arma=(arma)
		self.armatura=(armatura)
		self.fazione=fazione
		self.ini=d10()+int(ag)
	
	def buildFromList(self,attribute):
		a=attribute
		self.__init__(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11],a[12],a[13],a[14],a[15],a[16],a[17],a[18],a[19])
		return self
	
	def buildFromAttribute(self,name,primary,secondary,weapon,armor,faction,skill=[]):
		attribute=[]
		attribute.append(name)
		attribute.extend(primary)
		attribute.extend(secondary)
		attribute.append(weapon)
		attribute.append(armor)
		attribute.append(faction)
		self.buildFromList(attribute)
		
		for s in skill:
			q=eval('self.'+s)
		return self
		
	def fury(self):
		dado=d10()
		if(dado<10):
			return dado
		else:
			if(self.arma.kind=='sword'):
				if(d100()>self.ac):
					return self.fury()+dado
				else:
					return dado
			else:
				if(self.arma.kind=='bow'):
					if(d100()>self.ab):
						return self.fury()+dado
					else:
						return dado
				else:
					if(self.arma.kind=='magic'):
						if(d100()>self.vol):
							return self.fury()+dado
						else:
							return dado
				
	
	def wound(self,danni):
		da_d=int(danni)-int(self.br)-int(self.armatura)
		
		if(da_d>0) and not self.schivata:
			self.schivata=True
			if(d100()<self.ag):
				debug_print(self.nome+' schiva l\'attacco')
				da_d=0
		
		if(da_d>0) and self.parata<self.maxFend:
			da_d=0
			self.parata=self.parata+1
				
		debug_print(self.nome+' subisce '+str(da_d)+' ferite')
		if(da_d>0):
			self.fe-=int(da_d)		
		if(self.fe<-5):
			self.status=-1
		else:
			if(self.fe>-5)and(self.fe<0):
				self.fe=0
			self.status=0
	
	def attackLightning(self,target):
		debug_print(self.nome+' fa un attacco fulmineo')
		for i in range(0,self.a):
			self.attack(target)
			self.nemico=target.nome
	
	def attackInCharge(self,target):
		debug_print(self.nome+' fa un attacco in carica')
		if(self.posizione>=1):
			if(d100()>self.ac+10):
				target.wound(self.arma.strength(self.bf)+self.fury())
				target.posizione=0
				self.nemico=target.nome
	
	def attack(self,target):
		debug_print(self.nome+' fa un attacco')
		if(d100()>self.ac+self.getBonusMira()):
				target.wound(self.arma.strength(self.bf)+self.fury())
				self.arma.reloadTime=self.arma.reloadMax
				self.nemico=target.nome
				
	def magic(self,fighters,target):
		pass
	
	def sight(self,target):
		debug_print(self.nome+' mira')
		self.mira=True
	
	def disengage(self,target):
		self.posizione=1
		target.posizione=1	
	
	def reloads(self,target):
		self.arma.reloadTime=self.arma.reloadTime-1
	
	
	def tzeentchCurse(self,ndice,fighters):
		res=[]
		for i in range(0,max(self.mag,ndice)):
			res.append(d10())

		value=0
		tzeentch=[0,0,0,0,0,0,0,0,0,0]
		for r in res:
			tzeentch[r]=tzeentch[r]+1
			value=value+r
		
		for t in tzeentch:
			if(t>3):
				self.catastrophicalCaosManifestation(figthers)
			else:
				if(t>2):
					self.majorCaosManifestation(fighters)
				else:
					if(t>1):
						self.minorCaosManifestation(fighters)
		
		return value
		
	
	def minorCaosManifestation(self,fighters):
		res=d100()
		if(res>96):
			self.majorCaosManifestation(self,fighters)
			return 0	
		if(res>81):
			self.mag=1
			return 0
		if(res>71):
			self.fe=self.fe-1
			self.wound(0)
			return 0
		return 0
	
	def majorCaosManifestation(self,fighters):
		res=d100()
		if(res>96):
			self.catastrophicalCaosManifestation(self,fighters)
			return 0
		if(res>81):
			self.fazione='A'
			return 0
		if(res>71):
			self.mag=1
			return 0
		if(res>61):
			self.r=self.r-10
			self.br=self.br-1
			return 0
		if(res>51):
			self.fe=self.fe-10
			self.wound(0) #check if is dead
			return 0
		if(res>41):
			self.fol=self.fol+1
			return 0
		if(res>13):
			#add famiglio a fighters
			return 0
		if(res>11):
			self.mag=0
			return 0
	
	def catastrophicalCaosManifestation(self,fighters):
		res=d100()
		if(res>81):
			self.status=-1
			self.fe=-5
			return 0
		if(res>71):
			self.fe=self.fe-10
			self.wound(0)
			return 0
		if(res>61):
			return 0 #evoca demoni minori (self.mag demoni)
		if(res>51):
			self.mag=0
			return 0
		if(res>41):
			self.fol=self.fol+d10()
			return 0
		if(res>31):
			if(d10()>5):
				self.status=-1
				self.fe=-5
			return 0
		if(res>21):
			self.status=0 #svenuto
			return 0
		if(res>11):
			self.r=self.r-20
			self.br=self.br-2
			return 0
		for f in fighters:
			f.fe=f.fe-1
			
	def getBonusMira(self):
		if(self.arma.kind=='bow'):
			if(self.mira):
				return self.sharpshooter
			else: 
				return 0
		else:
			return 0
	
	def canDodge(self):
		self.cantDodge=False
	
	def maxNumberOfFend(self,maxFend):
		self.maxFend=maxFend
	
	def isSharpshooter(self):
		self.sharpshooter=20
			
	def stampa(self):
		print(str(self))
	
	def __str__(self):
		s=''
		s=s+(str(self.nome))+'\n'
		#s=s+('  WS  BS   S   T  AG Int  WP FEL')
		s=s+config['LENG_PRIMARY']+'\n'
		s=s+(' '+pN(self.ac)+' '+pN(self.ab)+' '+pN(self.f)+' '+pN(self.r)+' '+pN(self.ag)+' '+pN(self.i)+' '+pN(self.vol)+' '+pN(self.sim))+'\n'
		s=s+config['LENG_SECONDARY']+'\n'
		#s=s+('   A   W  SB  TB   M Mag  IP  FP')
		s=s+(' '+pN(self.a)+' '+pN(self.fe)+' '+pN(self.bf)+' '+pN(self.br)+' '+pN(self.m)+' '+pN(self.mag)+' '+pN(self.fol)+' '+pN(self.pf))+'\n'
		if(not self.cantDodge):
			s+='- '+config['LENG_DODGE']+'\n'
		if(self.maxFend>0):
			s+='- '+config['LENG_FEND']+'\n'
		s=s+('Team: '+self.fazione)+'\n'
		s=s+('--------------------------------')+'\n'
		return s
		
	def __lt__(self, other):
		return self.ini > other.ini
		
	def choseAction(self,fighters,target):
		punti=2
		if(self.arma.reloadTime!=0):
			self.reloads(target)
			punti=punti-1
		
		if(self.arma.reloadTime!=0):
			self.reloads(target)
			punti=punti-1
		
		if(self.arma.kind=='bow'):
			if(punti==2):
				if(self.posizione<1) and (d10()<3):
					self.disengage(target)
				else:
					self.sight(target)
					self.attack(target)
			else:
				if(punti>=1):
					self.attack(target)
				else:
					pass
				
		if(self.arma.kind=='sword'):
			if(punti==2):
				if(target.posizione>=1):
					self.attackInCharge(target)
				else:
					self.attackLightning(target)
			else:
				self.attack(target)
		

def oneTeamLeft(fighters):
	faction=fighters[0].fazione
	for w in fighters:
		if(w.fazione!=faction):
			return False
	return True


#Simulazione vera e propria

def getEnemyRandom(fighters,me):
	copia=copy.deepcopy(fighters)
	copia.sort(key= lambda x:x.posizione*5+x.ac/10+x.ab/10)	#accanisciti sul più debole, chi è lontano o nascosto è difficile che venga attaccato
	for w in copia:
		if(w.fazione!=me.fazione):
			return w
	return False
		
def getEnemy(fighters,me):
	if(me.nemico==-1):
		return getEnemyRandom(fighters,me)
	else:
		for w in fighters:
			if(w.nome==me.nemico):
				return w
		return getEnemyRandom(fighters,me)		
	
def battle(fighters):
	fighters.sort()
	
	counter=0
	while(not oneTeamLeft(fighters)):
		debug_print('round '+str(counter))
		for w in fighters:
			e=getEnemy(fighters,w)
			if(e != False):
				debug_print(w.nome+" attacca "+e.nome)
				w.choseAction(fighters,e)		
				try:		
					if(e.status==-1):
						fighters.remove(e)
				except ValueError:
					pass	
		for w in fighters:
			w.resetRoundStatus()
		counter=counter+1
			
	fazione=fighters[0].fazione
	vita=0
	nVivi=len(fighters)	
	for w in fighters:
		vita=vita+w.fe
	vita=vita/nVivi
	turni=counter
	return (fazione,vita,nVivi,turni)	
	

def simulation(fighters,precision):
	res=[]
	for i in range(0,precision):
		copia=copy.deepcopy(fighters)
		res.append(battle(copia))
		
	
	prob={}
	vita={}
	nVivi={}
	turni={}
	for r in res:
		prob[r[0]]=prob.get(r[0],0)+1
		vita[r[0]]=vita.get(r[0],0)+float(r[1])
		nVivi[r[0]]=nVivi.get(r[0],0)+float(r[2])
		turni[r[0]]=turni.get(r[0],0)+float(r[3])
	
	for key in prob:
		vita[key]=vita[key]/prob[key]
		nVivi[key]=nVivi[key]/prob[key]
		turni[key]=turni[key]/prob[key]
		prob[key]=prob[key]*100/precision
	
	return (prob,vita,nVivi,turni)

config = load_config_file()

FOLDER=config['FOLDER']

combattenti=load_fighter(FOLDER)

NUMBER_OF_SIMULATION=config['NUMBER_OF_SIMULATION']


LENG_EXPLAIN=config['LENG_EXPLAIN']
LENG_WOUNDS=config['LENG_WOUNDS']
LENG_ALIVE=config['LENG_ALIVE']
LENG_TURN=config['LENG_TURN']


workers=[]
pool = Pool()
ncore=multiprocessing.cpu_count()
for i in range(0,ncore):
	workers.append(pool.apply_async(simulation,[combattenti,int(NUMBER_OF_SIMULATION/ncore)]))
pool.close()
pool.join()

prob={}
vita={}
nVivi={}
turni={}
for w in workers:
	res=w.get()
	for r in res[0]:
		prob[r[0]]=prob.get(r[0],0)+res[0][r[0]]	
		vita[r[0]]=vita.get(r[0],0)+float(res[1][r[0]])
		nVivi[r[0]]=nVivi.get(r[0],0)+float(res[2][r[0]])
		turni[r[0]]=turni.get(r[0],0)+float(res[3][r[0]])

for key in prob:
	vita[key]=vita[key]/len(workers)
	nVivi[key]=nVivi[key]/len(workers)
	turni[key]=turni[key]/len(workers)
	prob[key]=prob[key]/len(workers)
		
result=(prob,vita,nVivi,turni)

#result=simulation(combattenti,NUMBER_OF_SIMULATION)

print(LENG_EXPLAIN)
for r in result[0]:
	print(r+': '+pN(result[0][r])+'% '+pN(round(result[1][r],2))+' '+LENG_WOUNDS+' '+pN(round(result[2][r],2))+' '+LENG_ALIVE+' '+pN(round(result[3][r],2))+' '+LENG_TURN+' ')
