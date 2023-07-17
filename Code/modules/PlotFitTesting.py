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

def plot_fit_test_data(fp):

    load_df = pd.read_csv(fp,sep='\t',skiprows=7).rename(columns={'in': 'Crosshead (in)','lbf':'Load (lbf)','sec':'Time (sec)'})
    load_df = load_df[load_df['Load (lbf)'] > 0.25].reset_index()
    first_contact = load_df['Crosshead (in)'].iloc[0]
    load_df['Crosshead (in)'] = load_df['Crosshead (in)'].apply(lambda x: x - first_contact)
    fig = px.line(load_df, x='Crosshead (in)', y='Load (lbf)', title='Load vs Crosshead')
    max_load = load_df['Load (lbf)'].max()
    fig.update_xaxes(title_text='Crosshead (in)')
    fig.update_yaxes(title_text='Load (lbf)')
    # #Load in text file and remove last two data points since they are outliers
    # load_df = pd.read_csv(fp,sep='\t',skiprows=7).rename(columns={'in': 'Crosshead (in)','lbf':'Load (lbf)','sec':'Time (sec)'})
    # load_df = load_df[load_df['Load (lbf)'] > 0.25].reset_index()
    # first_contact = load_df['Crosshead (in)'].iloc[0]
    # load_df['Crosshead (in)'] = load_df['Crosshead (in)'].apply(lambda x: x - first_contact)


    # # find indices if change points approximate
    # change_points = load_df[(load_df['Load (lbf)'].diff()) < -20].index
    # before_failure = change_points[0] - 3
    # after_failure = change_points[0] + 3
    # end_start_markers = load_df.iloc[[before_failure,after_failure]]
    # max_load = load_df.iloc[before_failure][0]

    # ###### Fitting the Force Displacement Curve Before and After Failure
    # predicted_figures = []
    # for index in [before_failure,after_failure]:
    #     if index == before_failure:
    #         X = load_df[['Crosshead (in)']].iloc[:index+1]
    #         y = load_df[['Load (lbf)']].iloc[:index+1]
    #         degree = 1
    #     else:
    #         X = load_df[['Crosshead (in)']].iloc[index:-10]
    #         y = load_df[['Load (lbf)']].iloc[index:-10]
    #         degree = 3

    #     poly_pipe = Pipeline([
    #         ('Polynomial-Crosshead',PolynomialFeatures(degree)),
    #         ('lin-reg', LinearRegression())
    #                             ])
    #     poly_pipe.fit(X,y)
    #     y_predict = poly_pipe.predict(X)
    #     y_predict_df = pd.DataFrame(y_predict, columns=["Predicted Load (lbf)"])

    #     if index == before_failure:
    #         predicted_figures.append(go.Scatter(
    #             x = load_df['Crosshead (in)'].iloc[:index+1], 
    #             y = y_predict_df["Predicted Load (lbf)"],  
    #             marker = dict(color = 'purple'),
    #             name = 'Fit Before Failure'
    #             ))
    #     else:
    #         predicted_figures.append(go.Scatter(
    #             x = load_df['Crosshead (in)'].iloc[index:-10], #Guessing the end cutoff before the second failure
    #             y = y_predict_df["Predicted Load (lbf)"],  
    #             marker = dict(color = 'purple'),
    #             name = 'Fit After Failure'
    #         ))

    # # Create the original scatter plot
    # actual_load_trace = go.Scatter(
    #     x = load_df['Crosshead (in)'],
    #     y = load_df['Load (lbf)'],
    #     mode = 'markers',
    #     marker = dict(
    #         color = 'red',
    #         size = 3
    #     ),
    #     name = 'Force vs. Displacement'
    # )

    # # Create a scatter plot for the drop points
    # end_start_trace = go.Scatter(
    #     x = end_start_markers['Crosshead (in)'],
    #     y = end_start_markers['Load (lbf)'],
    #     mode = 'markers',
    #     marker = dict(
    #         color = 'purple',
    #         size = 5
    #     ),
    #     name = 'Drop Points'
    # )

    # # Create a layout
    # layout = go.Layout(
    #     title = 'Force vs. Displacement',
    #     xaxis = dict(title = 'Crosshead (in)'),  # x-axis label
    #     yaxis = dict(title = 'Load (lbf)'),  # y-axis label
    #     hovermode ='closest' # handles multiple points landing on the same vertical
    # )

    # # Create the figure with both scatter plots
    #return go.Figure(data=[actual_load_trace, end_start_trace,predicted_figures[0],predicted_figures[1]], layout=layout),max_load
    return fig, max_load


def plot_test_specimens(specimens_df):
    # Group the specimens_df based on the 'Description' column
    grouped_df = specimens_df.groupby('Description')

    # Create a new figure to hold all the plots
    fig = go.Figure()
    # Define a color scale for the different groups
    colors = ['blue', 'green', 'red', 'orange', 'purple']  # Add more colors as needed

    # Iterate over each group
    for i, (description, group) in enumerate(grouped_df):
        # Iterate over each row within the group
        for _, row in group.iterrows():
            test_specimen = row['TestSpecimens']
            if isinstance(test_specimen.testing_data_fig, go.Figure):
                for trace in test_specimen.testing_data_fig.data:
                    # Set the color of the trace based on the group
                    trace.update(line=dict(color=colors[i]))
                    # Add the trace to the figure
                    fig.add_trace(trace)

    # Update the figure layout
    fig.update_layout(showlegend=False)

    # Show the figure
    fig.show()
