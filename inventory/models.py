from django.contrib.auth.models import User
from django.db import models


STATUS_IN_STOCK = 'in_stock'
STATUS_OUT = 'out_of_stock'
STATUS_DAMAGED = 'damaged'

STATUS_CHOICES = [
    (STATUS_IN_STOCK, 'In Stock'),
    (STATUS_OUT, 'Out of Stock'),
    (STATUS_DAMAGED, 'Damaged'),
]


class LabItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    category = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_IN_STOCK)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ItemIssue(models.Model):
    item = models.ForeignKey(LabItem, on_delete=models.CASCADE, related_name="issues")
    student_name = models.CharField(max_length=120)
    taken_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-taken_at"]

    def __str__(self):
        return f"{self.item.name} - {self.student_name}"
