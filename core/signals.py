from django.dispatch import receiver
from store.signals import order_create


@receiver(order_create)
def after_order_create(sender, **kwargs):
    print(f'New order created successfully! {kwargs["order"].id}')
