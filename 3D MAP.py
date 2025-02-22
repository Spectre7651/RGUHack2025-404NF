
import datetime
import matplotlib.pyplot as plt
import numpy as np
import imageio.v2 as imageio  # Using imageio.v2 to avoid deprecation warning
import os
from mpl_toolkits.basemap import Basemap

# Directory to save images
output_dir = './'
os.makedirs(output_dir, exist_ok=True)

# Set up figure for plotting with higher DPI
plt.ion()
fig, ax0 = plt.subplots(figsize=(5.3, 4), dpi=150)  # Increased DPI for higher resolution
ax0.set_position([0.0, 0.0, 1.0, 1.0])

lat_viewing_angle = [20, 20]
lon_viewing_angle = [-180, 180]
rotation_steps = 150
lat_vec = np.linspace(lat_viewing_angle[0], lat_viewing_angle[0], rotation_steps)
lon_vec = np.linspace(lon_viewing_angle[0], lon_viewing_angle[1], rotation_steps)

# Initial Basemap setup
m1 = Basemap(projection='ortho', 
             lat_0=lat_vec[0], lon_0=lon_vec[0], resolution=None)

# Add axis for space background effect
galaxy_image = plt.imread('./nathan-anderson-eS7HrvG0mcA-unsplash.jpg')  # Background image
ax0.imshow(galaxy_image)
ax0.set_axis_off()
ax1 = fig.add_axes([0.25, 0.2, 0.5, 0.5])

# Define map coordinates from full-scale globe
map_coords_xy = [m1.llcrnrx, m1.llcrnry, m1.urcrnrx, m1.urcrnry]
zoom_prop = 2.0  # Use 1.0 for full-scale map

# Generate and save each frame as a PNG
for pp in range(len(lat_vec)):
    ax1.clear()
    ax1.set_axis_off()
    m = Basemap(projection='ortho', resolution='l',
                lat_0=lat_vec[pp], lon_0=lon_vec[pp],
                llcrnrx=-map_coords_xy[2]/zoom_prop,
                llcrnry=-map_coords_xy[3]/zoom_prop,
                urcrnrx=map_coords_xy[2]/zoom_prop,
                urcrnry=map_coords_xy[3]/zoom_prop)

    m.bluemarble(scale=0.5)
    m.drawcoastlines()

    # Save each frame with higher DPI
    frame_filename = os.path.join(output_dir, f"{pp}.png")
    plt.savefig(frame_filename, bbox_inches='tight', pad_inches=0, dpi=200, transparent=True)  # Higher DPI
    plt.pause(0.01)

# Create a GIF from saved images
images = []
for pp in range(len(lat_vec)):
    filename = os.path.join(output_dir, f"{pp}.png")
    images.append(imageio.imread(filename))

# Save the images as a high-resolution GIF
imageio.mimsave('3D_Globe_HighRes.gif', images, duration=0.5)

print("High-resolution GIF created successfully!")
