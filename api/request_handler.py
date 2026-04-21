from api import endpoints as ep
import logging

def getURL(env="dev"):
    logging.log(logging.INFO, "getURL")    
    return ep.usersUrl[env]
