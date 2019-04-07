from threading import Thread
import threading 
import random
import time

def isThinking(philosopher):
	print("Philosopher {} is thinking and waiting.\n".format(philosopher + 1))
	time.sleep(1)
	
def hasStartedEating(lock, philosopher, mode):
	lock.acquire() #Lock internally uses semaphores
	if mode == 0:
		print("Philosopher {} has started eating with fork {} and {}.".format(philosopher + 1, philosopher + 1, num_philosophers if philosopher == 0 else philosopher))
		forks[philosopher] = 1
		forks[philosopher - 1] = 1
		print("Forks :", forks, "Plates :", plates,"\n")
	else:
		print("Philosopher {} has started eating with fork {} and {}.".format(philosopher + 1, philosopher + 1, (philosopher + 1) % num_philosophers + 1))
		forks[philosopher] = 1
		forks[(philosopher + 1) % num_philosophers] = 1
		print("Forks :", forks, "Plates :", plates, "\n")
	lock.release()	#Releases the semaphores
	
def hasFinishedEating(philosopher, mode):
	if mode == 0:
		print("Philosopher {} has finished eating and released fork {} and {}.".format(philosopher + 1, philosopher + 1, num_philosophers if philosopher == 0 else philosopher))
		forks[philosopher] = 0
		forks[philosopher - 1] = 0
		plates[philosopher] = 1
		print("Forks :", forks, "Plates :", plates, "\n")
	else:
		print("Philosopher {} has finished eating and released fork {} and {}.".format(philosopher + 1, philosopher + 1, (philosopher + 1) % num_philosophers + 1))
		forks[philosopher] = 0
		forks[(philosopher + 1) % num_philosophers] = 0
		plates[philosopher] = 1
		print("Forks :", forks, "Plates :", plates, "\n")

lock = threading.Lock() #Initialize lock
		
num_philosophers = int(input("Enter number of philosophers: ")) #Take number of philosophers from user
forks = [0] * num_philosophers #Initialize forks
plates = [0] * num_philosophers #Initialize plates
print("\nForks :", forks, "Plates :",plates) #Print first state

plist = random.sample(range(num_philosophers), num_philosophers) #Generate random list(no copies) of philosophers
plist1 = [] #Used for function hasFinishedEating

mode = [] #Mode list for storing 0 or 1; 0 looks to the left and 1 looks to the right

print("\n----Queue for Eating----")
for philosopher in plist:
	print("Philosopher {}".format(philosopher + 1))
print("------------------------\n")

while len(plist) != 0:
	for philosopher in plist:
		if forks[philosopher] == 0 and forks[philosopher - 1] == 0 and plates[philosopher] == 0:
			mode.append(0)
			plist1.append(philosopher)
			thread = Thread(target = hasStartedEating, args = (lock, philosopher, 0, ))
			thread.start()
			plist = plist[: plist.index(philosopher)] + plist[plist.index(philosopher) + 1 :]
			time.sleep(1)
		elif forks[philosopher] == 0 and forks[(philosopher + 1) % num_philosophers] == 0 and plates[philosopher] == 0:
			mode.append(1)
			plist1.append(philosopher)
			thread = Thread(target = hasStartedEating, args = (lock, philosopher, 1, ))
			thread.start()
			plist = plist[: plist.index(philosopher)] + plist[plist.index(philosopher) + 1 :]
			time.sleep(1)
		else:
			isThinking(philosopher)
	for philosopher in plist1:
		hasFinishedEating(philosopher, mode[plist1.index(philosopher)])
		time.sleep(1)
	plist1 = [] #Flushing contents of plist1 
	mode = [] #Flushing contents of mode
