languages = {
             'en':'BotEN_nacib',
            }
            
def dumpLangs():
    print '-'*10
    print 'Avaiable languages:'
    print '-'*10
    for lang in languages.keys():
        print '\t',lang
    print '-'*10
    
dumpLangs()
language = '__none__'
while not language in languages: language = raw_input('what language do you wanna?')
exec 'import %s as lang' % languages[language]

class Bot(object):
    pass
    