# caproject
#----------------------------------------------------------------------------------------------------------------------------------------
This aim of this project is to build a program to measure the various In-Order and Out-Of-Order execution times for a given set of MIPS instructions. 
#----------------------------------------------------------------------------------------------------------------------------------------
The project is built in two parts:
1. Assuming only one pipeline exists (Sequential Instruction Execution)
2. Assuming that there are infinite pipelines available (Parallel Instruction Execution)
#---------------------------------------------------------------------------
Before each of the functionalities are executed, the program calculates the various data dependencies in the given MIPS program.
The register relations are stored in the list named 'variables'. Each register used in the MIPS program is entered into the list along with the registers on which it depends to compute it's value.
The 'variable' list is key to filtering out the various dependencies in the program. Once the 'variable' list is computed, it is used to compute each of the three types of dependencies:
1. Read After Write (RAW)
2. Write After Read (WAR)
3. Write After Write (WAW)
The dependencies are stored as two tuples in the lists 'raw','war' and 'waw' respectively.
Once calculated, the dependencies are then used to chunk out the interdependent instructions. The instructions in the chunked out lists are dependent within the list and independent across the lists
Once chunks are calculated, the execution of the instructions and calculation of the time in the form of Cycles per Instruction (CPI) is done for various cases as follows:
#---------------------------------------------------------------------------
One pipeline:
In case resources are limited to the use of one pipeline, the code follows the following sequence for instruction execution.
- Compute all possible permutations of the instructions while maintaining chunk ordering. This done using a self developed algorithm that efficiently computes only those permutations in which the chunk ordering is maintained.
- Calculate the CPI for all the various permutations computed in previous step.
- Find the minimum CPI among all the possible Out-Of-Order executions
It is to be noted that the CPI is the best possible CPI with the availability of a single pipeline.
#---------------------------------------------------------------------------
Infinite Pipelines:
In case the resources are not subject to any limits or we assume that the resources available are much larger as compared to those required. The execution follows a software implementation of Tomasulo's Algorithm where dependencies are dependent upon the use of registers. Independent instructions are added onto parallel pipelines whereas dependept ones are pipelined to the same pipeline as the dependent instruction with suitable stalls in between. It is to be duly noted that the CPI calculated here is the best possible CPI we can get for any Out-Of-Order execution of the set of instructions.
#----------------------------------------------------------------------------------------------------------------------------------------
Specifications:
The program is built using the Python programming language (Python 2.7xx)
The libraries used include:
1. itertools - for the calculation of the various permutations needed
2. re - for filtering out the MIPS program and making it abstract enough to be used by the program
3. time - to pause the program so as to give the CPU enough time to compute the results
#----------------------------------------------------------------------------------------------------------------------------------------
The program can be launched by using the Python Shell and calling the file 'caproject.py'. The prompts on screen will help users get the desired results
The files 'a.asm' , 'b.asm' , 'e.asm' are example files used during the testing of the program. The output obtained for these files are optimized and will give the best results
The program ignores any branches, loops or jump statements in the set of MIPS instructions. Any use of these will result in an omission of the line and the execution of the remaining code excluding the branch/jump/loop statement.
The program takes an exponential amount of time to compute the single pipeline results for a very large set of instructions. Any lag/hanging of the program is due to the computational burden placed on the CPU and is not a defect of the implementation.
#----------------------------------------------------------------------------------------------------------------------------------------
Credits: 
The program is a part of the Computer Architecture Semester project.
The group members include (in order of contribution)
- Santhoshini Reddy - IS201401040 - CSE UG2
- Chris Andrew - IS201401015 - CSE UG2
- Nikath Yasmeen - IS201401042 - CSE UG2
- Shriya Ragini - IS201411009 - ECE UG2
The group would also like to thank the Teaching Assistants and Prof. Amitava Das for their guidance and help in the project.
#----------------------------------------------------------------------------------------------------------------------------------------#----------------------------------------------------------------------------------------------------------------------------------------
