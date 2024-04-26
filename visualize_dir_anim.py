import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

# Function to update the plot
def update_plot(num):
    global dfs, axs, window_size
    
    for file_name, df in dfs:
        num_vehicles = int(file_name.split('_')[2].split('.')[0])  # Extracting number of vehicles from file name
        color = vehicle_colors.get(num_vehicles, 'black')  # Use predefined color or black if not found
        axs[0].plot(df['step'] / 5, df['system_total_stopped'].rolling(window=window_size).mean(), label=f'{num_vehicles} vehicles', color=color)
        axs[1].plot(df['step'] / 5, df['TL_accumulated_waiting_time'].rolling(window=window_size).mean(), label=f'{num_vehicles} vehicles', color=color)
    
    # Adjust legends
    axs[0].legend().remove()
    axs[1].legend().remove()

# Get all CSV files in the "outputs/" directory
output_directory = "outputs/"
csv_files = [file for file in os.listdir(output_directory) if file.endswith('.csv')]

# Create a list to store dataframes
dfs = []

# Read each CSV file and store its dataframe in the list
for file_name in csv_files:
    file_path = os.path.join(output_directory, file_name)
    df = pd.read_csv(file_path)
    dfs.append((file_name, df))  # Store file name along with dataframe

# Apply a rolling mean to smooth out spikes
window_size = 500

# Define colors for each number of vehicles
vehicle_colors = {
    600: 'red',
    2300: 'blue',
    4000: 'green'
}

# Plotting
fig, axs = plt.subplots(2, 1, figsize=(10, 10))

# Create animation
ani = animation.FuncAnimation(fig, update_plot, frames=None, interval=1000)  # Update every second

# Show the plot
plt.show()
