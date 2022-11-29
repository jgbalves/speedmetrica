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
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def create_dataframe_ams1(file):
    uploaded_file = file
    df=pd.read_csv(uploaded_file, skiprows=13, low_memory=False)
    df=df.drop([0,1])
    df = df.reset_index().drop(columns=['index'])
    df = df.apply(pd.to_numeric)
    return df


def create_dataframe_iracing(file):
    df=pd.read_csv(file, skiprows=9, low_memory=False)
    df=df.drop([0,1])
    df = df.reset_index().drop(columns=['index'])
    df = df.apply(pd.to_numeric)
    return df


def lap_counter_ams(dataframe):
    lap_num = [0]   # Putting first lap as lap 0

    for index in range(1, len(dataframe['Lap Distance'])):
        lap_num_prv = lap_num[index - 1]
        if dataframe['Lap Distance'][dataframe.index[index - 1]] > dataframe['Lap Distance'][dataframe.index[index]]:
            lap_num.append(lap_num_prv + 1)
        else:
            lap_num.append(lap_num_prv)
    
    dataframe['Lap Number'] = lap_num
    lap_list = dataframe['Lap Number'].unique().tolist()
    
    lap_times = []
    for lap in lap_list:
        lap_time = dataframe[dataframe['Lap Number'] == lap]['Time'].iloc[-1] - dataframe[dataframe['Lap Number'] == lap]['Time'].iloc[0]
        lap_time_minutes = lap_time//60
        lap_time_seconds = lap_time % 60
        lap_time = f'{lap_time_minutes:.0f}:{lap_time_seconds:.3f}'
        lap_times.append(lap_time)

    lap_list = list(zip(lap_list, lap_times))
    return lap_list


def lap_counter_iracing(dataframe):
    lap_list = dataframe['Lap'].unique().tolist()

    lap_times = []
    for lap in lap_list:
        lap_time = dataframe[dataframe['Lap'] == lap]['LapCurrentLapTime'].iloc[-1]
        lap_time_minutes = lap_time//60
        lap_time_seconds = lap_time % 60
        lap_time = f'{lap_time_minutes:.0f}:{lap_time_seconds:.3f}'
        lap_times.append(lap_time)

    lap_list = list(zip(lap_list, lap_times))
    return lap_list


def calculate_variance_iracing(df1, df2):
    df1['Lap Time'] = df1['LapCurrentLapTime'] - df1['LapCurrentLapTime'].iloc[0]
    df2['Lap Time'] = df2['LapCurrentLapTime'] - df2['LapCurrentLapTime'].iloc[0]
    
    result = pd.merge(df1, df2, how="outer", on=['LapDist']).sort_values('LapDist')
    result = result.interpolate(method='linear')
    result['Variance'] = result['Lap Time_x'] - result['Lap Time_y']
    return result


def calculate_variance_ams1(df1, df2):
    df1['Lap Time'] = df1['Time'] - df1['Time'].iloc[0]
    df2['Lap Time'] = df2['Time'] - df2['Time'].iloc[0]

    result = pd.merge(df1, df2, how="outer", on=['Lap Distance']).sort_values('Lap Distance')
    result = result.interpolate(method='linear')
    result['Variance'] = result['Lap Time_x'] - result['Lap Time_y']
    return result


def calculate_attitude_velocity_ams1(dataframe):
    dataframe['Attitude Velocity'] = 57.3 * ((9.81 * dataframe['G Force Lat'])/(0.277*dataframe['Ground Speed']))
    return dataframe


def plot_outing_ams1(df_list):
    fig = make_subplots(
        rows=9,
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
        title='Lap Comparison',
        plot_bgcolor='rgb(230, 230,230)',
        showlegend=True,
        hovermode  = 'x unified',
        yaxis1_title="Variance",
        yaxis2_title="Ground Speed",
        yaxis3_title="Throttle",
        yaxis4_title="Brake ",
        yaxis5_title="Steering Pct",
        yaxis6_title="G Lat",
        yaxis7_title="Gear",
        yaxis8_title="RPM",
        yaxis9_title="Attitude Velocity"
        )

    outing_names = []    # Outing names in legend
    for outing in range(len(df_list)):
        outing_names.append(f'Outing {outing+1}')

    # Variance Plot
    df1 = df_list[0]
    df2 = df_list[1]
    variance = calculate_variance_ams1(df1, df2)

    #Plots
    fig.add_trace(    # Variance
                go.Scatter(
                    x=variance['Lap Distance'],
                    y=variance['Variance'],
                    legendgroup=f'Outing 1-2',
                    name=f'Variance'),
                row=1,
                col=1)

    for x, df in enumerate(df_list):
        
        # Math Channels 
        df = calculate_attitude_velocity_ams1(df)    # Attitude Velocity
        
        fig.add_trace(    # Speed
                go.Scatter(
                    x=df['Lap Distance'],
                    y=df['Ground Speed'],
                    legendgroup=f'Outing {x}',
                    name=f'Speed {x+1}'),
                row=2,
                col=1)

        fig.add_trace(    # Throttle
                go.Scatter(
                    x=df['Lap Distance'],
                    y=df['Throttle Position'],
                    legendgroup=f'Outing {x}',
                    name=f'Throttle {x+1}'),
                row=3,
                col=1)

        fig.add_trace(    # Brake
                go.Scatter(
                    x=df['Lap Distance'],
                    y=df['Brake Pedal Position'],
                    legendgroup=f'Outing {x}',
                    name=f'Brake {x+1}'),
                row=4,
                col=1)

        fig.add_trace(    # Steering Wheel Pct
                go.Scatter(
                    x=df['Lap Distance'],
                    y=df['Steering Wheel Pct'],
                    legendgroup=f'Outing {x}',
                    name=f'Steering {x+1}'),
                row=5,
                col=1)

        fig.add_trace(    # G Lat
                go.Scatter(
                    x=df['Lap Distance'],
                    y=df['G Force Lat'],
                    legendgroup=f'Outing {x}',
                    name=f'Glat {x+1}'),
                row=6,
                col=1)

        fig.add_trace(    # Gear
                go.Scatter(
                    x=df['Lap Distance'],
                    y=df['Gear'],
                    legendgroup=f'Outing {x}',
                    name=f'Gear {x+1}'),
                row=7,
                col=1)

        fig.add_trace(    # RPM
                go.Scatter(
                    x=df['Lap Distance'],
                    y=df['Engine RPM'],
                    legendgroup=f'Outing {x}',
                    name=f'RPM {x+1}'),
                row=8,
                col=1)

        fig.add_trace(    # Attitude Velocity
                go.Scatter(
                    x=df['Lap Distance'],
                    y=df['Attitude Velocity'],
                    legendgroup=f'Outing {x}',
                    name=f'Attitude Velocity {x+1}'),
                row=9,
                col=1)
        fig.update_traces(xaxis='x7')    # to only have the bottom axis
    
    return fig


def plot_outing_iracing(df_list):
    fig = make_subplots(
        rows=8,
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
        title='Lap Comparison',
        plot_bgcolor='rgb(230, 230,230)',
        showlegend=True,
        hovermode  = 'x unified',
        yaxis1_title="Variance",
        yaxis2_title="Ground Speed",
        yaxis3_title="Throttle",
        yaxis4_title="Brake ",
        yaxis5_title="Steering Pct",
        yaxis6_title="G Lat",
        yaxis7_title="Gear",
        yaxis8_title="RPM"
        )

    outing_names = []    # Outing names in legend
    for outing in range(len(df_list)):
        outing_names.append(f'Outing {outing+1}')

    # Variance Plot
    df1 = df_list[0]
    df2 = df_list[1]
    variance = calculate_variance_iracing(df1, df2)

    #Plots
    fig.add_trace(    # Variance
                go.Scatter(
                    x=variance['LapDist'],
                    y=variance['Variance'],
                    legendgroup=f'Outing 1-2',
                    name=f'Variance'),
                row=1,
                col=1)

    for x, df in enumerate(df_list):
        fig.add_trace(    # Speed
                go.Scatter(
                    x=df['LapDist'],
                    y=df['Speed'],
                    legendgroup=f'Outing {x}',
                    name=f'Speed {x+1}'),
                row=2,
                col=1)

        fig.add_trace(    # Throttle
                go.Scatter(
                    x=df['LapDist'],
                    y=df['Throttle'],
                    legendgroup=f'Outing {x}',
                    name=f'Throttle {x+1}'),
                row=3,
                col=1)

        fig.add_trace(    # Brake
                go.Scatter(
                    x=df['LapDist'],
                    y=df['Brake'],
                    legendgroup=f'Outing {x}',
                    name=f'Brake {x+1}'),
                row=4,
                col=1)

        fig.add_trace(    # Steering Wheel Pct
                go.Scatter(
                    x=df['LapDist'],
                    y=df['SteeringWheelAngle'],
                    legendgroup=f'Outing {x}',
                    name=f'Steering {x+1}'),
                row=5,
                col=1)

        fig.add_trace(    # G Lat
                go.Scatter(
                    x=df['LapDist'],
                    y=df['LatAccel'],
                    legendgroup=f'Outing {x}',
                    name=f'Glat {x+1}'),
                row=6,
                col=1)

        fig.add_trace(    # Gear
                go.Scatter(
                    x=df['LapDist'],
                    y=df['Gear'],
                    legendgroup=f'Outing {x}',
                    name=f'Gear {x+1}'),
                row=7,
                col=1)

        fig.add_trace(    # RPM
                go.Scatter(
                    x=df['LapDist'],
                    y=df['RPM'],
                    legendgroup=f'Outing {x}',
                    name=f'RPM {x+1}'),
                row=8,
                col=1)
        fig.update_traces(xaxis='x7')
    
    return fig


def plot_grip_factor_tire_pressure(df_list):

    # # Creating plot figure
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Tire Press - FL", "Tire Press - FR", "Tire Press - RL", "Tire Press - RR")
    )
    fig.update_layout(title='Corner Grip Factor over Tyre Pressures',
                      plot_bgcolor='rgb(230, 230,230)',
                      showlegend=True)

    # # loop for all outings
    for x, df in enumerate(df_list):
        # # Cleaning data
        df['G Force Lat'] = np.sqrt(df['G Force Lat'] ** 2)
        clean1 = df['G Force Long'] >= -2   # Due to pressing ESC in AMS the long G gets noise
        clean2 = df['G Force Long'] <= 2
        df = df[clean1 & clean2]

        # # Conditional grip factors creation
        df['Combined G'] = np.sqrt(df['G Force Lat'] ** 2 + df['G Force Long'] ** 2)    # ok
        df['Overall Grip Factor'] = np.where(df['Combined G'] > 1, df['Combined G'], np.nan)   # ok
        df['Cornering Grip Factor'] = np.where(df['G Force Lat'] > 0.5, df['Combined G'], np.nan)   # LatG > 0.5
        df['Braking Grip Factor'] = np.where(df['G Force Long'] > 1, df['Combined G'], np.nan)   # LongG > 1
        df['Traction Grip Factor'] = np.where(
            (df['G Force Lat'] > 0.5) & (df['G Force Long'] < 0), df['Combined G'], np.nan)
        df['Aero Grip Factor'] = np.where(
            (df['G Force Lat'] > 1) & (df['Ground Speed'] > 120), df['Combined G'], np.nan)
        df['Trail Braking Grip Factor'] = np.where(
            (df['G Force Lat'] > 0.5) & (df['G Force Long'] > 0), df['Combined G'], np.nan)

        columns = [
            'Overall Grip Factor',
            'Cornering Grip Factor',
            'Braking Grip Factor',
            'Traction Grip Factor',
            'Aero Grip Factor',
            'Tire Press - FL',
            'Tire Press - FR',
            'Tire Press - RL',
            'Tire Press - RR']

        df = df.groupby(['Lap Number'])[columns].mean()

        fig.add_trace(
            go.Scatter(
                x=df['Tire Press - FL'],
                y=df['Cornering Grip Factor'],
                mode='lines+markers',
                name=f'FL - Outing {x+1}'),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df['Tire Press - FR'],
                y=df['Cornering Grip Factor'],
                mode='lines+markers',
                name=f'FR - Outing {x+1}'),
            row=1, col=2
        )

        fig.add_trace(
            go.Scatter(
                x=df['Tire Press - RL'],
                y=df['Cornering Grip Factor'],
                mode='lines+markers',
                name=f'RL - Outing {x+1}'),
            row=2, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df['Tire Press - RR'],
                y=df['Cornering Grip Factor'],
                mode='lines+markers',
                name=f'RR - Outing {x+1}'),
            row=2, col=2
        )

    return fig


def plot_grip_factor_aero(df_list):

    # # Creating plot figure
    fig = make_subplots(
        rows=1, cols=1
    )
    fig.update_layout(title='Aero Grip Factor',
                      plot_bgcolor='rgb(230, 230,230)',
                      showlegend=True)

    # # loop for all outings
    for x, df in enumerate(df_list):
        # # Cleaning data
        df['G Force Lat'] = np.sqrt(df['G Force Lat'] ** 2)
        clean1 = df['G Force Long'] >= -2   # Due to pressing ESC in AMS the long G gets noise
        clean2 = df['G Force Long'] <= 2
        df = df[clean1 & clean2]

        # # Conditional grip factors creation
        df['Combined G'] = np.sqrt(df['G Force Lat'] ** 2 + df['G Force Long'] ** 2)    # ok
        df['Overall Grip Factor'] = np.where(df['Combined G'] > 1, df['Combined G'], np.nan)   # ok
        df['Cornering Grip Factor'] = np.where(df['G Force Lat'] > 0.5, df['Combined G'], np.nan)   # LatG > 0.5
        df['Braking Grip Factor'] = np.where(df['G Force Long'] > 1, df['Combined G'], np.nan)   # LongG > 1
        df['Traction Grip Factor'] = np.where(
            (df['G Force Lat'] > 0.5) & (df['G Force Long'] < 0), df['Combined G'], np.nan)
        df['Aero Grip Factor'] = np.where(
            (df['G Force Lat'] > 1) & (df['Ground Speed'] > 120), df['Combined G'], np.nan)
        df['Trail Braking Grip Factor'] = np.where(
            (df['G Force Lat'] > 0.5) & (df['G Force Long'] > 0), df['Combined G'], np.nan)

        columns = [
            'Overall Grip Factor',
            'Cornering Grip Factor',
            'Braking Grip Factor',
            'Traction Grip Factor',
            'Aero Grip Factor',
            'Tire Press - FL',
            'Tire Press - FR',
            'Tire Press - RL',
            'Tire Press - RR']

        df = df.groupby(['Lap Number'])[columns].mean()

        fig.add_trace(
            go.Scatter(
                y=df['Aero Grip Factor'],
                mode='lines+markers',
                name=f'Outing {x+1}'),
            row=1, col=1
        )

    return fig


def plot_grip_factor_radar(df_list):
    
    # # Creating plot figure
    fig = go.Figure()
    fig.update_layout(title='Grip Factors',
                      plot_bgcolor='rgb(230, 230,230)',
                      showlegend=True)

    # # loop for all outings
    for x, df in enumerate(df_list):
        # # Cleaning data
        df['G Force Lat'] = np.sqrt(df['G Force Lat'] ** 2)
        clean1 = df['G Force Long'] >= -2   # Due to pressing ESC in AMS the long G gets noise
        clean2 = df['G Force Long'] <= 2
        df = df[clean1 & clean2]

        # # Conditional grip factors creation
        df['Combined G'] = np.sqrt(df['G Force Lat'] ** 2 + df['G Force Long'] ** 2)    # ok
        df['Overall Grip Factor'] = np.where(df['Combined G'] > 1, df['Combined G'], np.nan)   # ok
        df['Cornering Grip Factor'] = np.where(df['G Force Lat'] > 0.5, df['Combined G'], np.nan)   # LatG > 0.5
        df['Braking Grip Factor'] = np.where(df['G Force Long'] > 1, df['Combined G'], np.nan)   # LongG > 1
        df['Traction Grip Factor'] = np.where(
            (df['G Force Lat'] > 0.5) & (df['G Force Long'] < 0), df['Combined G'], np.nan)
        df['Aero Grip Factor'] = np.where(
            (df['G Force Lat'] > 1) & (df['Ground Speed'] > 120), df['Combined G'], np.nan)
        df['Trail Braking Grip Factor'] = np.where(
            (df['G Force Lat'] > 0.5) & (df['G Force Long'] > 0), df['Combined G'], np.nan)

        columns = [
            'Overall Grip Factor',
            'Cornering Grip Factor',
            'Braking Grip Factor',
            'Traction Grip Factor',
            'Aero Grip Factor',
            'Trail Braking Grip Factor']

        df = df[columns].mean()

        fig.add_trace(go.Scatterpolar(
            r=df,
            theta=columns,
            fill='toself',
            name=f'Outing {x}'))

    return fig

