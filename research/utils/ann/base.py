import datetime
import platform

from abc import ABC, abstractmethod


class ANN(ABC):

    def __init__(self, config):
        self.backend = None
        self.config = config

    @abstractmethod
    def load(self, path):
        ...

    @abstractmethod
    def index(self, embeddings):
        ...

    @abstractmethod
    def append(self, embeddings):
        ...

    @abstractmethod
    def delete(self, ids):
        ...

    @abstractmethod
    def search(self, queries, limit):
        ...

    @abstractmethod
    def count(self):
        ...

    @abstractmethod
    def save(self, path):
        ...

    def setting(self, name, default=None):
        backend = self.config.get(self.config["backend"])

        setting = backend.get(name) if backend else None
        return setting if setting else default

    def metadata(self, settings=None):
        create = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        if settings:
            self.config["build"] = {
                "create": create,
                "python": platform.python_version(),
                "settings": settings,
                "system": f"{platform.system()} ({platform.machine()})",
            }

        self.config["update"] = create
