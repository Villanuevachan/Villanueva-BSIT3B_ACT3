from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Q
import json
from .models import Item


items = []

# Get all items
def get_items(request):
    return JsonResponse({"items": list(Item.objects.values())})

# Search items
def search_items(request):
    query = request.GET.get("search", "")
    filtered_items = Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return JsonResponse({"items": list(filtered_items.values())})

# Get single item
def get_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return JsonResponse({"id": item.id, "name": item.name, "description": item.description})

# Add a new item
@csrf_exempt
def add_item(request):
    if request.method == "POST":
        data = json.loads(request.body)
        item = Item.objects.create(name=data["name"], description=data.get("description", ""))
        return JsonResponse({"message": "Item added", "item": {"id": item.id, "name": item.name, "description": item.description}})

# Update an item
@csrf_exempt
def update_item(request, item_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        item = get_object_or_404(Item, id=item_id)
        item.name = data.get("name", item.name)
        item.description = data.get("description", item.description)
        item.save()
        return JsonResponse({"message": "Item updated", "item": {"id": item.id, "name": item.name, "description": item.description}})

# Delete an item
@csrf_exempt
def delete_item(request, item_id):
    if request.method == "DELETE":
        item = get_object_or_404(Item, id=item_id)
        item.delete()
        return JsonResponse({"message": "Item deleted"})
