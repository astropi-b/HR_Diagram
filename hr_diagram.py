import tkinter as tk
from tkinter import simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from astroquery.vizier import Vizier

# Function to fetch data for the cluster
def fetch_cluster_data(cluster_name):
    v = Vizier(columns=['**'], row_limit=10000)
    result = v.query_region(cluster_name, radius="0.5 deg", catalog=["I/345"])
    main_table = result[0]
    print("Available columns:", main_table.colnames)  # Print the column names
    return main_table

# Function to create a DataFrame from the fetched data
def create_gaia_dataframe(data):
    gaia = pd.DataFrame({
        'Teff': data['Teff'],
        'BP-RP': data['BP-RP'],
        'BP-G': data['BP-G'],
        'Gmag': data['Gmag'],
        'G-RP': data['G-RP'],
        'Lum': data['Lum'],
        'Plx': data['Plx'],
        'e_Plx': data['e_Plx']
    })
    return gaia

# Function to plot the HR diagram
def plot_hr_diagram_gaia(df, cluster_name):
    if 'Gmag' in df.columns and 'BP-RP' in df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        sc = ax.scatter(df['BP-RP'], df['Gmag'], s=1, alpha=0.5, color='blue')
        ax.invert_yaxis()
        ax.set_xlabel('BP - RP (Color Index)')
        ax.set_ylabel('G Magnitude')
        ax.set_title('HR Diagram for ' + cluster_name)
        ax.grid(True)
        return fig
    else:
        print("The required columns are not present in the DataFrame.")
        return None

# Function called when the button is pressed
def on_submit():
    cluster_name = entry.get()
    data = fetch_cluster_data(cluster_name)
    gaia = create_gaia_dataframe(data)
    gaia['Plx/e_Plx'] = gaia['Plx'] / gaia['e_Plx']
    gaia.dropna(subset=['Plx/e_Plx'], inplace=True)
    gaia = gaia[gaia['Plx/e_Plx'] > 5]
    fig = plot_hr_diagram_gaia(gaia, cluster_name)
    if fig:
        canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Main window
window = tk.Tk()
window.title("HR Diagram Plotter")

# Label for instruction
label = tk.Label(window, text="Enter any cluster of your choice (e.g., M53, M45):")
label.pack(side=tk.TOP, padx=20, pady=10)

# Input field
entry = tk.Entry(window)
entry.pack(side=tk.TOP, padx=20, pady=20)

# Button to trigger data fetch and plotting
button = tk.Button(window, text="Plot HR Diagram", command=on_submit)
button.pack(side=tk.TOP)

window.mainloop()