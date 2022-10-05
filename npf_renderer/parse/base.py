from abc import ABC, abstractmethod


class BaseNPFParser(ABC):
    @staticmethod
    @abstractmethod
    def process(post, content):
        pass

    @staticmethod
    @abstractmethod
    def parse(post, content):
        pass



