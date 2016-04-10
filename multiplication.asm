#---------------------------#---------------------------#---------------------------START
.data
str1: .asciiz "Enter the first number:\n"
str2: .asciiz "Enter the second number:\n"
str3: .asciiz "The product is:\n"
#---------------------------variables declaration

.text
.globl main
#---------------------------main function
main:
#---------------------------print str1
la $a0,str1
li $v0,4 
syscall 
li $v0,5
syscall
move $s0,$v0
#---------------------------read 1st integer

#---------------------------print str2
la $a0,str2
li $v0,4 
syscall 
li $v0,5
syscall
move $s1,$v0
#---------------------------read 2nd integer

#---------------------------v1 stores output
li $v1,0

#---------------------------Loop started
Loop:

add $v1,$v1,$s0
#---------------------------addition
subi $s1,$s1,1
#---------------------------loop increment
bnez $s1,Loop
#---------------------------loop check

#---------------------------Loop ended
exit:
la $a0,str3
li $v0,4 
syscall 
#---------------------------print str3
move $a0,$v1
li $v0,1
syscall
#---------------------------print product

#---------------------------#---------------------------#---------------------------END