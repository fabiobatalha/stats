# coding: utf-8

def tqx_dict(data):
    """
    Transform tqx string in a key, value dictionary.
    input: tqx=qId:0;out:csv
    output: {'reqId': 0, 'out': 'csv'}
    """

    return {k:v for k, v in [i.split(':') for i in data.split(';') if i]}
