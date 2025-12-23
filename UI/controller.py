import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

        self.flag = True

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        self._model.costruisci_grafo()
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo calcolato: {self._model.G.number_of_nodes()} nodi, {self._model.G.number_of_edges()} archi"))
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f'Informazioni sui pesi degli archi - valore minimo: {self._model.get_minimo():.2f} e valore massimo: {self._model.get_massimo():.2f}'))
        self._view.update()

    def handle_conta_edges(self, e):
        """ Handler per gestire il conteggio degli archi """""
        # TODO
        try:
            soglia = float(self._view.txt_name.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return
        min_p=self._model.get_minimo()
        max_p=self._model.get_massimo()

        if soglia< min_p or soglia> max_p:
            self._view.show_alert(f"Soglia fuori range ({min_p:.2f}-{max_p:.2f})")
            return

        minori, maggiori = self._model.conta_archi(soglia)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Numero archi con peso > {soglia}: {maggiori}"))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Numero archi con peso < {soglia}: {minori}"))
        self._view.page.update()

    def handle_ricerca(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """""
        if self.flag:
            self.flag = False
            try:
                soglia = float(self._view.txt_name.value)
                self._model.ricerca_cammino(soglia)
                self._view.lista_visualizzazione_3.controls.clear()
                self._view.lista_visualizzazione_3.controls.append(
                    ft.Text(f"Numero archi percorso più lungo: {len(self._model.soluzione_best)}"))
                self._view.update()

                self._view.lista_visualizzazione_3.controls.append(ft.Text(
                    f"Peso cammino massimo: {str(self._model.compute_weight_path(self._model.soluzione_best))}"))

                for ii in self._model.soluzione_best:
                    self._view.lista_visualizzazione_3.controls.append(ft.Text(
                        f"{ii[0]} --> {ii[1]}: {str(ii[2]['weight'])}"))
            except ValueError:
                self._view.show_alert("Valore numerico non non valido!")

            self._view.update()
            self.flag = True