import os
import matplotlib.pyplot as plt
import pandas as pd

# Get all CSV files in the "outputs/" directory
output_directory = "../testing/output_700/"
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
}

# Define a dictionary to store legend handles and labels
legend_handles_labels = {}

# Plotting
fig, axs = plt.subplots(2, 1, figsize=(10, 10))

# Plot each metric from each dataframe with rolling mean
for file_name, df in dfs:
    num_vehicles = int(file_name.split('_')[2].split('.')[0])  # Extracting number of vehicles from file name
    color = vehicle_colors.get(num_vehicles, 'lightblue')  # Use predefined color or black if not found
    line1, = axs[0].plot(df['step'] / 5, df['system_total_stopped'].rolling(window=window_size).mean(), color=color)
    line2, = axs[1].plot(df['step'] / 5, df['TL_accumulated_waiting_time'].rolling(window=window_size).mean(), color=color)
    
    # Store only one legend entry per number of vehicles
    if num_vehicles not in legend_handles_labels:
        legend_handles_labels[num_vehicles] = (line1, line2, f'{num_vehicles} vehicles')

# Set titles
# axs[0].set_title('System Total Stopped')
# axs[1].set_title('Total Accumulated Waiting Time')

# Set x and y labels
axs[0].set_xlabel('Time (steps)')
axs[0].set_ylabel('System Total Stopped')
axs[1].set_xlabel('Time (steps)')
axs[1].set_ylabel('Total Accumulated Waiting Time')

# Add legends
# legend_handles = [handle for handle, _, _ in legend_handles_labels.values()]
# legend_labels = [label for _, _, label in legend_handles_labels.values()]
# axs[0].legend(legend_handles, legend_labels)
# axs[1].legend(legend_handles, legend_labels)

# Adjust layout
plt.tight_layout()

# Save the plot to a file
#plt.savefig('plots/plot_all.png')

# Show the plot
plt.show()
