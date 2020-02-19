""" This python module factors out some functions that are used in the analysis notebook.
"""
import plotly
import plotly.graph_objs as go
from plotly.offline import iplot
import plotly.io as pio


def boxplot_grouped(dataframe, x_col, y_col, group_col, colors, title, x_title, y_title):
    """ Returns a plotly boxplot of specified x and y columns
        grouped by their values in a column group_col.
    """
    
    traces = []
    categories = dataframe[group_col].unique()
    for group, color in zip(categories, colors):
        traces.append(
            go.Box(
                y= getattr(dataframe[dataframe[group_col]==group],y_col),
                x= getattr(dataframe[dataframe[group_col]==group],x_col),
                boxpoints=False,
                name=group,
                marker=dict(
                    color=color),))

    layout = go.Layout(
        title=title,
        xaxis= dict(
            title= x_title,
            ticklen= 5,
            zeroline= False,
            gridwidth= 2,
        ),
        yaxis=dict(
            title= y_title,
            ticklen= 5,
            gridwidth= 2,
        ),
        legend=dict(orientation="h",
                   x=0, y=-0.3),
        boxmode='group'
    )
    fig = go.Figure(data=traces, layout=layout)
    iplot(fig)
    return fig

def grouped_plotter(dataframe, plot_title, kwargs=None):
    """ Returns a plot of selected columns grouped by values in provided columns.
    """
    PARAMETERS = {
        'x': 'FinancialYear',
        'x_title':'Financial year',
        'y': 'TotalScore',
        'y_title':'Total annual score',
        'group_column_inner': 'Manufacturer',
        'group_column_outer': 'VehicleType'
    }
    
    if kwargs is None:
        kwargs = PARAMETERS
    
    veh_types = dataframe[kwargs['group_column_outer']].unique()
    manufacturers = dataframe[kwargs['group_column_inner']].unique()
    traces = {x:[] for x in veh_types}
    #colors = colorlover.to_rgb(colorlover.scales[str(len(manufacturers))]['div']['RdBu'])
    stt = False
    for veh in veh_types:
        if veh == veh_types[-1]:
            stt = True
        for man in manufacturers:
            trace = go.Scatter(
                name=man,
                x=dataframe[(dataframe[kwargs['group_column_outer']]==veh)&(dataframe[kwargs['group_column_inner']]==man)][kwargs['x']],
                y=dataframe[(dataframe[kwargs['group_column_outer']]==veh)&(dataframe[kwargs['group_column_inner']]==man)][kwargs['y']],
                mode = 'lines',
                showlegend=stt)
            
            traces[veh].append(trace)
                                             
    fig = plotly.tools.make_subplots(rows=len(veh_types), cols=1, subplot_titles=[x+'s' for x in veh_types])
    
    for k, l in enumerate(veh_types):
        for i, _ in enumerate(manufacturers):                                                                                           
            fig.append_trace(traces[l][i], k+1, 1)
            fig['layout'][f'xaxis{k+1}'].update(title=kwargs['x_title'])
        fig['layout'][f'yaxis{k+1}'].update(title=kwargs['y_title'])

        
    fig['layout'].update(height=800, width=600, title=plot_title, )
    iplot(fig)
    return fig