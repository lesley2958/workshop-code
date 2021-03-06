from shapely.geometry import shape, LineString, Point
from descartes import PolygonPatch
import fiona
import matplotlib.pyplot as plt

# coordinates across the pathway of San Francisco to New York City flight
latlons = [(37.766, -122.43), (39.239, -114.89), (38.820, -104.82), (38.039, -97.96),
    (38.940, -92.32), (39.156, -86.53), (40.749, -84.08), (41.494, -81.66),
    (42.325, -80.06), (41.767, -78.01), (41.395, -75.68), (40.625, -73.780)]

path = [(x, y) for y, x in latlons] # reforms into correct format
ls = LineString(path) # converts to proper data type

with fiona.collection("shapefiles/statesp020.shp") as features: 
    states = [shape(f['geometry']) for f in features] # states as background visualization

fig = plt.figure(figsize=(24, 12), dpi=180) # figure initialization

for state in states:
    if state.geom_type == 'Polygon':
        state = [state]

    for poly in state:
        if ls.intersects(poly):
            alpha = 0.4
        else:
            alpha = 0.4

        try:
            poly_patch = PolygonPatch(poly, fc="#6699cc", ec="#6699cc", alpha=alpha, zorder=2) # creates visualization of each state
            fig.gca().add_patch(poly_patch)
        except:
            pass

fig.gca().plot(*ls.xy, color='#FFFFFF') # initializes plot line

for x, y in path:
    p = Point(x, y) 
    spot = p.buffer(.1)
    x, y = spot.exterior.xy
    plt.fill(x, y, color='#cc6666', aa=True)
    plt.plot(x, y, color='#cc6666', aa=True, lw=1.0)

fig.gca().axis([-125, -65, 25, 50])
fig.gca().axis('off')
fig.savefig("states.png", facecolor='#F2F2F2', edgecolor='#F2F2F2')
