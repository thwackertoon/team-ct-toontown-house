#include "Python.h"

extern char binary_ToontownHouse_py_enc_start[];
extern char binary_osize_start[];

const char jdeooepo[11] = "blah*=11.11";

const int kl = 11;

void decrypt(char *s, int l)
{
    int i;
    //l = strlen(s);
    int v;
    for(i = 0; i < l; i++) {
        v = s[i] ^ jdeooepo[i%kl];
        s[i] = v;
        }
        
}

int main (int argc, char *argv[])
{
    char *p;
    p = binary_ToontownHouse_py_enc_start;
    int sz = atoi((char *)binary_osize_start);
    
    printf("Starting game bootloader. Size: %i\n",sz);
    
    /*extern int Py_NoSiteFlag;
    Py_NoSiteFlag = 1;*/
    
    Py_SetProgramName(argv[0]);
	Py_InitializeEx(0);
    
    printf("Python Init\n");
    
    PySys_SetArgv(argc, argv);
    decrypt(p,sz);
    printf("Game data read and decrypted, starting...\n");
    PyRun_SimpleString(p);
	return 0;
}
