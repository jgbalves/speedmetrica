# # ==============================================================================
# #
# #   _____ ____  ________________     __  ___________________  _____________
# #  / ___// __ \/ ____/ ____/ __ \   /  |/  / ____/_  __/ __ \/  _/ ____/   |
# #  \__ \/ /_/ / __/ / __/ / / / /  / /|_/ / __/   / / / /_/ // // /   / /| |
# # ___/ / ____/ /___/ /___/ /_/ /  / /  / / /___  / / / _, _// // /___/ ___ |
# #/____/_/   /_____/_____/_____/  /_/  /_/_____/ /_/ /_/ |_/___/\____/_/  |_|
# #
# #                           www.speedmetrica.com
# #
# # ==============================================================================
# # Formula 1 Analysis at the page speedmetrica.com

# # Importing libraries
import fastf1 as ff1
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def populate_year():
    return [year for year in range(2022, 1949, -1)]

def populate_event(year):
    schedule = ff1.get_event_schedule(year)
    return [event for event in schedule['Location']]

def populate_session():
    return ['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Sprint', 'Race']

def populate_driver(year, location, chosen_session):
    session = ff1.get_session(year, location, chosen_session)
    session.load()
    return session.results['Abbreviation'].tolist()

def drivers_data(year, track, chosen_session, driver_list):
    session = ff1.get_session(year, track, chosen_session)
    session.load()
    base_lap = session.laps.pick_driver(driver_list[0]).pick_fastest()
    base_data = base_lap.get_car_data()
    base_data = base_data.add_distance(drop_existing=True)
    base_data['Time'] = base_data['Time'].dt.total_seconds()
    base_data['Delta'] = base_data['Time'] - base_data['Time']
    base_data = base_data.rename(columns=lambda x: f'{driver_list[0]}_'+ x )
    for driver in driver_list[1:]:
        driver_comp_lap = session.laps.pick_driver(driver).pick_fastest()
        driver_comp_data = driver_comp_lap.get_car_data()
        driver_comp_data = driver_comp_data.add_distance(drop_existing=True)
        driver_comp_data['Time'] = driver_comp_data['Time'].dt.total_seconds()
        driver_comp_data['Delta'] = driver_comp_data['Time'] - base_data[f'{driver_list[0]}_Time']
        driver_comp_data['Delta'] = driver_comp_data['Delta'].cumsum()
        driver_comp_data = driver_comp_data.rename(columns=lambda x: f'{driver}_'+ x )
        base_data = base_data.join(driver_comp_data)
    return base_data


def resulting_plot(year, track, chosen_session, driver_list):
    data_to_plot = drivers_data(year, track, chosen_session, driver_list)
    base_driver = driver_list[0]
    fig = make_subplots(
    rows=3,
    cols=1,
    subplot_titles=(),
    vertical_spacing=0.01)
    
    fig.update_xaxes(showspikes = True,
    spikemode  = 'across',
    spikesnap = 'cursor',
    showline=True,
    showgrid=True,
    )

    fig.update_layout(
        title='Fastest Lap Comparison',
        plot_bgcolor='rgb(230, 230,230)',
        showlegend=True,
        hovermode  = 'x unified')
    for driver in driver_list:
        fig.add_trace(
            go.Scatter(
                x=data_to_plot[f'{base_driver}_Distance'],
                y=data_to_plot[f'{driver}_Delta'],
                legendgroup=f'{driver}',
                mode='lines',
                name=f'{driver}'),
            row=1,
            col=1)
        fig.add_trace(
            go.Scatter(
                x=data_to_plot[f'{base_driver}_Distance'],
                y=data_to_plot[f'{driver}_Speed'],
                legendgroup=f'{driver}',
                showlegend=False,
                mode='lines',
                name=f'{driver}'),
            row=2,
            col=1)
        fig.add_trace(
            go.Scatter(
                x=data_to_plot[f'{base_driver}_Distance'],
                y=data_to_plot[f'{driver}_Throttle'],
                legendgroup=f'{driver}',
                showlegend=False,
                mode='lines',
                name=f'{driver}'),
            row=3,
            col=1)
    fig['layout']['yaxis']['title']='Time Delta [s]'
    fig['layout']['yaxis2']['title']='Speed [km/h]'
    fig['layout']['yaxis3']['title']='Throttle [%]'
    fig.update_traces(xaxis='x3')
    return fig
