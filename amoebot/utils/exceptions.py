class InitializationError(Exception):
   r""" raised when the initialisation format is incorrect
   """
   pass

class ShapeError(Exception):
   r""" raised when input sizes are mismatched
   """
   pass

class MovementError(Exception):
   r""" raised when particle receives invalid movement instructions.
   """
   pass