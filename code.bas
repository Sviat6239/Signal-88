let numA = 10
let numB = 20
let numC = 0
let numD = 5
let numE = 2
let numF = 3
let numG = 1

add numC numA numB
add numC numC numD
add numC numC numE
add numC numC numF

sub numC numC numD
add numC numC numD

mul numC numC numA
div numC numG numD

print "text"
tostr numA
print numA
toint numA


if numA == 10 then
    print "ten"
elseif numA == 5 then
    print "five"
elseif numA == 15 then
    print "fiveteen"
else 
    print "another value"
end if                
