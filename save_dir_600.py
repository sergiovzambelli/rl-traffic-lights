import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Get all CSV files in the "outputs/" directory
output_directory = "outputs/"
csv_files = [file for file in os.listdir(output_directory) if file.startswith('output_dqn_600')]

# Create empty lists to store dataframes
dfs_stopped = []
dfs_waiting_time = []

# Read each CSV file and store its dataframe in the list
for file_name in csv_files:
    file_path = os.path.join(output_directory, file_name)
    df = pd.read_csv(file_path)
    dfs_stopped.append(df['system_total_stopped'])
    dfs_waiting_time.append(df['TL_accumulated_waiting_time'])

# Combine all dataframes into a single dataframe
df_stopped_combined = pd.concat(dfs_stopped, axis=1)
df_waiting_time_combined = pd.concat(dfs_waiting_time, axis=1)

# Calculate rolling mean to smooth out spikes
window_size = 500
rolling_mean_stopped = df_stopped_combined.rolling(window=window_size).mean()
rolling_mean_waiting_time = df_waiting_time_combined.rolling(window=window_size).mean()

# Plotting
fig, axs = plt.subplots(2, 1, figsize=(10, 10))

# Define gradient of red colors
num_colors = len(rolling_mean_stopped.columns)
colors = [plt.cm.Reds(i/num_colors) for i in range(num_colors)]

# Plot system total stopped for all files
for i, column in enumerate(rolling_mean_stopped.columns):
    axs[0].plot(df.index / 5, rolling_mean_stopped[column], color=colors[i], label=f'{column} vehicles')

# Plot total accumulated waiting time for all files
for i, column in enumerate(rolling_mean_waiting_time.columns):
    axs[1].plot(df.index / 5, rolling_mean_waiting_time[column], color=colors[i], label=f'{column} vehicles')

# Set x and y labels
axs[0].set_xlabel('Time (steps)')
axs[0].set_ylabel('System Total Stopped')
axs[1].set_xlabel('Time (steps)')
axs[1].set_ylabel('Total Accumulated Waiting Time')


# Adjust layout
plt.tight_layout()

# Save the plot to a file
plt.savefig('plots/combined_plot_600.png')

# Show the plot
# plt.show()
