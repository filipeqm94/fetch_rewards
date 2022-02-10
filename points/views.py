import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, Transaction

# Create your views here.
# decorator to bypass the neccessity for the csrf token
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

    transaction = Transaction(
        payer=customer, points=data["points"], timestamp=data["timestamp"]
    )
    transaction.save()

    data = {"detail": "transaction created"}

    return JsonResponse(data)


# decorator to bypass the neccessity for the csrf token
@csrf_exempt
def spend(request):
    data = json.loads(request.body)
    points = data["points"]

    # get transactions ordered by date
    transactions = list(Transaction.objects.all().order_by("timestamp"))
    # this list will hold the customer affected by the spend call
    customers = []

    # deduct points
    for transaction in transactions:
        # points are 0 or below break out
        if points <= 0:
            break
        # subtract transaction points
        points = points - transaction.points
        # set deduceted points to always be a positive integer
        deducted_points = transaction.points if points > 0 else transaction.points + points

        # get customer related to the transaction
        customer = Customer.objects.get(pk=transaction.payer.pk)
        # update customer points
        customer.points -= deducted_points
        # save changes
        customer.save()

        # in order to create a list with only unique customers
        if customer not in customers:
            # set customer points to be the amount subtracted
            # determined by the transactions
            customer.points = deducted_points
            # add unique customer to the list
            customers.append(customer)
        else:
            # if customer was already on the list, add transaction points to the deducted points
            customers[customers.index(customer)].points += deducted_points

    # create response
    # iterate through customers list creating a new list
    # with the amount of points deducted from each customer
    response = [{"payer": c.name, "points": -c.points} for c in customers]

    return JsonResponse(response, safe=False)


def balances(request):
    # get a list of all customers
    customers = list(Customer.objects.all())
    response = {}
    for customer in customers:
        # for each customer in the list,
        # add a "customer.name" key and assign "customer.points" as value
        response[customer.name] = customer.points

    return JsonResponse(response)
