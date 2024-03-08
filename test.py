from datascience import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

matplotlib.use("TkAgg")

data: dict[str, Table] = {}

for dir_name, _, file_names in os.walk("./Music"):
	for file in file_names:
		if file.endswith(".csv"):
			file_name = file[:-4]
			data[file_name] = Table.read_table(f"{dir_name}/{file}")

explanatory_variables_radar = ["danceability", "energy", "acousticness", "instrumentalness", "liveness", "valence", "mode"]


def plot_radar_for_playlist(playlist_name):
	fig, ax = plt.subplots(figsize=(8, 4), subplot_kw={"polar": True})

	angles = list(np.linspace(0, 2 * np.pi, len(explanatory_variables_radar), endpoint=False))
	angles.append(angles[0])

	r = []

	for explanatory_variable in explanatory_variables_radar:
		r.append(np.mean(data[playlist_name].column(explanatory_variable)))

	r.append(r[0])

	ax.fill(angles, r)
	ax.plot(angles, r)

	ax.set_rmax(1)
	ax.set_rticks([0.5, 1])  # Less radial ticks

	plt.xticks(angles[:-1], explanatory_variables_radar, color='black', size=12)

	ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line


plot_radar_for_playlist("My Playlist")
plot_radar_for_playlist("HTTYD (1)")
plot_radar_for_playlist("HTTYD (2)")
plot_radar_for_playlist("HTTYD (3)")

plt.show()
