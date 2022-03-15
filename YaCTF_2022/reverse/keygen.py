from pwn import *

payload = "yactf{"
f = ["None"] * 20
f[4] = "-"
f[9] = "-"
f[14] = "-"
f[0] = 8
f[6] = 5
f[8] = 6
f[10] = 7
f[11] = 8
f[12] = 2
f[15] = 3
f[16] = 4
f[17] = 7
f[19] = "}"
#crackme = process("crackme_22fd0d55.elf")
#crackme.recvline()
for f[5] in range(1, 8):
    for f[13] in range(2, 10):
        for f[18] in range(3, 9):
            for f[1] in range(0, 10):
                for f[7] in range(1, 8):
                    for f[2] in range(0, 10):
                        for f[3] in range(0, 10):
                            v7 = f[2] + f[1] + 8 + f[3]
                            v8 = f[12] + f[11] + f[10] + f[13]
                            if ( (f[17] + f[16] + f[15] + f[18]) != (f[7] + f[6] + f[5] + f[8] + v7 + v8) / 3):
                                continue;
                            #if ( v7 != (f[17] + f[16] + f[15] + f[18]) / 2 ):
                                #continue;
                            #if ( (f[7] + f[6] + f[5] + f[8]) != (v8 - 7) ):
                                #continue;
                            if ( (v8 + v7) != 33 ):
                                continue;
                            if((f[5] + v8) != 31):
                                continue;
                            key = payload
                            crackme = process("./crackme_22fd0d55.elf")
                            crackme.recvline()
                            for k in f:
                                key+=str(k)
                            print(key)
                            crackme.sendline(key)
                            output = crackme.recvlineS()
                            if( output.split()[0] == "Congrats!"):
                                print(output)
                            crackme.close()



