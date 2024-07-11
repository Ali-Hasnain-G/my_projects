from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from django.utils import timezone

@receiver(post_save, sender=Product)
def update_created_at(sender, instance, created, **kwargs):
    if created:
        instance.created_at = timezone.now()
        instance.save()
