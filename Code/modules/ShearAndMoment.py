import sys
sys.path.append('../classes')
import numpy as np
import sympy as sym
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def shear_and_moment(P,L,Lw):
    # Define the symbols
    P = -P
    a, b, c, x, = sym.symbols('a b c x')

    # # Define the function
    # w = a*x**2 + b*x + c

    # # Define the equations
    # eq1 = sym.Eq(sym.integrate(w, (x, -Lw, Lw)), P)
    # eq2 = sym.Eq(w.subs(x, -Lw), 0)
    # eq3 = sym.Eq(w.subs(x, Lw), 0)

    # Solve the system of equations
    # solution = sym.solve((eq1, eq2, eq3), (a, b, c))
    # a_val = solution[a]
    # b_val = solution[b]
    # c_val = solution[c]

    x_vals = np.linspace(-10, 10, 1000)
    fig = make_subplots(rows=3,cols=1)

    # #Plotting Distributed Parabolic Load
    # w_solve = a_val*x**2 + b_val*x + c_val
    # wexpr1,wcond1 = 0, sym.And(-L<x,x<-Lw)
    # wexpr2,wcond2 = w_solve,sym.And(-Lw<x,x<Lw)
    # wexpr3,wcond3 = 0, sym.And(Lw<x,x<L)
    # w = sym.Piecewise((wexpr1,wcond1),(wexpr2,wcond2),(wexpr3,wcond3))
    # w_vals = np.array([float(sym.N(w.subs('x', x))) for x in x_vals])
    # w_val_at_0 = float(sym.N(w.subs('x', 0)))
    # fig.add_trace(go.Scatter(x=x_vals,y=w_vals,name='Distributed Load (lb/in)'),row=1,col=1)
    # fig.add_annotation(
    #     text=str(w_val_at_0)+" lbin", x=0, y=w_val_at_0, xref='x1', yref='y1', showarrow=False,
    #     font=dict(color='black'), bgcolor='white', bordercolor='black', borderwidth=1, borderpad=1
    # )

    # Plotting Constant Distributed Load
    w_solve = P/(2*Lw)
    wexpr1,wcond1 = 0, sym.And(-L<x,x<-Lw)
    wexpr2,wcond2 = w_solve,sym.And(-Lw<x,x<Lw)
    wexpr3,wcond3 = 0, sym.And(Lw<x,x<L)
    w = sym.Piecewise((wexpr1,wcond1),(wexpr2,wcond2),(wexpr3,wcond3))
    w_vals = np.array([float(sym.N(w.subs('x', x))) for x in x_vals])
    w_val_at_0 = float(sym.N(w.subs('x', 0)))
    fig.add_trace(go.Scatter(x=x_vals,y=w_vals,name='Distributed Load (lb/in)'),row=1,col=1)
    fig.add_annotation(
        text=str(w_val_at_0)+" lbin", x=0, y=w_val_at_0, xref='x1', yref='y1', showarrow=False,
        font=dict(color='black'), bgcolor='white', bordercolor='black', borderwidth=1, borderpad=1
    )


    #Solving and Plotting Shear
    Vexpr1,Vcond1 = -P/2, sym.And(-L<x,x<-Lw)
    Vexpr2,Vcond2 = sym.integrate(w_solve,x),sym.And(-Lw<=x,x<=Lw)
    Vexpr3,Vcond3 = P/2, sym.And(Lw<x,x<L)
    V = sym.Piecewise((Vexpr1,Vcond1),(Vexpr2,Vcond2),(Vexpr3,Vcond3))
    V_vals = np.array([float(sym.N(V.subs('x', x))) for x in x_vals])
    V_val_at_minus_Lw = float(sym.N(V.subs('x', -Lw)))
    fig.add_trace(go.Scatter(x=x_vals, y=V_vals,name='Distributed Shear (lb)'),row=2,col=1)
    fig.add_annotation(
        text=str(V_val_at_minus_Lw)+" lb", x=-Lw, y=V_val_at_minus_Lw, xref='x2', yref='y2', showarrow=False,
        font=dict(color='black'), bgcolor='white', bordercolor='black', borderwidth=1, borderpad=1
    )

    #Solving for Moment
    M = sym.integrate(V,x) - P/2*L
    M_vals = np.array([float(sym.N(M.subs('x', x))) for x in x_vals])
    M_val_at_0 = float(sym.N(M.subs('x', 0)))
    fig.add_trace(go.Scatter(x=x_vals, y=M_vals,name='Distributed Moment (lb)'),row=3,col=1)
    fig.add_annotation(
        text=str(M_val_at_0)+" lb*in", x=0.1, y=M_val_at_0, xref='x3', yref='y3', showarrow=False,
        font=dict(color='black'), bgcolor='white', bordercolor='black', borderwidth=1, borderpad=1
    )
    #Annotating the Plot
    fig.update_yaxes(title_text="Distributed Load (lb/in)", row=1, col=1)
    fig.update_yaxes(title_text="Distributed Shear (lb)", row=2, col=1)
    fig.update_yaxes(title_text="Distributed Moment (lb)", row=3, col=1)
    fig.update_xaxes(title_text="L (in)", row=3, col=1)
    fig.update_layout(
        height=750,
        title={
            'text': "<b>Distributed Load, Shear, and Moment SURFURS</b>",
            'y':0.945,
            'x':0.45,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    fig.add_annotation(
        text=f'Buckle Failure at: {-P} pounds',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.5,  # x position in normalized coordinates (far right is 1)
        y=1.06,   # y position in normalized coordinates (top is 1)
        font=dict(
            size=16  # change the size to fit your needs
        )
    )
    fig.update_layout(height=750)
    return w_val_at_0,V_val_at_minus_Lw, M_val_at_0, fig