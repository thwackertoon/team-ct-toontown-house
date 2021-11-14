import subprocess as sb

mn = raw_input("module name:")

data = open("basic.c","rb").read()
with open(mn+".c","wb") as f:
    f.write(data.replace("*",mn))

sb.call("gcc -shared -IC:\Panda3D-1.8.0\python\include -LC:\Panda3D-1.8.0\python\include -LC:\Panda3D-1.8.0\python\libs -o {0}.pyd {0}.c -lpython27".format(mn))
raw_input('done!')