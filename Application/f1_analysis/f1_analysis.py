import fastf1 as ff1
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def get_f1_plot(year, track, session, driver_list):
    '''random plot to check structure'''

    fig = make_subplots(
    rows=3,
    cols=1,
    subplot_titles=('Speed [km/h]', 'Throttle [%]', 'Delta [s]')
    )
    fig.update_layout(
        title='Drivers Comparison',
        plot_bgcolor='rgb(230, 230,230)',
        showlegend=True
    )

    for driver in driver_list:

        monza_quali = ff1.get_session(year, track, session)

        laps = monza_quali.load_laps(with_telemetry=True)
        fast_leclerc = laps.pick_driver(driver).pick_fastest()
        lec_car_data = fast_leclerc.get_car_data()
        lec_car_data = lec_car_data.add_distance(drop_existing=True)
        print(list(lec_car_data.columns))
        x_axle = lec_car_data['Distance']
        y_axle = lec_car_data['Speed']

        # The rest is just plotting
        fig.add_trace(
            go.Scatter(
                x=x_axle,
                y=y_axle,
                mode='lines',
                name=f'{driver}'
            ),
            row=1,
            col=1
        )
        fig.add_trace(
            go.Scatter(
                x=x_axle,
                y=lec_car_data['Throttle'],
                mode='lines',
                name=f'{driver}'
            ),
            row=2,
            col=1
        )

        fig.add_trace(
            go.Scatter(
                x=x_axle,
                y=lec_car_data['Time'],
                mode='lines',
                name=f'{driver}'
            ),
            row=3,
            col=1
        )

    return fig
