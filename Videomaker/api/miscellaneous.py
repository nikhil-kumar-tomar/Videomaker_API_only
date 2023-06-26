from .models import *
from django.db.models import Q
from django.conf import settings

def object_exists(factor:dict,model:str):
    """
    factor is a dictionary {"email":"abc@ghmail.com"} < usage is here, arguments are supposed to be passed like this
    Model is supposed to be passed as a string object like model="User" where User is the name of the model you are refering to
    """
    return eval(model).objects.filter(**factor).exists()

def object_get(factor:dict,model:str):
    """
    factor is a dictionary {"email":"abc@ghmail.com"} < usage is here, arguments are supposed to be passed like this
    Model is supposed to be passed as a string object like model="User" where User is the name of the model you are refering to
    """
    return eval(model).objects.get(**factor)

def object_creator(factor:dict,model:str):
    # this function is to create objects in user defined models
    return eval(model).objects.create(**factor)
    
def object_filter(factor:dict,model:str):
    """
    factor is a dictionary {"email":"abc@ghmail.com"} < usage is here, arguments are supposed to be passed like this
    Model is supposed to be passed as a string object like model="User" where User is the name of the model you are refering to
    """
    return eval(model).objects.filter(**factor)

def object_filter_orderby(factor:dict,model:str,orderby):
    """
    factor is a dictionary {"email":"abc@ghmail.com"} < usage is here, arguments are supposed to be passed like this
    Model is supposed to be passed as a string object like model="User" where User is the name of the model you are refering to
    """
    return eval(model).objects.filter(**factor).order_by(orderby)

def object_all(model):
    """
    factor is a dictionary {"email":"abc@ghmail.com"} < usage is here, arguments are supposed to be passed like this
    Model is supposed to be passed as a string object like model="User" where User is the name of the model you are refering to
    """
    return eval(model).objects.all()

def object_remove(factor:dict,model:str):
    """
    factor is a dictionary {"email":"abc@ghmail.com"} < usage is here, arguments are supposed to be passed like this
    Model is supposed to be passed as a string object like model="User" where User is the name of the model you are refering to
    """

    return eval(model).objects.filter(**factor).delete()

