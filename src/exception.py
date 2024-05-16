import sys

class CustomException(Exception):
    def __init__(self, error_message):
        # Get the current exception details
        exc_type, _, exc_tb = sys.exc_info()
        
        # Initialize the attributes
        self.traceback = exc_tb
        self.error_message = error_message
        self.error_type = exc_type.__name__ if exc_type else 'UnknownError'
        
        # Initialize the base Exception class
        super().__init__(error_message)

    def get_full_message(self):
        """
        Constructs and returns a detailed error message.
        """
        if self.traceback:
            filename = self.traceback.tb_frame.f_code.co_filename
            line = self.traceback.tb_lineno
        else:
            filename = 'Unknown file'
            line = 'Unknown line'
        
        return f"Error ({self.error_type}) occurred in file '{filename}', line {line}: {self.error_message}"

    def __str__(self):
        """
        Returns the string representation of the exception.
        """
        return self.get_full_message()

