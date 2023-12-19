from django.db import models

# Create your models here.
#Location
class AdministrativeRegion(models.Model):
    name = models.CharField(max_length=100)

class AdministrativeUnit(models.Model):
    name = models.CharField(max_length=100)

class Province(models.Model):
    models.ForeignKey(AdministrativeRegion, on_delete=models.CASCADE)
    models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)
    
class District(models.Model):
    models.ForeignKey(Province, on_delete=models.CASCADE)
    models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)

class Ward(models.Model):
    models.ForeignKey(District, on_delete=models.CASCADE)
    models.ForeignKey(AdministrativeUnit, on_delete=models.CASCADE)

class Location(models.Model):
    models.ForeignKey(Ward, on_delete=models.CASCADE)

#Cabinet
class Controller(models.Model):
    models.ForeignKey(Location, on_delete=models.CASCADE)

class CabinetType(models.Model):
    type = models.CharField(max_length=100)

class CostVersion(models.Model):
    version = models.CharField(max_length=100)

class Campaign(models.Model):
    models.ForeignKey(CostVersion, on_delete=models.CASCADE)

class Cabinet(models.Model):
    models.ForeignKey(Controller, on_delete=models.CASCADE)
    models.ForeignKey(CabinetType, on_delete=models.CASCADE)

class CampaignCabinet(models.Model):
    models.ForeignKey(Campaign, on_delete=models.CASCADE)
    models.ForeignKey(Cabinet, on_delete=models.CASCADE)

class Cell(models.Model):
    models.ForeignKey(Cabinet, on_delete=models.CASCADE)

class CellLog(models.Model):
    models.ForeignKey(Cell, on_delete=models.CASCADE)

class User(models.Model):
    username = models.CharField(max_length=100)

class Order(models.Model):
    orderId = models.CharField(max_length=100)

class OrderDetail(models.Model):
    models.ForeignKey(Cell, on_delete=models.CASCADE)
    models.ForeignKey(User, on_delete=models.CASCADE)
    models.ForeignKey(Order, on_delete=models.CASCADE)


