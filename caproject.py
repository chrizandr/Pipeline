import itertools
import re
import time
#-----------------------------------------------------------------------------------------------
def find(fin,sublist,inst):
    inst=set(inst)
    target=[]
    templist=[]
    count=0
    for each in fin:
        count+=1
        each=set(each)
        inst=set(inst)
        new=inst.difference(each)
        templist=list(itertools.combinations(new,len(sublist)))
        tar1=list(each)
        for i in templist:
            tar1=list(each)
            for j in list(i):
                tar1.append(j)
            target.append(tar1)
            
    return target
#-----------------------------------------------------------------------------------------------
def out_of_order(l1,l2):
    fin=[]
    fin=list(itertools.combinations(l2,len(l1[0])))
    for i  in range(1,len(l1)):
       fin=find(fin,l1[i],l2)
    l_1=[]
    for l in l1:
       for i in l:
        l_1.append(i)
    final=[]
    for i in range(0,len(fin)):
       temp=[]
       for j in range(0,len(l2)):
         temp.append(0)
       for j in  range(0,len(fin[i])):
         temp[fin[i][j]-1]=l_1[j]
       final.append(temp)
    return  final

#-----------------------------------------------------------------------------------------------
#Declaring variables
list1=['add','addi','sub','subi','multi','bne','beq','bnz']
list2=['lw','la','li','move']
list3=['sw','sa','sb']
read=['lw','la','add']
datatypes=['.asciiz','.byte','.word','.text','.data','.globl','syscall',':']
fname=raw_input("Enter file name: ")
instruction=["NULL"]
variables={}
operations=["NULL"]
counter=0
#Function returns first item of list
#---------------------------------------------
def getkey(item):
  return item[0]
#---------------------------------------------
#Reading the file line by line
#---------------------------------------------
with open(fname,"r") as fpointer:
#---------------------------------------------
 for line in fpointer:
  flag=1
  for j in datatypes:
    if line.find(j)!=-1:
      flag=0
      break
#Check if line is comment
#---------------------------------------------
  if line[0]=='#' or line[0]=='\n':
    continue
#Check if line is assembler instruction
#---------------------------------------------
  elif flag==0:
    continue
#---------------------------------------------
  else:
    counter+=1
    div=line.split(",")
    instruction.append(div[0].split()[0])
    #pre-processing
    #---------------------------------------------
    div[0]=div[0].split()[1]
    div[-1]=div[-1].split('#')[0]
    for i in range(0,len(div)):
      div[i]=div[i].strip()
      p=re.match(r'\d*\({1}\${1}\w+\W{1}',div[i])
      if p is not None:
        div[i]=div[i].split('(')[1].split(')')[0]
      div[i]=div[i].strip()
    #variables and instructions
    #---------------------------------------------
    operations.append([instruction[counter]])
    for i in div:
      operations[counter].append(i)
    for i in range(0,len(div)):
        k=len(div)-i-1
        if not variables.has_key(div[k]):
        #print div[k]
        #---------------------------------------------
          if instruction[counter] in list1:
            if k is 0:
              variables[div[k]]=[[counter,div[1],div[2]]]
            else:
              variables[div[k]]=[[counter]]
          elif instruction[counter] in list2:
            if k is 0:
              variables[div[k]]=[[counter,div[1]]]
            else:
              variables[div[k]]=[[counter]]
          elif instruction[counter] in list3:
            if k is 1:
              variables[div[k]]=[[counter,div[0]]]
            else:
              variables[div[k]]=[[counter]]
        else:
            if instruction[counter] in list1:
              if k is 0:
                prev=variables[div[k]]
                prev.append([counter,div[1],div[2]])
                variables[div[k]]=prev
              else:
                prev=variables[div[k]]
                prev.append([counter])
                variables[div[k]]=prev
            elif instruction[counter] in list2:
              if k is 0:
                prev=variables[div[k]]
                prev.append([counter,div[1]])
                variables[div[k]]=prev
              else:
                prev=variables[div[k]]
                prev.append([counter])
                variables[div[k]]=prev
            elif instruction[counter] in list3:
              if k is 1:
                 prev=variables[div[k]]
                 prev.append([counter,div[0]])
                 variables[div[k]]=prev
              else:
                 prev=variables[div[k]]
                 prev.append([counter])
                 variables[div[k]]=prev
#---------------------------------------------
l=[]
exclude=['$zero']
for x in variables.iterkeys():
  if x in exclude or x.isdigit() or str(x)[0]!='$':
    l.append(x)
#---------------------------------------------
for i in l:
  del variables[i]
#Dependencies calculated
#---------------------------------------------
raw=[]
prev="NULL" 
a=['sw','sb']
b=['la','lb','lw','move','li']
prev1="NULL"
first="NULL"
waw=[]
war=[]
#---------------------------------------------
for x in variables.iterkeys():
  for l in variables[x]:
    if len(l)<2 or (len(l)==2 and instruction[l[0]] in a):
      first=l[0]
      if prev!="NULL":
        if first!=prev:
          raw.append(sorted([first,prev]))  #prev=>write,first=>read
    if len(l)>2 or (len(l)==2 and instruction[l[0]] in b):
      prev=l[0]
      first1=l[0]
      if prev1!="NULL":
        if first1!=prev1:
          waw.append(sorted([first1,prev1]))
      if first !="NULL" and first!=prev:
        war.append(sorted([prev,first]))
      prev1=first1
  prev="NULL"
  prev1="NULL"
  first="NULL"
#---------------------------------------------
print "Calculating dependencies..."
time.sleep(1)
raw=sorted(raw,key=getkey)
waw=sorted(waw,key=getkey)
war=sorted(war,key=getkey)
print "The dependencies calculated are:"
print "Read after write: ",raw
print "Write after write: ",waw
print "Write after read: ",war
#---------------------------------------------
depset=[]
for c in war:
  c=sorted(c)
  if c not in depset:
   depset.append(c)
for c in raw:
  c=sorted(c)
  if c not in depset:
   depset.append(c)
for b in waw:
  b=sorted(b)
  if b not in depset:
    depset.append(b)
depset=sorted(depset,key=getkey)
#-----------------------------------------------------------------------------------------------
s=raw_input("Enter number of pipelines:\n1. One\n2. Infinite\n ")
if s=='1':
  chunk=[]
  cout=0
  for i in depset:
    flag=0
    for k in chunk:
      if i[1] in k:
          k.add(i[0])
          flag=1
      if i[0] in k:
          k.add(i[1])
          flag=1
    if flag==0:        
      chunk.append(set(i))
  for i in range(0,len(chunk)-1):
    for j in range(i+1,len(chunk)):
      if len(chunk[i]&chunk[j])>0:
        chunk[j]=chunk[i]|chunk[j]
        chunk[i].add(-1)
  chunk2=[]
  for i in chunk:
    if -1 not in i:
      chunk2.append(i)
  chunk=chunk2
  print chunk
  #---------------------------------------------
  a=[]
  for i in range(1,len(instruction)):
    a.append(i)
  #---------------------------------------------
  #In order execution CPI
  stall=0
  print "Trying in order execution first:"
  for j in range(1,len(a)):
      if sorted([a[j-1],a[j]]) in raw:
        if instruction[a[j-1]]=='lw':
          stall+=1
        elif instruction[a[j-1]]=='sw':
          stall+=2
  k=float(len(a)+stall)/len(a)
  print "CPI for in-order execution is : ",k
  time.sleep(1)
  #---------------------------------------------
  #Out of order execution for different permutations
  print "Trying out-of-order execution for different permutations of the instructions(without violating dependencies)"
  #---------------------------------------------
  fin=out_of_order(chunk,a)
  print "Found ",len(fin)," different out-of-order executions"
  #---------------------------------------------
  mincpi=999999999999.0
  count=0
  time.sleep(1)
  #---------------------------------------------
  for i in fin:
    count+=1
    print "For execution ",count,": ",
    stall=0
    for j in range(1,len(i)):
      if sorted([i[j-1],i[j]]) in raw:
        if instruction[i[j-1]]=='lw':
          stall+=1
        elif instruction[i[j-1]]=='sw':
          stall+=2
    k=float(len(i)+stall)/len(i)
    print "CPI = ",k
    if mincpi>k:
      mincpi=k
  #---------------------------------------------
  time.sleep(1)
  print "The minimum CPI found is : ",mincpi
#------------------------------------------------------------------------------------------------------
elif s=='2':
  print "Trying execution in parallel pipelines whenever possible"
  timer=[0]
  time.sleep(1)
  executed=[]
  #---------------------------------------------
  for i in range(1,len(instruction)):
    timer.append(0)
    flag=0
    temp=0
    if len(executed)>0:
       for j in executed:
           if sorted([i,j])  in raw:
              if instruction[j]=='lw':
                temp=1+timer[j]
                flag=1
              elif instruction[j]=='sw':
                temp=2+timer[j]
                flag=1
              else:
                temp=timer[j]
                flag=1
           elif sorted([i,j])  in war:
               temp=timer[j]+0
               flag=1
           elif sorted([i,j])  in waw:
               temp=timer[j]+1
               flag=1
           if timer[i]<temp:
               timer[i]=temp
       if flag==0:
           timer[i]=5
       executed.append(i)
    else:
       timer[i]=5
       executed.append(i)
  #---------------------------------------------
  print "Execution calculated:"
  for i in range(1,len(instruction)):
    print "Instruction ",i," enters at t=",timer[i]-5
  print "CPI = ",float(max(timer))/(len(instruction)-1)
#----------------------------------------------------------------------------------------------------------



