from utils import *
import random


class Track:
    def __init__(self, n_vertices=(5, 10), width=(200, 300), n_reward_gates=40):
        self.n_vertices = random.randint(n_vertices[0], n_vertices[1])
        self.width = random.randint(width[0], width[1])
        self.in_border_vertices = generate_polygon(n_vertices=self.n_vertices,
                                                   avg_radius=(RES[0] + RES[1] - 2 * self.width) / 2,
                                                   offset=self.width + 100)
        self.out_border_vertices = zoom_vertices(self.in_border_vertices, zoom=self.width)
        self.n_reward_gates = n_reward_gates
        self.reward_gates = []

        self.vertex_color = [255, 0, 100]

        self.polygons = []
        self.polygons_color = [51, 51, 51]

    def border_vertices(self):
        return self.out_border_vertices + self.in_border_vertices

    def start_line(self):
        start_vertex = random.randint(0, self.n_vertices - 1)
        start_pos = midpoint_vertex([
            midpoint_vertex(self.out_border_vertices[start_vertex]),
            midpoint_vertex(self.in_border_vertices[start_vertex])
        ])
        start_theta = math.degrees(slope_vertex(self.out_border_vertices[start_vertex])) + random.choice([-1, 1]) * 90
        return start_pos, start_theta

    # TODO
    def create_reward_gates(self):
        border_vertices_dicts, length_total_out = [], 0
        for i in range(self.n_vertices):
            border_vertices_dicts.append({
                "length_out": euclidean_distance(self.out_border_vertices[i][0], self.out_border_vertices[i][1]),
                "length_in": euclidean_distance(self.in_border_vertices[i][0], self.in_border_vertices[i][1]),
                "slope_out": slope_vertex_corrected(self.out_border_vertices[i]),
                "slope_in": slope_vertex_corrected(self.in_border_vertices[i])
            })
            length_total_out += border_vertices_dicts[i]["length_out"]
        for i in range(self.n_vertices):
            border_vertices_dicts[i]["n_reward_gates"] = \
                int(round(((self.n_reward_gates * border_vertices_dicts[i]["length_out"]) / length_total_out), 0))
        diff = self.n_reward_gates - sum([d["n_reward_gates"] for d in border_vertices_dicts])
        for _ in range(abs(diff)):
            rand_vertex = random.randint(0, self.n_vertices - 1)
            while border_vertices_dicts[rand_vertex]["n_reward_gates"] <= 1:
                rand_vertex = random.randint(0, self.n_vertices - 1)
            border_vertices_dicts[rand_vertex]["n_reward_gates"] += sign(diff)

        for i in range(self.n_vertices):
            step_out = border_vertices_dicts[i]["length_out"] / border_vertices_dicts[i]["n_reward_gates"]
            step_in = border_vertices_dicts[i]["length_in"] / border_vertices_dicts[i]["n_reward_gates"]
            for n in range(border_vertices_dicts[i]["n_reward_gates"]):
                self.reward_gates.append([
                    point_on_circle(
                        border_vertices_dicts[i]["slope_out"], n * step_out,
                        self.out_border_vertices[i][0][0], self.out_border_vertices[i][0][1]
                    ),
                    point_on_circle(
                        border_vertices_dicts[i]["slope_in"], n * step_in,
                        self.in_border_vertices[i][0][0], self.in_border_vertices[i][0][1]
                    )
                ])

        [print(d) for d in border_vertices_dicts]

    def create_polygons(self):
        for i in range(self.n_vertices):
            self.polygons.append(
                self.out_border_vertices[i] +
                [self.out_border_vertices[i][1], self.in_border_vertices[i][1]] +
                self.in_border_vertices[i][::-1] +
                [self.in_border_vertices[i][0], self.out_border_vertices[i][0]]
            )
