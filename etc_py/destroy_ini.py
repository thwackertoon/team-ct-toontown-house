import os

def r(path="."):
    if os.path.isfile(path):
        if path.endswith("desktop.ini"):
            print path
            os.system("attrib -h -s %s" %path)
            os.unlink(path)
        
    else:
        for x in os.listdir(path):
            r(os.path.join(path,x))
    
    
r()