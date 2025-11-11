import re
from datetime import datetime, timedelta

def get_error_from_exception(exc):
    error_params = str(exc).split("-")        
    error = {
        "error_code": (int(error_params[0]) 
                        if len(error_params) == 2 
                        else 500),
        "error_message": (error_params[1] 
                            if len(error_params) == 2
                            else "Internal server error")
        }
    return error

def check_empty(val):    
    if val is None:
        return True
    if val == "":
        return True    
    return False
    
def check_not_alpha(val):    
    if val.isalpha():
        return False
    return True

def check_special_characters(val):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if(not regex.search(val) == None):
        return True
    return False

def get_current_date_time():
    current_date_time = datetime.utcnow()
    current_date_time = current_date_time.strftime("%d-%b-%Y T%H:%M:%S")
    return current_date_time

def get_current_timestamp(delta):
    current_timestamp = datetime.utcnow()
    if delta:
        current_timestamp = current_timestamp + timedelta(seconds = delta)
    return current_timestamp