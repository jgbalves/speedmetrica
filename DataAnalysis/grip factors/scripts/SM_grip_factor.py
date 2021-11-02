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
# Functions to calculate and plot grip factors

# # Importing Libraries
import os
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go


class Outing:
    def __init__(self, path):
        # # Inputing data
        outing_path = path  # Path with all .csv to analyse
        outing_names = os.listdir(path)  # Fetch all files in path
        outing_names = [file for file in outing_names if '.csv' in file]  # Filtering the .csv


def grip_factor_tire_pressure(path):

    # # Inputing data
    outing_path = path    # Path with all .csv to analyse
    outing_names = os.listdir(path)    # Fetch all files in path
    outing_names = [file for file in outing_names if '.csv' in file]    # Filtering the .csv

    # # Creating plot figure
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Tire Press - FL", "Tire Press - FR", "Tire Press - RL", "Tire Press - RR")
    )
    fig.update_layout(title='Corner Grip Factor over Tyre Pressures',
                      plot_bgcolor='rgb(230, 230,230)',
                      showlegend=True)

    # # loop for all outings
    for file in outing_names:

        outing_csv = file
        outing_csv = f'{outing_path}\{outing_csv}'
        outing = pd.read_csv(outing_csv, sep=',', low_memory=False, skiprows=13)
        df = outing

        # # Removing motec double header
        df = df.drop([0], axis=0)
        df = df.reset_index()

        # # Converting strings to floats
        df['G Force Lat'] = np.sqrt((pd.to_numeric(df['G Force Lat'], downcast='float')) ** 2)
        df['G Force Long'] = pd.to_numeric(df['G Force Long'], downcast='float')
        df['Ground Speed'] = pd.to_numeric(df['Ground Speed'], downcast='float')
        df['Lap Distance'] = pd.to_numeric(df['Lap Distance'], downcast='float')
        df['Tire Press - FL'] = pd.to_numeric(df['Tire Press - FL'], downcast='float')
        df['Tire Press - FR'] = pd.to_numeric(df['Tire Press - FR'], downcast='float')
        df['Tire Press - RL'] = pd.to_numeric(df['Tire Press - RL'], downcast='float')
        df['Tire Press - RR'] = pd.to_numeric(df['Tire Press - RR'], downcast='float')

        # # Cleaning data
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
        df['Trail Breaking Grip Factor'] = np.where(
            (df['G Force Long'] > 1) & (df['G Force Lat'] > 1), df['Combined G'], np.nan)

        '''
        print(df['Overall Grip Factor'].mean())
        print(df['Cornering Grip Factor'].mean())
        print(df['Braking Grip Factor'].mean())
        print(df['Traction Grip Factor'].mean())
        print(df['Aero Grip Factor'].mean())
        '''

        # # Counting Laps
        lap_num = [0]   # Putting first lap as lap 0

        for index in range(1, len(df['Lap Distance'])):
            lap_num_prv = lap_num[index - 1]
            if df['Lap Distance'][df.index[index - 1]] > df['Lap Distance'][df.index[index]]:
                lap_num.append(lap_num_prv + 1)
            else:
                lap_num.append(lap_num_prv)

        df['Lap Number'] = lap_num

        columns = [
            'Overall Grip Factor',
            'Cornering Grip Factor',
            'Braking Grip Factor',
            'Traction Grip Factor',
            'Aero Grip Factor',
            'Tire Press - FL',
            'Tire Press - FR',
            'Tire Press - RL',
            'Tire Press - RR'
        ]

        df2 = df.groupby(['Lap Number'])[columns].mean()

        print(df2)

        fig.add_trace(
            go.Scatter(
                x=df2['Tire Press - FL'],
                y=df2['Cornering Grip Factor'],
                mode='lines+markers',
                name=f'FL - {file}'),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df2['Tire Press - FR'],
                y=df2['Cornering Grip Factor'],
                mode='lines+markers',
                name=f'FR - {file}'),
            row=1, col=2
        )

        fig.add_trace(
            go.Scatter(
                x=df2['Tire Press - RL'],
                y=df2['Cornering Grip Factor'],
                mode='lines+markers',
                name=f'RL - {file}'),
            row=2, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df2['Tire Press - RR'],
                y=df2['Cornering Grip Factor'],
                mode='lines+markers',
                name=f'RR - {file}'),
            row=2, col=2
        )

        # plt.scatter(df2['Tire Press - RR'], df2['Cornering Grip Factor']) (work with matplotlib)

    fig.show()    # Work with plotly
    # plt.show()    # Work with matplotlib


def aero_factor_wing_pos(path):

    # # Inputing data
    outing_path = path    # Path with all .csv to analyse
    outing_names = os.listdir(path)    # Fetch all files in path
    outing_names = [file for file in outing_names if '.csv' in file]    # Filtering the .csv

    # # Creating plot figure
    fig = make_subplots(
        rows=1, cols=1,
        subplot_titles="Tire Press - FL"
    )
    fig.update_layout(title='Aero Grip Factor Wing Position',
                      plot_bgcolor='rgb(230, 230,230)',
                      showlegend=True)

    # # loop for all outings
    for file in outing_names:

        outing_csv = file
        outing_csv = f'{outing_path}\{outing_csv}'
        outing = pd.read_csv(outing_csv, sep=',', low_memory=False, skiprows=13)
        df = outing
        # import pdb; pdb.set_trace()
        wing_pos = pd.read_csv(outing_csv, sep=',', low_memory=False, nrows=5)
        wing_pos = wing_pos.iloc[4]['MoTeC CSV']
        wing_pos = wing_pos.replace("'", '"')
        wing_pos = json.loads(wing_pos)
        import pdb; pdb.set_trace()

        # # Removing motec double header
        df = df.drop([0], axis=0)
        df = df.reset_index()

        # # Converting strings to floats
        df['G Force Lat'] = np.sqrt((pd.to_numeric(df['G Force Lat'], downcast='float')) ** 2)
        df['G Force Long'] = pd.to_numeric(df['G Force Long'], downcast='float')
        df['Ground Speed'] = pd.to_numeric(df['Ground Speed'], downcast='float')
        df['Lap Distance'] = pd.to_numeric(df['Lap Distance'], downcast='float')
        df['Tire Press - FL'] = pd.to_numeric(df['Tire Press - FL'], downcast='float')
        df['Tire Press - FR'] = pd.to_numeric(df['Tire Press - FR'], downcast='float')
        df['Tire Press - RL'] = pd.to_numeric(df['Tire Press - RL'], downcast='float')
        df['Tire Press - RR'] = pd.to_numeric(df['Tire Press - RR'], downcast='float')

        # # Cleaning data
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
        df['Trail Breaking Grip Factor'] = np.where(
            (df['G Force Long'] > 1) & (df['G Force Lat'] > 1), df['Combined G'], np.nan)

        '''
        print(df['Overall Grip Factor'].mean())
        print(df['Cornering Grip Factor'].mean())
        print(df['Braking Grip Factor'].mean())
        print(df['Traction Grip Factor'].mean())
        print(df['Aero Grip Factor'].mean())
        '''

        # # Counting Laps
        lap_num = [0]   # Putting first lap as lap 0

        for index in range(1, len(df['Lap Distance'])):
            lap_num_prv = lap_num[index - 1]
            if df['Lap Distance'][df.index[index - 1]] > df['Lap Distance'][df.index[index]]:
                lap_num.append(lap_num_prv + 1)
            else:
                lap_num.append(lap_num_prv)

        df['Lap Number'] = lap_num

        columns = [
            'Overall Grip Factor',
            'Cornering Grip Factor',
            'Braking Grip Factor',
            'Traction Grip Factor',
            'Aero Grip Factor',
            'Tire Press - FL',
            'Tire Press - FR',
            'Tire Press - RL',
            'Tire Press - RR'
        ]

        df2 = df.groupby(['Lap Number'])[columns].mean()

        print(df2)




