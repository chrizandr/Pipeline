.data
array: .byte 25
decimal: .byte 25
.text
main:
la $s0,array  
li $v0,12
syscall
la $t0,0($s0) 
#sb $v0,($t0)
li $t1,0   #size of intial arrau
loop:
 li $v0,12
 syscall
 sb $v0,($t0)
 addi $t0,$t0,1
 addi $t1,$t1,1
 bne $v0,'2',loop 
li $t3,0
la $s0,array 
la $t0,0($s0)  
la $s1,decimal
la $t9,0($s1)  #size of copy
cop:
 lb $t4,($t0)
 beq $t4,'2',print
 beq $t4,'.',skip
 sb $t4,($t9)
 lb $a0,($t0)
li $v0,11
syscall 
 addi $t9,$t9,1  
 skip:
   addi $t3,$t3,1
   addi $t0,$t0,1
 ble $t3,$t1,cop
li $a0,'c'
li $v0,11
syscall  
li $a0,'o'
li $v0,11
syscall  
li $a0,'p'
li $v0,11
syscall  
li $a0,'a'
li $v0,11
syscall  
li $a0,'r'
li $v0,11
syscall  
li $a0,'\n'
li $v0,11
syscall  
print:
addi $t4,$t1,-2
la $t5,0($s1)
prinloop:
  lb $a0,($t5)
  li $v0,11
  syscall
  addi $t5,$t5,1
  ble $t5,$t4,prinloop
li $a0,'\n'
li $v0,11
syscall
la $a0,($t1)
li $v0,1
syscall


 
