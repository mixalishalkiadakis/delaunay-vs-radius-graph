from scipy.spatial import Delaunay
import numpy as np
import matplotlib.pyplot as plt
import math

def radial_connect(points, radius):
    akmes = set()
    for i, center_point in enumerate(points):
        for j, point in enumerate(points):
            if i == j:
                continue
            if math.dist(center_point, point) < radius:
                edge = (min(i,j), max(i,j))
                akmes.add(edge)
    return akmes

def plot_edges(ax, points, edges, color="gray"):
    #for edge (point i, point j) in edges
    for i,j in edges:
        #plot x,y draws line from point x to point y
        ax.plot(
            [points[i, 0], points[j, 0]], #xi , xj
            [points[i, 1], points[j, 1]], #yi, yj
            color=color,
            linewidth=1
        )

#-------------------------------------------------
#POINTS GENERATED WITH AI
#-------------------------------------------------

track_points = np.array([
    # Εξωτερική πλευρά
    [10.0,  0.0],
    [ 9.2,  2.3],
    [ 7.1,  4.2],
    [ 3.8,  5.5],
    [ 0.0,  6.0],
    [-3.8,  5.5],
    [-7.1,  4.2],
    [-9.2,  2.3],
    [-10.0, 0.0],
    [-9.2, -2.3],
    [-7.1, -4.2],
    [-3.8, -5.5],
    [ 0.0, -6.0],
    [ 3.8, -5.5],
    [ 7.1, -4.2],
    [ 9.2, -2.3],

    # Εσωτερική πλευρά
    [ 7.0,  0.0],
    [ 6.4,  1.3],
    [ 5.0,  2.5],
    [ 2.7,  3.3],
    [ 0.0,  3.6],
    [-2.7,  3.3],
    [-5.0,  2.5],
    [-6.4,  1.3],
    [-7.0,  0.0],
    [-6.4, -1.3],
    [-5.0, -2.5],
    [-2.7, -3.3],
    [ 0.0, -3.6],
    [ 2.7, -3.3],
    [ 5.0, -2.5],
    [ 6.4, -1.3]
])


few_false_positives = np.array([
    [ 8.1,  1.0],
    [-4.5,  4.4],
    [ 1.0, -4.8]
])
points_few = np.vstack([
    track_points,
    few_false_positives
])


many_false_positives = np.array([
    [ 8.1,  1.0],
    [-4.5,  4.4],
    [ 1.0, -4.8],

    [ 8.0, -1.0],
    [ 6.2,  3.4],
    [ 4.4,  4.6],
    [ 1.8,  4.7],
    [-1.5,  4.8],
    [-6.0,  3.6],
    [-8.1,  1.1],
    [-8.0, -1.2],
    [-6.0, -3.4],
    [-4.1, -4.4],
    [ 4.0, -4.5],
    [ 6.5, -3.4],

    # False positives μέσα στο εσωτερικό της πίστας
    [ 0.0,  0.0],
    [ 1.5,  0.8],
    [-1.4,  1.0],
    [ 2.8, -0.4],
    [-3.0, -0.8],
    [ 0.5,  2.2],
    [-0.8, -2.1],
    [ 4.2,  0.5],
    [-4.3,  0.4],
    [ 2.0, -2.2],
    [-2.0,  2.3]
])
points_many = np.vstack([
    track_points,
    many_false_positives
])

#-------------------------------------------------
#get delaunay triangles
#-------------------------------------------------
tri_few = Delaunay(points_few)
tri_many = Delaunay(points_many)


#-------------------------------------------------
#get radial connected vertices
#-------------------------------------------------
radius = 4
akmes_few = radial_connect(points_few, radius)
akmes_many = radial_connect(points_many, radius)


fig, axes = plt.subplots(2, 2, figsize=(16, 10))


#-------------------------------------------------
# few false positives
#-------------------------------------------------
axes[0, 0].triplot(
    points_few[:, 0], # to prwto apo oles tis grammes -> ola ta x
    points_few[:, 1], #to deyteto apo oles tis grammes -> ola ta y
    tri_few.simplices,
    color="gray"
)

axes[0, 0].scatter(
    track_points[:, 0],
    track_points[:, 1],
    color="blue",
    s=45,
    label="Real cones"
)

axes[0, 0].scatter(
    few_false_positives[:, 0],
    few_false_positives[:, 1],
    color="red",
    marker="x",
    s=90,
    label="False positives"
)

axes[0, 0].set_title("Few false positives")
axes[0, 0].set_aspect("equal")
axes[0, 0].grid(alpha=0.3)
axes[0, 0].legend()


#-------------------------------------------------
# many false positives
#-------------------------------------------------
axes[0, 1].triplot(
    points_many[:, 0],
    points_many[:, 1],
    tri_many.simplices,
    color="gray"
)

axes[0, 1].scatter(
    track_points[:, 0],
    track_points[:, 1],
    color="blue",
    s=45,
    label="Real cones"
)

axes[0, 1].scatter(
    many_false_positives[:, 0],
    many_false_positives[:, 1],
    color="red",
    marker="x",
    s=90,
    label="False positives"
)

axes[0, 1].set_title("Many false positives")
axes[0, 1].set_aspect("equal")
axes[0, 1].grid(alpha=0.3)
axes[0, 1].legend()


#-------------------------------------------------
#few false radial
#-------------------------------------------------
plot_edges(axes[1,0], points_few, akmes_few)

axes[1, 0].scatter(
    track_points[:, 0],
    track_points[:, 1],
    color="blue",
    s=45,
    label="Real cones"
)

axes[1, 0].scatter(
    few_false_positives[:, 0],
    few_false_positives[:, 1],
    color="red",
    marker="x",
    s=90,
    label="False positives"
)

axes[1, 0].set_title("Few false positives")
axes[1, 0].set_aspect("equal")
axes[1, 0].grid(alpha=0.3)
axes[1, 0].legend()


#-------------------------------------------------
#many false radial
#-------------------------------------------------
plot_edges(axes[1,1], points_many, akmes_many)

axes[1, 1].scatter(
    track_points[:, 0],
    track_points[:, 1],
    color="blue",
    s=45,
    label="Real cones"
)

axes[1, 1].scatter(
    many_false_positives[:, 0],
    many_false_positives[:, 1],
    color="red",
    marker="x",
    s=90,
    label="False positives"
)

axes[1, 1].set_title("Few false positives")
axes[1, 1].set_aspect("equal")
axes[1, 1].grid(alpha=0.3)
axes[1, 1].legend()


plt.tight_layout()

plt.savefig(
    "results/comparison.png",
    dpi=200,
    bbox_inches="tight"
)

plt.show()

