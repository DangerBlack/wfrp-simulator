 #!/usr/bin/python
 # -*- coding: utf8 -*-
from weapon import *
from config import *

config = load_config_file()
DBG_PP_MODE=config['DBG_PP_MODE']

def debug_print(who,s):    
    if(DBG_PP_MODE):
        print('pg*['+who+'] '+s)

def pN(n):
    if(n<10):
        return '  '+str(n)
    if(n<100):
        return ' '+str(n)
    return ''+str(n)   

class pg:    
    def resetRoundStatus(self):
        self.mira=False
        self.schivata=self.cantDodge
        self.parata=0
        for w in (self.waitEvent):
            debug_print(self.nome,'QUQUE EVENT TIMER IS '+str(w[0]))
            if(w[0]<=0):
                debug_print(self.nome,"RING RING EVENT ->| "+self.nome+" | "+w[1]+" | "+self.arma.name)
                eval(w[1])
                debug_print(self.nome,self.arma.name)
                try:        
                    self.waitEvent.remove(w)
                except ValueError:
                    pass
            else:
                w[0]=w[0]-1
                
        
        
        
    def __init__(self,nome=None,ac=0,ab=0,f=0,r=0,ag=0,i=0,vol=0,sim=0,a=0,fe=0,bf=0,br=0,m=0,mag=0,fol=0,pf=0,arma=weapon('sword','sword','sword'),armatura=0,fazione=0):
        self.status=0
        #variabili d'ambiente
        self.posizione=0 #0 mischia 1 distante 2 riparato distante
        self.mira=False #true o false se ha mirato
        self.schivata=False #ha già schivato in questo round
        self.cantDodge=True #non so schivare?
        self.parata=0 #numero di parate fatte nel round
        self.maxFend=0 #può parare?
        self.nemico=-1
        self.sharpshooter=10
        self.hasChanneling=True
        self.channelingTime=0
        self.knowSpell=[] #list of list - [name, kind, function, round requested], kind= attack, defence, buffer, evocation,
        self.waitEvent=[] #list of event that have a timer [timer, callback]
        self.azioni=2 #number of action in a round
        
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
        
    def fury(self,magic=False):
        dado=d10()
        if(dado<10):
            return dado
        else:
            if(magic):
                if(d100()>self.vol):
                    return self.fury()+dado
                else:
                    return dado
            if(self.arma.kind=='sword'):
                if(d100()>self.ac):
                    return self.fury()+dado
                else:
                    return dado
            if(self.arma.kind=='bow'):
                if(d100()>self.ab):
                    return self.fury()+dado
                else:
                    return dado
            return dado
                    
                
    
    def wound(self,danni,magic=False):
        da_d=int(danni)-int(self.br)-int(self.armatura)
        
        if(da_d>0) and not self.schivata and not magic:
            self.schivata=True
            if(d100()<self.ag):
                debug_print(self.nome,' schiva l\'attacco')
                da_d=0
        
        if(da_d>0) and self.parata<self.maxFend and not magic:
            da_d=0
            debug_print(self.nome,' para l\'attacco')
            self.parata=self.parata+1
                
        debug_print(self.nome,'subisce ['+str(da_d)+'/'+str(self.fe)+'] ferite')
        if(da_d>0):
            self.fe-=int(da_d)      
        if(self.fe<=-5):
            self.status=-1
        else:
            if(self.fe>-5)and(self.fe<0):
                self.fe=0
            self.status=0
    
    def attackLightning(self,target):
        debug_print(self.nome,' fa un attacco fulmineo')
        for i in range(0,self.a):
            self.attack(target)
            self.nemico=target.nome
        debug_print(self.nome,' concluso attacco fulmineo')
    
    def attackInCharge(self,target):
        debug_print(self.nome,' fa un attacco in carica')
        if(self.posizione>=1):
            if(d100()>self.ac+10):
                target.wound(self.arma.strength(self.bf)+self.fury())
                target.posizione=0
                self.nemico=target.nome
        debug_print(self.nome,' concluso attacco in carica')
    
    def attack(self,target):
        debug_print(self.nome,' fa un attacco')
        if(d100()>self.ac+self.getBonusMira()):
                target.wound(self.arma.strength(self.bf)+self.fury())
                self.arma.reloadTime=self.arma.reloadMax
                self.nemico=target.nome
        debug_print(self.nome,' concluso attacco')
                
    def magic(self,knowSpell=[]):
        self.knowSpell=knowSpell
    
    def sight(self,target):
        debug_print(self.nome,' mira')
        self.mira=True
    
    def disengage(self,target):
        self.posizione=1
        target.posizione=1  
    
    def reloads(self,target):
        debug_print(self.nome,' ricarico')
        self.arma.reloadTime=self.arma.reloadTime-1
    
    def changeWeapon(self,w):
        droppedWeapon=self.arma
        self.arma=w
    
    def addWaitEvent(self,event):
        self.waitEvent.append(event);
        
    def tzeentchCurse(self,ndice,fighters):
        res=[]
        for i in range(0,max(self.mag,ndice)):
            res.append(d10())

        value=0
        tzeentch=[0,0,0,0,0,0,0,0,0,0,0]
        for r in res:
            tzeentch[r]=tzeentch[r]+1
            value=value+r
        
        res=0
        for t in tzeentch:
            if(t>3):
                res=self.catastrophicalCaosManifestation(fighters)
                print('tzeentch CURSE '+str(res))
            else:
                if(t>2):
                    res=self.majorCaosManifestation(fighters)
                    print('tzeentch CURSE '+str(res))
                else:
                    if(t>1):
                        res=self.minorCaosManifestation(fighters)
                        print('tzeentch CURSE '+str(res))
        return value
        
    
    def minorCaosManifestation(self,fighters):
        #print('minor curse')
        res=d100()
        if(res>96):
            self.majorCaosManifestation(fighters)
            return -1    
        if(res>81):
            self.addWaitEvent([d10(),'self.setMag(\''+str(int(self.mag)+1)+'\')'])
            self.mag=self.mag-1
            return -2
        if(res>71):
            self.fe=self.fe-1
            self.wound(0)
            return -3
        return 0
    
    def majorCaosManifestation(self,fighters):
        #print('major curse')
        res=d100()
        if(res>96):
            self.catastrophicalCaosManifestation(fighters)
            return -4
        if(res>81):
            self.addWaitEvent([d10(),'self.changeFaction(\''+self.fazione+ '\')'])
            self.fazione='A'
            return -5
        if(res>71):
            self.mag=self.mag-1
            return -6
        if(res>61):
            self.r=self.r-10
            self.br=self.br-1
            return -7
        if(res>51):
            self.fe=self.fe-10
            self.wound(0) #check if is dead
            return -8
        if(res>41):
            self.fol=self.fol+1
            return -9
        if(res>13):
            #add imps to the fighters
            fighters.append(pg('Daemon Imps',35,0,40,33,40,30,33,15,1,12,4,3,3,0,0,0,weapon('claws','sword','sword'),0,'A'))
            return -10
        if(res>11):
            self.mag=0
            return -11
    
    def catastrophicalCaosManifestation(self,fighters):
        debug_print(self.nome,'OH MY GOD - CHTULHU IS HERE')
        res=d100()
        if(res>81):
            self.status=-1
            self.fe=-5
            return -12
        if(res>71):
            self.fe=self.fe-d10()
            self.wound(0)
            return -13
        if(res>61):
            for i in range(0,self.mag):
                fighters.append(pg('Evoc '+str(i)+' Daemon',50,40,45,45,50,35,50,15,2,15,4,4,4,0,0,0,weapon('claws','sword','sword'),0,'A'))
            return -14 #evoca demoni minori (self.mag demoni)
        if(res>51):
            self.mag=0
            return -15
        if(res>41):
            self.fol=self.fol+d10()
            return -16
        if(res>31):
            if(d10()>5):#critico random
                self.status=-1
                self.fe=-5
            return -17
        if(res>21):
            time=d10()*6
            self.addWaitEvent([d10(),'self.setAction(\''+str(self.azioni)+ '\')'])
            self.addWaitEvent([d10(),'self.setBr(\''+str(self.br)+ '\')'])
            self.azioni=0
            self.br=0
            return -18
        if(res>11):
            self.r=self.r-20
            self.br=self.br-2
            return -19
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
    
    def changeFaction(self,faction):
        self.fazione=faction
    
    def setMag(self,mag):
        self.mag=int(mag)
    
    def setAction(self,action):
        self.action=int(action)    
    
    def setBr(self,br):
        self.br=int(br)
                
    def stampa(self):
        print(str(self))
    
    def __str__(self):
        config = load_config_file()
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
        punti=self.azioni
        if(not self.arma.reloadTime==0):
            self.reloads(target)
            punti=punti-1
        
        if(not self.arma.reloadTime==0):
            self.reloads(target)
            punti=punti-1
        
        if(self.mag>1 and d100()>50):
            chosedSpell=self.knowSpell[int(random.random()*len(self.knowSpell))]
            #chosedSpell=self.knowSpell[1]
            eval(chosedSpell[2]+'(self,target,fighters)')            
            #magicDart(self,target,fighters)
            punti=punti-chosedSpell[3]
        
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
