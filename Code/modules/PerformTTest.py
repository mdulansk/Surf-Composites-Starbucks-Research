from itertools import combinations
from scipy import stats
import plotly.graph_objects as go

import plotly.graph_objects as go

# def perform_t_test(specimens_df, num_bins=10):
#     grouped_df = specimens_df.groupby('Description')

#     # Perform t-test for 'Max Load (lb)'
#     print("T-test results for Max Load (lb):")
#     for group1, group2 in combinations(grouped_df.groups.keys(), 2):
#         data1 = grouped_df.get_group(group1)['Max Load (lb)']
#         data2 = grouped_df.get_group(group2)['Max Load (lb)']

#         # Ignore groups with only 1 value
#         if len(data1) < 2 or len(data2) < 2:
#             continue

#         t_stat, p_value = stats.ttest_ind(data1, data2)
#         print(f"Groups: {group1} vs {group2}")
#         print(f"t-statistic: {t_stat}, p-value: {p_value}")
#         if p_value < 0.05:
#             print("Null hypothesis rejected.")
#         else:
#             print("Null hypothesis cannot be rejected.")
#         print()

#         # Plot histograms for each group
#         fig = go.Figure()
#         fig.add_trace(go.Histogram(x=data1, name=group1, opacity=0.5, nbinsx=num_bins))
#         fig.add_trace(go.Histogram(x=data2, name=group2, opacity=0.5, nbinsx=num_bins))
#         fig.update_layout(
#             barmode='overlay',
#             xaxis_title='Max Load (lb)',
#             yaxis_title='Frequency',
#             title=f'Histogram: {group1} vs {group2}'
#         )
#         fig.update_traces(opacity=0.75)
#         fig.show()

#     # Perform t-test for 'Max Displacement (in)'
#     print("T-test results for Max Displacement (in):")
#     for group1, group2 in combinations(grouped_df.groups.keys(), 2):
#         data1 = grouped_df.get_group(group1)['Max Displacement (in)']
#         data2 = grouped_df.get_group(group2)['Max Displacement (in)']

#         # Ignore groups with only 1 value
#         if len(data1) < 2 or len(data2) < 2:
#             continue

#         t_stat, p_value = stats.ttest_ind(data1, data2)
#         print(f"Groups: {group1} vs {group2}")
#         print(f"t-statistic: {t_stat}, p-value: {p_value}")
#         if p_value < 0.05:
#             print("Null hypothesis rejected.")
#         else:
#             print("Null hypothesis cannot be rejected.")
#         print()

#         # Plot histograms for each group
#         fig = go.Figure()
#         fig.add_trace(go.Histogram(x=data1, name=group1, opacity=0.5, nbinsx=num_bins))
#         fig.add_trace(go.Histogram(x=data2, name=group2, opacity=0.5, nbinsx=num_bins))
#         fig.update_layout(
#             barmode='overlay',
#             xaxis_title='Max Displacement (in)',
#             yaxis_title='Frequency',
#             title=f'Histogram: {group1} vs {group2}'
#         )
#         fig.update_traces(opacity=0.75)
#         fig.show()
def perform_t_test(specimens_df, num_bins=10):
    grouped_df = specimens_df.groupby('Description')

    # Perform t-test for 'Max Load (lb)'
    print("T-test results for Max Load (lb):")
    for group1, group2 in combinations(grouped_df.groups.keys(), 2):
        data1 = grouped_df.get_group(group1)['Max Load (lb)']
        data2 = grouped_df.get_group(group2)['Max Load (lb)']

        # Ignore groups with only 1 value
        if len(data1) < 2 or len(data2) < 2:
            continue

        t_stat, p_value = stats.ttest_ind(data1, data2)
        print(f"Groups: {group1} vs {group2}")
        print(f"t-statistic: {t_stat}, p-value: {p_value}")
        if p_value < 0.05:
            print("Null hypothesis rejected.")
        else:
            print("Null hypothesis cannot be rejected.")
        print()

        # Plot histograms for each group
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=data1, name=group1, opacity=0.5, nbinsx=num_bins))
        fig.add_trace(go.Histogram(x=data2, name=group2, opacity=0.5, nbinsx=num_bins))
        fig.update_layout(
            barmode='overlay',
            xaxis_title='Max Load (lb)',
            yaxis_title='Frequency',
            title=f'Histogram: {group1} vs {group2}',
            height=300,  # Adjust the height as needed
            width=400,  # Adjust the width as needed
            margin=dict(l=20, r=20, t=30, b=20)  # Adjust the margin as needed
        )
        fig.update_traces(opacity=0.75)
        fig.show()

    # Perform t-test for 'Max Displacement (in)'
    print("T-test results for Max Displacement (in):")
    for group1, group2 in combinations(grouped_df.groups.keys(), 2):
        data1 = grouped_df.get_group(group1)['Max Displacement (in)']
        data2 = grouped_df.get_group(group2)['Max Displacement (in)']

        # Ignore groups with only 1 value
        if len(data1) < 2 or len(data2) < 2:
            continue

        t_stat, p_value = stats.ttest_ind(data1, data2)
        print(f"Groups: {group1} vs {group2}")
        print(f"t-statistic: {t_stat}, p-value: {p_value}")
        if p_value < 0.05:
            print("Null hypothesis rejected.")
        else:
            print("Null hypothesis cannot be rejected.")
        print()

        # Plot histograms for each group
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=data1, name=group1, opacity=0.5, nbinsx=num_bins))
        fig.add_trace(go.Histogram(x=data2, name=group2, opacity=0.5, nbinsx=num_bins))
        fig.update_layout(
            barmode='overlay',
            xaxis_title='Max Displacement (in)',
            yaxis_title='Frequency',
            title=f'Histogram: {group1} vs {group2}',
            height=300,  # Adjust the height as needed
            width=600,  # Adjust the width as needed
            margin=dict(l=20, r=20, t=30, b=20)  # Adjust the margin as needed
        )
        fig.update_traces(opacity=0.75)
        fig.show()

