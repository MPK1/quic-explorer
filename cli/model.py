import os
import abc
import uuid
import json
import datetime

class QUICObject(abc.ABC):

    def __init__(self, user: str):
        self.created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.created_by = user

    @classmethod
    @abc.abstractmethod
    def filename(cls):
        pass
    
    @classmethod
    def filepath(cls):
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', cls.filename())

    @classmethod
    def load_data_from_json(cls):
        try:
            with open(cls.filepath(), 'r') as file:
                cls._data = json.load(file)
        except FileNotFoundError:
            cls._data = []
        #cls._data = cls._data["items"]
        return cls._data

    def save_to_json(self):
        self._data["items"].append(self.__dict__)
        with open(self.filepath(), 'w') as file:
            json.dump(self._data, file, indent=4)
        return True
    
    @classmethod
    def get_by_uuid(cls, uuid: str):
        for item in cls._data["items"]:
            if item['uuid'] == uuid:
                return item
        return None


class QUICImplementation(QUICObject):

    def __init__(self, name: str, maintainer: str, language: str, repo_url: str, logo_url: str = None, user: str = None):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.maintainer = maintainer
        self.language = language
        self.repo_url = repo_url
        self.logo_url = logo_url
        super().__init__(user)

    @classmethod
    def filename(cls):
        return "implementations.json"


class QUICFeature(QUICObject):

    def __init__(self, name: str, description: str, value_type: str, value_meta: dict, user: str = None):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.value_type = value_type
        self.value_meta = value_meta
        super().__init__(user)

    @classmethod
    def filename(cls):
        return "features.json"


class QUICInfo(QUICObject):

    def __init__(self, implementation_uuid: str, feature_uuid: str, value, source=None, source_url=None, user: str = None):
        self.implementation_uuid = implementation_uuid
        self.feature_uuid = feature_uuid
        self.value = value
        self.source = source
        self.source_url = source_url
        super().__init__(user)

    def save_to_json(self):
        for item in self._data["items"]:
            if item['implementation_uuid'] == self.implementation_uuid and item['feature_uuid'] == self.feature_uuid:
                self._data["items"].remove(item)
        return super().save_to_json()
    
    @classmethod
    def filename(cls):
        return "entries.json"

def get_all_data():
    return (
        QUICImplementation._data["items"],
        QUICFeature._data["items"],
        QUICInfo._data["items"]
    )

models = [
    QUICImplementation,
    QUICFeature,
    QUICInfo
]

for model in models:
    model.load_data_from_json()