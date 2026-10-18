from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from myapp.models import Bank_branches, AccountNumber, Customer, Account, Transaction, loan, loan_details


class BankManagementSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.branch = Bank_branches.objects.create(
            branch_name="Main Branch",
            state="Karnataka",
            city="Bengaluru"
        )
        self.acc_num = AccountNumber.objects.create(account_number="123456789012")
        self.customer = Customer.objects.create(
            name="Test User",
            phone_no="9876543210",
            Aadhar_no="123456789012",
            DOB=date(1995, 5, 20),
            branch_connect=self.branch,
            account=self.acc_num,
            password="Password@123"
        )
        self.acc_savings = Account.objects.create(
            account_type="savings",
            balance=5000.0,
            account_number=self.acc_num
        )
        self.acc_current = Account.objects.create(
            account_type="current",
            balance=2000.0,
            account_number=self.acc_num
        )

        # Setup second user for transfer testing
        self.acc_num2 = AccountNumber.objects.create(account_number="987654321098")
        self.customer2 = Customer.objects.create(
            name="Second User",
            phone_no="9123456780",
            Aadhar_no="987654321098",
            DOB=date(1998, 1, 15),
            branch_connect=self.branch,
            account=self.acc_num2,
            password="Password@123"
        )
        self.acc_savings2 = Account.objects.create(
            account_type="savings",
            balance=1000.0,
            account_number=self.acc_num2
        )
        self.acc_current2 = Account.objects.create(
            account_type="current",
            balance=500.0,
            account_number=self.acc_num2
        )

    def test_starting_page(self):
        response = self.client.get(reverse('myapp:starting_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to IIIT-Bank")

    def test_create_account_get(self):
        response = self.client.get(reverse('myapp:create'))
        self.assertEqual(response.status_code, 200)

    def test_create_account_post(self):
        response = self.client.post(reverse('myapp:create'), {
            'name': 'New Customer',
            'phone_no': '9988776655',
            'Aadhar_no': '998877665544',
            'DOB': '1990-01-01',
            'branch': self.branch.branch_id,
            'password': 'Password@123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Customer.objects.filter(phone_no='9988776655').exists())

    def test_login_get_and_post(self):
        response = self.client.get(reverse('myapp:login'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('myapp:login'), {
            'name': 'Test User',
            'phone_no': '9876543210',
            'Aadhar_no': '123456789012',
            'password': 'Password@123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn(f'/main/{self.customer.customer_id}', response.url)

    def test_main_page(self):
        response = self.client.get(reverse('myapp:mainPage', kwargs={'customer_id': self.customer.customer_id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to IIIT-Bank")
        self.assertContains(response, "Loan Score")

    def test_check_balance(self):
        response = self.client.get(reverse('myapp:checkBalance', kwargs={'account_no': self.acc_num.account_number}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "5000.0")
        self.assertContains(response, "2000.0")

    def test_deposit(self):
        response = self.client.post(reverse('myapp:deposit', kwargs={'account_no': self.acc_num.account_number}), {
            'deposit': '1000',
            'type': 'savings'
        })
        self.assertEqual(response.status_code, 302)
        self.acc_savings.refresh_from_db()
        self.assertEqual(self.acc_savings.balance, 6000.0)

    def test_upi_transfer(self):
        response = self.client.post(reverse('myapp:upi', kwargs={'account_no': self.acc_num.account_number}), {
            'type_from': 'savings',
            'type_to': 'savings',
            'account_no': self.acc_num2.account_number,
            'transact': '500'
        })
        self.assertEqual(response.status_code, 200)
        self.acc_savings.refresh_from_db()
        self.acc_savings2.refresh_from_db()
        self.assertEqual(self.acc_savings.balance, 4500.0)
        self.assertEqual(self.acc_savings2.balance, 1500.0)

    def test_bill_payments(self):
        response = self.client.post(reverse('myapp:bill_payments', kwargs={'account_no': self.acc_num.account_number}), {
            'pay_class': 'Electricity-bill',
            'type': 'savings',
            'deposit': '200'
        })
        self.assertEqual(response.status_code, 200)
        self.acc_savings.refresh_from_db()
        self.assertEqual(self.acc_savings.balance, 4800.0)

    def test_transaction_history(self):
        Transaction.objects.create(
            transaction_details="Deposit Rs 1000",
            transaction_type="success",
            transaction_date=date.today(),
            types="savings",
            transaction_from=self.acc_num
        )
        response = self.client.get(reverse('myapp:transaction', kwargs={'account_no': self.acc_num.account_number}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Deposit Rs 1000")

    def test_loan_apply_and_pay(self):
        # Apply for loan
        response = self.client.post(reverse('myapp:loan', kwargs={'account_no': self.acc_num.account_number}), {
            'loan_type': 'Personal',
            'plan': '12-month/s[9%,1]',
            'loan_amount': '10000',
            'text': 'Personal emergency'
        })
        self.assertEqual(response.status_code, 200)
        created_loan = loan.objects.filter(account=self.acc_num).first()
        self.assertIsNotNone(created_loan)

        # Check loan details table
        response = self.client.get(reverse('myapp:loan_details_table', kwargs={'account_no': self.acc_num.account_number}))
        self.assertEqual(response.status_code, 200)

        # Pay loan installment
        if created_loan.loan_status == 'approved':
            response = self.client.post(reverse('myapp:pay_loan', kwargs={
                'refno': created_loan.loan_refno,
                'account_no': self.acc_num.account_number
            }))
            self.assertEqual(response.status_code, 302)

    def test_rollback_upi_transfer(self):
        # 1. Execute transfer
        self.client.post(reverse('myapp:upi', kwargs={'account_no': self.acc_num.account_number}), {
            'type_from': 'savings',
            'type_to': 'savings',
            'account_no': self.acc_num2.account_number,
            'transact': '500'
        })
        self.acc_savings.refresh_from_db()
        self.acc_savings2.refresh_from_db()
        self.assertEqual(self.acc_savings.balance, 4500.0)
        self.assertEqual(self.acc_savings2.balance, 1500.0)

        # 2. Get created transaction
        tx = Transaction.objects.filter(transaction_from=self.acc_num, transaction_to=self.acc_num2, transaction_type='success').first()
        self.assertIsNotNone(tx)

        # 3. Rollback transaction
        response = self.client.post(reverse('myapp:rollback_transaction', kwargs={'transaction_id': tx.transaction_id}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('rollback_status=success', response.url)

        # 4. Verify balances are restored
        self.acc_savings.refresh_from_db()
        self.acc_savings2.refresh_from_db()
        self.assertEqual(self.acc_savings.balance, 5000.0)
        self.assertEqual(self.acc_savings2.balance, 1000.0)

        # 5. Verify status changed to rolled_back and reversal record exists
        tx.refresh_from_db()
        self.assertEqual(tx.transaction_type, 'rolled_back')
        reversal = Transaction.objects.filter(transaction_type='reversed').first()
        self.assertIsNotNone(reversal)

    def test_rollback_deposit(self):
        # 1. Execute deposit
        self.client.post(reverse('myapp:deposit', kwargs={'account_no': self.acc_num.account_number}), {
            'deposit': '1000',
            'type': 'savings'
        })
        self.acc_savings.refresh_from_db()
        self.assertEqual(self.acc_savings.balance, 6000.0)

        # 2. Rollback deposit
        tx = Transaction.objects.filter(transaction_from=self.acc_num, transaction_type='success').first()
        response = self.client.post(reverse('myapp:rollback_transaction', kwargs={'transaction_id': tx.transaction_id}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('rollback_status=success', response.url)

        # 3. Balance restored
        self.acc_savings.refresh_from_db()
        self.assertEqual(self.acc_savings.balance, 5000.0)
