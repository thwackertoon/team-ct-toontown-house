import random

def fetchAll(gender,part,pp=''):
    names = [l.strip('\n\r').split('*')[1:] for l in open(pp+"data/etc/nomes.txt","r").readlines() if not l.startswith('#')]
    
    _n = {}
    
    for name in names:
        try:_n[str(name[0])].append(name[1])
        except:
            _n[str(name[0])] = []
            _n[str(name[0])].append(name[1])
    
    if part == 't':
        return _n[('0','1')[gender=='F']]+_n['2']
        
    elif part == 'f':
        return _n[('3','4')[gender=='F']]+_n['5']
        
    elif part == 'l1':
        return _n['6']+_n['7']
        
    elif part == 'l2':
        return _n['8']

def generateRandomToonNameExt(gender,pp=""):
    names = [l.split('*')[1:] for l in open(pp+"data/etc/nomes.txt","r").readlines() if not l.startswith('#')]
    
    _n = {}
    
    for name in names:
        try:_n[str(name[0])].append(name[1])
        except:
            _n[str(name[0])] = []
            _n[str(name[0])].append(name[1])
    
    names = _n
    
    title = random.random()>.5
    last = random.random()>.5
    
    titles_f = names["1"]+names["2"]
    titles_m = names["0"]+names["2"]
    
    titles_f.sort()
    titles_m.sort()
    
    firsts_f = names["4"]+names["5"]
    firsts_m = names["3"]+names["5"]
    
    firsts_f.sort()
    firsts_m.sort()
    
    lasts1_f = names["6"]+names["7"]
    lasts1_m = lasts1_f[:]
    
    lasts1_f.sort()
    lasts1_m.sort()
    
    lasts2_f = names["8"]
    lasts2_m = lasts2_f[:]
    
    lasts2_f.sort()
    lasts2_m.sort()
    
    if gender == 'F':
        t = (titles_f.index(random.choice(titles_f)),None)[not title]
        f = firsts_f.index(random.choice(firsts_f))
        l1 = (lasts1_f.index(random.choice(lasts1_f)),None)[not last]
        l2 = (lasts2_f.index(random.choice(lasts2_f)),None)[not last]
        
    elif gender == 'M':
        t = (titles_m.index(random.choice(titles_m)),None)[not title]
        f = firsts_m.index(random.choice(firsts_m))
        l1 = (lasts1_m.index(random.choice(lasts1_m)),None)[not last]
        l2 = (lasts2_m.index(random.choice(lasts2_m)),None)[not last]
    
    return (title,True,last,[t,f,l1,l2])

def generateRandomToonName(gender,pp=""):
    names = [l.split('*')[1:] for l in open(pp+"data/etc/nomes.txt","r").readlines() if not l.startswith('#')]
    
    _n = {}
    
    for name in names:
        try:_n[str(name[0])].append(name[1])
        except:
            _n[str(name[0])] = []
            _n[str(name[0])].append(name[1])
    
    names = _n
    
    title = random.random()>.5
    last = random.random()>.5
    
    stitle = ''
    sfirst = ''
    slast = ''
    
    if title:
        g = [0,1][gender=='F']
        t = random.choice(names[str(g)]+names["2"])
        #print t,g,gender
        stitle = t+' '
            
    if True: #first
        g = [3,4][gender=='F']
        t = random.choice(names[str(g)]+names["5"])
        #print t,g,gender
        sfirst = t+' '
            
    if last: #first
        t = random.choice(names["7"])
        #print t
        slast = t
        t = random.choice(names["8"])
        #print t
        slast += t
            
    return unicode((stitle+sfirst+slast).decode('latin-1')).replace('\n','')
    
if __name__ == "__main__":
    g = random.choice(["M","F"])
    print g,generateRandomToonName(g,"../../")