import sys
if len(sys.argv) == 2:
    open('osize','w').write(str(len(open('ToontownHouse.py.enc','rb').read())))
    sys.exit()

i = open('ToontownHouse.py','rb').read()
o = open('ToontownHouse.py.enc','wb')

key = bytearray('blah*=11.11')
kl = len(key)

def E(plaintext):
    return bytearray([ord(plaintext[i]) ^ key[i%kl] for i in xrange(len(plaintext))])

def D(ciphertext):
    return bytearray([ciphertext[i] ^ key[i%kl] for i in xrange(len(ciphertext))])

o.write(str(E(i)))    

print i == D(E(i))