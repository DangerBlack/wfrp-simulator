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
from weapon import weapon
from pg import pg

#Funzioni utili sempre

def debug_print(who,s):    
    if(DBG_PP_MODE):
        print('['+who+'] '+s)
    
def d10():
    return int(random.random()*10)+1;
    
def d100():
    return int(random.random()*100)+1;
            
    
def load_pg_from_file(filename,uid=0):
    config = load_yaml_file(filename)
    a=weapon(config['weapon'][0],config['weapon'][1],config['weapon'][2],config['weapon'][3])
    f=pg().buildFromAttribute(str(uid)+' - '+config['name'],config['primary'],config['secondary'],a,config['armor'],config['faction'],config['skill'])
    return f
    
def load_fighter(folder="fighters/*"):
    fighters=[]
    count=0
    for f in glob.glob(folder):
        fighter=load_pg_from_file(f,count)
        print(fighter)
        fighters.append(fighter)
        count=count+1
    return fighters

def pN(n):
    if(n<10):
        return '  '+str(n)
    if(n<100):
        return ' '+str(n)
    return ''+str(n)            

def oneTeamLeft(fighters):
    faction=fighters[0].fazione
    for w in fighters:
        if(w.fazione!=faction):
            return False
    return True


#Simulazione vera e propria

def getEnemyRandom(fighters,me):
    copia=copy.deepcopy(fighters)
    copia.sort(key= lambda x:x.posizione*5+x.ac/10+x.ab/10) #accanisciti sul più debole, chi è lontano o nascosto è difficile che venga attaccato
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
        debug_print('system','=======================>round '+str(counter))
        for w in fighters:
            debug_print(w.nome,'sono armato di '+w.arma.name)
            e=getEnemy(fighters,w)
            if(e != False):
                debug_print(w.nome,"sceglie bersaglio ["+e.nome+"]")
                w.choseAction(fighters,e)       
                try:        
                    if(e.status==-1):
                        fighters.remove(e)
                except ValueError:
                    pass
        debug_print('system','RESETTO IL TURNO')
        for w in fighters:
            debug_print(w.nome,""+str(len(w.waitEvent)))
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

DBG_PP_MODE=config['DBG_PP_MODE']
if(not DBG_PP_MODE):
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
else:
    result=simulation(combattenti,NUMBER_OF_SIMULATION)

print(LENG_EXPLAIN)
for r in result[0]:
    print(r+': '+pN(result[0][r])+'% '+pN(round(result[1][r],2))+' '+LENG_WOUNDS+' '+pN(round(result[2][r],2))+' '+LENG_ALIVE+' '+pN(round(result[3][r],2))+' '+LENG_TURN+' ')
