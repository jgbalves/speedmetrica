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
    print(outing.head())


if __name__ == '__main__':
    main()
