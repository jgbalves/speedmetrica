from matplotlib import pyplot as plt
import fastf1 as ff1
from fastf1 import plotting


def get_f1_plot():
    '''random plot to check structure'''
    plotting.setup_mpl()

    monza_quali = ff1.get_session(2019, 'Monza', 'Q')

    laps = monza_quali.load_laps(with_telemetry=True)
    fast_leclerc = laps.pick_driver('LEC').pick_fastest()
    lec_car_data = fast_leclerc.get_car_data()
    print(list(lec_car_data.columns))
    t = lec_car_data['Time']
    vCar = lec_car_data['Brake']

    # The rest is just plotting
    fig, ax = plt.subplots()
    ax.plot(t, vCar, label='Fast')
    ax.set_xlabel('Time')
    ax.set_ylabel('Speed [Km/h]')
    ax.set_title('Leclerc is')
    ax.legend()
    return fig

get_f1_plot()
