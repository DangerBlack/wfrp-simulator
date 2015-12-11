def debug_print(s):
    pass #print(s)
    
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
    debug_print('ndice: '+str(ndice))
    debug_print('me.mag: '+str(me.mag))
    bonus=0
    if(me.hasChanneling):
        bonus=me.mag
    value=me.tzeentchCurse(ndice,fighters)+bonus
    if(value>=dif):
        #print('incantesimo lanciato')
        target.wound(3+me.fury(True))
