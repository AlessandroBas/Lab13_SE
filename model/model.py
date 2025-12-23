import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):

        self.G = nx.DiGraph()
        self._nodes = []
        self._edges = []

        self.id_map = {}
        self.soluzione_best = []

        self._lista_cromosomi = []
        self._lista_geni = []
        self._lista_geni_connessi = []

        self.load_geni()
        self.load_cromosomi()
        self.load_geni_connessi()

    def load_cromosomi(self):
        self._lista_cromosomi = DAO.read_cromosomi()

    def load_geni(self):
        self._lista_geni = DAO.read_geni()
        self.id_map = {}
        for g in self._lista_geni:
            self.id_map[g.id] = g.cromosoma

    def load_geni_connessi(self):
        self._lista_geni_connessi = DAO.read_connesioni()

    def costruisci_grafo(self):

        self.G.clear()

        self._nodes = []
        self._edges = []

        #NODI
        for c in self._lista_cromosomi:
            self._nodes.append(c)
        self.G.add_nodes_from(self._nodes)

        #ARCHI
        edges = {}
        for g1, g2, corr in self._lista_geni_connessi:
            if (self.id_map[g1], self.id_map[g2]) not in edges:
                edges[(self.id_map[g1], self.id_map[g2])] = float(corr)
            else:
                edges[(self.id_map[g1], self.id_map[g2])] += float(corr)
        for k, v in edges.items():
            self._edges.append((k[0], k[1], v))
        self.G.add_weighted_edges_from(self._edges)

    def get_minimo (self):
        return min(d['weight'] for u, v, d in self.G.edges(data=True))

    def get_massimo (self):
        return max(d['weight'] for u, v, d in self.G.edges(data=True))

    def conta_archi(self,soglia):
        minori = 0
        maggiori = 0
        for u, v, d in self.G.edges(data=True):
            peso = d['weight']
            if peso > soglia:
                maggiori += 1
            elif peso < soglia:
                minori += 1
        return minori, maggiori

    def ricerca_cammino(self, t):
        self.soluzione_best.clear()

        for n in self.G.nodes():
            partial = []
            partial_edges = []

            partial.append(n)
            self.ricorsione(partial, partial_edges, t)

    def ricorsione(self, partial_nodes, partial_edges, t):
        n_last = partial_nodes[-1]
        neigh = self._get_admissible_neighbors(n_last, partial_edges, t)

        # stop
        if len(neigh) == 0:
            weight_path = self.compute_weight_path(partial_edges)
            weight_path_best = self.compute_weight_path(self.soluzione_best)
            if weight_path > weight_path_best:
                self.soluzione_best = partial_edges[:]
            return

        for n in neigh:
            partial_nodes.append(n)
            partial_edges.append((n_last, n, self.G.get_edge_data(n_last, n)))
            self.ricorsione(partial_nodes, partial_edges, t)
            partial_nodes.pop()
            partial_edges.pop()

    def _get_admissible_neighbors(self, node, partial_edges, soglia):
        result = []
        for u, v, data in self.G.out_edges(node, data=True):
            if data["weight"] > soglia:
                # controllo SOLO l'arco diretto
                if (u, v) not in [(x[0], x[1]) for x in partial_edges]:
                    result.append(v)
        return result

    def compute_weight_path(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]['weight']
        return weight