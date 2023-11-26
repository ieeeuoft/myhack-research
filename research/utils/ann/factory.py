from ..util import Resolver

from .faiss import Faiss
from .numpy import NumPy
from .torch import Torch


class ANNFactory:
    @staticmethod
    def create(config):
        ann = None
        backend = config.get("backend", "faiss")

        match backend:
            case "faiss":
                backend = Faiss(config)
            case "numpy":
                ann = NumPy(config)
            case"torch":
                ann = Torch(config)
            case _:
                ann = ANNFactory.resolve(backend, config)

        config["backend"] = backend

        return ann

    @staticmethod
    def resolve(backend, config):
        try:
            return Resolver()(backend)(config)
        except Exception as e:
            raise ImportError(f"Unable to resolve ann backend: '{backend}'") from e
