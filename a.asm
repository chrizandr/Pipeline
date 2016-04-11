addi   $gp, $zero, 1000   # putting base address 1000 into
lw   $s2, 4($gp)               # loading variable b into $s2
lw   $s3, ($gp)               # loading variable c into $s3
add $s1, $s2, $s3           # sum in $s1
sw   $s1, $gp                  # storing sum into variable a
addi $s1,$s1,4
addi $s4,$s1,$s5
