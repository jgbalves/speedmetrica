import fastf1 as ff1
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def car_data(year, track, chosen_session, driver):
    session_plot = ff1.get_session(year, track, chosen_session)
    session_plot.load()
    fast_lap = session_plot.laps.pick_driver(driver).pick_fastest()
    car_data = fast_lap.get_car_data()
    car_data = car_data.add_distance(drop_existing=True)
    return car_data


def speed_plot(year, track, chosen_session, driver_list):
    '''Speed x Distance comparison'''

    fig = make_subplots(
    rows=1,
    cols=1,
    subplot_titles=('')
    )
    fig.update_layout(
        title='Speed [km/h]',
        plot_bgcolor='rgb(230, 230,230)',
        showlegend=True
    )

    for driver in driver_list:
        data_to_plot = car_data(year, track, chosen_session, driver)

        # The rest is just plotting
        fig.add_trace(
            go.Scatter(
                x=data_to_plot['Distance'],
                y=data_to_plot['Speed'],
                mode='lines',
                name=f'{driver}'
            ),
            row=1,
            col=1
        )
    return fig

def throttle_plot(year, track, chosen_session, driver_list):
    '''Throttle x Distance comparison'''

    fig = make_subplots(
    rows=1,
    cols=1,
    subplot_titles=('')
    )
    fig.update_layout(
        title='Throttle [%]',
        plot_bgcolor='rgb(230, 230,230)',
        showlegend=True
    )

    for driver in driver_list:
        data_to_plot = car_data(year, track, chosen_session, driver)

        # The rest is just plotting
        fig.add_trace(
            go.Scatter(
                x=data_to_plot['Distance'],
                y=data_to_plot['Throttle'],
                mode='lines',
                name=f'{driver}'
            ),
            row=1,
            col=1
        )
    return fig

def delta_plot(year, track, chosen_session, driver_list):    # Note: create a table with driver 1 - driver 2 = delta
    '''delta to leader x Distance comparison'''

    fig = make_subplots(
    rows=1,
    cols=1,
    subplot_titles=('')
    )
    fig.update_layout(
        title='Delta [s]',
        plot_bgcolor='rgb(230, 230,230)',
        showlegend=True
    )
    
    for driver in driver_list:
        data_to_plot = car_data(year, track, chosen_session, driver)

        # The rest is just plotting
        fig.add_trace(
            go.Scatter(
                x=data_to_plot['Distance'],
                y=data_to_plot['Time'],
                mode='lines',
                name=f'{driver}'
            ),
            row=1,
            col=1
        )
    return fig
