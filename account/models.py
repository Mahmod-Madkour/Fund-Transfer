### account/models.py

from django.core.exceptions import ValidationError
from django.db import models

import uuid


### Profiel 
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def clean(self):
        if self.balance < 0.0:
            raise ValidationError('Balance must be greater than or equal 0.0')
        
    def __str__(self):
        return self.name

### Transfer 
class Transfer(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='sender_transfers')
    receiver = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='receiver_transfers')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def clean(self):
        if self.amount < 0.0:
            raise ValidationError('Amount must be greater than 0.0')
        
    def __str__(self):
        return f"Transfer from {self.sender} to {self.receiver}"
