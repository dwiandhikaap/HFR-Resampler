class InvalidOutputFPS(Exception):
    def __init__(self,message="The given output FPS value is invalid!"):
        self.message = message
        super().__init__(self.message)

class InvalidResolution(Exception):
    def __init__(self,message="The given output resolution value is invalid!"):
        self.message = message
        super().__init__(self.message)

class VideoReadError(Exception):
    def __init__(self,message="Unable to read video file!"):
        self.message = message
        super().__init__(self.message)

class InvalidCustomWeighting(Exception):
    def __init__(self,message="Invalid custom weighting function!"):
        self.message = message
        super().__init__(self.message)

class InvalidBlendMode(Exception):
    def __init__(self,message="Invalid blending mode!"):
        self.message = message
        super().__init__(self.message)