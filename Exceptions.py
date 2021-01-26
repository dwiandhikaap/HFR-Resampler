#still learning how to handle errors :pog:

class OutputFpsNotValid(Exception):
    def __init__(self,message="The given output FPS value is not valid!"):
        self.message = message
        super().__init__(self.message)