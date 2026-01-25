from django.db import models
from django.core.validators import RegexValidator
import uuid
import random

# Create your models here.


class Bank_branches(models.Model):
    def __str__(self):
        return f"{self.branch_name}-{self.branch_id}"
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)



class AccountNumber(models.Model):
    account_number = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(r'^\d{12}$', 'Account number must be exactly 12 digits.')
        ],
        unique=True
    )

    def __str__(self):
        return self.account_number

class Account(models.Model):
    account_choices = [
        ('current', 'Current'),
        ('savings', 'Savings')
    ]
    account_id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    account_type = models.CharField(max_length=10, choices=account_choices)
    balance = models.FloatField(default=0)
    account_number = models.ForeignKey(AccountNumber, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('account_number', 'account_type'),)

    def __str__(self):
        return f"{self.account_type} - {self.account_id}"


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60,null=False)
    phone_no = models.CharField(max_length=10,
                                    unique=True,
                                    validators=[
                                        RegexValidator(r'^\d{10}$')
                                    ],null=False)
    Aadhar_no = models.CharField(max_length=12,
                                    unique=True,
                                    validators=[
                                        RegexValidator(r'^\d{12}$')
                                    ],null=False)
    DOB = models.DateField()
    branch_connect = models.ForeignKey(Bank_branches,on_delete=models.CASCADE)
    account = models.OneToOneField(AccountNumber,on_delete = models.CASCADE)
    password = models.CharField(max_length = 128,null=True,blank=False,
                                validators=[
                                    RegexValidator(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)')
                                ])
    def __str__(self):
        return f"{self.name} - {self.account}"

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100,primary_key=True,editable=False)
    transaction_details = models.TextField(max_length=120)
    transaction_type = models.CharField(max_length=70)
    transaction_date = models.DateField()
    types = models.TextField(max_length=120,null=True)
    transaction_from = models.ForeignKey(AccountNumber,related_name='transactions_from',on_delete=models.CASCADE)
    transaction_to = models.ForeignKey(AccountNumber,related_name='transactions_to',null=True,on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        super(Transaction, self).save(*args, **kwargs)

    def generate_transaction_id(self):
        # Generate a unique ID using UUID
        return str(uuid.uuid4())
    def __str__(self):
        return f"{self.transaction_id} - {self.transaction_from}"
    

class loan(models.Model):
    plan_choices = [
        ('1-month/s[10%,1]','1-month/s[10%,1]'),
        ('36-month/s[8%,3]','36-month/s[8%,3]'),
        ('12-month/s[9%,1]','12-month/s[9%,1]'),
        ('24-month/s[8%,2]','24-month/s[8%,2]')
    ]
    
    loan_choices = [
        ('Personal', 'Personal'),
        ('Home', 'Home'),
        ('Car', 'Car'),
        ('Business', 'Business'),
        ('Education','Education')
    ]
    account = models.ForeignKey(AccountNumber,on_delete = models.CASCADE)
    loan_id = models.AutoField(primary_key=True)
    loan_refno = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(r'^\d{8}$', 'Account number must be exactly 8 digits.')
        ],
        unique=True
    )
    loan_type = models.CharField(max_length=100,null=False,choices = loan_choices)
    plan = models.CharField(max_length=100,null=False,choices = plan_choices)
    amount = models.FloatField()
    tp_amount = models.FloatField(null=True)
    m_amount = models.FloatField(null=True)
    penalty = models.FloatField(null=True)
    pay_amount = models.FloatField(null=True)
    due_date = models.DateField(null=True)
    date_applied = models.DateField(null=True)
    date_approved = models.DateField(null=True)
    date_released = models.DateField(null=True)
    date_rejected = models.DateField(null=True)
    loan_status = models.CharField(max_length=120)
    count = models.IntegerField(null=True)
    loan_desc = models.TextField(max_length=200,null=True)
    def __str__(self):
        return f"{self.loan_refno} - {self.loan_status}"

class loan_details(models.Model):
    account = models.ForeignKey(AccountNumber,on_delete = models.CASCADE)
    loan_details_id = models.AutoField(primary_key=True)
    loan_count = models.IntegerField()
    due_payments = models.IntegerField()
    penalties = models.IntegerField()
    
    def __str__(self):
        return f"{self.account.account_number} - {self.loan_count}"

    
    




# Create your models here.
