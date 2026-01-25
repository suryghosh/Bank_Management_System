from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Q,F
from .models import Bank_branches,AccountNumber,Transaction,Customer,Account,loan,loan_details
import random
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import re
from django.core.exceptions import ObjectDoesNotExist


def get_loan_details(account):
    try:
        details = loan_details.objects.get(account=account)
        return details
    except loan_details.DoesNotExist:
        return None


def months_between(start_date, end_date):
    # Calculate year difference in months
    year_diff = (end_date.year - start_date.year) * 12
    # Calculate the difference in months
    month_diff = end_date.month - start_date.month
    # Combine year and month difference
    total_months = year_diff + month_diff
    # Handle day comparison: subtract one month if end date day is earlier than start date day
    if end_date.day < start_date.day:
        total_months -= 1
    return total_months
def get_plan_values(str):
    match = re.match(r"(\d+)-month/s\[(\d+)%?,(\d+)\]", str)
    if match:
        months = int(match.group(1))  # 36
        interest = int(match.group(2))  # 10
        freq_of_payment_month = int(match.group(3))  # 1
    
    # Creating the dictionary
    plan_details = {
        "months": months,
        "interest": interest,
        "freq_of_payment_month": freq_of_payment_month
    }
    
    return plan_details


# Create your views here.
generated_numbers = set()


def gen_12_digit_number():
    random_number = random.randint(100000000000,999999999999)
    if  random_number not in generated_numbers:
        generated_numbers.add(random_number)
        return random_number
    
def gen_8_digit_number():
    random_number = random.randint(10000000,99999999)
    if  random_number not in generated_numbers:
        generated_numbers.add(random_number)
        return random_number

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def starting_page(request):
    return render(request,'myapp/startingPage.html')



# Create your views here.
def CreatePage(request):
    branches = Bank_branches.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        #to check if phone number present in database or not
        if phone_no:
            all_customers = Customer.objects.all()
            for i in all_customers:
                if i.phone_no == phone_no:
                    error = "phone_num"
                    return render(request,'myapp/error.html',{'error':error})

def get_loan_details(account):
    try:
        details = loan_details.objects.get(account=account)
        return details
    except loan_details.DoesNotExist:
        return None

def months_between(start_date, end_date):
    year_diff = (end_date.year - start_date.year) * 12
    month_diff = end_date.month - start_date.month
    total_months = year_diff + month_diff
    if end_date.day < start_date.day:
        total_months -= 1
    return total_months

def get_plan_values(plan):
    match = re.match(r"(\d+)-month/s\[(\d+)%?,(\d+)\]", plan)
    if match:
        months = int(match.group(1))
        interest = int(match.group(2))
        freq_of_payment_month = int(match.group(3))

    plan_details = {
        "months": months,
        "interest": interest,
        "freq_of_payment_month": freq_of_payment_month
    }

    return plan_details

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def gen_12_digit_number():
    random_number = random.randint(100000000000, 999999999999)
    if random_number not in generated_numbers:
        generated_numbers.add(random_number)
        return random_number

def gen_8_digit_number():
    random_number = random.randint(10000000, 99999999)
    if random_number not in generated_numbers:
        generated_numbers.add(random_number)
        return random_number

def loan_score(base_pay, loan_count, due_payments, penalties):
    loan_score = base_pay - (loan_count * 10) - (due_payments * 40) - (penalties * 30)
    return max(0, min(loan_score, 100))

def starting_page(request):
    return render(request, 'myapp/startingPage.html')

def CreatePage(request):
    branches = Bank_branches.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        if phone_no:
            all_customers = Customer.objects.all()
            for i in all_customers:
                if i.phone_no == phone_no:
                    error = "phone_num"
                    return render(request, 'myapp/error.html', {'error': error})

        aadhar_no = request.POST.get('Aadhar_no')
        if aadhar_no:
            all_customers = Customer.objects.all()
            for i in all_customers:
                if i.Aadhar_no == aadhar_no:
                    error = "aadhar_num"
                    return render(request, 'myapp/error.html', {'error': error})

        DOB = request.POST.get('DOB')
        if DOB:
            dob = datetime.strptime(DOB, '%Y-%m-%d').date()
            age = calculate_age(dob)
            if age < 18:
                error_message = 'You must be at least 18 years old to open a account.'
                return render(request, 'myapp/error.html', {'error_message': error_message})

        branch_id = request.POST.get('branch')
        password = request.POST.get('password')
        Account_number = gen_12_digit_number()

        branch = Bank_branches.objects.get(branch_id=branch_id)
        accountNumber = AccountNumber(account_number=Account_number)
        customer = Customer(name=name, phone_no=phone_no, Aadhar_no=aadhar_no, DOB=DOB, branch_connect=branch, password=password, account=accountNumber)
        account_current = Account(account_type='current', account_number=accountNumber)
        account_savings = Account(account_type='savings', account_number=accountNumber)
        accountNumber.save()
        customer.save()
        account_current.save()
        account_savings.save()
        return redirect(f'/accountNumber/{Account_number}')

    return render(request, 'myapp/CreatePage.html', {'branches': branches})

def showAccountNum(request, account_num):
    account = AccountNumber.objects.get(account_number=account_num)
    customer = Customer.objects.get(account=account)
    return render(request, 'myapp/accountNum.html', {'customer': customer})

def mainPage(request, customer_id):
    customer = Customer.objects.get(customer_id=customer_id)
    account = Account.objects.get(account_number=customer.account, account_type='savings')
    details = loan.objects.filter(account=customer.account)
    person_details = get_loan_details(customer.account)
    if person_details is None:
        details_person = loan_details(account=customer.account, loan_count=0, due_payments=0, penalties=0)
        details_person.save()
        score = loan_score(100, details_person.loan_count, details_person.due_payments, details_person.penalties)
    p_details = loan_details.objects.get(account=customer.account)
    score = loan_score(100, p_details.loan_count, p_details.due_payments, p_details.penalties)
    counts = {'count_approved': 0, 'count_released': 0, 'count_pending': 0, 'count_rejected': 0}
    for i in details:
        if i.loan_status == 'approved':
            counts['count_approved'] += 1
        elif i.loan_status == 'rejected':
            counts['count_rejected'] += 1
        elif i.loan_status == 'pending':
            counts['count_pending'] += 1
        elif i.loan_status == 'released':
            counts['count_released'] += 1
    return render(request, 'myapp/main.html', {'customer': customer, 'account': account, 'counts': counts, 'score': score})

def loginPage(request):
    allcustomer = Customer.objects.all()
    context = {}
    if request.method == 'POST':
        username = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        aadhar_no = request.POST.get('Aadhar_no')
        password = request.POST.get('password')
        for customer in allcustomer:
            if customer.name == username and customer.phone_no == phone_no and customer.Aadhar_no == aadhar_no and customer.password == password:
                return redirect(f'/main/{customer.customer_id}')
        context['invalid_credentials'] = True

    return render(request, 'myapp/loginpage.html', context)

def checkBalance(request, account_no):
    account = AccountNumber.objects.get(account_number=account_no)
    customer = Customer.objects.get(account=account)
    account_details_current = Account.objects.get(account_number=account, account_type='current')
    account_details_savings = Account.objects.get(account_number=account, account_type='savings')
    return render(request,'myapp/checkbalance.html',{'customer':customer,'account_current':account_details_current,'account_savings':account_details_savings})

#showing account number page
def showAccountNum(request, account_num):
    account = AccountNumber.objects.get(account_number=account_num)
    customer = Customer.objects.get(account = account)
    return render(request,'myapp/accountNum.html',{'customer':customer})

def mainPage(request,customer_id):
    customer = Customer.objects.get(customer_id=customer_id)
    account = Account.objects.get(account_number = customer.account,account_type='savings')
    details = loan.objects.filter(account=customer.account)
    person_details = get_loan_details(customer.account)
    if person_details == None:
        details_person = loan_details(account=customer.account,loan_count = 0,due_payments = 0,penalties = 0)
        details_person.save()
        score = loan_score(100,details_person.loan_count,details_person.due_payments,details_person.penalties)
    p_details = loan_details.objects.get(account=customer.account)
    score = loan_score(100,p_details.loan_count,p_details.due_payments,p_details.penalties)
    counts = {'count_approved':0,'count_released':0,'count_pending':0,'count_rejected':0}
    for i in details:
        if i.loan_status == 'approved':
            counts['count_approved']+=1
        elif i.loan_status == 'rejected':
            counts['count_rejected']+=1
        elif i.loan_status == 'pending':
            counts['count_pending']+=1
        elif i.loan_status == 'released':
            counts['count_released']+=1
    return render(request,'myapp/main.html',{'customer':customer,'account':account,'counts':counts,'score':score})

def loginPage(request):
    allcustomer = Customer.objects.all()
    context = {}
    if request.method=='POST':
        username = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        aadhar_no = request.POST.get('Aadhar_no')
        password = request.POST.get('password')
        for customer in allcustomer:
            if customer.name == username and customer.phone_no == phone_no and customer.Aadhar_no ==aadhar_no and customer.password == password:
                return redirect(f'/main/{customer.customer_id}')
        context['invalid_credentials'] = True 
                
        
    return render(request,'myapp/loginpage.html',context)

def checkBalance(request,account_no):
    account = AccountNumber.objects.get(account_number=account_no)
    customer = Customer.objects.get(account = account)
    account_details_current = Account.objects.get(account_number=account,account_type='current')
    account_details_savings = Account.objects.get(account_number=account,account_type='savings')
    return render(request,'myapp/checkbalance.html',{'customer':customer,'account_current':account_details_current,'account_savings':account_details_savings})

def deposit(request,account_no):
    account = AccountNumber.objects.get(account_number=account_no)
    customer = Customer.objects.get(account = account)
    account_details_current = Account.objects.get(account_number=account,account_type='current')
    account_details_savings = Account.objects.get(account_number=account,account_type='savings')
    if request.method == 'POST':
        amount = request.POST.get('deposit')
        account_type = request.POST.get('type')
        if account_type == 'savings':
            account_details_savings.balance += float(amount)
            account_details_savings.save()
            transaction = Transaction(transaction_details = "successfully deposited rs"+amount,transaction_type='success',transaction_date=date.today(),transaction_from=account,transaction_to=None,types = "savings")
            transaction.save()
            return redirect(f'/main/{customer.customer_id}?success=true')
        
            
        account_details_current.balance += float(amount)
        account_details_current.save()
        transaction = Transaction(transaction_details = "successfully deposited rs"+amount,transaction_type='success',transaction_date=date.today(),transaction_from=account,transaction_to=None,types="current")
        transaction.save()
        return redirect(f'/main/{customer.customer_id}?success=true')
    return render(request,'myapp/deposit.html',{'customer':customer,'account_current':account_details_current,'account_savings':account_details_savings})

def upi(request,account_no):
    account = AccountNumber.objects.get(account_number=account_no)
    customer = Customer.objects.get(account = account)
    account_details_current = Account.objects.get(account_number=account,account_type='current')
    account_details_savings = Account.objects.get(account_number=account,account_type='savings')
    customers = Customer.objects.all()
    context1 = {'transaction':None}
    if request.method == 'POST':
        account_type_from = request.POST.get('type_from')
        account_type_to = request.POST.get('type_to')
        account_num = request.POST.get('account_no')
        amount = request.POST.get('transact')
        
        if account_num == account_no:
            transaction = Transaction(transaction_details = "invalid transaction",transaction_type='failed',transaction_date=date.today(),transaction_from=account,transaction_to=account,types=None)
            transaction.save()
            return render(request,'myapp/upi.html',{'customer':customer,'account_current':account_details_current,'transaction':'same'})
        for i in customers:
            if i.account.account_number == account_num:
                account_to = AccountNumber.objects.get(account_number=account_num)
                if account_type_from == 'savings':
                    if account_details_savings.balance - float(amount)<0:
                        transaction = Transaction(transaction_details = "insufficient funds tried to transact amount:"+ amount,transaction_type='failed',transaction_date=date.today(),transaction_from=account,transaction_to=account_to,types="savings")
                        transaction.save()
                        return render(request,'myapp/upi.html',{'customer':customer,'account_savings':account_details_savings,'transaction':'failed'})
                    else:
                        if account_type_to == 'savings':
                            account_details_to_savings = Account.objects.get(account_number = account_to,account_type = 'savings')
                            customer_to = Customer.objects.get(account = account_to)
                            account_details_savings.balance -= float(amount)
                            account_details_to_savings.balance += float(amount)
                            account_details_savings.save()
                            account_details_to_savings.save()
                            transaction = Transaction(transaction_details = "successfully transfered amount:"+ amount,transaction_type='success',transaction_date=date.today(),transaction_from=account,transaction_to=account_to,types="savings -> savings")
                            transaction.save()
                            return render(request,'myapp/upi.html',{'customer':customer,'account_savings':account_details_savings,'customer_to':customer_to,'account_details_to_savings':account_details_to_savings,'transaction':'pass'})
                        else:
                            account_details_to_current = Account.objects.get(account_number = account_to,account_type = 'current')
                            customer_to = Customer.objects.get(account = account_to)
                            account_details_savings.balance -= float(amount)
                            account_details_to_current.balance += float(amount)
                            account_details_savings.save()
                            account_details_to_current.save()
                            transaction = Transaction(transaction_details = "successfully transfered amount:" + amount,transaction_type='success',transaction_date=date.today(),transaction_from=account,transaction_to=account_to,types="savings -> current")
                            transaction.save()
                            return render(request,'myapp/upi.html',{'customer':customer,'account_savings':account_details_savings,'customer_to':customer_to,'account_details_to_current':account_details_to_current,'transaction':'pass'})
                else:
                    if account_details_current.balance - float(amount)<0:
                        transaction = Transaction(transaction_details = "insufficient funds tried to transact amount:"+ amount,transaction_type='failed',transaction_date=date.today(),transaction_from=account,transaction_to=account_to,types="current")
                        transaction.save()
                        return render(request,'myapp/upi.html',{'customer':customer,'account_current':account_details_current,'transaction':'failed'})
                    else:
                        if account_type_to == 'savings':
                            account_details_to_savings = Account.objects.get(account_number = account_to,account_type = 'savings')
                            customer_to = Customer.objects.get(account = account_to)
                            account_details_current.balance -= float(amount)
                            account_details_to_savings.balance += float(amount)
                            account_details_current.save()
                            account_details_to_savings.save()
                            transaction = Transaction(transaction_details = "successfully transfered amount:"+ amount,transaction_type='success',transaction_date=date.today(),transaction_from=account,transaction_to=account_to,types="current -> savings")
                            transaction.save()
                            return render(request,'myapp/upi.html',{'customer':customer,'account_current':account_details_current,'customer_to':customer_to,'account_details_to_savings':account_details_to_savings,'transaction':'pass'})
                        else:
                            account_details_to_current = Account.objects.get(account_number = account_to,account_type = 'current')
                            customer_to = Customer.objects.get(account = account_to)
                            account_details_current.balance -= float(amount)
                            account_details_to_current.balance += float(amount)
                            account_details_current.save()
                            account_details_to_current.save()
                            transaction = Transaction(transaction_details = "successfully transfered amount:"+ amount,transaction_type='success',transaction_date=date.today(),transaction_from=account,transaction_to=account_to,types="current -> current")
                            transaction.save()
                            return render(request,'myapp/upi.html',{'customer':customer,'account_current':account_details_current,'customer_to':customer_to,'account_details_to_current':account_details_to_current,'transaction':'pass'})
                    
        transaction = Transaction(transaction_details = "transferring amount to invalid account",transaction_type='failed',transaction_date=date.today(),transaction_from=account,transaction_to=None,types = None)
        transaction.save()
        return render(request,'myapp/upi.html',{'customer':customer,'account':account_details_current,'transaction':'noAccountAvail'})
    return render(request,'myapp/upi.html',{'customer':customer,'account':account_details_current})

    
def transaction(request,account_no):
    account = AccountNumber.objects.get(account_number=account_no)
    customer = Customer.objects.get(account=account)
    account_details_current = Account.objects.get(account_number=account,account_type='current')
    account_details_savings = Account.objects.get(account_number=account,account_type='savings')
    customers = Customer.objects.all()
    Transactions = Transaction.objects.all()
    combined_transactions = Transaction.objects.filter(
    Q(transaction_from=account) | Q(transaction_to=account))
    dict = {}   
    for i in customers:
        dict[i.account.account_number] = i.name
    return render(request,'myapp/transaction.html',{'com_trans':combined_transactions,'customer':customer,'map':dict,'account_current':account_details_current})

def update(request,account_no):
    branches = Bank_branches.objects.all()
    account = AccountNumber.objects.get(account_number = account_no)
    account_type_current = Account.objects.get(account_number=account,account_type='current') 
    customer = Customer.objects.get(account=account)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        #to check if phone number present in database or not
        if phone_no:
            all_customers = Customer.objects.all()
            for i in all_customers:
                if phone_no != customer.phone_no and i.phone_no == phone_no:
                    error = "phone_num"
                    return render(request,'myapp/update.html',{'error':error,'customer':customer,'account':account_type_current})
                
        aadhar_no = request.POST.get('Aadhar_no')
        #to check if aadhar number present in database or not
        if aadhar_no:
            all_customers = Customer.objects.all()
            for i in all_customers:
                if aadhar_no != customer.Aadhar_no and i.Aadhar_no == aadhar_no:
                    error = "aadhar_num"
                    return render(request,'myapp/update.html',{'error':error,'customer':customer,'account':account_type_current})
        
        branch_id = request.POST.get('branch')
        password = request.POST.get('password')
        branch = Bank_branches.objects.get(branch_id=branch_id)
        customer1 = Customer(name=name,phone_no=phone_no,Aadhar_no=aadhar_no,branch_connect = branch,password=password,DOB=customer.DOB,account=customer.account,customer_id=customer.customer_id)
        customer1.save()
        error = 'saved'
        return render(request,'myapp/update.html',{'error':error,'customer':customer,'account':account_type_current})
        
    return render(request,'myapp/update.html',{'customer':customer,'branches':branches,'account':account_type_current})

def delete(request,account_no):
    account = AccountNumber.objects.get(account_number = account_no)
    account_type_current = Account.objects.get(account_number=account,account_type='current') 
    customer = Customer.objects.get(account=account)
    if request.method == 'POST':
        account.delete()
        message = 'account deleted successfully'
        return render(request,'myapp/startingPage.html',{'message':message})
    
    return render(request,'myapp/delete.html',{'customer':customer,'account':account_type_current})

def bill_payments(request,account_no):
    account = AccountNumber.objects.get(account_number = account_no)
    account_details_current = Account.objects.get(account_number=account,account_type='current')
    account_details_savings = Account.objects.get(account_number=account,account_type='savings')
    customer = Customer.objects.get(account=account)
    if request.method == 'POST':
        payment_to = request.POST.get('pay_class')
        account_type = request.POST.get('type')
        amount = request.POST.get('deposit')
        
        if account_type == 'savings':
            if account_details_savings.balance - float(amount)<0:
                transaction = Transaction(transaction_details = "insufficient funds tried to transact amount: "+ amount + " for " + payment_to,transaction_type='failed',transaction_date=date.today(),transaction_from=account,transaction_to=None,types="savings")
                transaction.save()
                return render(request,'myapp/billpayments.html',{'customer':customer,'account_savings':account_details_savings,'transaction':'failed'})
            else:
                account_details_savings.balance -= float(amount) 
                account_details_savings.save()
                transaction = Transaction(transaction_details = "successfully transfered amount: " + amount + " for " + payment_to,transaction_type='success',transaction_date=date.today(),transaction_from=account,transaction_to=None,types="savings -> " + payment_to)
                transaction.save()
                return render(request,'myapp/billpayments.html',{'customer':customer,'account_savings':account_details_savings,'transaction':'pass','payment_to':payment_to})
        else:
            if account_details_current.balance - float(amount)<0:
                transaction = Transaction(transaction_details = "insufficient funds tried to transact amount: "+ amount + " for " + payment_to,transaction_type='failed',transaction_date=date.today(),transaction_from=account,transaction_to=None,types="current")
                transaction.save()
                return render(request,'myapp/billpayments.html',{'customer':customer,'account_current':account_details_current,'transaction':'failed'})
            else:
                account_details_current.balance -= float(amount) 
                account_details_current.save()
                transaction = Transaction(transaction_details = "successfully transfered amount: "+ amount + " for " + payment_to,transaction_type='success',transaction_date=date.today(),transaction_from=account,transaction_to=None,types="current -> "+payment_to)
                transaction.save()
                return render(request,'myapp/billpayments.html',{'customer':customer,'account_current':account_details_current,'transaction':'pass','payment_to':payment_to})
                          
    return render(request,'myapp/billpayments.html',{'customer':customer})

def loan_score(base_pay,loan_count,due_payments,penalties):
    loan_score = base_pay - (loan_count*10) - (due_payments*40) - (penalties*30)
    return max(0,min(loan_score,100))
    

def loan_given(request,account_no):
    account = AccountNumber.objects.get(account_number = account_no)
    customer = Customer.objects.get(account = account)
    account_details_savings = Account.objects.get(account_number = account,account_type='savings')
    person_details = get_loan_details(account)
    transaction=""
    if person_details == None:
        details_person = loan_details(account=account,loan_count = 0,due_payments = 0,penalties = 0)
        details_person.save()
    
    else:
        details = loan_details.objects.get(account=account)
        score = loan_score(100,details.loan_count,details.due_payments,details.penalties)
        if request.method == 'POST':
            loan_type = request.POST.get('loan_type')
            desc = request.POST.get('text')
            plan_type = request.POST.get('plan')
            amount = request.POST.get('loan_amount')
            ref_no = gen_8_digit_number()
            plan_details = get_plan_values(plan_type)
            
            
            #conditions
            if score>70 and details.loan_count<5:
               tp_amount = int(int(amount) * (1+(int(plan_details['interest'])*(int(plan_details['months'])/12))/100))
               m_amount = int(tp_amount/int(plan_details['months']))
               penalty = int(0.05*m_amount)
               due_date = datetime.now()+relativedelta(months = int(plan_details['freq_of_payment_month']))
               loan_taken = loan(account=account,loan_refno = ref_no,loan_type=loan_type,plan=plan_type,amount=amount,date_applied = date.today(),date_approved=date.today(),date_released=None,date_rejected=None,loan_status = 'approved',loan_desc=desc,tp_amount=tp_amount,m_amount=m_amount,penalty=penalty,due_date=due_date,pay_amount=m_amount,count=int((plan_details['months'])/(plan_details['freq_of_payment_month'])))
               transaction='success'
               account_details_savings.balance +=float(amount)
               loan_details.objects.filter(account=account).update(loan_count=F('loan_count') + 1)
               account_details_savings.save()
               loan_taken.save()
               return render(request,'myapp/loan.html',{'customer':customer,'transaction':transaction})

            elif score>=30 and score<=70 and details.loan_count<5:
                loan_taken = loan(account=account,loan_refno = ref_no,loan_type=loan_type,plan=plan_type,amount=amount,date_applied = date.today(),date_approved=None,date_released=None,date_rejected=None,loan_status = 'pending',loan_desc=desc,tp_amount=None,m_amount=None,penalty=None,due_date=None,pay_amount=None,count=int((plan_details['months'])/(plan_details['freq_of_payment_month'])))
                loan_details.objects.filter(account=account).update(loan_count=F('loan_count') + 1)
                transaction='pending'
                loan_taken.save()
                return render(request,'myapp/loan.html',{'customer':customer,'transaction':transaction})
            elif score<30 or details.loan_count>=5:
                loan_taken = loan(account=account,loan_refno = ref_no,loan_type=loan_type,plan=plan_type,amount=amount,date_applied = date.today(),date_approved=None,date_released=None,date_rejected=None,loan_status = 'rejected',loan_desc=desc,tp_amount=None,m_amount=None,penalty=None,due_date=None,pay_amount=None,count=int((plan_details['months'])/(plan_details['freq_of_payment_month'])))
                transaction='failed'
                loan_taken.save()
                return render(request,'myapp/loan.html',{'customer':customer,'transaction':transaction})
                
               
            
    
    return render(request,'myapp/loan.html',{'customer':customer,})

def loan_details_table(request,account_no):
    account = AccountNumber.objects.get(account_number = account_no)
    customer = Customer.objects.get(account = account)
    account_details_savings = Account.objects.get(account_number = account,account_type='savings')
    details = loan.objects.filter(account=account)
    person_details = loan_details.objects.get(account=account)
    transaction_status = request.GET.get('transaction_status', 'success')
    
    
    for i in details:
        if i.loan_status == 'approved' or i.loan_status == 'approved overdue':
            if i.due_date < date.today():
                i.loan_status = 'approved '+' overdue'
                i.pay_amount = i.pay_amount+i.penalty
                plan_details = get_plan_values(i.plan)
                months_diff = months_between(i.due_date,date.today())
                person_details.due_payments +=int(months_diff/plan_details['freq_of_payment_month'])+1
                person_details.penalties +=int(months_diff/plan_details['freq_of_payment_month'])+1
                person_details.save()
                i.save()
    
    return render(request,'myapp/loandetails.html',{'details':details,'customer':customer,'transaction':transaction_status})

def pay_loan(request,refno,account_no):
    account = AccountNumber.objects.get(account_number = account_no)
    customer = Customer.objects.get(account = account)
    account_details_savings = Account.objects.get(account_number = account,account_type='savings')
    loan_taken = loan.objects.get(loan_refno=refno)
    person_details = loan_details.objects.get(account=account)
    plan_details = get_plan_values(loan_taken.plan)
    loan_pending = loan.objects.filter(loan_status = 'pending')
    details = loan.objects.filter(account=account)
     
    # Process the payment logic
    if loan_taken.count > 1:
            # Example penalty logic (if overdue)
            if loan_taken.due_date < date.today():
                if account_details_savings < loan_taken.pay_amount+loan_taken.penalty:
                    transaction_status = 'failed'
                    url = reverse('myapp:loan_details_table', kwargs={'account_no': account_no})
                    url_with_params = f"{url}?transaction_status={transaction_status}"
                    return redirect(url_with_params)
                account_details_savings.balance -= loan_taken.pay_amount+loan_taken.penalty
                person_details.due_payments -= 1
                person_details.penalties -= 1
                loan_taken.count -= 1
                account_details_savings.save()
                person_details.save()
                if loan_taken.due_date < date.today():
                    loan_taken.pay_amount = loan_taken.pay_amount+loan_taken.penalty
                    loan_taken.save()
                    
                else:
                    loan_taken.pay_amount = loan_taken.pay_amount
                    loan_taken.save()
                    
                
                
            else:
                loan_taken.due_date = loan_taken.due_date + relativedelta(months=plan_details['freq_of_payment_month'])
                if account_details_savings.balance < loan_taken.pay_amount:
                    transaction_status = 'failed'
                    url = reverse('myapp:loan_details_table', kwargs={'account_no': account_no})
                    url_with_params = f"{url}?transaction_status={transaction_status}"
                    return redirect(url_with_params)
                account_details_savings.balance -= loan_taken.pay_amount
                loan_taken.pay_amount = loan_taken.m_amount
                loan_taken.count -= 1
                account_details_savings.save()
                loan_taken.save()
                 
                
    elif loan_taken.count == 1:
            
            if loan_taken.due_date < date.today():
                if account_details_savings.balance < loan_taken.pay_amount+loan_taken.penalty:
                    transaction_status = 'failed'
                    url = reverse('myapp:loan_details_table', kwargs={'account_no': account_no})
                    url_with_params = f"{url}?transaction_status={transaction_status}"
                    return redirect(url_with_params)
                account_details_savings.balance -= loan_taken.pay_amount+loan_taken.penalty
                person_details.due_payments -= 1
                person_details.penalties -= 1
                person_details.loan_count -= 1
                loan_taken.count -= 1
                loan_taken.m_amount = 0
                loan_taken.penalty = 0
                loan_taken.pay_amount = 0
                loan_taken.loan_status='released'
                person_details.save()
                account_details_savings.save()
                loan_taken.save()
                for i in loan_pending:
                    if loan_score(100,person_details.loan_count,person_details.due_payments,person_details.penalties) >= 70:
                        i.loan_status = 'approved'
                        plan_details_1 = get_plan_values(i.plan)
                        i.due_date = date.today() + relativedelta(months=plan_details_1['freq_of_payment_month'])
                        account_details_savings.balance += i.amount 
                        i.tp_amount = int(int(i.amount) * (1+(int(plan_details_1['interest'])*(int(plan_details_1['months'])/12))/100))
                        i.m_amount = int(i.tp_amount/int(plan_details_1['months']))
                        i.penalty = int(0.05*i.m_amount)
                        i.pay_amount = i.m_amount
                        person_details.save()
                        account_details_savings.save()
                        i.save()
                
                
                
            else:
                loan_taken.due_date = loan_taken.due_date + relativedelta(months=plan_details['freq_of_payment_month'])
                if account_details_savings.balance < loan_taken.pay_amount:
                    transaction_status = 'failed'
                    url = reverse('myapp:loan_details_table', kwargs={'account_no': account_no})
                    url_with_params = f"{url}?transaction_status={transaction_status}"
                    return redirect(url_with_params) 
                account_details_savings.balance -= loan_taken.pay_amount
                person_details.loan_count -= 1
                loan_taken.count -= 1
                loan_taken.m_amount = 0
                loan_taken.penalty = 0
                loan_taken.pay_amount = 0
                loan_taken.loan_status='released'
                person_details.save()
                account_details_savings.save()
                loan_taken.save()
                for i in loan_pending:
                    if loan_score(100,person_details.loan_count,person_details.due_payments,person_details.penalties) >= 70:
                        i.loan_status = 'approved'
                        plan_details_1 = get_plan_values(i.plan)
                        i.due_date = date.today() + relativedelta(months=plan_details_1['freq_of_payment_month'])
                        account_details_savings.balance += i.amount 
                        i.tp_amount = int(int(i.amount) * (1+(int(plan_details_1['interest'])*(int(plan_details_1['months'])/12))/100))
                        i.m_amount = int(i.tp_amount/int(plan_details_1['months']))
                        i.penalty = int(0.05*i.m_amount)
                        i.pay_amount = i.m_amount
                        person_details.save()
                        account_details_savings.save()
                        i.save()
    return redirect(reverse('myapp:loan_details_table',kwargs={'account_no':account_no})) 
            

        # Redirect back to the same page after processing
    
    
    
