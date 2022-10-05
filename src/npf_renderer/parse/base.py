from abc import ABC, abstractmethod


class BaseNPFParser(ABC):
    @staticmethod
    @abstractmethod
    def process(content):
        pass

    @staticmethod
    @abstractmethod
    def parse(content):
        pass



