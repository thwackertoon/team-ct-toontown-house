import glob, os
for x in glob.glob("*/*.pyc"):
    print x
    os.unlink(x)

#copies too    
for x in glob.glob("*/*(*"):
    print x
    os.unlink(x)
    
raw_input('done!')