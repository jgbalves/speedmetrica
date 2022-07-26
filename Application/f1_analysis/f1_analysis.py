import fastf1 as ff1
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


def populate_year():
    return [year for year in range(2022, 1949, -1)]

def populate_event(year):
    schedule = ff1.get_event_schedule(year)
    return [event for event in schedule['Location']]

def populate_session(year, location):
    schedule = ff1.get_event_schedule(year)
    schedule = schedule[schedule.Location == f'{location}']
    sessions = list(schedule)
    sessions = [t for t in sessions if (t.startswith('Session') and not  t.endswith('Date'))]
    sessions = schedule[(sessions)].values.tolist().pop()
    return sessions

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
    subplot_titles=('Time Delta [s]', 'Speed [km/h]', 'Throttle [%]'))
    fig.update_layout(
        title='Fastest Lap Comparison',
        plot_bgcolor='rgb(230, 230,230)',
        showlegend=True)
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
    return fig
