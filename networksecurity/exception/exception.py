import sys

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_detail:sys):
        _, _, exc_tb = error_detail.exc_info()
        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.error_message = error_message
        super().__init__(self.error_message)

    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(self.file_name, self.lineno, str(self.error_message))

    def __repr__(self):
        return NetworkSecurityException.__name__.str()
