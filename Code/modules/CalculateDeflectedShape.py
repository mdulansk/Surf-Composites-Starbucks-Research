from sympy import symbols, Function, Eq, Derivative, dsolve
import matplotlib.pyplot as plt
import numpy as np

def CalculateDeflectedShape(Eval, Ival, Lval, Load):
# Define symbols
    x, L, E, I, q = symbols('x L E I q')

    # Define the unknown function
    y = Function('y')(x)

    # Define the Euler-Bernoulli equation
    beam_eq = Eq(Derivative(y, x, x, x, x), q/(E*I))

    # Define boundary conditions
    bc1 = {y.subs(x, 0): 0}
    bc2 = {y.subs(x, L): 0}
    bc3 = {Derivative(y, x, x).subs(x, 0): 0}
    bc4 = {Derivative(y, x, x).subs(x, L): 0}

    # Solve the differential equation
    sol = dsolve(beam_eq, ics={**bc1, **bc2, **bc3, **bc4})
    print(sol)

    #####################
    # User Input        #
    #####################


    qval = -Load/Lval
    deflection = sol.subs(E, Eval).subs(I, Ival).subs(L, Lval).subs(q, qval)

    def plot_deflection(deflection, Lval):
        x_vals = np.linspace(0, Lval, 100)
        y_vals = [deflection.rhs.subs(x, val).evalf() for val in x_vals]
        
        plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y_vals, label="Beam Deflection")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Deflection of the Beam')
        plt.legend()
        plt.grid(True)
        plt.show()

    plot_deflection(deflection, Lval)
