from __future__ import absolute_import

import json
import uuid

from kombu.serialization import register


class CustomJSONEncoder(json.JSONEncoder):
    """
    Handles encoding of objects of type:
        - <class 'speaklater._LazyString'>
    """
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def custom_decoder(obj):
    # Add custom decoding here.
    return obj


def custom_dumps(obj):
    return json.dumps(obj, cls=CustomJSONEncoder)


def custom_loads(obj):
    return json.loads(obj.decode('utf8'), object_hook=custom_decoder)


# Register custom JSON encoder and decoder to kombu serialization registry
def register_kombu_custom_serializer():
    register(
        'customjson',
        custom_dumps,
        custom_loads,
        content_type='application/x-customjson',
        content_encoding='utf-8'
    )
