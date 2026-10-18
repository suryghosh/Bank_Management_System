# Bank Management System

A full-stack Bank Management System developed using **Django** and **SQL** that supports user authentication, twin account creation (Savings & Current), transaction processing, peer-to-peer fund transfers, loan scoring & management, and a robust **ACID-compliant Transaction Rollback Mechanism**.

---

## Key Features

### 1. Customer & Account Management
- **Automatic Account Generation**: Generates a unique 12-digit account number upon registration.
- **Twin Account Architecture**: Each customer is automatically provisioned with both a **Savings** and a **Current** account under their unique account number.
- **Age & Credential Validation**: Enforces minimum age (18+), phone number uniqueness, Aadhar number uniqueness, and strong password policy.
- **Profile Updates & Deletion**: Secure account modification and deletion workflows.

### 2. Financial Transactions
- **Deposits**: Deposit funds into either Savings or Current account with instant balance updates.
- **P2P UPI Money Transfers**: Transfer funds between any accounts and account types (Savings ↔ Current, Savings ↔ Savings, etc.) with real-time fund checks.
- **Bill Payments**: Pay bills for utility services including Rent, Electricity, Gas, Broadband & Data-Card, Mobile Recharge, and Club Membership.
- **Transaction History**: Real-time searchable transaction ledger displaying transaction parties, dates, account types, status, and details.

### 3. Credit Scoring & Loan Management
- **Dynamic Credit Scoring (0–100)**: Proprietary credit scoring algorithm calculated based on base score, active loan count, due payments, and accumulated penalties:
  $$\text{Score} = \max(0, \min(100, 100 - (\text{loans} \times 10) - (\text{due payments} \times 40) - (\text{penalties} \times 30)))$$
- **Multiple Loan Types & Flexible Plans**: Apply for Personal, Home, Car, Business, or Education loans with customizable monthly plans and interest rates.
- **Automated Underwriting**:
  - Score $> 70$: Instant approval and automated disbursement to Savings account.
  - Score $30 - 70$: Marked as pending review.
  - Score $< 30$ or $\ge 5$ loans: Automatically rejected.
- **Installment Tracking & Repayment**: Tracks due dates, monthly payments, automated penalty calculation for overdue loans, and auto-approval of pending loans upon clearing active obligations.

---

## Rollback Mechanism

The system implements a dual-layer rollback architecture to ensure data integrity, financial consistency, and error recovery:

### Layer 1: Database-Level Atomicity (`transaction.atomic`)
Every financial operation that modifies multiple database tables is strictly wrapped in Django's `django.db.transaction.atomic()` context:
- **Account Creation**: If customer creation or account assignment fails, generated account records are rolled back immediately.
- **Money Transfers (UPI)**: Debiting the sender account, crediting the destination account, and creating the audit transaction log occur atomically. If any error occurs during the operation, all changes roll back to prevent lost funds.
- **Loan Disbursement & Repayments**: Deducting balances, updating loan states, updating penalty/due payment counts, and approving pending loans execute within an atomic transaction.
- **Safe Deletion**: Deleting customer accounts and associated records occurs atomically.

### Layer 2: Application-Level Transaction Rollback & Reversal
Users and administrators can reverse and rollback eligible successful transactions (e.g., transfers, deposits, bill payments) with full audit preservation:
- **Route**: `POST /transaction/rollback/<transaction_id>/`
- **Fund Verification**: Prior to reversing a transfer, the system checks that the destination account holds sufficient balance to return the funds. If the recipient has insufficient balance, the rollback aborts safely without altering records.
- **Atomic State Restoration**: Re-credits the sender account and re-debits the recipient account inside an atomic transaction.
- **Immutable Audit Trail**: The original transaction is marked as `rolled_back` and a corresponding `reversed` transaction record is appended to the ledger for complete traceability.
- **User Interface**: Dedicated "Rollback" action directly in the transaction ledger with confirmation prompts and real-time status feedback.

---

## Tech Stack

- **Backend**: Python 3.10+, Django 5.x
- **Database**: SQLite (Development) / PostgreSQL / MySQL (Production compatible)
- **Frontend**: HTML5, CSS3, Bootstrap 5, FontAwesome
- **Utilities**: `python-dateutil`, `django-extensions`, `sqlparse`

---

## Project Structure

```text
Bank_Management_System/
├── IIITBank/                   # Django Project Root
│   ├── settings.py             # Configuration & Installed Apps
│   ├── urls.py                 # Core routing
│   ├── wsgi.py / asgi.py
├── myapp/                      # Banking Application
│   ├── models.py               # Bank_branches, Customer, Account, Transaction, Loan
│   ├── views.py                # Banking views & rollback logic
│   ├── urls.py                 # App routing
│   ├── templates/myapp/        # Responsive HTML5 UI templates
│   ├── static/myapp/           # Stylesheets and visual assets
│   ├── templatetags/           # Custom template filters
│   └── tests.py                # Comprehensive test suite (13 test cases)
├── manage.py                   # Django CLI tool
├── requirements.txt            # Dependency specification
└── db.sqlite3                  # Local database
```

---

## Getting Started

### 1. Prerequisites
Ensure you have Python 3.10 or higher installed:
```bash
python --version
```

### 2. Clone the Repository
```bash
git clone https://github.com/suryghosh/Bank_Management_System.git
cd Bank_Management_System
```

### 3. Create and Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations
```bash
python manage.py migrate
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
Access the application at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Admin Portal & Test Credentials

### Django Administration
Access the administrative portal at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/):
- **Username**: `ghosh`
- **Password**: `ghosh`

*(Alternative superuser accounts: `ghosh009` / `Ghosh2004@` or `ghosh_007` / `ghosh123`)*

### Sample Customer Account (Pre-configured)
- **Customer Name**: `Surya Narayan ghosh`
- **Phone Number**: `7010967092`
- **Aadhar Number**: `121233447777`
- **Password**: `Ghosh2004@`
- **Account Number**: `147832395351`

---

## Running the Automated Test Suite

Run the full suite of unit and integration tests (including atomic rollback validation):
```bash
python manage.py test
```

Expected output:
```text
Creating test database for alias 'default'...
.............
----------------------------------------------------------------------
Ran 13 tests in 0.282s

OK
Destroying test database for alias 'default'...
```

---

## License

This project is licensed under the MIT License.
