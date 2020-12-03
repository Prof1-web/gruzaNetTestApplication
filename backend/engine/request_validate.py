from flask import request
from engine.response import MakeResponse
import json


def validate(form):
    """ Validate request data by class. It's decorator """
    def wrapper(f):
        def decorator(*args, **kwargs):
            try:
                request_data = json.loads(request.data)
            except:
                return MakeResponse(status_code=400)

            # all class propertyies
            class_properties = vars(form)
            # class properties type. In format {property: type}
            class_annotations = class_properties["__annotations__"]
            request_data_for_func = {}

            for field in class_annotations:
                try:
                    if not field in class_properties or field in request_data:
                        # cast data to the required type
                        request_data_for_func.update({field: class_annotations[field](request_data[field])})
                    else:
                        request_data_for_func.update({field: class_properties[field]})
                except:
                    return MakeResponse(status_code=400)
            return f(request_data_for_func, *args, **kwargs)
        return decorator
    return wrapper
