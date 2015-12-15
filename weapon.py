import random
#definizione delle classi delle armi e dei personaggi
class weapon:
    def __init__(self,name,kind,strength,reloadTime=0):
        self.name=name
        self.kind=kind
        self.strength=eval(strength)        
        self.reloadTime=reloadTime
        self.reloadMax=reloadTime

def debug_print(who,s):    
    #pass
    print('weapon*['+who+'] '+s)

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

def magic():
    return 0
    
def magicDart(me,target,fighters):
    dif=6
    ndice=int(dif/5-me.mag/5)
    #print('lancio incantesimo usando: '+str(max(me.mag,ndice))+' dadi')
    debug_print(me.nome,'dardo magico')
    bonus=0
    if(me.hasChanneling):
        bonus=me.mag
    value=me.tzeentchCurse(ndice,fighters)+bonus
    if(value>=dif):
        #print('incantesimo lanciato')
        target.wound(3+me.fury(True))

def releaseForce(me,target,fighters):
    dif=4
    ndice=int(dif/5-me.mag/5)
    bonus=0
    if(me.hasChanneling):
        bonus=me.mag
    value=me.tzeentchCurse(ndice,fighters)+bonus
    if(value>=dif):
        if(d100()>target.vol):
            debug_print('system','?????????????????????')
            debug_print(me.nome,'magia lanciata + effetto su ['+target.nome+']')
            debug_print('system','?????????????????????')
            target.changeWeapon(weapon('hand','sword','hands',0))
            target.addWaitEvent([2,'''self.changeWeapon(weapon('sword','sword','sword',0))'''])
            #target.arma=weapon('hand','sword','hands',0)
            #target.waitEvent.append([2,'''self.arma = weapon('hand','sword','hands',0)'''])
