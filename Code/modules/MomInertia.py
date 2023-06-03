import numpy as np
import plotly.graph_objects as go

def moments_of_inertia(yzs, E, mats):
    # Calculate centroid
    areas = []
    ycs = []
    zcs = []
    ea = []
    length = 24 #inches
    weight = 0
    
    fig = go.Figure(layout=go.Layout(showlegend=True))  # Create a Plotly Figure object
    
    for i, yz in enumerate(yzs):
        y, z = yz
        areas.append(0.5*np.abs(np.dot(y,np.roll(z,1))-np.dot(z,np.roll(y,1))))
        ycs.append(np.sum(y)/len(y))
        zcs.append(np.sum(z)/len(z))
        ea.append(E[i]*areas[i])
        weight += areas[i]*length*mats[list(mats)[i]][1]
    
    EA = sum(ea)
    yc = np.sum([E[i]*areas[i]*ycs[i] for i in range(len(ycs))]) / EA
    zc = np.sum([E[i]*areas[i]*zcs[i] for i in range(len(zcs))]) / EA

    for i, yz in enumerate(yzs):
        y, z = yz
        y = y - yc  # shift y-coordinates so that centroid is at y=0
        z = z - zc  # shift z-coordinates so that centroid is at z=0
        fig.add_trace(go.Scatter(x=np.concatenate((y, [y[0]])), y=np.concatenate((z, [z[0]])),name=list(mats)[i], mode='lines', line=dict(color=mats[list(mats)[i]][0])))

    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(color='black', symbol='x'), showlegend=False))
    EIyy = 0.0
    EIzz = 0.0
    EIyz = 0.0

    for yz, e in zip(yzs, E):
        y, z = yz

        y_c =  sum(y)/len(y) - yc
        z_c = sum(z)/len(z) - zc
        A = 0.5*np.abs(np.dot(y,np.roll(z,1))-np.dot(z,np.roll(y,1)))
        b = np.max(y) - np.min(y)
        h = np.max(z) - np.min(z)
        Iyy = (b * h**3) / 12.0
        Izz = (h * b**3) / 12.0
        EIyy += e * (Iyy + A * z_c**2)
        EIzz += e * (Izz + A * y_c**2)
        EIyz += e * np.sum(y_c * z_c) * A
    fig.update_layout(
    title='Geometry of Test Specimen',
    title_font=dict(size=20, family='Arial', color='black'),
    title_x=0.475,  # Center the title horizontally
    )
    fig.update_layout(xaxis_title='y-axis (in)', yaxis_title='z-axis (in)', yaxis=dict(scaleanchor="x", scaleratio=1))  # Set the axis labels and make the plot square
    return EIyy, EIzz, EIyz, EA, weight, 0, 0, fig
