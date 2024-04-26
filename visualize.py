import sys
import matplotlib.pyplot as plt
import pandas as pd

# Get the command line arguments for file names
command_line_names = sys.argv[1:]

# Create a list to store dataframes
dfs = []

# # Read the CSV files and store them in the list
# for name in command_line_names:
#     file_name = f"output_{name}.csv"
#     df = pd.read_csv(file_name)
#     dfs.append(df)
  
file_name = f"outputs/output_test.csv"
df = pd.read_csv(file_name)
dfs.append(df)
    
# Apply a rolling mean to smooth out spikes
window_size = 10

# Plotting
fig, axs = plt.subplots(2, 1, figsize=(10, 10))

# Plot each metric from each dataframe with rolling mean
for i, df in enumerate(dfs):
    axs[0].plot(df['step']/5, df['system_total_stopped'].rolling(window=window_size).mean(), label='label')
    axs[1].plot(df['step']/5, df['TL_accumulated_waiting_time'].rolling(window=window_size).mean(), label='label')

# Set titles
axs[0].set_xlabel('Time (steps)')
axs[0].set_ylabel('System Total Stopped')
axs[1].set_xlabel('Time (steps)')
axs[1].set_ylabel('Total Accumulated Waiting Time')

# Adjust layout
plt.tight_layout()

# Show the plot
# plt.show()

plt.savefig('plots/test.png')
