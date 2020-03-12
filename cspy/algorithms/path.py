from types import BuiltinFunctionType
from operator import add
from numpy import zeros, array
from collections import deque


class Path(object):

    _REF = add

    def __init__(self, G, path, max_res, min_res):
        self.G = G
        self.path = path
        self.max_res = max_res
        self.min_res = min_res

    def __repr__(self):
        return str(self)

    def __str__(self):  # for printing purposes
        return "Path({0},{1},{2})".format(self.path, self.max_res, self.min_res)

    def _check_feasibility(self):
        shortest_path_edges = deque(e for e in zip(self.path, self.path[1:]))
        if any(e not in self.G.edges() for e in shortest_path_edges):
            raise Exception("No edge found")
        else:
            shortest_path_edges_w_data = deque()
            for e in shortest_path_edges:
                edge = deque(edge for edge in self.G.edges(data=True)
                             if edge[0:2] == e)[0]
                shortest_path_edges_w_data.append(edge)

        total_res = zeros(self.G.graph['n_res'])
        # Check path for resource feasibility by adding one edge at a time
        for edge in shortest_path_edges_w_data:
            if isinstance(self._REF, BuiltinFunctionType):
                total_res += self._edge_extract(edge)
            else:
                total_res = self._REF(total_res, edge)
            if (all(total_res <= self.max_res) and
                    all(total_res >= self.min_res)):
                pass
            else:
                break
        else:
            return True
        return edge

    @staticmethod
    def _edge_extract(edge):
        return array(edge[2]['res_cost'])