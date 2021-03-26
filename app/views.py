from django.http import JsonResponse
from django.shortcuts import render

import json
from pathlib import Path

# the hidden file dump
STORE = './.dumps'


def _fetch_run(dir_name: str) -> tuple:
    r"""
    """

    # complete path to the state files
    config0file = Path(STORE) / Path(dir_name) / Path('init0.json')
    tracks_file = Path(STORE) / Path(dir_name) / Path('tracks.json')

    with open(config0file, 'r') as f:
        config0 = json.load(f)

    with open(tracks_file, 'r') as f:
        tracks = json.load(f)

    return (config0, tracks)


def index(request: object):
    r""" render index page from template
    """
    return render(request=request, template_name='index.html', context=None)


def history(request: object, run: str) -> object:
    r"""
    """
    if request.method == 'GET':
        config0, tracks = _fetch_run(dir_name=run)
        response = dict(
            config0=config0,
            tracks=tracks
        )
        return JsonResponse(response)
    return JsonResponse(dict())

def _get_available_runs():
    return [e.name for e in Path(STORE).iterdir() if e.is_dir() and e.name != "logs"]

def algorithms(request: object) -> object:
    if request.method == 'GET':
        print(_get_available_runs())
        return JsonResponse(
            dict(Algorithms=_get_available_runs())
        )

