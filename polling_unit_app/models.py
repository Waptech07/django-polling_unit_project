from django.db import models

# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LGA(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    total_result = models.IntegerField(default=0)  # New field for the summed total result

class Ward(models.Model):
    name = models.CharField(max_length=100)
    lga = models.ForeignKey(LGA, on_delete=models.CASCADE)

class PollingUnit(models.Model):
    name = models.CharField(max_length=100)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)

class AnnouncedPUResult(models.Model):
    polling_unit = models.ForeignKey(PollingUnit, on_delete=models.CASCADE)
    result = models.IntegerField()

class Party(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return self.name