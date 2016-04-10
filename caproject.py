import re
list1=['add','addi','sub','subi','multi','bne','beq','bnz']
list2=['lw','sw','la','li','sb']
read=['lw','la','add']
datatypes=['.asciiz','.byte','.word','.text','.data','.globl',':','syscall']
fname=raw_input("Enter file name: ")
instruction=["NULL"]
variables={}
operations=["NULL"]
counter=0
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
    div[-1]=div[-1].split()[0]
    for i in range(0,len(div)):
      if re.match("\d+\W+\w+\W+",div[i]):
        div[i]=div[i].split('(')[1].split(')')[0]
        div[i]=div[i].strip(" ")
      #variables and instructions
    operations.append([instruction[counter]])
    for i in div:
      operations[counter].append(i)
    for i in range(0,len(div)):
        k=len(div)-i-1
        if not variables.has_key(div[k]):
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
for x in variables.iterkeys():
  if x=='$zero':
    l.append(x)
  if x.isdigit():
    l.append(x)
for i in l:
  del variables[i]
print operations
print instruction
print variables
#dependencies
#read after write
raw=[]
prev="NULL"
a=['sw','sb']
b=['la','lb','lw']

for x in variables.iterkeys():
 for l in variables[x]:
  if len(l)<2 or (len(l)==2 and instruction[l[0]] in a):
    first=l[0]
    if prev!="NULL":
     if (first-prev)<=5 and first!=prev:
      raw.append([first,prev])    
  if len(l)>2 or (len(l)==2 and instruction[l[0]] in b):
    prev=l[0]
prev="NULL"
print raw
print raw.sort()