from bson import ObjectId
import re

# Library for converting between python and javascript data objects.

def serialize(obj, key = None):
    # Return an object if it is simple; otherwise recursively iterate through.
    if (type(obj) is list): # Loop through the elements.
        new_list = []
        for el in obj:
            new_list.append(serialize(el))
        return new_list
    elif (type(obj) is dict): # Loop through the key, value pairs
        new_dict = {}
        for k, v in obj.items():
            new_dict[snake_to_camel(k)] = serialize(v, key = k)
        return new_dict
    else : # Check to see if the bare object needs special processing.
        if (type(obj) is ObjectId) and (re.search(r'(_id)', key)):
            # Convert the ObjectID to a string so we can push through JSON.
            return str(obj)
        else:
            return obj
        # if isinstance(obj, np.generic):
        #     return np.asscalar(obj)



def deserialize(obj, key = None):
    # Return an object if it is simple; otherwise recursively iterate through.
    if (type(obj) is list):
        new_list = []
        for el in obj:
            new_list.append(deserialize(el))
        return new_list
    elif (type(obj) is dict):
        new_dict = {}
        for k, v in obj.items():
            nk = camel_to_snake(k)
            new_dict[nk] = deserialize(v, key = nk)
        return new_dict
    else:
        if (type(obj) is str) and (re.search(r'(_id)', key)):
            # Convert to an ObjectID for use in Mongo!
            return ObjectId(obj)
        else:
            return obj


# Functions for preserving naming conventions in the separate languages.
def camel_to_snake(camel):
    # Convert camelCase to snake_case.
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def snake_to_camel(snake):
    # Convert snake_case to camelCase.
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), snake)
