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
# Calculating and plotting grip factors

# # Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def main():

    outing_csv = 'velocitta_stock.csv'
    outing_path = Path(Path.home(), 'Github', 'speedmetrica', 'DataAnalysis', 'grip factors', 'csv outings', outing_csv)
    outing = pd.read_csv(outing_path, sep=',', low_memory=False, skiprows=13)
    df = outing
    df = df.drop([0], axis=0)
    df['G Force Lat'] = pd.to_numeric(df['G Force Lat'], downcast='float')
    df['G Force Long'] = pd.to_numeric(df['G Force Long'], downcast='float')
    df['Combined G'] = np.sqrt(df['G Force Lat'] ** 2 + df['G Force Long'] ** 2)
    df['Overall Grip Factor'] = [i > 1 for i in df['Combined G']]
    # df['Cornering Grip Factor'] = [i for i in df['Combined G'] if i > 0.5 in df['G Force Lat']]
    df['Cornering Grip Factor'] = np.where(df['G Force Lat'] > 0.5, df['Combined G'], np.nan)
    df['Braking Grip Factor'] = np.where(df['G Force Long'] < -1, df['Combined G'], np.nan)
    # df['Traction Grip Factor'] = np.where([df['G Force Lat'] > 0.5 & df['G Force Long'] > 0], df['Combined G'], np.nan)
    cornering_grip_factor = df[(df['G Force Lat'] > 0.5)]['Combined G'].mean()
    braking_grip_factor = df[(df['G Force Long'] < -1)]['Combined G'].mean()
    traction_grip_factor = df[((df['G Force Lat'] > 0.5) & (df['G Force Long'] > 0))]['Combined G'].mean()
    print(cornering_grip_factor)
    print(braking_grip_factor)
    print(traction_grip_factor)
    # df['Aero Grip Factor'] =
    # print(df['Overall Grip Factor'].head(50))
    # print(df.loc[df['Cornering Grip Factor'] == np.nan])
    # print(df.loc[df['Overall Grip Factor'] == True])


if __name__ == '__main__':
    main()
