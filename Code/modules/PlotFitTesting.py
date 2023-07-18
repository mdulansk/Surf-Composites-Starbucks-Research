import sys
import os
sys.path.append('../classes')
sys.path.append('../modules')
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np

def plot_fit_test_data(fp):

    load_df = pd.read_csv(fp, sep='\t', skiprows=7).rename(columns={'in': 'Crosshead (in)', 'lbf': 'Load (lbf)', 'sec': 'Time (sec)'})
    load_df = load_df[load_df['Load (lbf)'] > 0.25].reset_index()
    first_contact = load_df['Crosshead (in)'].iloc[0]
    load_df['Crosshead (in)'] = load_df['Crosshead (in)'].apply(lambda x: x - first_contact)
    fig = px.line(load_df, x='Crosshead (in)', y='Load (lbf)', title='Load vs Crosshead')
    fig.update_xaxes(title_text='Crosshead (in)')
    fig.update_yaxes(title_text='Load (lbf)')

    # Find the first failure point (local maximum) after a load value greater than 100 pounds
    displ_values = load_df['Crosshead (in)'].values
    load_values = load_df['Load (lbf)'].values

    # Find the index where the load values are greater than 100 pounds
    start_idx = np.argmax(load_values > 100)

    # Find the index where the gradient goes from positive to negative, after the start_idx
    idx = start_idx + np.argmax(np.gradient(load_values[start_idx:]) < 0)

    max_displ = displ_values[idx]
    max_load = load_values[idx]

    # Add red marker at the first failure point
    fig.add_trace(go.Scatter(x=[max_displ], y=[max_load], mode='markers', marker=dict(color='red'), name='First Failure'))

    return fig, max_load, max_displ

def plot_test_specimens(specimens_df):
    # Group the specimens_df based on the 'Description' column
    grouped_df = specimens_df.groupby('Description')

    # Create a list to hold all the figures
    figures = []

    # Define a color scale for the different groups
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'magenta']  # Add more colors as needed

    # Iterate over each group
    for i, (description, group) in enumerate(grouped_df):
        # Create a new figure for the group
        fig = go.Figure()
        legend_labels = []  # List to store legend labels for the specific group

        # Iterate over each row within the group
        for _, row in group.iterrows():
            test_specimen = row['TestSpecimens']
            if isinstance(test_specimen.testing_data_fig, go.Figure):
                for trace in test_specimen.testing_data_fig.data:
                    # Set the color and legend label of the trace based on the group
                    trace.update(line=dict(color=colors[i]), showlegend=True, name=description)
                    # Add the trace to the group's figure
                    fig.add_trace(trace)
                    # Store the legend label
                    legend_labels.append(description)

        # Update the layout and legend for the group's figure
        fig.update_layout(showlegend=True, legend_title_text='Description')
        # Set the legend labels
        for j, label in enumerate(legend_labels):
            fig.data[j].name = label

        # Add the group's figure to the list
        figures.append(fig)

    # Create an overlapping plot for all specimens
    overlapping_fig = go.Figure()
    legend_labels = []  # List to store legend labels for the overlapping plot

    # Iterate over each group again
    for i, (description, group) in enumerate(grouped_df):
        # Iterate over each row within the group
        for _, row in group.iterrows():
            test_specimen = row['TestSpecimens']
            if isinstance(test_specimen.testing_data_fig, go.Figure):
                for trace in test_specimen.testing_data_fig.data:
                    # Set the color and legend label of the trace based on the group
                    trace.update(marker=dict(color=colors[i]), line=dict(color=colors[i]), showlegend=True, name=description)
                    # Add the trace to the overlapping plot
                    overlapping_fig.add_trace(trace)
                    # Store the legend label
                    legend_labels.append(description)

    # Update the layout and legend for the overlapping plot
    overlapping_fig.update_layout(showlegend=True, legend_title_text='Description')
    # Set the legend labels
    for j, label in enumerate(legend_labels):
        overlapping_fig.data[j].name = label

    # Show the separate plots for each group
    for fig in figures:
        fig.show()

    # Show the overlapping plot
    overlapping_fig.show()




