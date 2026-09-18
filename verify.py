import numpy as np

print("=== Problem 1: bisection ===")
def f(x):
    return (2 - 2*3**x)*x**2 + 4*(2*x-2)*3**x + 4*(2-2*x)

def f_factored(x):
    return 2*(x-2)**2*(1-3**x)

# check factorization matches
for x in [-2,-1,0,0.5,1,2,2.5,3]:
    print(x, f(x), f_factored(x))

print("\nbisection by hand, 4 iterations on [-2,3]")
a,b = -2.0,3.0
for i in range(1,5):
    c = (a+b)/2
    fa,fc = f(a), f(c)
    print(f"iter {i}: a={a:.6f} b={b:.6f} c={c:.6f} f(c)={fc:.6f}")
    if fa*fc < 0:
        b = c
    else:
        a = c
print(f"final interval [{a},{b}], midpoint={ (a+b)/2 }, error bound={ (b-a)/2 }")

print("\nnumber of iterations for error<1e-3")
n = 0
width = 5.0
while width/2 >= 1e-3:
    width /= 2
    n += 1
print("n =", n, "resulting error bound", width/2)

print("\nfull bisection to 1e-4")
a,b=-2.0,3.0
it=0
while (b-a)/2 > 1e-4:
    c=(a+b)/2
    if f(a)*f(c) < 0:
        b=c
    else:
        a=c
    it+=1
print("root approx:", (a+b)/2, "iterations:", it)

print("\n=== Problem 2: fixed point ===")
def g1(x): return (x**3+2)/3
def g2(x): return np.sign(3*x-2)*abs(3*x-2)**(1/3)
def g3(x): return (4*x-2)/(x**2+1)

def g1p(x): return x**2
def g2p(x): return 1/ (abs(3*x-2)**(2/3)) if (3*x-2)!=0 else float('inf')
def g3p(x): return -4*(x**2-x-1)/(x**2+1)**2

for name,gp in [("g1'",g1p),("g2'",g2p),("g3'",g3p)]:
    print(name, "at x=1:", gp(1), " at x=-2:", gp(-2), " at x=4:", gp(4))

for name,g in [("g1",g1),("g2",g2),("g3",g3)]:
    x_old = 1.0
    x = 4.0
    it=0
    vals=[x]
    diverged=False
    while abs(x-x_old) > 1e-6:
        x_old = x
        try:
            x = g(x)
        except Exception as e:
            print(name, "error", e); diverged=True; break
        it+=1
        vals.append(x)
        if it>200 or abs(x)>1e8:
            diverged=True
            break
    print(f"\n{name}: iterations={it}, converged_to={x if not diverged else 'DIVERGED'} , first vals={vals[:6]}")

print("\n=== Problem 3: Newton ===")
def fN(x): return x - np.exp(-x)
def fNp(x): return 1 + np.exp(-x)

x0 = 2.0
x1 = x0 - fN(x0)/fNp(x0)
x2 = x1 - fN(x1)/fNp(x1)
print("x0=",x0,"x1=",x1,"x2=",x2)

x = 2.0
it=0
while abs(fN(x)) > 0:
    xn = x - fN(x)/fNp(x)
    it+=1
    if abs(xn-x) < 1e-10:
        x = xn
        break
    x = xn
    if it>100: break
print("newton converged root:", x, "iterations:", it)

print("\n=== Problem 4 ===")
def g4(x): return 3*np.exp(np.exp(-x))/5

x = 0.0
x_old = 1.0
it=0
xs=[x]
while abs(x_old-x) > 1e-6:
    x_old = x
    x = g4(x)
    it+=1
    xs.append(x)
print("iterations:", it, "x=", x, "sequence:", xs)

def g4p(x): return -np.exp(-x)*g4(x)
# bound L on interval [min(xs), max(xs)]
lo, hi = min(xs), max(xs)
grid = np.linspace(lo,hi,10000)
L = max(abs(g4p(t)) for t in grid)
print("L bound on [",lo,hi,"] =", L)
last_step = abs(xs[-1]-xs[-2])
err_bound = L/(1-L)*last_step
print("error bound estimate:", err_bound)
