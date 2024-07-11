import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

# Now you can import your models and perform operations
from myapp.models import Product

# Define your models and other logic here
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Example usage or additional logic
if __name__ == "__main__":
    # Code to run when executing this script directly
    pass
