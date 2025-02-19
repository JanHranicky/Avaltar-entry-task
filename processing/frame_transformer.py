class FrameTransformer:
    """
    Frame Transformer class used to register and apply multiple transformations to a frame
    """
    def __init__(self):
        self.transfromations = []
    
    def add_transformation(self, transformation):
        """Adds processor to the pipeline

        Args:
            transformation (FrameTransformation): instance of FrameTransformation class
        """
        self.transfromations.append(transformation)
    
    def transform(self,frame):
        """Applies registered transformations to a frame and returns the modified frame

        Args:
            frame (_type_): _description_

        Returns:
            _type_: _description_
        """
        for transform in self.transfromations:
            frame = transform.apply(frame)
        return frame