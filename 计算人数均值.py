import json
import math
f = open('ccc.json', 'r')
content = f.read()
time_seq= json.loads(content)

sumI=0
sumR=0


for i in range(int(2*len(time_seq)/3),len(time_seq)):
    sumI=sumI+time_seq[i][1]
    sumR = sumR + time_seq[i][2]
sqR=0
EI=sumI/len(time_seq)*3
ER=sumR/len(time_seq)*3
sqI=0
for i in range(int(2*len(time_seq)/3),len(time_seq)):
    sqI =sqI+ (time_seq[i][1]-EI)*(time_seq[i][1]-EI)
    sqR=sqR+(time_seq[i][2]-ER)*(time_seq[i][2]-ER)

print("I均：", math.sqrt(sqI) / len(time_seq) * 3)
print("R均：",math.sqrt(sqR) / len(time_seq) * 3)