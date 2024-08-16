**لیست کوئری ها:**   

 **1 :**
ایجاد ۲۰ هزار رکورد با داده های تصادفی در جدول حساب بانکی:  

 -ابتدا ایجاد 1000 رکورد تصادفی در جدول Person
```
from  person.temp  import create_fake_persons
create_fake_persons(total_records=1000,batch_size=500)
```
-سپس اجاد 2000 حساب بانکی 
```
from bank_account.temp import create_fake_bankaccounts
create_fake_bankaccounts(total_records=2000,batch_size=500)
```

 **2 :**
لیست نام صاحب هر حساب و موجودی آن حساب :  

 
```
bank_accounts = BankAccount.objects.values_list('owner__first_name', 'owner__last_name', 'balance')

```
**3 :**
حسابی که بیشترین موجودی را دارد :  

 
```
first=BankAccount.objects.order_by('-balance').first()

```
می توان این دستور را اینگونه نیز اجرا کرد: 
```
from django.db.models import Max
max_balance = BankAccount.objects.aggregate(Max("balance",default=0))['balance__max']
balance_account = BankAccount.objects.filter(balance=max_balance).first()
```
 **4 :**
5 حسابی که کمترین موجودی را دارند :  

 
```
lowest_accounts = BankAccount.objects.order_by('balance')[:5]

```
  **5 :**
تابعی که مقدار مشخصی پول را از حسابی به حساب دیگر منتقل کند:  

 
```
from person.temp import transfer_value
transfer_value(from_account_number="3358757738337063",from_owner_firstname="Joann",from_owner_lastname="Williams",to_account_number="1379130651687472",to_owner_firstname="Brett",to_owner_lastname="Wade", value=100)

``` 
 **6 :**
لیست حساب هایی که شناسه ی حساب از موجودی آن بیشتر است :  

 
```
from django.db.models import F
from django.db.models.functions import Cast
from django.db.models import F,DecimalField

accounts = BankAccount.objects.annotate(account_number_decimal=Cast('account_number', output_field=DecimalField())).filter(account_number_decimal__gt=F('balance'))

```
  **7 :**
لیست حساب هایی که کد ملی صاحب حساب از موجودی آن بیشتر است :  

 
```
from bank_account.temp import get_higher_national_code 
accounts = get_higher_national_code()
```
