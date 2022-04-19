from matplotlib import pyplot as plt
import fastf1 as ff1
from fastf1 import plotting


def get_f1_plot(year, track, session, driver1, driver2):
    '''random plot to check structure'''
    plotting.setup_mpl()

    monza_quali = ff1.get_session(year, track, session)

    laps = monza_quali.load_laps(with_telemetry=True)
    fast_leclerc = laps.pick_driver(driver1).pick_fastest()
    lec_car_data = fast_leclerc.get_car_data()
    lec_car_data = lec_car_data.add_distance(drop_existing=True)
    print(list(lec_car_data.columns))
    x_axle = lec_car_data['Distance']
    y_axle = lec_car_data['Speed']

    # The rest is just plotting
    fig, ax = plt.subplots()
    ax.plot(x_axle, y_axle, label='LEC Speed')
    ax.set_xlabel('Distance')
    ax.set_ylabel('Speed [Km/h]')
    ax.set_title('Leclerc')
    ax.legend()
    return fig
