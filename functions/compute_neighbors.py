from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.Heegaard_Diagram_class import Heegaard_diagram

def compute_neighbors(diagram: Heegaard_diagram) -> None:
	"""Record which regions share an edge with which, in place.

	Fills the red_neighbors and blue_neighbors attributes of every region of
	the diagram, each as a list of (region, shared edge) pairs.
	"""
	for i in diagram.regions.keys():

        # We compute the red neighbors
		for edge in diagram.regions[i].red_edges:
			for j in diagram.regions.keys():
				if edge[::-1] in diagram.regions[j].red_edges:
					diagram.regions[i].add_neighbor([diagram.regions[j],edge], 'red')
					break
        
        # We compute the blue neighbors
		for edge in diagram.regions[i].blue_edges:
			for j in diagram.regions.keys():
				if edge[::-1] in diagram.regions[j].blue_edges:
					diagram.regions[i].add_neighbor([diagram.regions[j],edge], 'blue')
					break