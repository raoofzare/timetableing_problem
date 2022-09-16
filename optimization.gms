option MIP=CPLEX;

set c
    l
    d
    h
    j

scalar Dlast 'last day'  /5/
       Hfirst1 'first hour in the afternoon' /4/
       Hfirst2 /8/
       K 'number of classes' /8/
       M /55/

alias(d,d1)
alias(h,h1)

parameter
n(c)
a(c,l)
b(l,d,h)
s(j,c)
t(h,h1)
p(c,h)
;

$GDXIN %gdxincname%
$LOAD c, l, d, h, j, n, a, s, b, t, p
$GDXIN

display n, a, s, b, t, p;

variable z1,z2,z3;
binary variable delta(c,d,h);
nonnegative variable w;
nonnegative variable v(c,d);
binary variable y(c);

equation
obj1
obj2
obj3
const1
const2
const3
const4
const5
const6
const61
const7
const8
const9
;

obj1..
         z1 =e= w;

obj2..
         z2 =e= sum((c,d) $ (n(c)>1 and d.val < Dlast), v(c,d));

obj3..
         z3 =e= sum((c) $ (n(c) > 1), y(c));

const1(c)..
         sum((d,h), delta(c,d,h)) =e= n(c);

const2(d,h,h1)..
         sum((c), delta(c,d,h)) + t(h,h1)*sum((c), delta(c,d,h1)) =l= K;

const3(d,h,h1,l)..
         sum((c)$(a(c,l) = 1), delta(c,d,h)) + t(h,h1)*sum((c)$(a(c,l) = 1), delta(c,d,h1)) =l= 1;

const4(d,h,h1,j)..
         sum((c) $ (s(j,c) = 1), delta(c,d,h)) + t(h,h1)*sum((c) $ (s(j,c) = 1), delta(c,d,h1)) =l= 1;

const5(c,l,d,h) $ (a(c,l) = 1)..
         delta(c,d,h) =l= b(l,d,h);

const6(c,d) $ (n(c) > 1)..
         sum((h), delta(c,d,h)) =l= 1;

const61(c,d,h)..
         delta(c,d,h) =l= p(c,h);

const7..
         sum((c,d,h) $ (h.val = Hfirst1), delta(c,d,h)) + sum((c,d,h) $ (h.val = Hfirst2), delta(c,d,h)) - w =l= 0;

const8(c,d) $ (n(c) > 1 and d.val < Dlast)..
         sum((h), delta(c,d,h)) + sum((h), delta(c,d+1,h)) - v(c,d) =l= 1;

const9(c,d,h) $ (n(c) > 1)..
         sum((d1,h1) $ (d.val<>d1.val and h.val<>h1.val), delta(c,d1,h1)) - y(c)*(n(c)-1) =l= M*(1-delta(c,d,h));

option optcr=0;
model proj2 /obj1, const1, const2, const3, const4, const5, const6, const61, const7/;
solve proj2 using MIP minimizing z1;
display delta.l,z1.l;

equation const10;

const10..
         w =e= z1.l;
model proj2_1 /obj1, obj2, const1, const2, const3, const4, const5, const6, const61, const7, const8, const10/;
solve proj2_1 using MIP minimizing z2;
display delta.l,z1.l,z2.l;


equation const11;

const11..
         sum((c,d) $ (n(c)>1 and d.val < Dlast), v(c,d)) =e= z2.l;
model proj2_2 /obj1, obj2, obj3, const1, const2, const3, const4, const5, const6, const61, const7, const8, const9, const10, const11/;
solve proj2_2 using MIP minimizing z3;
display delta.l,z1.l,z2.l,z3.l;


