import re
list1=['add','addi','sub','subi','multi','bne','beq','bnz']
list2=['lw','sw','la','li','sb','move']
read=['lw','la','add']
datatypes=['.asciiz','.byte','.word','.text','.data','.globl',':','syscall']
fname=raw_input("Enter file name: ")
instruction=["NULL"]
variables={}
operations=["NULL"]
counter=0

def getkey(item):
  return item[0]

with open(fname,"r") as fpointer:
 for line in fpointer:
  flag=1
  for j in datatypes:
    if line.find(j)!=-1:
      flag=0
      break
    #check if line is comment
  if line[0]=='#' or line[0]=='\n':
    continue
    #check if line is assembler instruction

  elif flag==0:
    continue

  else:
    counter+=1
    div=line.split(",")
    instruction.append(div[0].split()[0])
      #pre-prcessing
    div[0]=div[0].split()[1]
    div[-1]=div[-1].split('#')[0]
    for i in range(0,len(div)):
      div[i]=div[i].strip()
      p=re.match(r'\d*\({1}\${1}\w+\W{1}',div[i])
      if p is not None:
        div[i]=div[i].split('(')[1].split(')')[0]
      div[i]=div[i].strip()
      #variables and instructions
    operations.append([instruction[counter]])
    for i in div:
      operations[counter].append(i)
    for i in range(0,len(div)):
        k=len(div)-i-1
        if not variables.has_key(div[k]):
          #print div[k]
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
l=[]
exclude=['$zero']
for x in variables.iterkeys():
  if x in exclude or x.isdigit() or str(x)[0]!='$':
    l.append(x)

for i in l:
  del variables[i]

#print variables
#print "---------------------"
#print operations  
#dependencies
#read after write
raw=[]
prev="NULL" #raw
a=['sw','sb']
b=['la','lb','lw','move','li']
prev1="NULL" #waw
first="NULL"
waw=[]
war=[]
for x in variables.iterkeys():
  for l in variables[x]:
    if len(l)<2 or (len(l)==2 and instruction[l[0]] in a):
      first=l[0]
      if prev!="NULL":
        if first!=prev:
          raw.append([first,prev])  #prev=>write,first=>read
    if len(l)>2 or (len(l)==2 and instruction[l[0]] in b):
      prev=l[0]
      first1=l[0]
      if prev1!="NULL":
        if first1!=prev1:
          waw.append([first1,prev1])
      if first !="NULL" and first!=prev:
        war.append([prev,first])
      prev1=first1
  prev="NULL"
  prev1="NULL"
  first="NULL"
#print raw
raw=sorted(raw,key=getkey)
waw=sorted(waw,key=getkey)
war=sorted(war,key=getkey)
'''
print war
print raw
print waw
'''
#------------------------------------------------------------------------------
#chunking out dependecy blocks
depset=[]
for c in war:
  if c not in depset:
   depset.append(c)
for c in raw:
  if c not in depset:
   depset.append(c)
for b in waw:
  if b not in depset:
    depset.append(b)
depset=sorted(depset,key=getkey)
#rint "------------------"
#rint depset

chunk=[]
cout=0
for i in depset:
  flag=0
  for k in chunk:
    if i[1] in k:
	k.append(i[0])
	flag=1
    elif i[0] in k:
        k.append(i[1])
        flag=1
  if flag==0:        
    chunk.append(i)

print "--------------"
a=[]
for i in chunk:
  for k in i:
   a.append(k)
b=[]
for m in range(1,len(operations)):
  if m not in a:
   b.append(m)
b.sort()

for l in b:
  print operations[l]
print "________"

for i in chunk:
   i.sort()
   for k in i:
     print operations[int(k)]
   print "--------------"
#------------------------------------------------------------------------------
#calucalting cpi
prev=-1
stall=0
for i in range(1,len(operations)):
  k=operations[i]
  for n in raw:
    if i==n[0] or i==n[1]:
     if prev==n[0] or prev==n[1]:
        stall+=1
        print k,"dependent on ",operations[prev]," stalling for 1 cycle "
  prev=i
k= 5 + len(operations) -2 + stall
print float(k)/(len(operations)-1)
  
'''opcount=0
tcpi=0
opcpi=0
for op in operations:
    opcount+=1
    opcpi=5
    for l in raw:
       if l[0]==opcount:
          opcpi+=l[0]-l[1]
    for l in waw:
       if l[0]==opcount:
          opcpi+=
    for l in war:
        if l[0]==opcount:
           opcpi+=
    tcpi+=opcpi
cpi=tcpi/opcount
print "-----> CPI : "+str(cpi)
'''

