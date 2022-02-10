import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Transaction

"""
{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
{ "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }
{ "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }
{ "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
{ "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }

{ "points": 5000 }
"""

# Create your views here.


@csrf_exempt
def transaction(request):
    data = json.loads(request.body)

    # create customer if does not exist
    is_customer = Customer.objects.filter(name=data["payer"]).exists()
    if not is_customer:
        new_customer = Customer(name=data["payer"])
        new_customer.save()
        print("New Customer >", new_customer)

    # get newly created or existing customer
    customer = Customer.objects.get(name=data["payer"])
    # add points to customer
    customer.points += data["points"]
    # save changes made to customer
    customer.save()

    transaction = Transaction(payer=customer, points=data["points"])
    transaction.save()

    data = {"detail": "transaction created"}

    return JsonResponse(data)


def spend(request):
    data = {"hello": "spend"}

    return JsonResponse(data)


def balances(request):
    # get a list of all customers
    customers = list(Customer.objects.all())
    data = {}
    for customer in customers:
        # for each customer in the list,
        # add a "customer.name" key and assign "customer.points" as value
        data[customer.name] = customer.points

    return JsonResponse(data)
