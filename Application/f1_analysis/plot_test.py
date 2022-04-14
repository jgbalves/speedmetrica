# x and y given as array_like objects
import plotly.express as px
import fastf1 as tnt

def get_f1_plot():
    '''just testing'''
    fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
    # fig.show()
    return fig
