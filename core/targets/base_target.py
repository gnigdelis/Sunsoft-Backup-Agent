from abc import (
    ABC,
    abstractmethod,
)


class BaseTarget(ABC):

    @abstractmethod
    def analyse(self):

        pass

    @abstractmethod
    def collect(self):

        pass

    @abstractmethod
    def validate(self):

        pass