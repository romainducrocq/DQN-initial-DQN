from utils import *
import random


class Track:
    def __init__(self, n_vertices=(5, 10), width=(200, 300)):
        self.n_vertices = random.randint(n_vertices[0], n_vertices[1])
        self.width = random.randint(width[0], width[1])
        self.in_border_vertices = generate_polygon(n_vertices=self.n_vertices, avg_radius=(RES[0]+RES[1]-2*self.width)/2, offset=self.width+100)
        self.out_border_vertices = zoom_vertices(self.in_border_vertices, zoom=self.width)

        self.vertex_color = [255, 0, 100]

        self.polygons = []
        self.polygons_color = [51, 51, 51]

    def border_vertices(self):
        return self.out_border_vertices + self.in_border_vertices

    def start_line(self):
        start_vertex = random.randint(0, self.n_vertices-1)
        start_pos = midpoint_vertex([
            midpoint_vertex(self.out_border_vertices[start_vertex]),
            midpoint_vertex(self.in_border_vertices[start_vertex])
        ])
        start_theta = math.degrees(slope_vertex(self.out_border_vertices[start_vertex])) + [-1, 1][random.randint(0, 1)]*90
        return start_pos, start_theta

    def create_polygons(self):
        for i in range(self.n_vertices):
            self.polygons.append(
                self.out_border_vertices[i] +
                [self.out_border_vertices[i][1], self.in_border_vertices[i][1]] +
                self.in_border_vertices[i][::-1] +
                [self.in_border_vertices[i][0], self.out_border_vertices[i][0]]
            )
