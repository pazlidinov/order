from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)    
    phone = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name + " " + self.surname)


class Course(models.Model):
    name = models.CharField(max_length=250)
    duration = models.CharField(max_length=250)
    times_in_week = models.IntegerField(default=0)
    time_of_lesson = models.TimeField()
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    info = models.TextField()

    def __str__(self):
        return str(self.name)


class Registration(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="customers"
    )
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="courses")
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return str(self.customer)
