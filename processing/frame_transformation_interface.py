from abc import ABC, abstractmethod

class FrameTransformation(ABC):

    @abstractmethod
    def apply(self, frame):
        pass