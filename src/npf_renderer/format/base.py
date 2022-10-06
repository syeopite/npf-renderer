import abc


class BaseFormatter(abc.ABC):
    """Abstract class to represent methods all formatters would have"""

    # Although we could get away with using staticmethods for the parsers
    # The interpreting part is going to be significantly more advanced. Thus:

    @abc.abstractmethod
    def __init__(self, post, content, layout=None, trails=None):
        pass

    # @abc.abstractmethod
    # def process(self, post, content):
    #     pass

    @abc.abstractmethod
    def format(self):
        pass
