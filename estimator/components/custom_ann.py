from annoy import AnnoyIndex
from typing import Literal
import json


class CustomAnnoy(AnnoyIndex):
    """
    Custom AnnoyIndex class with modifications for saving and loading labels.
    """
    def __init__(self, f: int, metric: Literal["angular", "euclidean", "manhattan", "hamming", "dot"]):
        super().__init__(f, metric)
        self.label = []

    def add_item(self, i: int, vector, label: str) -> None:
        """
        Add an item to the Annoy index with a corresponding label.

        Args:
            i (int): Index of the item.
            vector: Item vector.
            label (str): Corresponding label.
        """
        super().add_item(i, vector)
        self.label.append(label)

    def get_nns_by_vector(self, vector, n: int, search_k: int = ..., include_distances: Literal[False] = ...):
        """
        Get nearest neighbors of a vector and return their labels.

        Args:
            vector: Query vector.
            n (int): Number of neighbors to retrieve.
            search_k (int, optional): Search depth. Defaults to None.
            include_distances (Literal[False], optional): Include distances. Defaults to False.

        Returns:
            list: List of labels for nearest neighbors.
        """
        indexes = super().get_nns_by_vector(vector, n, search_k, include_distances)
        labels = [self.label[link] for link in indexes]
        return labels

    def load(self, fn: str, prefault: bool = ...):
        """
        Load Annoy index and corresponding labels from .ann and .json files.

        Args:
            fn (str): Filepath of the .ann file.
            prefault (bool, optional): Prefault option. Defaults to ... (not specified).
        """
        super().load(fn)
        path = fn.replace(".ann", ".json")
        self.label = json.load(open(path, "r"))

    def save(self, fn: str, prefault: bool = ...):
        """
        Save Annoy index and labels to .ann and .json files.

        Args:
            fn (str): Filepath of the .ann file.
            prefault (bool, optional): Prefault option. Defaults to ... (not specified).
        """
        super().save(fn)
        path = fn.replace(".ann", ".json")
        json.dump(self.label, open(path, "w"))

