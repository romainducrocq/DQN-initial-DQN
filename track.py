from utils import *


class Track:
    def __init__(self, n_vertices, irregularity, spikeyness):
        self.n_vertices = n_vertices
        self.vertices = generate_polygon(0, 0, (RES[0]+RES[1])/2, irregularity, spikeyness, n_vertices)

        self.vertex_color = [0, 0, 0]