import uuid, json, requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.conf import settings
from .models import KhaltiTransaction

def khalti_payment_page(request):
    transaction_id = str(uuid.uuid4())
    amount_npr = 500
    amount_paisa = amount_npr * 100

    KhaltiTransaction.objects.create(
        transaction_id=transaction_id,
        product_name="UGrowit Fertilizer",
        amount=amount_paisa,
        status="PENDING"
    )

    return render(request, "khalti_payment/khalti_payment.html", {
        "amount": amount_npr,
        "product_name": "UGrowit Fertilizer",
        "transaction_id": transaction_id,
        "khalti_public_key": settings.KHALTI_PUBLIC_KEY,
    })

@csrf_exempt
def khalti_verify(request):
    if request.method == "POST":
        data = json.loads(request.body)
        token = data.get("token")
        amount = data.get("amount")

        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}"
        }

        response = requests.post(settings.KHALTI_VERIFY_URL, data={
            "token": token,
            "amount": amount
        }, headers=headers)

        resp_data = response.json()

        if response.status_code == 200:
            transaction_id = resp_data.get("product_identity")
            try:
                txn = KhaltiTransaction.objects.get(transaction_id=transaction_id)
                txn.status = "SUCCESS"
                txn.khalti_token = token
                txn.mobile = resp_data.get("mobile")
                txn.verified_at = now()
                txn.save()
                return JsonResponse({"success": True})
            except KhaltiTransaction.DoesNotExist:
                return JsonResponse({"success": False, "error": "Transaction not found"}, status=404)

        return JsonResponse({"success": False, "error": resp_data}, status=400)

def payment_success(request):
    return render(request, "khalti_payment/success.html")
