from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    rooms = list(Room.objects.values('id', 'title', 'x', 'y', 'n_to', 's_to', 'e_to', 'w_to'))
    players = room.playerNames(player_id)
    inventory = player.items_res()
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'inventory': inventory, 'x':room.x, 'y':room.y, 'players':players, 'rooms': rooms}, safe=True)

@csrf_exempt
@api_view(["GET"])
def players(request):
    user = request.user
    player = user.player
    player_id = player.id
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'players':players}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        
        for p_uuid in currentPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        for p_uuid in nextPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
            
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'x':nextRoom.x, 'y':nextRoom.y, 'players':players, 'error_msg':""}, safe=True)

    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    message = data['message']
    room = player.room()
    currentPlayerUUIDs = room.playerUUIDs(player_id)
    for p_uuid in currentPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} says "{message}"'})

    return JsonResponse({'name':player.user.username, 'title':room.title, 'message':message}, safe=True)


@csrf_exempt
@api_view(["POST"])
def get(request):
    player = request.user.player
    room = player.room()
    data = json.loads(request.body)
    item = data['item']
    try:
        item_taken = room.items.get(name=item)
    except Item.DoesNotExist:
        return JsonResponse({'error_msg':'That item does not exist'}, safe=True)

    message = player.get_item(item)
    inventory = player.items_res()
    room_items = room.items_res()
    return JsonResponse({'message': message, 'item': {"name": item_taken.name, "description": item_taken.description}, 'inventory': inventory, 'room_items': room_items, 'error_msg':""}, safe=True)


@csrf_exempt
@api_view(["POST"])
def drop(request):
    player = request.user.player
    room = player.room()
    data = json.loads(request.body)
    item = data['item']
    try:
        player.items.get(name=item)
    except Item.DoesNotExist:
        return JsonResponse({'error_msg':'You don\'t have that item!'}, safe=True)

    message = player.drop_item(item)
    inventory = player.items_res()
    room_items = room.items_res()
    return JsonResponse({'message': message, 'inventory': inventory, 'room_items': room_items, 'error_msg':""}, safe=True)

@csrf_exempt
@api_view(["GET"])
def inventory(request):
    player = request.user.player
    inventory = player.items_res()
    return JsonResponse({'inventory': inventory}, safe=True)

@csrf_exempt
@api_view(["GET"])
def look(request):
    player = request.user.player
    room = player.room()
    room_items = room.items_res()
    return JsonResponse({'room_items':room_items}, safe=True)