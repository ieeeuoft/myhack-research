import numpy as np
import pickle

from research.utils.ann.base import ANN


class NumPy(ANN):

    def __init__(self, config):
        super().__init__(config)

        self.all, self.cat, self.dot, self.zeros = np.all, np.concatenate, np.dot, np.zeros

    def load(self, path):
        with open(path, "rb") as handle:
            self.backend = self.tensor(pickle.load(handle))

    def index(self, embeddings):
        self.backend = self.tensor(embeddings)

        self.config["offset"] = embeddings.shape[0]
        self.metadata(self.settings())

    def append(self, embeddings):
        new = embeddings.shape[0]

        self.backend = self.cat((self.backend, self.tensor(embeddings)), axis=0)

        self.config["offset"] += new
        self.metadata()

    def delete(self, ids):
        ids = [x for x in ids if x < self.backend.shape[0]]

        self.backend[ids] = self.tensor(self.zeros((len(ids), self.backend.shape[1])))

    def search(self, queries, limit):
        scores = self.dot(self.tensor(queries), self.backend.T).tolist()
        return [sorted(enumerate(score), key=lambda x: x[1], reverse=True)[:limit] for score in scores]

    def count(self):
        return self.backend[~self.all(self.backend == 0, axis=1)].shape[0]

    def save(self, path):
        with open(path, "wb") as handle:
            pickle.dump(self.backend, handle)

    def tensor(self, array):
        return array

    def settings(self):
        return {"numpy": np.__version__}
