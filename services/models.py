from django.db import models

class Network(models.Model):
    name = models.CharField(max_length=20) # e.g., MTN, Airtel
    status = models.BooleanField(default=True) # Turn off if network is down

    def __str__(self):
        return self.name

class DataPlan(models.Model):
    PLAN_TYPES = (
        ('SME', 'SME'),
        ('GIFTING', 'Gifting'),
        ('CORPORATE', 'Corporate'),
    )

    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, default='SME')
    name = models.CharField(max_length=50) # e.g., 1GB SME Data
    price = models.DecimalField(max_digits=10, decimal_places=2) # Your selling price
   
    # This ID is critical for connecting to API providers later
    plan_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.network} - {self.name} (N{self.price})"