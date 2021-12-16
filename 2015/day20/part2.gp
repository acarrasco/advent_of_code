n=2;
target=floor(33100000/11);
k = 50
while(vecsum(select(d -> d*k >= n, divisors(n++))) < target,);
print(n);