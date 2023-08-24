from django.db import models
from django.contrib.auth.models import AbstractUser,User

# Create your models here.
class Ward(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class KCBMSUser(AbstractUser):
    is_ward_admin = models.BooleanField(default=False)
    is_edu_admin = models.BooleanField(default=False)
    is_accountant = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(KCBMSUser,on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward,on_delete=models.DO_NOTHING,blank=True,null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class FinancialYear(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField()

    def __str__(self):
        return self.name
    
class Allocation(models.Model):
    ward = models.ForeignKey(Ward,on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear,on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.ward.name} ward's {self.financial_year.name}'s allocation"

class Application(models.Model):
    GENDER_CHOICES = (
        ('f','Female'),
        ('m','Male'),
    )
    FAMILY_STATUS_CHOICES = (
        ('o','Orphan'),
        ('s','Single Parents'),
        ('b','Both Parents')
    )
    SCHOOL_TYPE_CHOICES = (
        ('p','Primary School'),
        ('s','Secondary School'),
        ('t','Tertiary School')
    )
    full_name = models.CharField(max_length=100)
    birth_cert_no = models.CharField(max_length=100)
    admission_no = models.CharField(max_length=100)
    ward = models.ForeignKey(Ward,on_delete=models.CASCADE)
    gender = models.CharField(max_length=2,choices=GENDER_CHOICES)
    disability_status = models.BooleanField(default=False)
    family_status = models.CharField(max_length=2,choices=FAMILY_STATUS_CHOICES)
    institution = models.CharField(max_length=100)
    school_type = models.CharField(max_length=100,choices=SCHOOL_TYPE_CHOICES)
    bank = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    financial_year = models.ForeignKey(FinancialYear,on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name