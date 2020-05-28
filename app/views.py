from .. amoebot.grid.trigrid import TriangularGrid
from .. amoebot.elements.node.manager import NodeManager
from .. amoebot.elements.bot.manager import AmoebotManager
from .. amoebot.functional.tracker import StateTracker

from django.http import JsonResponse
from django.shortcuts import render

def simulator():
    # asynchronously simulate the algorithm
    return

def index(request):
    # render page from template
    return

def history(request):
    if request.method == 'GET':
        response = simulator()
        return JsonResponse(response)