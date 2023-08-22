from abc import *


class LoginAbstractClass(metaclass=ABCMeta):
    @abstractmethod
    def login(self) -> str:
        pass

    @abstractmethod
    def get_password(self) -> str:
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass
