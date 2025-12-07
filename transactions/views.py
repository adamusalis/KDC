import requests
import time
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .serializers import PurchaseSerializer
from .models import Transaction
from services.models import DataPlan

# --- 1. BUY DATA (Simulation Mode) ---
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_data(request):
    serializer = PurchaseSerializer(data=request.data)
    if serializer.is_valid():
        plan_id = serializer.validated_data['plan_id']
        target_phone = serializer.validated_data['phone_number']
        user = request.user

        # Get Plan & Check Balance
        plan = get_object_or_404(DataPlan, id=plan_id)
        if user.wallet_balance < plan.price:
            return Response({"error": "Insufficient funds"}, status=400)

        # --- FAKE API SIMULATION ---
        # Tomorrow: You will replace this with the real API call
        try:
            time.sleep(1) # Pretend to wait for network
           
            # Pretend it was successful
            api_response = {"Status": "successful", "message": "Simulation Success"}
            status = 200

            if status == 200:
                with transaction.atomic():
                    user.wallet_balance -= plan.price
                    user.save()

                    Transaction.objects.create(
                        user=user,
                        plan=plan,
                        target_phone_number=target_phone,
                        amount=plan.price,
                        status='SUCCESS',
                        provider_response=str(api_response)
                    )

                return Response({
                    "message": "Data Sent Successfully! (SIMULATION)",
                    "new_balance": user.wallet_balance
                })
            else:
                return Response({"error": "Provider Failed"}, status=400)

        except Exception as e:
            return Response({"error": "Connection Error"}, status=500)

    return Response(serializer.errors, status=400)


# --- 2. FUND WALLET (Paystack) ---
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fund_wallet(request):
    reference = request.data.get('reference')
    if not reference:
        return Response({"error": "No reference provided"}, status=400)

    if Transaction.objects.filter(transaction_id=reference).exists():
        return Response({"error": "Transaction already processed"}, status=400)

    # REPLACE THIS WITH YOUR REAL SECRET KEY
    PAYSTACK_SECRET_KEY = "sk_test_e6ccbf96d256744588f1b02a9c2b94f43e5e221a"
   
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    url = f"https://api.paystack.co/transaction/verify/{reference}"
   
    try:
        response = requests.get(url, headers=headers)
        result = response.json()
       
        if result['status'] and result['data']['status'] == 'success':
            amount_kobo = result['data']['amount']
            amount_naira = amount_kobo / 100
           
            user = request.user
           
            with transaction.atomic():
                user.wallet_balance += request.user.wallet_balance.__class__(amount_naira)
                user.save()
               
                Transaction.objects.create(
                    user=user,
                    amount=amount_naira,
                    status='SUCCESS',
                    transaction_id=reference,
                    provider_response="Wallet Funded via Paystack",
                    target_phone_number=user.phone_number
                )
           
            return Response({"message": "Wallet Funded Successfully!", "new_balance": user.wallet_balance})
        else:
            return Response({"error": "Payment verification failed"}, status=400)

    except Exception as e:
        return Response({"error": "Could not verify transaction"}, status=500)