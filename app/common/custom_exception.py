import sys

class CustomException(Exception):
    def __init__(self,message:str,error_detail:Exception=None):
        self.error_message=self.get_detailed_error_message(message,error_detail)
        super().__init__(self.error_message)

    def get_detailed_error_message(self,message,error_detail):
        _,_,exc_tb=sys.exc_info()
        filename=exc_tb.tb_frame.f_code.co_filename
        line_number=exc_tb.tb_lineno
        return f"{message}, filename: {filename}, line_number: {line_number}"
    
    def __str__(self):
        return self.error_message