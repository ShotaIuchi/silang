python3 sip.py $1 -o output.ll
llvm-as output.ll -o output.bc
clang output.bc -o output.out