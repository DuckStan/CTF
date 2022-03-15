import itertools
import random
import threading
import time
def main_proc(seconds):

    payload = list(range(0,64))
    vars =[0, 1]
    combo = [-1]*64
    ideal = False
    counter = 0
    first_f = 63
    maxis = 0
    while(counter < 64):
        #random.seed()
        for init in range(0, 64):
            first_f = init
            random.seed()
            for i in range(0, 64):
                if(random.random() > 0.5):
                    for j in range(0, 64):
                        second_f = j
                        mnozh_1 = first_f//8
                        ostatok_1 = first_f - 8*mnozh_1
                        mnozh_2 = second_f//8
                        ostatok_2 = second_f - 8*mnozh_2
                        if(random.random() < 0.5):
                            if(abs(mnozh_1 - mnozh_2)==2) and (abs(ostatok_1 - ostatok_2) ==1):
                                if(combo[second_f] == -1): #and (random.random() > 0.05):
                                    counter +=1
                                    combo[second_f] = payload[i]
                                    first_f = second_f
                                    break
                                else:
                                    continue
                            elif (abs(mnozh_1-mnozh_2)==1) and (abs(ostatok_1-ostatok_2)==2):
                                if(combo[second_f] == -1): #and (random.random() > 0.05):
                                    counter +=1
                                    combo[second_f] = payload[i]
                                    first_f = second_f
                                    break
                                else:
                                    continue    
                        else:
                            if (abs(mnozh_1-mnozh_2)==1) and (abs(ostatok_1-ostatok_2)==2):
                                if(combo[second_f] == -1): #and (random.random() > 0.05):
                                    counter +=1
                                    combo[second_f] = payload[i]
                                    first_f = second_f
                                    break
                                else:
                                    continue    
                            elif(abs(mnozh_1 - mnozh_2)==2) and (abs(ostatok_1 - ostatok_2) ==1):
                                if(combo[second_f] == -1): #and (random.random() > 0.05):
                                    counter +=1
                                    combo[second_f] = payload[i]
                                    first_f = second_f
                                    break
                                else:
                                    continue
                else:
                    for j in reversed(range(0, 64)):
                        second_f = j
                        mnozh_1 = first_f//8
                        ostatok_1 = first_f - 8*mnozh_1
                        mnozh_2 = second_f//8
                        ostatok_2 = second_f - 8*mnozh_2
                        if(random.random() > 0.5):
                            if(abs(mnozh_1 - mnozh_2)==2) and (abs(ostatok_1 - ostatok_2) ==1):
                                if(combo[second_f] == -1): #and (random.random() > 0.05):
                                    counter +=1
                                    combo[second_f] = payload[i]
                                    first_f = second_f
                                    break
                                else:
                                    continue
                            elif (abs(mnozh_1-mnozh_2)==1) and (abs(ostatok_1-ostatok_2)==2):
                                if(combo[second_f] == -1): #and (random.random() > 0.05):
                                    counter +=1
                                    combo[second_f] = payload[i]
                                    first_f = second_f
                                    break
                                else:
                                    continue    
                        else:
                            if (abs(mnozh_1-mnozh_2)==1) and (abs(ostatok_1-ostatok_2)==2):
                                if(combo[second_f] == -1): #and (random.random() > 0.05):
                                    counter +=1
                                    combo[second_f] = payload[i]
                                    first_f = second_f
                                    break
                                else:
                                    continue    
                            elif(abs(mnozh_1 - mnozh_2)==2) and (abs(ostatok_1 - ostatok_2) ==1):
                                if(combo[second_f] == -1): #and (random.random() > 0.05):
                                    counter +=1
                                    combo[second_f] = payload[i]
                                    first_f = second_f
                                    break
                                else:
                                    continue
                                
            if(counter > maxis):
                maxis = counter
                print(combo)
                print(maxis)
            if(counter == 64):
                print("Yes!seq")
                print(combo)
                break
            counter = 0
            combo = [-1] *64
    print(combo)

start = time.perf_counter()
t = threading.Thread(target=main_proc, args=[1])
t.start()
print(f'Active Threads: {threading.active_count()}')
t.join()
end = time.perf_counter()
print(f'Finished in {round(end-start, 2)} second(s)')                
