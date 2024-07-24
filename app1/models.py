from django.db import models
from django.contrib.auth.hashers import make_password


# Create your models here.
class UserIDSequence(models.Model):
    current_id = models.IntegerField(default=0)
    def __str__(self):
        return str(self.current_id)
    
class CompanyIDSequence(models.Model):
    current_id = models.IntegerField(default=0)
    def __str__(self):
        return str(self.current_id)
    
class SubUserIDSequence(models.Model):
    current_id = models.IntegerField(default=0)
    def __str__(self):
        return str(self.current_id)

class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True, editable=False)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(null=False)
    phone_number = models.IntegerField(null=False)
    linkedin_url = models.URLField(null=True)
    firstname = models.CharField(max_length=50,null=False)
    lastname = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=150,null=False)  
    user_type = models.CharField(max_length=12,default='admin')
    company_type = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.user_id:
            user_sequence, created = UserIDSequence.objects.get_or_create(pk=1)
            user_sequence.current_id += 1
            self.user_id = f'NL{user_sequence.current_id:03d}'
            user_sequence.save()
        if self.password:
            # Hash the password
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
    def __str__(self):
        return self.user_id
    
class Company(models.Model):
    # Company Details
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='companies')
    company_id = models.CharField(max_length=10, primary_key=True, editable=False)
    name = models.CharField(max_length=100, null=True)
    date_of_incorporation = models.DateField(null= True)
    email = models.EmailField(null=True)
    website_url = models.URLField(null=True)
    linkedin_url = models.URLField(null=True)
    subscription_type = models.CharField(max_length=20, null=True)
    business_type = models.ForeignKey('BusinessType', on_delete=models.CASCADE,null=True)
    sector = models.ForeignKey('Sector', on_delete=models.CASCADE,null=True)
    company_type = models.CharField(max_length=10, null=True)
    location = models.CharField(max_length=20, null=True)

    def save(self, *args, **kwargs):
        if not self.company_id:
            company_sequence, created = CompanyIDSequence.objects.get_or_create(pk=1)
            company_sequence.current_id += 1
            self.company_id = f'C{company_sequence.current_id:03d}'
            company_sequence.save()
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_id

class CompanyProfile(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='company_profiles')
    tam = models.FloatField()
    cagr = models.FloatField()
    number_of_clients_users = models.IntegerField()
    previous_year_revenue = models.FloatField()
    current_year_revenue_arr = models.FloatField()
    current_monthly_burn_rate = models.FloatField()
    forecasted_revenue_for_next_year = models.FloatField()
    business_stage = models.ForeignKey('BusinessStage', on_delete=models.CASCADE)
    equity_funds_raised_so_far = models.FloatField()
    funds_needed = models.FloatField()
    business_plan = models.FileField(upload_to='business_plan',null=True)
    pitch_and_product = models.FileField(upload_to='pitch_and_product',null=True)

    

class Sector(models.Model):
    #company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='sectors')
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class BusinessType(models.Model):
    #company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='business_types')
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class BusinessStage(models.Model):
    #company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='business_stages')
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Founder(models.Model):
    company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='founders')
    name=models.CharField(max_length=50)
    linkedin_url=models.URLField()
    short_profile=models.TextField(null=True)
    photo=models.ImageField(upload_to='photos',null=True)
    phone_number=models.IntegerField()
    email=models.EmailField()
    def __str__(self):
        return self.name

class ExecutiveMember(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='executive_members')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Advisor(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='advisors')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phonenumber = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Challenge(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='challenges')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class SolvedProblem(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='solved_problems')
    description = models.TextField()

    def __str__(self):
        return self.description

class Competitor(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='competitors')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class SocialMedia(models.Model):
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='social_media_urls')
    #name=models.CharField(max_length=25)
    url=models.URLField()

class Client(models.Model):
    company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='clients')
    name=models.CharField(max_length=25)
    logo=models.ImageField(upload_to='clients_logo',null=True)

class CapTable(models.Model):
    company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='cap_tables')
    name = models.CharField(max_length=200)
    email= models.EmailField()
    linkedin_url=models.URLField()
    photo = models.ImageField(upload_to='photos',null=True)
    percentage_of_shares= models.DecimalField(max_digits=5,decimal_places=2)








class Team(models.Model):
    subuser_id = models.CharField(max_length=10, primary_key=True)
    #creator_id = models.ForeignKey(User,on_delete=models.CASCADE)
    creator_id = models.CharField(max_length=15)
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(null=False)
    phone_number = models.IntegerField(null=False)
    linkedin_url = models.URLField(null=True)
    firstname = models.CharField(max_length=50,null=False)
    lastname = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=10,null=False)  
    user_type = models.CharField(max_length=12)

    def save(self, *args, **kwargs):
        if not self.subuser_id:
            subuser_sequence, created = SubUserIDSequence.objects.get_or_create(pk=1)
            subuser_sequence.current_id += 1
            self.subuser_id = f'SUBNL{subuser_sequence.current_id:03d}'
            subuser_sequence.save()
        if self.password:
            # Hash the password
            self.password = make_password(self.password)
        super(Team, self).save(*args, **kwargs)
    def __str__(self):
        return self.subuser_id




class HomogenousProduct(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    selling_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    units_sold = models.IntegerField()
    expected_growth_rate = models.IntegerField()
    revenue_from_product = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def calculate_revenue_from_product(self):
        if isinstance(self.selling_price_per_unit, str):
            self.selling_price_per_unit = float(self.selling_price_per_unit)
        if isinstance(self.units_sold, str):
            self.units_sold = int(self.units_sold)
        return self.selling_price_per_unit * self.units_sold

    def save(self, *args, **kwargs):
        # Calculate revenue_from_product before saving
        self.revenue_from_product = self.calculate_revenue_from_product()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name


 
class HeterogenousProduct(models.Model):
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    expected_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    expected_growth_rate = models.IntegerField()
    def __str__(self):
        return self.product_name
    
class CompanyRevenue(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    total_revenue = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def calculate_total_revenue(self):
        homogenous_revenue = HomogenousProduct.objects.filter(company_id=self.company_id).aggregate(total=models.Sum('revenue_from_product'))['total'] or 0
        heterogenous_revenue = HeterogenousProduct.objects.filter(company_id=self.company_id).aggregate(total=models.Sum('expected_revenue'))['total'] or 0
        return homogenous_revenue + heterogenous_revenue
    
    def save(self, *args, **kwargs):
        # Calculate total_revenue before saving
        self.total_revenue = self.calculate_total_revenue()
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"Total Revenue for {self.company_id}"








# class IncomeStatementOld(models.Model):
#     company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
#     begin_date = models.DateTimeField()
#     end_date = models.DateTimeField()

#     product_name = models.CharField(max_length=100)
#     total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
#     total_taxes = models.DecimalField(max_digits=10, decimal_places=2)
#     total_dividends = models.DecimalField(max_digits=10, decimal_places=2)
    

    
#     total_cogs = models.DecimalField(max_digits=10, decimal_places=2)
#     cogs_direct_labor = models.DecimalField(max_digits=10, decimal_places=2)
#     cogs_material = models.DecimalField(max_digits=10, decimal_places=2)
#     cogs_parts = models.DecimalField(max_digits=10, decimal_places=2)
#     cogs_distribution = models.DecimalField(max_digits=10, decimal_places=2)
#     cogs_other = models.DecimalField(max_digits=10, decimal_places=2)

#     total_operating_expenses = models.DecimalField(max_digits=10, decimal_places=2)
#     opexpense_rent = models.DecimalField(max_digits=10, decimal_places=2)
#     opexpense_utilities = models.DecimalField(max_digits=10, decimal_places=2)
#     opexpense_overhead = models.DecimalField(max_digits=10, decimal_places=2)
#     opexpense_legal = models.DecimalField(max_digits=10, decimal_places=2)
#     opexpense_depreciation = models.DecimalField(max_digits=10, decimal_places=2)
#     opexpense_marketing_ads = models.DecimalField(max_digits=10, decimal_places=2)
#     opexpense_insurance = models.DecimalField(max_digits=10, decimal_places=2)
#     opexpense_interest = models.DecimalField(max_digits=10, decimal_places=2)
#     opexpense_travel = models.DecimalField(max_digits=10, decimal_places=2)
#     opexpense_wages = models.DecimalField(max_digits=10, decimal_places=2)
#     opexpense_other = models.DecimalField(max_digits=10, decimal_places=2)

    

#     #creator_id = models.IntegerField()
#     #modifier_id = models.IntegerField(null=True)
#     creator_id = models.CharField(max_length=12)
#     modifier_id = models.CharField(max_length=12,null=True)

#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now_add=True)

    

#     class Meta:
#         db_table = 'nl_income_statement'


# class BalanceSheet(models.Model):
#     company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
#     begin_date = models.DateTimeField()
#     end_date = models.DateTimeField()

#     total_current_assets = models.DecimalField(max_digits=10, decimal_places=2)
#     ca_cash = models.DecimalField(max_digits=10, decimal_places=2)
#     ca_accounts_receivables = models.DecimalField(max_digits=10, decimal_places=2)
#     ca_prepaid_expenses = models.DecimalField(max_digits=10, decimal_places=2)
#     ca_inventory = models.DecimalField(max_digits=10, decimal_places=2)
#     ca_other = models.DecimalField(max_digits=10, decimal_places=2)

#     total_non_current_assets = models.DecimalField(max_digits=10, decimal_places=2)
#     nca_property = models.DecimalField(max_digits=10, decimal_places=2)
#     nca_charity = models.DecimalField(max_digits=10, decimal_places=2)
#     nca_equipment = models.DecimalField(max_digits=10, decimal_places=2)
#     nca_leases = models.DecimalField(max_digits=10, decimal_places=2)
#     nca_other = models.DecimalField(max_digits=10, decimal_places=2)

#     total_current_liabilities = models.DecimalField(max_digits=10, decimal_places=2)
#     cl_accounts_payable = models.DecimalField(max_digits=10, decimal_places=2)
#     cl_accrued_expenses = models.DecimalField(max_digits=10, decimal_places=2)
#     cl_unearned_revenue = models.DecimalField(max_digits=10, decimal_places=2)
#     cl_other = models.DecimalField(max_digits=10, decimal_places=2)

#     total_non_current_liabilities = models.DecimalField(max_digits=10, decimal_places=2)
#     ncl_longterm_debt = models.DecimalField(max_digits=10, decimal_places=2)
#     ncl_other = models.DecimalField(max_digits=10, decimal_places=2)

#     shareholder_equity = models.DecimalField(max_digits=10, decimal_places=2)
#     equity_investment_capital = models.DecimalField(max_digits=10, decimal_places=2)
#     equity_retained_earnings = models.DecimalField(max_digits=10, decimal_places=2)

#     # creator_id = models.IntegerField()
#     # modifier_id = models.IntegerField(null=True)
    
#     creator_id = models.CharField(max_length=12)
#     modifier_id = models.CharField(max_length=12,null=True)

#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'nl_balance_sheet'


# class CashFlow(models.Model):
#     company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
#     begin_date = models.DateTimeField()
#     end_date = models.DateTimeField()

#     net_financing = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_finance_inflow_drawing = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_finance_inflow_distribution = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_finance_inflow_other = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_finance_outflow_loan_payments = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_finance_outflow_other = models.DecimalField(max_digits=10, decimal_places=2)


#     net_investments = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_invest_inflow_loans = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_invest_inflow_sell_property = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_invest_inflow_sell_equip = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_invest_inflow_other = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_invest_outflow_buy_property = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_invest_outflow_buy_equip = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_invest_outflow_other = models.DecimalField(max_digits=10, decimal_places=2)


#     net_operations = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_ops_inflow_customers = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_ops_inflow_depreciation = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_ops_inflow_amortization = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_ops_inflow_other = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_ops_outflow_wages = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_ops_outflow_overhead = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_ops_outflow_interest = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_ops_outflow_taxes = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_ops_outflow_accounts_receivable = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_ops_outflow_inventory_increase = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_ops_outflow_other = models.DecimalField(max_digits=10, decimal_places=2)

    
    
#     cf_beginning_balance = models.DecimalField(max_digits=10, decimal_places=2)
#     cf_change_in_cash = models.DecimalField(max_digits=10, decimal_places=2)

#     # creator_id = models.IntegerField()
#     # modifier_id = models.IntegerField(null=True)

#     creator_id = models.CharField(max_length=12)
#     modifier_id = models.CharField(max_length=12,null=True)

#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'nl_cash_flow'


class IncomeStatement(models.Model):
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    date = models.DateTimeField()

    total_revenue = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    operating_revenue = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    cost_of_revenue = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    gross_profit = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    operating_expense = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    selling_general_and_administrative_expense = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    general_and_administrative_expenses = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    selling_and_marketing_expense = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    research_and_development_expense = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    operating_income = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    net_non_operating_interest_income_expense= models.DecimalField(max_digits=10, decimal_places=2,null=True)
    interest_income_non_operating = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    interest_expense_non_operating = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    other_income_or_expense = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    gain_or_loss_on_sale_of_security = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    special_income_or_charges = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    write_off = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    other_non_operating_income_or_expenses = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    pretax_income = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    tax_provision = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    net_income = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    preference_share_dividends = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    net_income_to_common_stockholders = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    equity_share_dividends = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    retained_earnings = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    basic_eps = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    diluted_eps = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    depreciation_and_amortization = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    ebitda = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    monthly_or_quarterly_or_yearly = models.CharField(max_length=15,null=True)

    creator_id = models.CharField(max_length=12,null=True)
    modifier_id = models.CharField(max_length=12,null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)


    


    




