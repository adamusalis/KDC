from django.db import models
from django.conf import settings
from services.models import DataPlan
import uuid

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    plan = models.ForeignKey(DataPlan, on_delete=models.SET_NULL, null=True, blank=True)
   
    # We store the phone number they sent data TO (might be different from their own)
    target_phone_number = models.CharField(max_length=15)
   
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
   
    # Unique ID for tracking (useful for support tickets)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
   
    # API response from the provider (e.g., "Transaction Successful ID: 5544")
    provider_response = models.TextField(blank=True, null=True)
   
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate a unique ID if one doesn't exist
        if not self.transaction_id:
            self.transaction_id = str(uuid.uuid4()).replace('-', '')[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status}"