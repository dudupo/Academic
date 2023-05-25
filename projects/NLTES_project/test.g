primes:= [];
numbers:= [2..1000];
for p in numbers do
  Add(primes, p);
  for n in numbers do
   if n mod p = 0 then
    Unbind(numbers[n-1]);
   fi;
  od;
od;
#Print(primes, "\n");


G1:= PGL(2, 13);
Print(G1, "\n"); 


