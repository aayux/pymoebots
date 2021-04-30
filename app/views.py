from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os

import json
from pathlib import Path
from amoebot.simulator import AmoebotSimulator

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
    return [
        e.name for e in Path(STORE).iterdir() if e.is_dir() and e.name != "logs"
    ]


def _check_run_existence(run):
    for e in Path(STORE).iterdir():
        if e.is_dir() and e.name != "logs" and e.name == run:
            return True
    return False


def _empty_run_data(run):
    for e in (Path(STORE) / Path(run)).iterdir():
        if e.name != "init0.json":
            os.remove(e)


def _run_algorithm(algorithm, config_number, rounds=None):
    sim = AmoebotSimulator(
        max_rnds=rounds,
        config_num=config_number,
        algorithm=algorithm
    )
    sim.exec_sequential(time_it=True)


@csrf_exempt  # REMOVE EXEMPTION IF MOVING TO PRODUCTION.
def algorithms(request: object, run: str = None) -> object:
    if request.method == 'GET':
        if run:
            config0, tracks = _fetch_run(dir_name=run)
            response = dict(
                config0=config0,
                tracks=tracks
            )
            return JsonResponse(response)
        return JsonResponse(
            dict(Algorithms=_get_available_runs())
        )

    if request.method == 'POST':
        data = json.loads(request.body)
        algorithm_name = data.pop("algorithm")
        config_number = data.pop("name")
        rounds = 5000
        if "rounds" in data:
            rounds = data.pop("rounds")
        run_name = "run-" + config_number
        dir_path = Path(STORE) / Path(run_name)
        if _check_run_existence(run_name):
            _empty_run_data(run_name)
        else:
            os.mkdir(dir_path)

        with open(dir_path / Path('init0.json'), 'w') as json_file:
            json.dump(data, json_file)

        _run_algorithm(
            algorithm=algorithm_name, config_number=config_number, rounds=rounds
        )

        config0, tracks = _fetch_run(dir_name=run_name)
        response = dict(
            config0=config0,
            tracks=tracks
        )
        return JsonResponse(response)
