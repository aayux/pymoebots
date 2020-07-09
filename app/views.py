from django.http import JsonResponse
from django.shortcuts import render

import json
from pathlib import Path

def _fetch_run(filename:str) -> tuple:
    r"""
    """
    # the hidden file dump
    store = './.dumps'
    
    filename = f'{filename}.json'

    # complete path to the state files
    config0file = Path(store) / Path('init0') / Path(filename)
    tracks_file = Path(store) / Path('tracks') / Path(filename)

    with open(config0file, 'r') as f:
        config0 = json.load(f)

    with open(tracks_file, 'r') as f:
        tracks = json.load(f)

    return (config0, tracks)

def index(request:object):
    r""" render index page from template
    """
    return render(request=request, template_name='index.html', context=None)

def history(request:object, run:str) -> object:
    r"""
    """
    if request.method == 'GET':
        init0, tracks = _fetch_run(run)
        response = dict(
                        init0=init0,
                        tracks=tracks
                    )
        return JsonResponse(response)
    return JsonResponse(dict())