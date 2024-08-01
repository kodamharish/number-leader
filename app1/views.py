from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from .context_processors import custom_user,custom_subuser
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
#File Handling
from django.utils.deconstruct import deconstructible
from django.core.files.storage import FileSystemStorage
import os

#Mail Configuration
from django.core.mail import send_mail
from numberleader import settings
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

def contact(request):
    return render(request,'contact_us.html')


#Login and Logout

# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         # Check if the user exists in both User and Team models
#         user = User.objects.filter(username=username).first()
#         team = Team.objects.filter(username=username).first()

#         if user:
#             if check_password(password, user.password):
#                 request.session['current_user_id'] = user.user_id
#                 if user.user_type == 'admin':
#                     return redirect('admin_dashboard')
#                 if user.user_type == 'super_admin':
#                     return redirect('super_admin_dashboard')
#                 # elif user.user_type == 'editor':
#                 #     return redirect('editor_dashboard')
#                 # elif user.user_type == 'user':
#                 #     return redirect('user_dashboard')
#             else:
#                 messages.error(request, 'Invalid username or password')
#         elif team:
#             if check_password(password, team.password):
#                 request.session['current_subuser_id'] = team.subuser_id
#                 if team.user_type == 'admin':
#                     return redirect('admin_dashboard')
#                 elif team.user_type == 'editor':
#                     return redirect('editor_dashboard')
#                 elif team.user_type == 'user':
#                     return redirect('user_dashboard')
#             else:
#                 messages.error(request, 'Invalid username or password')
#         else:
#             messages.error(request, 'Invalid username or password')
#         return render(request, 'login.html')
#     else:
#         return render(request, 'login.html')
    
def login1(request):
    first_company_id = first_company_id
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Get the "Remember Me" value

        # Check if the user exists in both User and Team models
        user = User.objects.filter(username=username).first()
        team = Team.objects.filter(username=username).first()

        if user:
            if check_password(password, user.password):
                request.session['current_user_id'] = user.user_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                    # return redirect('admin_dashboard')

                else:
                    request.session.set_expiry(0)  # Browser close
                if user.user_type == 'admin':
                    return redirect('admin_dashboard',first_company_id)
                if user.user_type == 'super_admin':
                    return redirect('super_admin_dashboard')
               
            else:
                messages.error(request, 'Invalid username or password')
        elif team:
            if check_password(password, team.password):
                request.session['current_subuser_id'] = team.subuser_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                else:
                    request.session.set_expiry(0)  # Browser close
                if team.user_type == 'admin':
                    return redirect('admin_dashboard')
                elif team.user_type == 'editor':
                    return redirect('editor_dashboard')
                elif team.user_type == 'user':
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    



def login11(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Get the "Remember Me" value

        # Check if the user exists in both User and Team models
        user = User.objects.filter(username=username).first()
        team = Team.objects.filter(username=username).first()

        if user:
            if check_password(password, user.password):
                request.session['current_user_id'] = user.user_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                else:
                    request.session.set_expiry(0)  # Browser close
                first_company_id = first_company_id
                if user.user_type == 'admin':
                    return redirect('admin_dashboard',first_company_id)
                elif user.user_type == 'super_admin':
                    return redirect('super_admin_dashboard')
                # Uncomment and adjust these lines if needed
                # elif user.user_type == 'editor':
                #     return redirect('editor_dashboard')
                # elif user.user_type == 'user':
                #     return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        elif team:
            if check_password(password, team.password):
                request.session['current_subuser_id'] = team.subuser_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                else:
                    request.session.set_expiry(0)  # Browser close
                
                if team.user_type == 'admin':
                    return redirect('admin_dashboard')
                elif team.user_type == 'editor':
                    return redirect('editor_dashboard')
                elif team.user_type == 'user':
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
        
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')


from .context_processors import getAllCompanies
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Get the "Remember Me" value

        # Check if the user exists in both User and Team models
        user = User.objects.filter(username=username).first()
        team = Team.objects.filter(username=username).first()

        if user:
            if check_password(password, user.password):
                request.session['current_user_id'] = user.user_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                else:
                    request.session.set_expiry(0)  # Browser close

                # Get the first_company_id using getAllCompanies function
                companies_info = getAllCompanies(request)
                current_user_company_profile1 = getAllCompanies(request)

                first_company_id = companies_info.get('first_company_id')
                current_user_company_profile2 = current_user_company_profile1.get('current_user_company_profiles')

                print('current_user_company_profile2',current_user_company_profile2)
                if user.user_type == 'admin':
                    return redirect('admin_dashboard')
                    

                elif user.user_type == 'super_admin':
                    return redirect('super_admin_dashboard')
                # Uncomment and adjust these lines if needed
                # elif user.user_type == 'editor':
                #     return redirect('editor_dashboard')
                # elif user.user_type == 'user':
                #     return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        elif team:
            if check_password(password, team.password):
                request.session['current_subuser_id'] = team.subuser_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                else:
                    request.session.set_expiry(0)  # Browser close
                
                if team.user_type == 'admin':
                    return redirect('admin_dashboard')
                elif team.user_type == 'editor':
                    return redirect('editor_dashboard')
                elif team.user_type == 'user':
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
        
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return redirect('login')



# Sign Up
def signup(request):
    if request.method == 'POST':
        # Extract form data using request.POST.get
        #User Details
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        linkedin_url = request.POST.get('linkedin_url', '')  # Optional field
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname', '')  # Optional field
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Company Details
        company_name = request.POST.get('company_name')
        company_email = request.POST.get('company_email')
        company_website_url = request.POST.get('company_website_url')
        company_linkedin_url = request.POST.get('company_linkedin_url')
        subscription_type = request.POST.get('subscription_type')
        company_type = request.POST.get('company_type')
        # Founders Details
        founder_name = request.POST.get('founder_name')
        founder_email = request.POST.get('founder_email')
        founder_linkedin_url = request.POST.get('founder_linkedin_url')
        founder_phone_number = request.POST.get('founder_phone_number')
        founder_short_profile = request.POST.get('founder_short_profile')
        founder_photo = request.FILES.get('founder_photo')

        # Validate passwords
        if password != confirm_password:
            messages.error(request,'Passwords do not match')
            return redirect('signup')    
        # Validate if the username or email already exists
        if User.objects.filter(username=username).exists() or Team.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('signup')    
        if User.objects.filter(email=email).exists() or Team.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return redirect('signup')
            
        # Create and save User object
        user = User(
            username=username,
            email=email,
            phone_number=phone_number,
            linkedin_url=linkedin_url,
            firstname=firstname,
            lastname=lastname,
            password=password,
            company_type = company_type
        )
        
        user.save()

        # Ensure the user was saved correctly
        if user.pk:
            # Create and save Company object
            company = Company(
                user_id=user,  # This should match the foreign key field in Company model
                name=company_name,
                email=company_email,
                website_url=company_website_url,
                linkedin_url=company_linkedin_url,
                subscription_type = subscription_type
                
            )
            
            company.save()

            # Ensure the company was saved correctly
            if company.pk:
                company_id = Company.objects.get(company_id = company.pk)
                founder =Founder(
                    company_id = company_id,
                    name=founder_name,
                    email=founder_email,
                    linkedin_url=founder_linkedin_url,
                    phone_number=founder_phone_number,
                    short_profile = founder_short_profile,
                    photo = founder_photo
                )
                founder.save()
                messages.error(request,'User Created Succesfully')
                return redirect('signup')
                
            else:
                messages.error(request,'Something went wrong please try again later')
                return redirect('signup')
                
        else:
            messages.error(request,'Something went wrong please try again later')
            return redirect('signup')
           
    else:
        return render(request, 'sign_up.html')





#Super Admin
def superAdminDashboard(request):
    admins_count = User.objects.count()
    editors_count = Team.objects.filter(user_type='editor').count()
    users_count = Team.objects.filter(user_type='user').count()

    startups = User.objects.filter(company_type='Startup').count()
    investors= User.objects.filter(company_type='Investor').count()
    ca_firms= User.objects.filter(company_type='CA_firm').count()
    companys = Company.objects.count()
    context = {
        'admins_count': admins_count,
        'editors_count': editors_count,
        'users_count': users_count,
        'startups':startups,
        'investors':investors,
        'ca_firms':ca_firms,
        'companys':companys
    }

    return render(request,'super_admin/dashboard.html',context)


def startups(request):
    startups = User.objects.filter(company_type='Startup').all()
    context = {'startups':startups}
    return render(request,'super_admin/startups.html',context)

def investors(request):
    investors= User.objects.filter(company_type='Investor').all()
    context = {'investors':investors}
    return render(request,'super_admin/investors.html',context)

def ca_firms(request):
    ca_firms= User.objects.filter(company_type='CA_firm').all()
    context = {'ca_firms':ca_firms}
    return render(request,'super_admin/ca_firms.html',context)

def companies(request):
    companies = Company.objects.all()
    context ={'companies':companies}
    return render(request,'super_admin/companies.html',context)

def admins(request):
    admins = User.objects.all()
    context = {'admins':admins}

    return render(request,'super_admin/admins.html',context)

def editors(request):
    editors = Team.objects.filter(user_type='editor')
    context = {'editors':editors}

    return render(request,'super_admin/editors.html',context)

def users(request):
    users = Team.objects.filter(user_type='user')
    context = {'users':users}

    return render(request,'super_admin/users.html',context)




#Admin

def myTeam(request):
    if request.method == 'POST':
        pass          
    else:
        user_context = custom_user(request)
        current_user = user_context.get('current_user')  
        subuser_context = custom_subuser(request)
        current_subuser = subuser_context.get('current_subuser') 
        if current_user:
            total_team_data = Team.objects.filter(creator_id =current_user)
        if current_subuser:
                total_team_data = Team.objects.filter(creator_id = current_subuser)

        context = {'total_team_data':total_team_data}
        return render(request, 'admin/my_team.html',context)

def addTeam(request):
    if request.method == 'POST':
        # Extract form data using request.POST.get
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        linkedin_url = request.POST.get('linkedin_url', '')  # Optional field
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname', '')  # Optional field
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')
        companyID = request.POST.get('company')

        
        # Validate passwords
        if password != confirm_password:
            messages.error(request,'Passwords do not match')
            return redirect('add_team')
            
        # Validate if the username or email already exists
        if Team.objects.filter(username=username).exists() or User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('add_team')
            
        if Team.objects.filter(email=email).exists() or User.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return redirect('add_team')
        user_context = custom_user(request)
        current_user = user_context.get('current_user')  
        subuser_context = custom_subuser(request)
        current_subuser = subuser_context.get('current_subuser') 
        #creator_id = current_subuser.creator_id

        if current_user:
            # Fetch the User instance for the creator_id
              #creator_user = User.objects.get(user_id=current_user.user_id)
              creator_user = current_user.user_id
        if current_subuser:
              if current_subuser.user_type == 'editor':
                  # Fetch the User instance for the creator_id
                  #creator_user = Team.objects.get(subuser_id=current_subuser.subuser_id)
                  creator_user = current_subuser.subuser_id

        # Fetch the Company instance based on company_id
        company_id = Company.objects.get(company_id=companyID)
        # Create and save User object
        team = Team(
            username=username,
            creator_id=creator_user,
            company_id = company_id,
            email=email,
            phone_number=phone_number,
            linkedin_url=linkedin_url,
            firstname=firstname,
            lastname=lastname,
            password=password,
            user_type = user_type
        )
        
        team.save()
        # Get the current site domain
        current_site = get_current_site(request)
        domain = current_site.domain

        # Construct the Login URL
        signin_url = f'http://{domain}/login'

        subject='Number Leader Registration Details'
        txt='''Welcome to  Number Leader

               Below are your Login Details :

               First Name : {}
               First Name : {}
               Email : {}
               Username : {}
               Password : {}
               Phone Number : {}
               Linkedin URL : {}
               User Type : {}
               Company : {}

               You can Login by using below this URL : {}        
                '''
        message=txt.format(firstname,lastname,email,username,password,phone_number,linkedin_url,user_type,company_id.name,signin_url)
        from_email=settings.EMAIL_HOST_USER
        to_list=[email]
        send_mail(subject, message,from_email,to_list,fail_silently=True)
        messages.error(request,'Member Created Successfully')
        return redirect('add_team')       
           
    else:
        return render(request, 'admin/add_team.html')
    

def updateTeam(request, id):
    if request.method == 'POST':
        # Fetch the existing Team instance using subuser_id
        team = get_object_or_404(Team, subuser_id=id)

        # Extract form data using request.POST.get
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        linkedin_url = request.POST.get('linkedin_url', '')  # Optional field
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname', '')  # Optional field
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        companyID = request.POST.get('company')

        

        user_context = custom_user(request)
        current_user = user_context.get('current_user')  

        # # Fetch the User instance for the creator_id
        # creator_user = User.objects.get(user_id=current_user.user_id)

        subuser_context = custom_subuser(request)
        current_subuser = subuser_context.get('current_subuser') 

        if current_user:
            # Fetch the User instance for the creator_id
              #creator_user = User.objects.get(user_id=current_user.user_id)
              creator_user = current_user.user_id
        if current_subuser:
              if current_subuser.user_type == 'editor':
                  # Fetch the User instance for the creator_id
                  #creator_user = Team.objects.get(subuser_id=current_subuser.subuser_id)
                  creator_user = current_subuser.subuser_id


        
        # Fetch the Company instance based on company_id
        company_id = Company.objects.get(company_id=companyID)

        # Update the Team instance
        team.username = username
        team.creator_id = creator_user
        team.company_id = company_id
        team.email = email
        team.phone_number = phone_number
        team.linkedin_url = linkedin_url
        team.firstname = firstname
        team.lastname = lastname
        team.password = password
        team.user_type = user_type
        
        team.save()

        # Get the current site domain
        current_site = get_current_site(request)
        domain = current_site.domain

        # Construct the Login URL
        signin_url = f'http://{domain}/login'

        subject='Number Leader - Updated Details'
        txt='''Welcome to  Number Leader

               Below are your Updated Login Details :

               First Name : {}
               First Name : {}
               Email : {}
               Username : {}
               Password : {}
               Phone Number : {}
               Linkedin URL : {}
               User Type : {}
               Company : {}

               You can Login by using below this URL : {}        
                '''
        message=txt.format(firstname,lastname,email,username,password,phone_number,linkedin_url,user_type,company_id.company_name,signin_url)
        from_email=settings.EMAIL_HOST_USER
        to_list=[email]
        send_mail(subject, message,from_email,to_list,fail_silently=True)
        messages.success(request, 'Member Updated Successfully')
        return redirect('add_team')       
    else:
        context={'team': get_object_or_404(Team, subuser_id=id)}
        return render(request, 'admin/update_team.html',context)

def deleteTeam(request,id):
    team = get_object_or_404(Team, subuser_id=id)    
    # Delete the team member
    team.delete()
    # Show a success message
    messages.success(request, 'Member Deleted Successfully')
    return redirect('my_team')
 



def adminDashboard(request):
    # companys = Company.objects.all()
    # company_profile = CompanyProfile.objects.get(company_id = id)
    # founders = Founder.objects.filter(company_id = id)
    # clients = Client.objects.filter(company_id = id)

    # context = {
    #     'companys':companys,
    #     # 'company_profile': company_profile,
    #     # 'founders':founders,
    #     # 'clients':clients
    # }
    
    return render(request,'admin/dashboard.html') 

def addCompany(request):
    if request.method == 'POST':
        # company data
        startup_name = request.POST.get('startup_name')
        date_of_incorporation = request.POST.get('date_of_incorporation')
        email = request.POST.get('email')
        linkedin_url = request.POST.get('linkedin_url')
        sector_name = request.POST.get('sector')
        type_of_business = request.POST.get('type_of_business')
        no_of_employees = request.POST.get('no_of_employees')
        website_url = request.POST.get('website_url')
        location = request.POST.get('location')
        product_or_service = request.POST.get('product_or_service')
        subscription_type = request.POST.get('subscription_type')
        #company profile
        tam = request.POST.get('tam')
        cagr = request.POST.get('cagr')
        previous_year_revenue = request.POST.get('previous_year_revenue')
        current_year_revenue = request.POST.get('current_year_revenue')
        current_monthly_burn_rate = request.POST.get('current_monthly_burn_rate')
        forecasted_revenue_for_next_year = request.POST.get('forecasted_revenue_for_next_year')
        stage_of_business = request.POST.get('stage_of_business')
        equity_funds_raised_so_far = request.POST.get('equity_funds_raised_so_far')
        funds_needed = request.POST.get('funds_needed')
       


        #business_introductory_video_file = request.FILES.get('business_introductry_video_file')
        #business_introductory_video_url = request.POST.get('business_introductry_video_url')

        # business_plan = request.FILES.get('business_plan')
        # vision = request.POST.get('vision')
        # mission = request.POST.get('mission')
        # usp = request.POST.get('usp')

        user_context = custom_user(request)
        current_user = user_context.get('current_user') 

        sector = Sector.objects.get(name=sector_name)
        type_of_business = BusinessType.objects.get(name=type_of_business)
        stage_of_business = BusinessStage.objects.get(name=stage_of_business)

        # Create the Company instance
        company = Company(
            user_id=current_user,  # This should match the foreign key field in Company model
            name=startup_name,
            date_of_incorporation = date_of_incorporation,
            email = email,
            linkedin_url = linkedin_url,
            sector = sector,
            business_type = type_of_business,
            website_url=website_url,
            location = location,
            company_type = product_or_service,
            subscription_type = subscription_type
            
        )
        company.save()

        # Create the CompanyProfile instance
        company_profile = CompanyProfile(
            company_id=company,
            number_of_clients_users = no_of_employees, 
            tam = tam,
            cagr = cagr,
            previous_year_revenue = previous_year_revenue,
            current_year_revenue_arr = current_year_revenue,
            current_monthly_burn_rate = current_monthly_burn_rate,
            forecasted_revenue_for_next_year = forecasted_revenue_for_next_year,
            business_stage = stage_of_business,
            equity_funds_raised_so_far = equity_funds_raised_so_far,
            funds_needed = funds_needed

        )
        company_profile.save()

        # Save founders
        founder_count = int(request.POST.get('founder_count', 1))
        for i in range(1, founder_count + 1):
            founder_name = request.POST.get(f'founder_{i}_name')
            linkedin_profile = request.POST.get(f'founder_{i}_linkedin_profile')
            short_profile = request.POST.get(f'founder_{i}_short_profile')
            phone_no = request.POST.get(f'founder_{i}_phno')
            email = request.POST.get(f'founder_{i}_email')
            photo = request.FILES.get(f'founder_{i}_photo')
            if founder_name and linkedin_profile and short_profile and phone_no and email and photo:
                founder = Founder(
                    company_id=company,
                    name=founder_name,
                    linkedin_url=linkedin_profile,
                    short_profile=short_profile,
                    phone_number=phone_no,
                    email=email,
                    photo=photo
                )
                founder.save()

        # Save executive members
        executive_member_count = int(request.POST.get('executive_member_count', 1))
        for i in range(1, executive_member_count + 1):
            executive_member_name = request.POST.get(f'executive_member_{i}_name')
            executive_member_email = request.POST.get(f'executive_member_{i}_email')
            executive_member_designation = request.POST.get(f'executive_member_{i}_designation')

            if executive_member_name and executive_member_email and executive_member_designation :
                executive_member = ExecutiveMember(
                    company_id = company,
                    name = executive_member_name,
                    email = executive_member_email,
                    designation = executive_member_designation
                    
                )
                executive_member.save()

        # Save advisors
        advisor_count = int(request.POST.get('advisor_count', 1))
        for i in range(1, advisor_count + 1):
            advisor_name = request.POST.get(f'advisor_{i}_name')
            advisor_email = request.POST.get(f'advisor_{i}_email')
            advisor_phno = request.POST.get(f'advisor_{i}_phno')

            if advisor_name and advisor_email and advisor_phno :
                advisor = Advisor(
                    company_id = company,
                    name = advisor_name,
                    email = advisor_name,
                    phonenumber = advisor_phno
                    
                )
                advisor.save()

        # Save solved problems
        problem_solved_count = int(request.POST.get('problem_solved_count', 1))
        for i in range(1, problem_solved_count + 1):
            problem_solved = request.POST.get(f'problem_solved_{i}')
            

            if problem_solved :
                solved_problem = SolvedProblem(
                    company_id = company,
                    description = problem_solved
                     
                )
                solved_problem.save()
        
        # Save challenges
        challenge_count = int(request.POST.get('challenge_count', 1))
        for i in range(1, challenge_count + 1):
            challenge = request.POST.get(f'challenge_{i}')
            

            if challenge :
                challenge = Challenge(
                    company_id = company,
                    name = challenge
                     
                )
                challenge.save()

        # Save competitors
        competitor_count = int(request.POST.get('competitor_count', 1))
        for i in range(1, competitor_count + 1):
            competitor = request.POST.get(f'competitor_{i}')
            

            if competitor :
                competitor = Competitor(
                    company_id = company,
                    name = competitor
                     
                )
                competitor.save()

    

        # Save social media URLs
        url_count = int(request.POST.get('url_count', 2))
        for i in range(1, url_count + 1):
            url = request.POST.get(f'url_{i}')
            if url:
                social_media = SocialMedia(
                    company_id=company,
                    url=url
                )
                social_media.save()

        # Save clients
        client_count = int(request.POST.get('client_count', 1))
        for i in range(1, client_count + 1):
            client_name = request.POST.get(f'client_name_{i}')
            client_logo = request.FILES.get(f'client_logo_{i}')
            if client_name and client_logo:
                client = Client(
                    company_id=company,
                    name=client_name,
                    logo=client_logo
                )
                client.save()

        return redirect('add_company')  # Redirect to a success page
    else:
        sectors = Sector.objects.all()
        business_types = BusinessType.objects.all()
        business_stages = BusinessStage.objects.all()
        context = { 'sectors':sectors,'business_types':business_types,'business_stages':business_stages}
        return render(request,'admin/add_company.html',context)






def updateCompany(request, company_id):
    company = get_object_or_404(Company, company_id=company_id)
    company_profile = get_object_or_404(CompanyProfile, company_id=company)
    founders = company.founders.all()
    executive_members = company.executive_members.all()
    advisors = company.advisors.all()
    solved_problems = company.solved_problems.all()
    challenges = company.challenges.all()
    competitors = company.competitors.all()
    clients = company.clients.all()
    social_media_urls = company.social_media_urls.all()

    if request.method == 'POST':
        # Update company data
        company.name = request.POST.get('startup_name')
        company.date_of_incorporation = request.POST.get('date_of_incorporation')
        company.email = request.POST.get('email')
        company.linkedin_url = request.POST.get('linkedin_url')
        company.sector = Sector.objects.get(name=request.POST.get('sector'))
        company.business_type = BusinessType.objects.get(name=request.POST.get('type_of_business'))
        company.website_url = request.POST.get('website_url')
        company.location = request.POST.get('location')
        company.company_type = request.POST.get('product_or_service')
        company.subscription_type = request.POST.get('subscription_type')
        company.save()

        # Update company profile
        company_profile.number_of_clients_users = request.POST.get('no_of_employees')
        company_profile.tam = request.POST.get('tam')
        company_profile.cagr = request.POST.get('cagr')
        company_profile.previous_year_revenue = request.POST.get('previous_year_revenue')
        company_profile.current_year_revenue_arr = request.POST.get('current_year_revenue')
        company_profile.current_monthly_burn_rate = request.POST.get('current_monthly_burn_rate')
        company_profile.forecasted_revenue_for_next_year = request.POST.get('forecasted_revenue_for_next_year')
        company_profile.business_stage = BusinessStage.objects.get(name=request.POST.get('stage_of_business'))
        company_profile.equity_funds_raised_so_far = request.POST.get('equity_funds_raised_so_far')
        company_profile.funds_needed = request.POST.get('funds_needed')
        company_profile.save()

        # Update founders
        founder_count = int(request.POST.get('founder_count', founders.count()))
        for i in range(1, founder_count + 1):
            founder_name = request.POST.get(f'founder_{i}_name')
            linkedin_profile = request.POST.get(f'founder_{i}_linkedin_profile')
            short_profile = request.POST.get(f'founder_{i}_short_profile')
            phone_no = request.POST.get(f'founder_{i}_phone_no')
            email = request.POST.get(f'founder_{i}_email')
            photo = request.FILES.get(f'founder_{i}_photo')

            founder = founders[i - 1]  # Assuming founders is a queryset or list of founders
            founder.name = founder_name
            founder.linkedin_url = linkedin_profile
            founder.short_profile = short_profile
            founder.phone_number = phone_no
            founder.email = email
            if photo:
                founder.photo = photo
            founder.save()

        # Update executive members
        executive_member_count = int(request.POST.get('executive_member_count', executive_members.count()))
        for i in range(1, executive_member_count + 1):
            executive_member_name = request.POST.get(f'executive_member_{i}_name')
            executive_member_email = request.POST.get(f'executive_member_{i}_email')
            executive_member_designation = request.POST.get(f'executive_member_{i}_designation')

            executive_member = executive_members[i - 1]  # Assuming executive_members is a queryset or list of executive members
            executive_member.name = executive_member_name
            executive_member.email = executive_member_email
            executive_member.designation = executive_member_designation
            executive_member.save()

        # Update advisors
        advisor_count = int(request.POST.get('advisor_count', advisors.count()))
        for i in range(1, advisor_count + 1):
            advisor_name = request.POST.get(f'advisor_{i}_name')
            advisor_email = request.POST.get(f'advisor_{i}_email')
            advisor_phno = request.POST.get(f'advisor_{i}_phno')
            
            advisor = advisors[i - 1]  # Assuming advisors is a queryset or list of advisors
            advisor.name = advisor_name
            advisor.email = advisor_email
            advisor.phonenumber = advisor_phno
            advisor.save()

        # Update solved problems
        problem_solved_count = int(request.POST.get('problem_solved_count', solved_problems.count()))
        for i in range(1, problem_solved_count + 1):
            problem_solved = request.POST.get(f'problem_solved_{i}')

            solved_problem = solved_problems[i - 1]  # Assuming solved_problems is a queryset or list of solved problems
            solved_problem.description = problem_solved
            solved_problem.save()

        # Update challenges
        challenge_count = int(request.POST.get('challenge_count', challenges.count()))
        for i in range(1, challenge_count + 1):
            challenge_name = request.POST.get(f'challenge_{i}')

            challenge = challenges[i - 1]  # Assuming challenges is a queryset or list of challenges
            challenge.name = challenge_name
            challenge.save()

        # Update competitors
        competitor_count = int(request.POST.get('competitor_count', competitors.count()))
        for i in range(1, competitor_count + 1):
            competitor_name = request.POST.get(f'competitor_{i}')

            competitor = competitors[i - 1]  # Assuming competitors is a queryset or list of competitors
            competitor.name = competitor_name
            competitor.save()

        # Update social media URLs
        url_count = int(request.POST.get('url_count', social_media_urls.count()))
        for i in range(1, url_count + 1):
            url = request.POST.get(f'url_{i}')
            if url:
                if i <= len(social_media_urls):
                    social_media = social_media_urls[i - 1]
                    social_media.url = url
                    social_media.save()

        # Update clients
        client_count = int(request.POST.get('client_count', clients.count()))
        for i in range(1, client_count + 1):
            client_name = request.POST.get(f'client_{i}')
            client_logo = request.FILES.get(f'client_{i}_logo')

            if client_name:
                if i <= len(clients):
                    client = clients[i - 1]
                    client.name = client_name
                    if client_logo:
                        client.logo = client_logo
                    client.save()


        # Redirect to a success page
        return redirect('update_company', company_id=company_id)
    
    else:
        sectors = Sector.objects.all()
        business_types = BusinessType.objects.all()
        business_stages = BusinessStage.objects.all()
        context = {
            'company': company,
            'company_profile': company_profile,
            'sectors': sectors,
            'business_types': business_types,
            'business_stages': business_stages,
            'founders': founders,
            'executive_members': executive_members,
            'advisors': advisors,
            'solved_problems': solved_problems,
            'challenges': challenges,
            'competitors': competitors,
            'clients':clients,
            'social_media_urls':social_media_urls
        }
        return render(request, 'admin/update_company.html', context)








def companyProfileForm(request,id):
    company = Company.objects.get(company_id = id)

    if request.method == 'POST':
        # company data
        startup_name = request.POST.get('startup_name')
        date_of_incorporation = request.POST.get('date_of_incorporation')
        email = request.POST.get('email')
        linkedin_url = request.POST.get('linkedin_url')
        sector_name = request.POST.get('sector')
        type_of_business = request.POST.get('type_of_business')
        no_of_employees = request.POST.get('no_of_employees')
        website_url = request.POST.get('website_url')
        location = request.POST.get('location')
        product_or_service = request.POST.get('product_or_service')
        subscription_type = request.POST.get('subscription_type')
        #company profile
        tam = request.POST.get('tam')
        cagr = request.POST.get('cagr')
        previous_year_revenue = request.POST.get('previous_year_revenue')
        current_year_revenue = request.POST.get('current_year_revenue')
        current_monthly_burn_rate = request.POST.get('current_monthly_burn_rate')
        forecasted_revenue_for_next_year = request.POST.get('forecasted_revenue_for_next_year')
        stage_of_business = request.POST.get('stage_of_business')
        equity_funds_raised_so_far = request.POST.get('equity_funds_raised_so_far')
        funds_needed = request.POST.get('funds_needed')
       


        #business_introductory_video_file = request.FILES.get('business_introductry_video_file')
        #business_introductory_video_url = request.POST.get('business_introductry_video_url')

        # business_plan = request.FILES.get('business_plan')
        # vision = request.POST.get('vision')
        # mission = request.POST.get('mission')
        # usp = request.POST.get('usp')

        user_context = custom_user(request)
        current_user = user_context.get('current_user') 

        sector = Sector.objects.get(name=sector_name)
        type_of_business = BusinessType.objects.get(name=type_of_business)
        stage_of_business = BusinessStage.objects.get(name=stage_of_business)

        # # Create the Company instance
        company = Company(
            user_id=current_user,  # This should match the foreign key field in Company model
            company_id = company,
            name=startup_name,
            date_of_incorporation = date_of_incorporation,
            email = email,
            linkedin_url = linkedin_url,
            sector = sector,
            business_type = type_of_business,
            website_url=website_url,
            location = location,
            company_type = product_or_service,
            subscription_type = subscription_type
            
        )
        company.save()

        # Create the CompanyProfile instance
        company_profile = CompanyProfile(
            company_id=company,
            number_of_clients_users = no_of_employees, 
            tam = tam,
            cagr = cagr,
            previous_year_revenue = previous_year_revenue,
            current_year_revenue_arr = current_year_revenue,
            current_monthly_burn_rate = current_monthly_burn_rate,
            forecasted_revenue_for_next_year = forecasted_revenue_for_next_year,
            business_stage = stage_of_business,
            equity_funds_raised_so_far = equity_funds_raised_so_far,
            funds_needed = funds_needed

        )
        company_profile.save()

        # Save founders
        founder_count = int(request.POST.get('founder_count', 1))
        for i in range(1, founder_count + 1):
            founder_name = request.POST.get(f'founder_{i}_name')
            linkedin_profile = request.POST.get(f'founder_{i}_linkedin_profile')
            short_profile = request.POST.get(f'founder_{i}_short_profile')
            phone_no = request.POST.get(f'founder_{i}_phno')
            email = request.POST.get(f'founder_{i}_email')
            photo = request.FILES.get(f'founder_{i}_photo')
            if founder_name and linkedin_profile and short_profile and phone_no and email and photo:
                founder = Founder(
                    company_id=company,
                    name=founder_name,
                    linkedin_url=linkedin_profile,
                    short_profile=short_profile,
                    phone_number=phone_no,
                    email=email,
                    photo=photo
                )
                founder.save()

        # Save executive members
        executive_member_count = int(request.POST.get('executive_member_count', 1))
        for i in range(1, executive_member_count + 1):
            executive_member_name = request.POST.get(f'executive_member_{i}_name')
            executive_member_email = request.POST.get(f'executive_member_{i}_email')
            executive_member_designation = request.POST.get(f'executive_member_{i}_designation')

            if executive_member_name and executive_member_email and executive_member_designation :
                executive_member = ExecutiveMember(
                    company_id = company,
                    name = executive_member_name,
                    email = executive_member_email,
                    designation = executive_member_designation
                    
                )
                executive_member.save()

        # Save advisors
        advisor_count = int(request.POST.get('advisor_count', 1))
        for i in range(1, advisor_count + 1):
            advisor_name = request.POST.get(f'advisor_{i}_name')
            advisor_email = request.POST.get(f'advisor_{i}_email')
            advisor_phno = request.POST.get(f'advisor_{i}_phno')

            if advisor_name and advisor_email and advisor_phno :
                advisor = Advisor(
                    company_id = company,
                    name = advisor_name,
                    email = advisor_name,
                    phonenumber = advisor_phno
                    
                )
                advisor.save()

        # Save solved problems
        problem_solved_count = int(request.POST.get('problem_solved_count', 1))
        for i in range(1, problem_solved_count + 1):
            problem_solved = request.POST.get(f'problem_solved_{i}')
            

            if problem_solved :
                solved_problem = SolvedProblem(
                    company_id = company,
                    description = problem_solved
                     
                )
                solved_problem.save()
        
        # Save challenges
        challenge_count = int(request.POST.get('challenge_count', 1))
        for i in range(1, challenge_count + 1):
            challenge = request.POST.get(f'challenge_{i}')
            

            if challenge :
                challenge = Challenge(
                    company_id = company,
                    name = challenge
                     
                )
                challenge.save()

        # Save competitors
        competitor_count = int(request.POST.get('competitor_count', 1))
        for i in range(1, competitor_count + 1):
            competitor = request.POST.get(f'competitor_{i}')
            

            if competitor :
                competitor = Competitor(
                    company_id = company,
                    name = competitor
                     
                )
                competitor.save()

    

        # Save social media URLs
        url_count = int(request.POST.get('url_count', 2))
        for i in range(1, url_count + 1):
            url = request.POST.get(f'url_{i}')
            if url:
                social_media = SocialMedia(
                    company_id=company,
                    url=url
                )
                social_media.save()

        # Save clients
        client_count = int(request.POST.get('client_count', 1))
        for i in range(1, client_count + 1):
            client_name = request.POST.get(f'client_name_{i}')
            client_logo = request.FILES.get(f'client_logo_{i}')
            if client_name and client_logo:
                client = Client(
                    company_id=company,
                    name=client_name,
                    logo=client_logo
                )
                client.save()

        return redirect('add_company')  # Redirect to a success page
    else:
        sectors = Sector.objects.all()
        business_types = BusinessType.objects.all()
        business_stages = BusinessStage.objects.all()
        context = { 'sectors':sectors,'business_types':business_types,'business_stages':business_stages,'company':company}
        return render(request,'admin/company_profile_form.html',context)

def companyProfile(request, id):
    company = get_object_or_404(Company, company_id=id)
    try:
        company_profile = CompanyProfile.objects.get(company_id=id)
    except CompanyProfile.DoesNotExist:
        company_profile = None

    

    if request.method == 'POST':
            # Company profile
            excecutive_summary = request.POST.get('excecutive_summary')
            technology_profile = request.POST.get('technology_profile')
            type_of_industry = request.POST.get('type_of_industry')
            no_of_employees = request.POST.get('no_of_employees')
            ceo = request.POST.get('ceo')
            cfo = request.POST.get('cfo')
            cmo = request.POST.get('cmo')
            vp = request.POST.get('vp')
            # Create the CompanyProfile instance and associate it with the Company instance
            company_profile = CompanyProfile(
            company_id=company,  # Associate with the newly created Company instancec
            excecutive_summary=excecutive_summary,
            technology_profile=technology_profile,
            type_of_industry=type_of_industry,
            no_of_employees=no_of_employees,
            ceo=ceo,
            cfo=cfo,
            cmo=cmo,
            vp=vp
            )
            company_profile.save()

            
            messages.success(request, 'Data saved Successfully')
            return redirect('comprehensive_profile')
    else:
        context = {'company': company,'company_profile': company_profile }
        return render(request, 'admin/company_profile.html', context)
    

def comprehensiveProfile(request,id):
    company_profile = CompanyProfile.objects.get(company_id = id)
    context ={'company_profile': company_profile}

    return render(request, 'admin/comprehensive.html', context)





def businessPlan(request, id):
    company = Company.objects.get(company_id = id)
    company_profile = CompanyProfile.objects.get(company_id = id)
    if request.method == 'POST':
        business_plan = request.FILES.get('business_plan')
        new_business_plan = request.FILES.get('new_business_plan')
        company_profile.business_plan= business_plan
       
        if new_business_plan:
            company_profile.business_plan= new_business_plan
            #company_profile.save()
        company_profile.save()

        return redirect('business_plan',company.company_id)

    else:
        
        context = {
            'company':company,
            'company_profile': company_profile,
        }

        return render(request, 'admin/business_plan.html', context)
    
def pitchAndProduct(request, id):
    company = Company.objects.get(company_id = id)
    company_profile = CompanyProfile.objects.get(company_id = id)
    if request.method == 'POST':
        pitch_video = request.FILES.get('pitch_video')
        new_pitch_video = request.FILES.get('new_pitch_video')
        product_video = request.FILES.get('product_video')
        new_product_video = request.FILES.get('new_product_video')
        company_profile.pitch_video= pitch_video
        company_profile.product_video= product_video

        if new_pitch_video or new_product_video:
            company_profile.pitch_video= new_pitch_video
            company_profile.product_video= new_product_video
            #company_profile.save()
        company_profile.save()
        return redirect('pitch_and_product',company.company_id)

    else:
        
        context = {
            'company':company,
            'company_profile': company_profile,
        }

        return render(request, 'admin/pitch_and_product.html', context)

def capTable(request, id):
    company = Company.objects.get(company_id = id)
    company_profile = CompanyProfile.objects.get(company_id = id)
    cap_table = CapTable.objects.filter(company_id = id)
    context = {
        'company':company,
        'company_profile': company_profile,
        'cap_table': cap_table 
        }
   

    return render(request, 'admin/cap_table.html', context)

def capTableForm(request, id):
    company = Company.objects.get(company_id = id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        linkedin_url = request.POST.get('linkedin_url')
        percentage_of_shares = request.POST.get('percentage_of_shares')
        photo = request.FILES.get('photo')

        cap_table = CapTable(
            company_id = company,
            name = name,
            email = email,
            linkedin_url = linkedin_url,
            percentage_of_shares = percentage_of_shares,
            photo = photo
        )
        cap_table.save()
        messages.success(request,'Data saved successfully')
        return redirect('cap_table',company.company_id)

    else:
        company_profile = CompanyProfile.objects.get(company_id = id)
        
    
        context = {
            'company':company,
            'company_profile': company_profile,
        }

        return render(request, 'admin/cap_table_form.html', context)



def financialStatement(request,id):
    company_profile = CompanyProfile.objects.get(company_id = id)
    homogenous_products = HomogenousProduct.objects.filter(company_id = id)
    heterogenous_products = HeterogenousProduct.objects.filter(company_id = id)
    context ={'company_profile': company_profile,'homogenous_products':homogenous_products,'heterogenous_products':heterogenous_products}

    return render(request,'admin/financial_statement.html',context)


def incomeStatement12(request,id):
    company = Company.objects.get(company_id=id)

    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        begin_date = request.POST.get('begin_date')
        end_date = request.POST.get('end_date')
        #product details
        product_name = request.POST.get('product_name')
        total_revenue = request.POST.get('total_revenue')
        total_taxes = request.POST.get('total_taxes')
        total_dividends = request.POST.get('total_dividends')
        #cost of goods sold details
        total_cogs = request.POST.get('total_cogs')
        cogs_direct_labor = request.POST.get('cogs_direct_labor')
        cogs_material = request.POST.get('cogs_material')
        cogs_parts = request.POST.get('cogs_parts')
        cogs_distribution = request.POST.get('cogs_distribution')
        cogs_other = request.POST.get('cogs_other')
        #operating expense details
        total_operating_expenses = request.POST.get('total_operating_expenses')
        opexpense_rent = request.POST.get('opexpense_rent')
        opexpense_utilities = request.POST.get('opexpense_utilities')
        opexpense_overhead = request.POST.get('opexpense_overhead')
        opexpense_legal = request.POST.get('opexpense_legal')
        opexpense_depreciation = request.POST.get('opexpense_depreciation')
        opexpense_marketing_ads = request.POST.get('opexpense_marketing_ads')
        opexpense_insurance = request.POST.get('opexpense_insurance')
        opexpense_interest = request.POST.get('opexpense_interest')
        opexpense_travel = request.POST.get('opexpense_travel')
        opexpense_wages = request.POST.get('opexpense_wages')
        opexpense_other = request.POST.get('opexpense_other')

        user_context = custom_user(request)
        current_user = user_context.get('current_user') 
                
       

        income_statement = IncomeStatement(
            company_id = company,
            begin_date = begin_date,
            end_date = end_date,

            product_name = product_name,
            total_revenue = total_revenue,
            total_taxes = total_taxes,
            total_dividends = total_dividends,

            total_cogs= total_cogs,
            cogs_direct_labor = cogs_direct_labor,
            cogs_material = cogs_material,
            cogs_parts = cogs_parts,
            cogs_distribution = cogs_distribution,
            cogs_other = cogs_other,

            total_operating_expenses = total_operating_expenses,
            opexpense_rent = opexpense_rent,
            opexpense_utilities = opexpense_utilities,
            opexpense_overhead = opexpense_overhead,
            opexpense_legal = opexpense_legal,
            opexpense_depreciation = opexpense_depreciation,
            opexpense_marketing_ads = opexpense_marketing_ads,
            opexpense_insurance = opexpense_insurance,
            opexpense_interest = opexpense_interest,
            opexpense_travel = opexpense_travel,
            opexpense_wages = opexpense_wages,
            opexpense_other = opexpense_other,

            creator_id = current_user.user_id,
            #modifier_id = modifier_id

        )
        income_statement.save()
        return redirect('planning_budgeting_income_statement_table',company.company_id)


    else:
        context = {'company':company}
        return render(request,'admin/income_statement.html',context)





from calendar import month_abbr
from datetime import date





def get_period_label(begin_date, end_date):
    # Define financial quarters
    quarters = {
        'Q1': (1, 3),  # January to March
        'Q2': (4, 6),  # April to June
        'Q3': (7, 9),  # July to September
        'Q4': (10, 12)  # October to December
    }

    # Check if dates span a full year
    if begin_date == begin_date.replace(month=1, day=1) and end_date == end_date.replace(month=12, day=31):
        return f'{begin_date.strftime("%b %d, %Y")} - {end_date.strftime("%b %d, %Y")}', 'Annually Data'

    # Check if dates span more than one year
    if begin_date.year != end_date.year:
        return f'{begin_date.strftime("%b %d, %Y")} - {end_date.strftime("%b %d, %Y")}', 'Irregular Data'

    # Same month case
    if begin_date.month == end_date.month:
        return month_abbr[begin_date.month], 'Monthly Data'
    
    # Quarterly cases
    for quarter, (start_month, end_month) in quarters.items():
        if begin_date.month == start_month and end_date.month == end_month:
            months = [month_abbr[m] for m in range(start_month, end_month + 1)]
            return f'{quarter} ({", ".join(months)})', 'Quarterly Data'
    
    # Custom or irregular period
    return f'{begin_date.strftime("%b %d, %Y")} - {end_date.strftime("%b %d, %Y")}', 'Irregular Data'



import calendar
import json
from datetime import datetime

def get_months_quarters_years():
    # Get all month names
    months = list(calendar.month_name)[1:]  # Exclude empty string at index 0
    
    # Define quarters
    # quarters = {
    #     'Q1': months[0:3],   # January, February, March
    #     'Q2': months[3:6],   # April, May, June
    #     'Q3': months[6:9],   # July, August, September
    #     'Q4': months[9:12]   # October, November, December
    # }

    # Define quarters with month names
    quarters = {
        'Q1': 'Jan,Feb,Mar',
        'Q2': 'Apr,May,Jun',
        'Q3': 'Jul,Aug,Sep',
        'Q4': 'Oct,Nov,Dec'
    }
    
    # Get the last seven years
    current_year = datetime.now().year
    years = [str(current_year - i) for i in range(7)]
    
    return months, quarters, years

# Example usage
months, quarters, years = get_months_quarters_years()

# # Convert to JSON for embedding in HTML/JavaScript
months_json = json.dumps(months)
#quarters_json = json.dumps(list(quarters.keys()))
quarters_json = json.dumps(quarters)  # No need to list keys; use values directly
years_json = json.dumps(years)

# # Print JSON strings (or send them to your template rendering system)
# print(months_json)
# print(quarters_json)
# print(years_json)


def get_last_seven_years_labels():
    current_year = date.today().year
    return [str(year) for year in range(current_year - 1, current_year - 8, -1)]










    
from datetime import datetime





def incomeStatementTable1(request, id):
    company = Company.objects.get(company_id=id)
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')

        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')
            #print(year, month_name, 'monthly')

            # Convert month name to month number
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)
            
            income_statement = IncomeStatement(
                company_id=company,
                date=date,
                monthly_or_quarterly_or_yearly = month_name 
            )
            income_statement.save()
            return redirect('income_statement', id)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')
            #print(year, quarter, 'quarterly')

            # Map quarters to starting months
            quarter_start_months = {
                'Q1': 1,
                'Q2': 4,
                'Q3': 7,
                'Q4': 10
            }
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)
            
            income_statement = IncomeStatement(
                company_id=company,
                date=date,
                #monthly_or_quarterly_or_yearly = quarter_value +" "+ str(year)
                monthly_or_quarterly_or_yearly = quarter_value 

            )
            income_statement.save()
            return redirect('income_statement', id)

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            #print(year, 'yearly')
            date = datetime(year, 1, 1)
            
            income_statement = IncomeStatement(
                company_id=company,
                date=date,
                monthly_or_quarterly_or_yearly = year
            )
            income_statement.save()
            return redirect('income_statement', id)
    
    else:
        company = Company.objects.get(company_id=id)
        income_statements = IncomeStatement.objects.filter(company_id=id)
        months, quarters, years = get_months_quarters_years()
        
        context = {
            'company': company,
            'income_statements': income_statements,
            'months': months,
            'quarters': quarters,
            'years': years,
            'months_json': months_json,
            'quarters_json': quarters_json,
            'years_json': years_json
        }
        return render(request, 'admin/income_statement_table.html', context)
    
#New
def incomeStatementTable2(request, id):
    company = Company.objects.get(company_id=id)
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')

        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')
            #print(year, month_name, 'monthly')

            # Convert month name to month number
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)


            request.session['monthly_date'] = date
            request.session['monthly_month_name'] = month_name
            
            # income_statement = IncomeStatement(
            #     company_id=company,
            #     date=date,
            #     monthly_or_quarterly_or_yearly = month_name 
            # )
            # income_statement.save()
            return redirect('income_statement', id)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')
            #print(year, quarter, 'quarterly')

            # Map quarters to starting months
            quarter_start_months = {
                'Q1': 1,
                'Q2': 4,
                'Q3': 7,
                'Q4': 10
            }
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)

            request.session['quarterly_date'] = date
            request.session['quarterly_quarter_value'] = quarter_value
            
            # income_statement = IncomeStatement(
            #     company_id=company,
            #     date=date,
            #     #monthly_or_quarterly_or_yearly = quarter_value +" "+ str(year)
            #     monthly_or_quarterly_or_yearly = quarter_value 

            # )
            # income_statement.save()
            return redirect('income_statement', id)

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            #print(year, 'yearly')
            date = datetime(year, 1, 1)

            request.session['yearly_date'] = date
            request.session['yearly_year'] = quarter_value
            
            
            # income_statement = IncomeStatement(
            #     company_id=company,
            #     date=date,
            #     monthly_or_quarterly_or_yearly = year
            # )
            # income_statement.save()
            return redirect('income_statement', id)
    
    else:
        company = Company.objects.get(company_id=id)
        income_statements = IncomeStatement.objects.filter(company_id=id)
        months, quarters, years = get_months_quarters_years()
        
        context = {
            'company': company,
            'income_statements': income_statements,
            'months': months,
            'quarters': quarters,
            'years': years,
            'months_json': months_json,
            'quarters_json': quarters_json,
            'years_json': years_json
        }
        return render(request, 'admin/income_statement_table.html', context)
    

def incomeStatementTable3(request, id):
    company = Company.objects.get(company_id=id)
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')

        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')
            #print(year, month_name, 'monthly')

            # Convert month name to month number
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)


            request.session['monthly_date'] = date
            request.session['monthly_month_name'] = month_name
            
           
            return redirect('income_statement', id)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')
            #print(year, quarter, 'quarterly')

            # Map quarters to starting months
            quarter_start_months = {
                'Q1': 1,
                'Q2': 4,
                'Q3': 7,
                'Q4': 10
            }
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)

            request.session['quarterly_date'] = date
            request.session['quarterly_quarter_value'] = quarter_value
            
            
            return redirect('income_statement', id)

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            #print(year, 'yearly')
            date = datetime(year, 1, 1)

            request.session['yearly_date'] = date
            request.session['yearly_year'] = quarter_value
            
            
            
            return redirect('income_statement', id)
    
    else:
        company = Company.objects.get(company_id=id)
        income_statements = IncomeStatement.objects.filter(company_id=id)
        months, quarters, years = get_months_quarters_years()
        
        context = {
            'company': company,
            'income_statements': income_statements,
            'months': months,
            'quarters': quarters,
            'years': years,
            'months_json': months_json,
            'quarters_json': quarters_json,
            'years_json': years_json
        }
        return render(request, 'admin/income_statement_table.html', context)
    

from datetime import datetime

def incomeStatementTable(request, id):
    company = Company.objects.get(company_id=id)
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')

        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')

            # Convert month name to month number
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)

            request.session['monthly_date'] = date.strftime('%Y-%m-%d')
            request.session['monthly_month_name'] = month_name

            selected_monthly_income_statement= IncomeStatement.objects.filter(company_id=id,date=date,monthly_or_quarterly_or_yearly=month_name)

            if selected_monthly_income_statement:
                messages.error(request,f'Income Statment for {str(year)} {month_name} already exists pls enter next month Statement')
                return redirect('planning_budgeting_income_statement_table',id)

            else:
              return redirect('income_statement', id)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')

            # Map quarters to starting months
            quarter_start_months = {
                'Q1': 1,
                'Q2': 4,
                'Q3': 7,
                'Q4': 10
            }
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)

            request.session['quarterly_date'] = date.strftime('%Y-%m-%d')
            request.session['quarterly_quarter_value'] = quarter_value
            quarterly_quarter_value = request.session.get('quarterly_quarter_value')


            print(quarter_value,'quarter_value')
            print(quarterly_quarter_value,'quarterly_quarter_value')
            

            selected_quarterly_income_statement= IncomeStatement.objects.filter(company_id=id,date=date,monthly_or_quarterly_or_yearly=quarter_value)

            if selected_quarterly_income_statement:
                messages.error(request,f'Income Statment for {str(year)} {quarter_value} already exists pls enter next month Statement')
                return redirect('planning_budgeting_income_statement_table',id)

            else:
              return redirect('income_statement', id)
            
            

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            date = datetime(year, 1, 1)

            request.session['yearly_date'] = date.strftime('%Y-%m-%d')
            request.session['yearly_year'] = year

            selected_yearly_income_statement= IncomeStatement.objects.filter(company_id=id,date=date,monthly_or_quarterly_or_yearly = year)

            if selected_yearly_income_statement:
                messages.error(request,f'Income Statment for {str(year)}  already exists pls enter next month Statement')
                return redirect('planning_budgeting_income_statement_table',id)

            else:
              return redirect('income_statement', id)
            
            
            
    
    else:
        company = Company.objects.get(company_id=id)
        income_statements = IncomeStatement.objects.filter(company_id=id)
        months, quarters, years = get_months_quarters_years()
        
        # context = {
        #     'company': company,
        #     'income_statements': income_statements,
        #     'months': months,
        #     'quarters': quarters,
        #     'years': years,
        # }

        context = {
            'company': company,
            'income_statements': income_statements,
            'months': months,
            'quarters': quarters,
            'years': years,
            'months_json': months_json,
            'quarters_json': quarters_json,
            'years_json': years_json
        }
        return render(request, 'admin/income_statement_table.html', context)



def incomeStatement1(request, id):
    company = Company.objects.get(company_id=id)
    income_statement = IncomeStatement.objects.filter(company_id=id).last()

    if request.method == 'POST':
        # Retrieve and validate POST data
        operating_revenue = request.POST.get('operating_revenue')
        cost_of_revenue = request.POST.get('cost_of_revenue')
        research_and_development_expense = request.POST.get('research_and_development_expense')
        general_and_administrative_expenses = request.POST.get('general_and_administrative_expenses')
        selling_and_marketing_expense = request.POST.get('selling_and_marketing_expense')
        interest_income_non_operating = request.POST.get('interest_income_non_operating')
        interest_expense_non_operating = request.POST.get('interest_expense_non_operating')
        gain_or_loss_on_sale_of_security = request.POST.get('gain_or_loss_on_sale_of_security')
        special_income_or_charges = request.POST.get('special_income_or_charges')
        write_off = request.POST.get('write_off')
        other_non_operating_income_or_expenses = request.POST.get('other_non_operating_income_or_expenses')
        tax_provision = request.POST.get('tax_provision')
        preference_share_dividends = request.POST.get('preference_share_dividends')
        equity_share_dividends = request.POST.get('equity_share_dividends')
        diluted_eps = request.POST.get('diluted_eps')
        depreciation_and_amortization = request.POST.get('depreciation_and_amortization')
        no_of_equity_shares = request.POST.get('no_of_equity_shares')

        # Convert to integers if not None, otherwise set to 0
        operating_revenue = int(operating_revenue) if operating_revenue else 0
        cost_of_revenue = int(cost_of_revenue) if cost_of_revenue else 0
        research_and_development_expense = int(research_and_development_expense) if research_and_development_expense else 0
        general_and_administrative_expenses = int(general_and_administrative_expenses) if general_and_administrative_expenses else 0
        selling_and_marketing_expense = int(selling_and_marketing_expense) if selling_and_marketing_expense else 0
        interest_income_non_operating = int(interest_income_non_operating) if interest_income_non_operating else 0
        interest_expense_non_operating = int(interest_expense_non_operating) if interest_expense_non_operating else 0
        gain_or_loss_on_sale_of_security = int(gain_or_loss_on_sale_of_security) if gain_or_loss_on_sale_of_security else 0
        special_income_or_charges = int(special_income_or_charges) if special_income_or_charges else 0
        write_off = int(write_off) if write_off else 0
        other_non_operating_income_or_expenses = int(other_non_operating_income_or_expenses) if other_non_operating_income_or_expenses else 0
        tax_provision = int(tax_provision) if tax_provision else 0
        preference_share_dividends = int(preference_share_dividends) if preference_share_dividends else 0
        equity_share_dividends = int(equity_share_dividends) if equity_share_dividends else 0
        diluted_eps = int(diluted_eps) if diluted_eps else 0
        depreciation_and_amortization = int(depreciation_and_amortization) if depreciation_and_amortization else 0
        no_of_equity_shares = int(no_of_equity_shares) if no_of_equity_shares else 0

        # Ensure income_statement is not None
        # if income_statement is None:
        #     income_statement = IncomeStatement(company_id=id)

        # Update income statement fields
        income_statement.operating_revenue = operating_revenue
        income_statement.cost_of_revenue = cost_of_revenue
        income_statement.general_and_administrative_expenses = general_and_administrative_expenses
        income_statement.selling_and_marketing_expense = selling_and_marketing_expense
        income_statement.research_and_development_expense = research_and_development_expense
        income_statement.interest_income_non_operating = interest_income_non_operating
        income_statement.interest_expense_non_operating = interest_expense_non_operating
        income_statement.gain_or_loss_on_sale_of_security = gain_or_loss_on_sale_of_security
        income_statement.special_income_or_charges = special_income_or_charges
        income_statement.write_off = write_off
        income_statement.other_non_operating_income_or_expenses = other_non_operating_income_or_expenses
        income_statement.tax_provision = tax_provision
        income_statement.preference_share_dividends = preference_share_dividends
        income_statement.equity_share_dividends = equity_share_dividends
        income_statement.diluted_eps = diluted_eps
        income_statement.depreciation_and_amortization = depreciation_and_amortization
        income_statement.no_of_equity_shares = no_of_equity_shares

        # Calculate derived fields
        income_statement.total_revenue = operating_revenue
        income_statement.gross_profit = income_statement.total_revenue - cost_of_revenue
        income_statement.selling_general_and_administrative_expense = general_and_administrative_expenses + selling_and_marketing_expense
        income_statement.operating_expense = income_statement.selling_general_and_administrative_expense + research_and_development_expense
        income_statement.operating_income = income_statement.gross_profit - income_statement.operating_expense
        income_statement.net_non_operating_interest_income_expense = interest_income_non_operating - interest_expense_non_operating
        income_statement.other_income_or_expense = gain_or_loss_on_sale_of_security + special_income_or_charges + write_off + other_non_operating_income_or_expenses
        income_statement.pretax_income = income_statement.operating_income + income_statement.net_non_operating_interest_income_expense + income_statement.other_income_or_expense
        income_statement.net_income = income_statement.pretax_income - tax_provision
        income_statement.net_income_to_common_stockholders = income_statement.net_income - preference_share_dividends
        income_statement.retained_earnings = income_statement.net_income_to_common_stockholders - equity_share_dividends
        income_statement.basic_eps = income_statement.net_income_to_common_stockholders / no_of_equity_shares
        income_statement.ebitda = income_statement.operating_income + depreciation_and_amortization

        # Save income statement
        income_statement.save()

        return redirect('planning_budgeting_income_statement_table', id)
    else:
        context = {'company': company, 'income_statement': income_statement}
        return render(request, 'admin/income_statement.html', context)

#New
def incomeStatement(request, id):
    company = Company.objects.get(company_id=id)
    #income_statement = IncomeStatement.objects.filter(company_id=id).last()

    if request.method == 'POST':
        # Retrieve and validate POST data
        operating_revenue = request.POST.get('operating_revenue')
        cost_of_revenue = request.POST.get('cost_of_revenue')
        research_and_development_expense = request.POST.get('research_and_development_expense')
        general_and_administrative_expenses = request.POST.get('general_and_administrative_expenses')
        selling_and_marketing_expense = request.POST.get('selling_and_marketing_expense')
        interest_income_non_operating = request.POST.get('interest_income_non_operating')
        interest_expense_non_operating = request.POST.get('interest_expense_non_operating')
        gain_or_loss_on_sale_of_security = request.POST.get('gain_or_loss_on_sale_of_security')
        special_income_or_charges = request.POST.get('special_income_or_charges')
        write_off = request.POST.get('write_off')
        other_non_operating_income_or_expenses = request.POST.get('other_non_operating_income_or_expenses')
        tax_provision = request.POST.get('tax_provision')
        preference_share_dividends = request.POST.get('preference_share_dividends')
        equity_share_dividends = request.POST.get('equity_share_dividends')
        diluted_eps = request.POST.get('diluted_eps')
        depreciation_and_amortization = request.POST.get('depreciation_and_amortization')
        no_of_equity_shares = request.POST.get('no_of_equity_shares')

        # Convert to integers if not None, otherwise set to 0
        operating_revenue = int(operating_revenue) if operating_revenue else 0
        cost_of_revenue = int(cost_of_revenue) if cost_of_revenue else 0
        research_and_development_expense = int(research_and_development_expense) if research_and_development_expense else 0
        general_and_administrative_expenses = int(general_and_administrative_expenses) if general_and_administrative_expenses else 0
        selling_and_marketing_expense = int(selling_and_marketing_expense) if selling_and_marketing_expense else 0
        interest_income_non_operating = int(interest_income_non_operating) if interest_income_non_operating else 0
        interest_expense_non_operating = int(interest_expense_non_operating) if interest_expense_non_operating else 0
        gain_or_loss_on_sale_of_security = int(gain_or_loss_on_sale_of_security) if gain_or_loss_on_sale_of_security else 0
        special_income_or_charges = int(special_income_or_charges) if special_income_or_charges else 0
        write_off = int(write_off) if write_off else 0
        other_non_operating_income_or_expenses = int(other_non_operating_income_or_expenses) if other_non_operating_income_or_expenses else 0
        tax_provision = int(tax_provision) if tax_provision else 0
        preference_share_dividends = int(preference_share_dividends) if preference_share_dividends else 0
        equity_share_dividends = int(equity_share_dividends) if equity_share_dividends else 0
        diluted_eps = int(diluted_eps) if diluted_eps else 0
        depreciation_and_amortization = int(depreciation_and_amortization) if depreciation_and_amortization else 0
        no_of_equity_shares = int(no_of_equity_shares) if no_of_equity_shares else 0

        # Ensure income_statement is not None
        # if income_statement is None:
        #     income_statement = IncomeStatement(company_id=id)

        
        monthly_date  = request.session.get('monthly_date') 
        monthly_month_name = request.session.get('monthly_month_name')
        quarterly_date  = request.session.get('quarterly_date') 
        quarterly_quarter_value = request.session.get('quarterly_quarter_value')
        yearly_date  = request.session.get('yearly_date') 
        yearly_year  = request.session.get('yearly_year') 

        if monthly_date and monthly_month_name:
            date = monthly_date
            monthly_or_quarterly_or_yearly = monthly_month_name
        if quarterly_date and quarterly_quarter_value:
            date = quarterly_date
            monthly_or_quarterly_or_yearly = quarterly_quarter_value
        if yearly_date and yearly_year:
            date = yearly_date
            monthly_or_quarterly_or_yearly = yearly_year

        print(date,'date')
        print(monthly_or_quarterly_or_yearly,'monthly_or_quarterly_or_yearly')


        # Update income statement fields
        operating_revenue = operating_revenue
        cost_of_revenue = cost_of_revenue
        general_and_administrative_expenses = general_and_administrative_expenses
        selling_and_marketing_expense = selling_and_marketing_expense
        research_and_development_expense = research_and_development_expense
        interest_income_non_operating = interest_income_non_operating
        interest_expense_non_operating = interest_expense_non_operating
        gain_or_loss_on_sale_of_security = gain_or_loss_on_sale_of_security
        special_income_or_charges = special_income_or_charges
        write_off = write_off
        other_non_operating_income_or_expenses = other_non_operating_income_or_expenses
        tax_provision = tax_provision
        preference_share_dividends = preference_share_dividends
        equity_share_dividends = equity_share_dividends
        diluted_eps = diluted_eps
        depreciation_and_amortization = depreciation_and_amortization
        no_of_equity_shares = no_of_equity_shares

        # Calculate derived fields
        total_revenue = operating_revenue
        gross_profit = total_revenue - cost_of_revenue
        selling_general_and_administrative_expense = general_and_administrative_expenses + selling_and_marketing_expense
        operating_expense = selling_general_and_administrative_expense + research_and_development_expense
        operating_income = gross_profit - operating_expense
        net_non_operating_interest_income_expense = interest_income_non_operating - interest_expense_non_operating
        other_income_or_expense = gain_or_loss_on_sale_of_security + special_income_or_charges + write_off + other_non_operating_income_or_expenses
        pretax_income = operating_income + net_non_operating_interest_income_expense + other_income_or_expense
        net_income = pretax_income - tax_provision
        net_income_to_common_stockholders = net_income - preference_share_dividends
        retained_earnings = net_income_to_common_stockholders - equity_share_dividends
        basic_eps = net_income_to_common_stockholders / no_of_equity_shares
        ebitda = operating_income + depreciation_and_amortization

        income_statement = IncomeStatement (
            company_id = company,
            date = date,
            operating_revenue = operating_revenue,
            cost_of_revenue = cost_of_revenue,
            general_and_administrative_expenses = general_and_administrative_expenses,
            selling_and_marketing_expense = selling_and_marketing_expense,
            research_and_development_expense = research_and_development_expense,
            interest_income_non_operating = interest_income_non_operating,
            interest_expense_non_operating = interest_expense_non_operating,
            gain_or_loss_on_sale_of_security = gain_or_loss_on_sale_of_security,
            special_income_or_charges = special_income_or_charges,
            write_off = write_off,
            other_non_operating_income_or_expenses = other_non_operating_income_or_expenses,
            tax_provision = tax_provision,
            preference_share_dividends = preference_share_dividends,
            equity_share_dividends = equity_share_dividends,
            diluted_eps = diluted_eps,
            depreciation_and_amortization = depreciation_and_amortization,
            no_of_equity_shares = no_of_equity_shares,
            total_revenue = total_revenue,
            gross_profit = gross_profit,
            selling_general_and_administrative_expense = selling_general_and_administrative_expense,
            operating_expense = operating_expense,
            operating_income = operating_income,
            net_non_operating_interest_income_expense = net_non_operating_interest_income_expense,
            other_income_or_expense = other_income_or_expense,
            pretax_income = pretax_income,
            net_income = net_income,
            net_income_to_common_stockholders = net_income_to_common_stockholders,
            retained_earnings = retained_earnings,
            basic_eps = basic_eps,
            ebitda = ebitda,
            monthly_or_quarterly_or_yearly = monthly_or_quarterly_or_yearly

        )

        # Save income statement
        income_statement.save()

        return redirect('planning_budgeting_income_statement_table', id)
    else:
        # context = {'company': company, 'income_statement': income_statement}
        context = {'company': company}
        return render(request, 'admin/income_statement.html', context)






def balanceSheetTable1(request, id):
    company = Company.objects.get(company_id=id)
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')

        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')
            #print(year, month_name, 'monthly')

            # Convert month name to month number
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)
            
            balance_sheet = BalanceSheet(
                company_id=company,
                date=date,
                monthly_or_quarterly_or_yearly = month_name 
            )
            balance_sheet.save()
            return redirect('balance_sheet', id)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')
            #print(year, quarter, 'quarterly')

            # Map quarters to starting months
            quarter_start_months = {
                'Q1': 1,
                'Q2': 4,
                'Q3': 7,
                'Q4': 10
            }
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)
            
            balance_sheet = BalanceSheet(
                company_id=company,
                date=date,
                #monthly_or_quarterly_or_yearly = quarter_value +" "+ str(year)
                monthly_or_quarterly_or_yearly = quarter_value 

            )
            balance_sheet.save()
            return redirect('balance_sheet', id)

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            #print(year, 'yearly')
            date = datetime(year, 1, 1)
            
            balance_sheet = BalanceSheet(
                company_id=company,
                date=date,
                monthly_or_quarterly_or_yearly = year
            )
            balance_sheet.save()
            return redirect('balance_sheet', id)
    
    else:
        company = Company.objects.get(company_id=id)
        balance_sheets = BalanceSheet.objects.filter(company_id=id)
        months, quarters, years = get_months_quarters_years()
        
        context = {
            'company': company,
            'balance_sheets': balance_sheets,
            'months': months,
            'quarters': quarters,
            'years': years,
            'months_json': months_json,
            'quarters_json': quarters_json,
            'years_json': years_json
        }
        return render(request, 'admin/balance_sheet_table.html', context)


#New
def balanceSheetTable(request, id):
    company = Company.objects.get(company_id=id)
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')

        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')
            #print(year, month_name, 'monthly')

            # Convert month name to month number
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)
            
            # balance_sheet = BalanceSheet(
            #     company_id=company,
            #     date=date,
            #     monthly_or_quarterly_or_yearly = month_name 
            # )
            # balance_sheet.save()

            request.session['balance_sheet_monthly_date'] = date.strftime('%Y-%m-%d')
            request.session['balance_sheet_monthly_month_name'] = month_name

            selected_monthly_balance_sheet= BalanceSheet.objects.filter(company_id=id,date=date,monthly_or_quarterly_or_yearly=month_name)

            if selected_monthly_balance_sheet:
                messages.error(request,f'Balance Sheet for {str(year)} {month_name} already exists pls enter next month Statement')
                return redirect('planning_budgeting_balance_sheet_table',id)
            else:
              return redirect('balance_sheet', id)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')
            #print(year, quarter, 'quarterly')

            # Map quarters to starting months
            quarter_start_months = {
                'Q1': 1,
                'Q2': 4,
                'Q3': 7,
                'Q4': 10
            }
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)
            
            # balance_sheet = BalanceSheet(
            #     company_id=company,
            #     date=date,
            #     #monthly_or_quarterly_or_yearly = quarter_value +" "+ str(year)
            #     monthly_or_quarterly_or_yearly = quarter_value 

            # )
            # balance_sheet.save()
            request.session['balance_sheet_quarterly_date'] = date.strftime('%Y-%m-%d')
            request.session['balance_sheet_quarterly_quarter_value'] = quarter_value

            selected_quarterly_balance_sheet= BalanceSheet.objects.filter(company_id=id,date=date,monthly_or_quarterly_or_yearly=quarter_value)

            if selected_quarterly_balance_sheet:
                messages.error(request,f'Balance Sheet for {str(year)} {quarter_value} already exists pls enter next month Statement')
                return redirect('planning_budgeting_balance_sheet_table',id)
            else:
              return redirect('balance_sheet', id)
            

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            #print(year, 'yearly')
            date = datetime(year, 1, 1)
            
            # balance_sheet = BalanceSheet(
            #     company_id=company,
            #     date=date,
            #     monthly_or_quarterly_or_yearly = year
            # )
            # balance_sheet.save()
            request.session['balance_sheet_yearly_date'] = date.strftime('%Y-%m-%d')
            request.session['balance_sheet_yearly_year'] = year
            selected_yearly_balance_sheet= BalanceSheet.objects.filter(company_id=id,date=date,monthly_or_quarterly_or_yearly=year)

            if selected_yearly_balance_sheet:
                messages.error(request,f'Balance Sheet for {str(year)} already exists pls enter next month Statement')
                return redirect('planning_budgeting_balance_sheet_table',id)
            else:
              return redirect('balance_sheet', id)
            
    
    else:
        company = Company.objects.get(company_id=id)
        balance_sheets = BalanceSheet.objects.filter(company_id=id)
        months, quarters, years = get_months_quarters_years()
        
        context = {
            'company': company,
            'balance_sheets': balance_sheets,
            'months': months,
            'quarters': quarters,
            'years': years,
            'months_json': months_json,
            'quarters_json': quarters_json,
            'years_json': years_json
        }
        return render(request, 'admin/balance_sheet_table.html', context)


def balanceSheet1(request, id):
    company = Company.objects.get(company_id=id)
    balance_sheet = BalanceSheet.objects.filter(company_id=id).last()

    if request.method == 'POST':
        # Retrieve and validate POST data
        cash = request.POST.get('cash')
        cash_equivalents = request.POST.get('cash_equivalents')
        other_short_term_investments = request.POST.get('other_short_term_investments')
        gross_accounts_receivable = request.POST.get('gross_accounts_receivable')
        allowance_for_doubtful_accounts_receivable = request.POST.get('allowance_for_doubtful_accounts_receivable')
        other_receivables = request.POST.get('other_receivables')
        raw_materials = request.POST.get('raw_materials')
        work_in_process = request.POST.get('work_in_process')
        finished_goods = request.POST.get('finished_goods')
        hedging_current_assets = request.POST.get('hedging_current_assets')
        other_current_assets = request.POST.get('other_current_assets')
        land_and_improvements = request.POST.get('land_and_improvements')
        buildings_and_improvements = request.POST.get('buildings_and_improvements')
        machinery_furniture_equipment = request.POST.get('machinery_furniture_equipment')
        other_properties = request.POST.get('other_properties')
        leases = request.POST.get('leases')
        accumulated_depreciation = request.POST.get('accumulated_depreciation')
        goodwill = request.POST.get('goodwill')
        other_intangible_assets = request.POST.get('other_intangible_assets')
        long_term_equity_investment = request.POST.get('long_term_equity_investment')
        other_non_current_assets = request.POST.get('other_non_current_assets')
        accounts_payable = request.POST.get('accounts_payable')
        income_tax_payable = request.POST.get('income_tax_payable')
        pension_and_other_post_retirement_benefit_plans_current = request.POST.get('pension_and_other_post_retirement_benefit_plans_current')
        current_debt = request.POST.get('current_debt')
        capital_lease_obligation = request.POST.get('capital_lease_obligation')
        current_deferred_revenue = request.POST.get('current_deferred_revenue')
        other_current_liabilities = request.POST.get('other_current_liabilities')
        long_term_debt = request.POST.get('long_term_debt')
        long_term_capital_lease_obligation = request.POST.get('long_term_capital_lease_obligation')
        non_current_deferred_taxes_liabilities = request.POST.get('non_current_deferred_taxes_liabilities')
        non_current_deferred_revenue = request.POST.get('non_current_deferred_revenue')
        trade_and_other_payables_non_current = request.POST.get('trade_and_other_payables_non_current')
        other_non_current_liabilities = request.POST.get('other_non_current_liabilities')
        common_stock = request.POST.get('common_stock')
        retained_earnings = request.POST.get('retained_earnings')
        gains_or_losses_not_affecting_retained_earnings = request.POST.get('gains_or_losses_not_affecting_retained_earnings')
        other_equity_adjustments = request.POST.get('other_equity_adjustments')


        

        # Convert to integers if not None, otherwise set to 0
        cash = int(cash) if cash else 0
        cash_equivalents = int(cash_equivalents) if cash_equivalents else 0
        other_short_term_investments = int(other_short_term_investments) if other_short_term_investments else 0
        gross_accounts_receivable = int(gross_accounts_receivable) if gross_accounts_receivable else 0
        allowance_for_doubtful_accounts_receivable = int(allowance_for_doubtful_accounts_receivable) if allowance_for_doubtful_accounts_receivable else 0
        other_receivables = int(other_receivables) if other_receivables else 0
        raw_materials = int(raw_materials) if raw_materials else 0
        work_in_process = int(work_in_process) if work_in_process else 0
        finished_goods = int(finished_goods) if finished_goods else 0
        hedging_current_assets = int(hedging_current_assets) if hedging_current_assets else 0
        other_current_assets = int(other_current_assets) if other_current_assets else 0
        land_and_improvements = int(land_and_improvements) if land_and_improvements else 0
        buildings_and_improvements = int(buildings_and_improvements) if buildings_and_improvements else 0
        machinery_furniture_equipment = int(machinery_furniture_equipment) if machinery_furniture_equipment else 0
        other_properties = int(other_properties) if other_properties else 0
        leases = int(leases) if leases else 0
        accumulated_depreciation = int(accumulated_depreciation) if accumulated_depreciation else 0
        goodwill = int(goodwill) if goodwill else 0
        other_intangible_assets = int(other_intangible_assets) if other_intangible_assets else 0
        long_term_equity_investment = int(long_term_equity_investment) if long_term_equity_investment else 0
        other_non_current_assets = int(other_non_current_assets) if other_non_current_assets else 0
        accounts_payable = int(accounts_payable) if accounts_payable else 0
        income_tax_payable = int(income_tax_payable) if income_tax_payable else 0
        pension_and_other_post_retirement_benefit_plans_current = int(pension_and_other_post_retirement_benefit_plans_current) if pension_and_other_post_retirement_benefit_plans_current else 0
        current_debt = int(current_debt) if current_debt else 0
        capital_lease_obligation = int(capital_lease_obligation) if capital_lease_obligation else 0
        current_deferred_revenue = int(current_deferred_revenue) if current_deferred_revenue else 0
        other_current_liabilities = int(other_current_liabilities) if other_current_liabilities else 0
        long_term_debt = int(long_term_debt) if long_term_debt else 0
        long_term_capital_lease_obligation = int(long_term_capital_lease_obligation) if long_term_capital_lease_obligation else 0
        non_current_deferred_taxes_liabilities = int(non_current_deferred_taxes_liabilities) if non_current_deferred_taxes_liabilities else 0
        non_current_deferred_revenue = int(non_current_deferred_revenue) if non_current_deferred_revenue else 0
        trade_and_other_payables_non_current = int(trade_and_other_payables_non_current) if trade_and_other_payables_non_current else 0
        other_non_current_liabilities = int(other_non_current_liabilities) if other_non_current_liabilities else 0
        common_stock = int(common_stock) if common_stock else 0
        retained_earnings = int(retained_earnings) if retained_earnings else 0
        gains_or_losses_not_affecting_retained_earnings = int(gains_or_losses_not_affecting_retained_earnings) if gains_or_losses_not_affecting_retained_earnings else 0
        other_equity_adjustments = int(other_equity_adjustments) if other_equity_adjustments else 0

        

        # Ensure income_statement is not None
        # if income_statement is None:
        #     income_statement = IncomeStatement(company_id=id)

        # Update income statement fields
        balance_sheet.cash = cash
        balance_sheet.cash_equivalents = cash_equivalents
        balance_sheet.other_short_term_investments = other_short_term_investments
        balance_sheet.gross_accounts_receivable = gross_accounts_receivable
        balance_sheet.allowance_for_doubtful_accounts_receivable = allowance_for_doubtful_accounts_receivable 
        balance_sheet.other_receivables = other_receivables
        balance_sheet.raw_materials = raw_materials
        balance_sheet.work_in_process = work_in_process
        balance_sheet.finished_goods = finished_goods
        balance_sheet.hedging_current_assets = hedging_current_assets
        balance_sheet.other_current_assets = other_current_assets
        balance_sheet.land_and_improvements = land_and_improvements
        balance_sheet.buildings_and_improvements = buildings_and_improvements
        balance_sheet.machinery_furniture_equipment = machinery_furniture_equipment
        balance_sheet.other_properties = other_properties
        balance_sheet.leases = leases
        balance_sheet.accumulated_depreciation = accumulated_depreciation
        balance_sheet.goodwill = goodwill
        balance_sheet.other_intangible_assets = other_intangible_assets
        balance_sheet.long_term_equity_investment = long_term_equity_investment
        balance_sheet.other_non_current_assets = other_non_current_assets
        balance_sheet.accounts_payable = accounts_payable
        balance_sheet.income_tax_payable = income_tax_payable
        balance_sheet.pension_and_other_post_retirement_benefit_plans_current = pension_and_other_post_retirement_benefit_plans_current
        balance_sheet.current_debt = current_debt
        balance_sheet.capital_lease_obligation = capital_lease_obligation
        balance_sheet.current_deferred_revenue = current_deferred_revenue
        balance_sheet.other_current_liabilities = other_current_liabilities
        balance_sheet.long_term_debt = long_term_debt
        balance_sheet.long_term_capital_lease_obligation = long_term_capital_lease_obligation
        balance_sheet.non_current_deferred_taxes_liabilities = non_current_deferred_taxes_liabilities
        balance_sheet.non_current_deferred_revenue = non_current_deferred_revenue
        balance_sheet.trade_and_other_payables_non_current = trade_and_other_payables_non_current
        balance_sheet.other_non_current_liabilities = other_non_current_liabilities
        balance_sheet.common_stock = common_stock
        balance_sheet.retained_earnings = retained_earnings 
        balance_sheet.gains_or_losses_not_affecting_retained_earnings = gains_or_losses_not_affecting_retained_earnings
        balance_sheet.other_equity_adjustments = other_equity_adjustments
        
        
        # Calculate derived fields
        balance_sheet.cash_and_cash_equivalents = cash + cash_equivalents
        balance_sheet.inventory = raw_materials + work_in_process + finished_goods
        balance_sheet.capital_stock = common_stock
        balance_sheet.cash_cash_equivalents_and_short_term_investments = balance_sheet.cash_and_cash_equivalents + other_short_term_investments
        balance_sheet.accounts_receivable = gross_accounts_receivable + allowance_for_doubtful_accounts_receivable
        balance_sheet.receivables = balance_sheet.accounts_receivable + other_receivables
        balance_sheet.current_assets = balance_sheet.cash_cash_equivalents_and_short_term_investments + balance_sheet.receivables + balance_sheet.inventory + hedging_current_assets + other_current_assets
        balance_sheet.gross_ppe = land_and_improvements + buildings_and_improvements + machinery_furniture_equipment + other_properties + leases
        balance_sheet.net_ppe = balance_sheet.gross_ppe + accumulated_depreciation
        balance_sheet.goodwill_and_other_intangible_assets = goodwill + other_intangible_assets
        balance_sheet.investments_and_advances = long_term_equity_investment
        balance_sheet.total_non_current_assets = balance_sheet.net_ppe + balance_sheet.goodwill_and_other_intangible_assets + balance_sheet.investments_and_advances + other_non_current_assets
        balance_sheet.total_assets = balance_sheet.current_assets + balance_sheet.total_non_current_assets
        balance_sheet.payables_and_accrued_expenses = accounts_payable + income_tax_payable
        balance_sheet.current_debt_and_capital_lease_obligation = current_debt + capital_lease_obligation
        balance_sheet.current_deferred_liabilities = current_deferred_revenue
        balance_sheet.current_liabilities = balance_sheet.payables_and_accrued_expenses + pension_and_other_post_retirement_benefit_plans_current + balance_sheet.current_debt_and_capital_lease_obligation + balance_sheet.current_deferred_liabilities + other_current_liabilities
        balance_sheet.long_term_debt_and_capital_lease_obligation = long_term_debt + capital_lease_obligation
        balance_sheet.non_current_deferred_liabilities = non_current_deferred_taxes_liabilities + non_current_deferred_revenue 
        balance_sheet.total_non_current_liabilities_net_minority_interest = balance_sheet.long_term_debt_and_capital_lease_obligation + balance_sheet.non_current_deferred_liabilities + trade_and_other_payables_non_current + other_non_current_liabilities
        balance_sheet.total_liabilities_net_minority_interest = balance_sheet.current_liabilities + balance_sheet.total_non_current_liabilities_net_minority_interest
        balance_sheet.stockholders_equity = balance_sheet.capital_stock + retained_earnings + gains_or_losses_not_affecting_retained_earnings + other_equity_adjustments
        balance_sheet.total_equity_gross_minority_interest = balance_sheet.stockholders_equity
        # Save balance sheet
        balance_sheet.save()

        return redirect('planning_budgeting_balance_sheet_table', id)
    else:
        context = {'company': company, 'balance_sheet': balance_sheet}
        return render(request, 'admin/balance_sheet.html', context)

#New   
def balanceSheet(request, id):
    company = Company.objects.get(company_id=id)
    #balance_sheet = BalanceSheet.objects.filter(company_id=id).last()

    if request.method == 'POST':
        # Retrieve and validate POST data
        cash = request.POST.get('cash')
        cash_equivalents = request.POST.get('cash_equivalents')
        other_short_term_investments = request.POST.get('other_short_term_investments')
        gross_accounts_receivable = request.POST.get('gross_accounts_receivable')
        allowance_for_doubtful_accounts_receivable = request.POST.get('allowance_for_doubtful_accounts_receivable')
        other_receivables = request.POST.get('other_receivables')
        raw_materials = request.POST.get('raw_materials')
        work_in_process = request.POST.get('work_in_process')
        finished_goods = request.POST.get('finished_goods')
        hedging_current_assets = request.POST.get('hedging_current_assets')
        other_current_assets = request.POST.get('other_current_assets')
        land_and_improvements = request.POST.get('land_and_improvements')
        buildings_and_improvements = request.POST.get('buildings_and_improvements')
        machinery_furniture_equipment = request.POST.get('machinery_furniture_equipment')
        other_properties = request.POST.get('other_properties')
        leases = request.POST.get('leases')
        accumulated_depreciation = request.POST.get('accumulated_depreciation')
        goodwill = request.POST.get('goodwill')
        other_intangible_assets = request.POST.get('other_intangible_assets')
        long_term_equity_investment = request.POST.get('long_term_equity_investment')
        other_non_current_assets = request.POST.get('other_non_current_assets')
        accounts_payable = request.POST.get('accounts_payable')
        income_tax_payable = request.POST.get('income_tax_payable')
        pension_and_other_post_retirement_benefit_plans_current = request.POST.get('pension_and_other_post_retirement_benefit_plans_current')
        current_debt = request.POST.get('current_debt')
        capital_lease_obligation = request.POST.get('capital_lease_obligation')
        current_deferred_revenue = request.POST.get('current_deferred_revenue')
        other_current_liabilities = request.POST.get('other_current_liabilities')
        long_term_debt = request.POST.get('long_term_debt')
        long_term_capital_lease_obligation = request.POST.get('long_term_capital_lease_obligation')
        non_current_deferred_taxes_liabilities = request.POST.get('non_current_deferred_taxes_liabilities')
        non_current_deferred_revenue = request.POST.get('non_current_deferred_revenue')
        trade_and_other_payables_non_current = request.POST.get('trade_and_other_payables_non_current')
        other_non_current_liabilities = request.POST.get('other_non_current_liabilities')
        common_stock = request.POST.get('common_stock')
        retained_earnings = request.POST.get('retained_earnings')
        gains_or_losses_not_affecting_retained_earnings = request.POST.get('gains_or_losses_not_affecting_retained_earnings')
        other_equity_adjustments = request.POST.get('other_equity_adjustments')


        

        # Convert to integers if not None, otherwise set to 0
        cash = int(cash) if cash else 0
        cash_equivalents = int(cash_equivalents) if cash_equivalents else 0
        other_short_term_investments = int(other_short_term_investments) if other_short_term_investments else 0
        gross_accounts_receivable = int(gross_accounts_receivable) if gross_accounts_receivable else 0
        allowance_for_doubtful_accounts_receivable = int(allowance_for_doubtful_accounts_receivable) if allowance_for_doubtful_accounts_receivable else 0
        other_receivables = int(other_receivables) if other_receivables else 0
        raw_materials = int(raw_materials) if raw_materials else 0
        work_in_process = int(work_in_process) if work_in_process else 0
        finished_goods = int(finished_goods) if finished_goods else 0
        hedging_current_assets = int(hedging_current_assets) if hedging_current_assets else 0
        other_current_assets = int(other_current_assets) if other_current_assets else 0
        land_and_improvements = int(land_and_improvements) if land_and_improvements else 0
        buildings_and_improvements = int(buildings_and_improvements) if buildings_and_improvements else 0
        machinery_furniture_equipment = int(machinery_furniture_equipment) if machinery_furniture_equipment else 0
        other_properties = int(other_properties) if other_properties else 0
        leases = int(leases) if leases else 0
        accumulated_depreciation = int(accumulated_depreciation) if accumulated_depreciation else 0
        goodwill = int(goodwill) if goodwill else 0
        other_intangible_assets = int(other_intangible_assets) if other_intangible_assets else 0
        long_term_equity_investment = int(long_term_equity_investment) if long_term_equity_investment else 0
        other_non_current_assets = int(other_non_current_assets) if other_non_current_assets else 0
        accounts_payable = int(accounts_payable) if accounts_payable else 0
        income_tax_payable = int(income_tax_payable) if income_tax_payable else 0
        pension_and_other_post_retirement_benefit_plans_current = int(pension_and_other_post_retirement_benefit_plans_current) if pension_and_other_post_retirement_benefit_plans_current else 0
        current_debt = int(current_debt) if current_debt else 0
        capital_lease_obligation = int(capital_lease_obligation) if capital_lease_obligation else 0
        current_deferred_revenue = int(current_deferred_revenue) if current_deferred_revenue else 0
        other_current_liabilities = int(other_current_liabilities) if other_current_liabilities else 0
        long_term_debt = int(long_term_debt) if long_term_debt else 0
        long_term_capital_lease_obligation = int(long_term_capital_lease_obligation) if long_term_capital_lease_obligation else 0
        non_current_deferred_taxes_liabilities = int(non_current_deferred_taxes_liabilities) if non_current_deferred_taxes_liabilities else 0
        non_current_deferred_revenue = int(non_current_deferred_revenue) if non_current_deferred_revenue else 0
        trade_and_other_payables_non_current = int(trade_and_other_payables_non_current) if trade_and_other_payables_non_current else 0
        other_non_current_liabilities = int(other_non_current_liabilities) if other_non_current_liabilities else 0
        common_stock = int(common_stock) if common_stock else 0
        retained_earnings = int(retained_earnings) if retained_earnings else 0
        gains_or_losses_not_affecting_retained_earnings = int(gains_or_losses_not_affecting_retained_earnings) if gains_or_losses_not_affecting_retained_earnings else 0
        other_equity_adjustments = int(other_equity_adjustments) if other_equity_adjustments else 0

        

        # Ensure income_statement is not None
        # if income_statement is None:
        #     income_statement = IncomeStatement(company_id=id)

        balance_sheet_monthly_date  = request.session.get('balance_sheet_monthly_date') 
        balance_sheet_monthly_month_name = request.session.get('balance_sheet_monthly_month_name')
        balance_sheet_quarterly_date  = request.session.get('balance_sheet_quarterly_date') 
        balance_sheet_quarterly_quarter_value = request.session.get('balance_sheet_quarterly_quarter_value')
        balance_sheet_yearly_date  = request.session.get('balance_sheet_yearly_date') 
        balance_sheet_yearly_year  = request.session.get('balance_sheet_yearly_year')

        if balance_sheet_monthly_date and balance_sheet_monthly_month_name:
            date = balance_sheet_monthly_date
            monthly_or_quarterly_or_yearly = balance_sheet_monthly_month_name
        if balance_sheet_quarterly_date and balance_sheet_quarterly_quarter_value:
            date = balance_sheet_quarterly_date
            monthly_or_quarterly_or_yearly = balance_sheet_quarterly_quarter_value
        if balance_sheet_yearly_date and balance_sheet_yearly_year:
            date = balance_sheet_yearly_date
            monthly_or_quarterly_or_yearly = balance_sheet_yearly_year

        # Update income statement fields
        cash = cash
        cash_equivalents = cash_equivalents
        other_short_term_investments = other_short_term_investments
        gross_accounts_receivable = gross_accounts_receivable
        allowance_for_doubtful_accounts_receivable = allowance_for_doubtful_accounts_receivable 
        other_receivables = other_receivables
        raw_materials = raw_materials
        work_in_process = work_in_process
        finished_goods = finished_goods
        hedging_current_assets = hedging_current_assets
        other_current_assets = other_current_assets
        land_and_improvements = land_and_improvements
        buildings_and_improvements = buildings_and_improvements
        machinery_furniture_equipment = machinery_furniture_equipment
        other_properties = other_properties
        leases = leases
        accumulated_depreciation = accumulated_depreciation
        goodwill = goodwill
        other_intangible_assets = other_intangible_assets
        long_term_equity_investment = long_term_equity_investment
        other_non_current_assets = other_non_current_assets
        accounts_payable = accounts_payable
        income_tax_payable = income_tax_payable
        pension_and_other_post_retirement_benefit_plans_current = pension_and_other_post_retirement_benefit_plans_current
        current_debt = current_debt
        capital_lease_obligation = capital_lease_obligation
        current_deferred_revenue = current_deferred_revenue
        other_current_liabilities = other_current_liabilities
        long_term_debt = long_term_debt
        long_term_capital_lease_obligation = long_term_capital_lease_obligation
        non_current_deferred_taxes_liabilities = non_current_deferred_taxes_liabilities
        non_current_deferred_revenue = non_current_deferred_revenue
        trade_and_other_payables_non_current = trade_and_other_payables_non_current
        other_non_current_liabilities = other_non_current_liabilities
        common_stock = common_stock
        retained_earnings = retained_earnings 
        gains_or_losses_not_affecting_retained_earnings = gains_or_losses_not_affecting_retained_earnings
        other_equity_adjustments = other_equity_adjustments
        
        
        # Calculate derived fields
        cash_and_cash_equivalents = cash + cash_equivalents
        inventory = raw_materials + work_in_process + finished_goods
        capital_stock = common_stock
        cash_cash_equivalents_and_short_term_investments = cash_and_cash_equivalents + other_short_term_investments
        accounts_receivable = gross_accounts_receivable + allowance_for_doubtful_accounts_receivable
        receivables = accounts_receivable + other_receivables
        current_assets = cash_cash_equivalents_and_short_term_investments + receivables + inventory + hedging_current_assets + other_current_assets
        gross_ppe = land_and_improvements + buildings_and_improvements + machinery_furniture_equipment + other_properties + leases
        net_ppe = gross_ppe + accumulated_depreciation
        goodwill_and_other_intangible_assets = goodwill + other_intangible_assets
        investments_and_advances = long_term_equity_investment
        total_non_current_assets = net_ppe + goodwill_and_other_intangible_assets + investments_and_advances + other_non_current_assets
        total_assets = current_assets + total_non_current_assets
        payables_and_accrued_expenses = accounts_payable + income_tax_payable
        current_debt_and_capital_lease_obligation = current_debt + capital_lease_obligation
        current_deferred_liabilities = current_deferred_revenue
        current_liabilities = payables_and_accrued_expenses + pension_and_other_post_retirement_benefit_plans_current + current_debt_and_capital_lease_obligation + current_deferred_liabilities + other_current_liabilities
        long_term_debt_and_capital_lease_obligation = long_term_debt + capital_lease_obligation
        non_current_deferred_liabilities = non_current_deferred_taxes_liabilities + non_current_deferred_revenue 
        total_non_current_liabilities_net_minority_interest = long_term_debt_and_capital_lease_obligation + non_current_deferred_liabilities + trade_and_other_payables_non_current + other_non_current_liabilities
        total_liabilities_net_minority_interest = current_liabilities + total_non_current_liabilities_net_minority_interest
        stockholders_equity = capital_stock + retained_earnings + gains_or_losses_not_affecting_retained_earnings + other_equity_adjustments
        total_equity_gross_minority_interest = stockholders_equity

        balance_sheet = BalanceSheet(
            company_id = company,
            date = date,
            cash = cash,
            cash_equivalents = cash_equivalents,
            other_short_term_investments = other_short_term_investments,
            gross_accounts_receivable = gross_accounts_receivable,
            allowance_for_doubtful_accounts_receivable = allowance_for_doubtful_accounts_receivable,
            other_receivables = other_receivables,
            raw_materials = raw_materials,
            work_in_process = work_in_process,
            finished_goods = finished_goods,
            hedging_current_assets = hedging_current_assets,
            other_current_assets = other_current_assets,
            land_and_improvements = land_and_improvements,
            buildings_and_improvements = buildings_and_improvements,
            machinery_furniture_equipment = machinery_furniture_equipment,
            other_properties = other_properties,
            leases = leases,
            accumulated_depreciation = accumulated_depreciation,
            goodwill = goodwill,
            other_intangible_assets = other_intangible_assets,
            long_term_equity_investment = long_term_equity_investment,
            other_non_current_assets = other_non_current_assets,
            accounts_payable = accounts_payable,
            income_tax_payable = income_tax_payable,
            pension_and_other_post_retirement_benefit_plans_current = pension_and_other_post_retirement_benefit_plans_current,
            current_debt = current_debt,
            capital_lease_obligation = capital_lease_obligation,
            current_deferred_revenue = current_deferred_revenue,
            other_current_liabilities = other_current_liabilities,
            long_term_debt = long_term_debt,
            long_term_capital_lease_obligation = long_term_capital_lease_obligation,
            non_current_deferred_taxes_liabilities = non_current_deferred_taxes_liabilities,
            non_current_deferred_revenue = non_current_deferred_revenue,
            trade_and_other_payables_non_current = trade_and_other_payables_non_current,
            other_non_current_liabilities = other_non_current_liabilities,
            common_stock = common_stock,
            retained_earnings = retained_earnings,
            gains_or_losses_not_affecting_retained_earnings = gains_or_losses_not_affecting_retained_earnings,
            other_equity_adjustments = other_equity_adjustments,
            cash_and_cash_equivalents = cash_and_cash_equivalents,
            inventory = inventory,
            capital_stock = capital_stock,
            cash_cash_equivalents_and_short_term_investments = cash_cash_equivalents_and_short_term_investments,
            accounts_receivable = accounts_receivable,
            receivables = receivables,
            current_assets = current_assets,
            gross_ppe = gross_ppe,
            net_ppe = net_ppe,
            goodwill_and_other_intangible_assets = goodwill_and_other_intangible_assets,
            investments_and_advances = investments_and_advances,
            total_non_current_assets = total_non_current_assets,
            total_assets = total_assets,
            payables_and_accrued_expenses = payables_and_accrued_expenses,
            current_debt_and_capital_lease_obligation = current_debt_and_capital_lease_obligation,
            current_deferred_liabilities = current_deferred_liabilities,
            current_liabilities = current_liabilities,
            long_term_debt_and_capital_lease_obligation = long_term_debt_and_capital_lease_obligation,
            non_current_deferred_liabilities = non_current_deferred_liabilities,
            total_non_current_liabilities_net_minority_interest = total_non_current_liabilities_net_minority_interest,
            total_liabilities_net_minority_interest = total_liabilities_net_minority_interest,
            stockholders_equity = stockholders_equity,
            total_equity_gross_minority_interest = total_equity_gross_minority_interest,
            monthly_or_quarterly_or_yearly = monthly_or_quarterly_or_yearly
  

        )



        # Save balance sheet
        balance_sheet.save()

        return redirect('planning_budgeting_balance_sheet_table', id)
    else:
        #context = {'company': company, 'balance_sheet': balance_sheet}
        context = {'company': company}

        return render(request, 'admin/balance_sheet.html', context)


from django.shortcuts import redirect, render
from django.utils.timezone import datetime, timedelta
from django.contrib import messages
from .models import CashFlow, BalanceSheet, IncomeStatement

def cashFlowTableOld(request, id):
    company = Company.objects.get(company_id=id)
    
    def check_previous_entry_exists(date, company, period_type):
        # Calculate the previous period based on the type
        if period_type == 'monthly':
            # First day of the previous month
            previous_month = date.replace(day=1) - timedelta(days=1)
            previous_period_date = previous_month.replace(day=1)
        elif period_type == 'quarterly':
            # Calculate the start month of the previous quarter
            previous_quarter_start_month = ((date.month - 1) // 3 * 3) - 3
            if previous_quarter_start_month < 1:
                previous_quarter_start_month = 10
                year = date.year - 1
            else:
                year = date.year
            previous_period_date = datetime(year, previous_quarter_start_month, 1)
        elif period_type == 'yearly':
            # Start of the previous year
            previous_period_date = datetime(date.year - 1, 1, 1)
        
        # Check if the previous period exists in BalanceSheet or IncomeStatement
        # period_exists = (
        #     BalanceSheet.objects.filter(company_id=company, date=previous_period_date).exists() or
        #     IncomeStatement.objects.filter(company_id=company, date=previous_period_date).exists()
        # )
        period_exists = (
            BalanceSheet.objects.filter(company_id=company, date=previous_period_date).exists() and
            IncomeStatement.objects.filter(company_id=company, date=previous_period_date).exists()
        )
        
        return period_exists
    
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')
        



        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)

            # cpee= check_previous_entry_exists(date, company, 'monthly')
            # print(cpee,'cpee')
            
            if not check_previous_entry_exists(date, company, 'monthly'):
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous month.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=month_name 
                )
                cash_flow.save()
                return redirect('cash_flow', id)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')

            quarter_start_months = {
                'Q1': 1,
                'Q2': 4,
                'Q3': 7,
                'Q4': 10
            }
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)
            
            if not check_previous_entry_exists(date, company, 'quarterly'):
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous quarter.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=quarter_value
                )
                cash_flow.save()
                return redirect('cash_flow', id)

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            date = datetime(year, 1, 1)
            
            if not check_previous_entry_exists(date, company, 'yearly'):
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous year.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=year
                )
                cash_flow.save()
                return redirect('cash_flow', id)
    
    cash_flows = CashFlow.objects.filter(company_id=id)
    months, quarters, years = get_months_quarters_years()
    
    context = {
        'company': company,
        'cash_flows': cash_flows,
        'months': months,
        'quarters': quarters,
        'years': years,
        'months_json': months_json,
        'quarters_json': quarters_json,
        'years_json': years_json
    }
    return render(request, 'admin/cash_flow_table.html', context)



def cashFlowTableOld1(request, id):
    company = Company.objects.get(company_id=id)
    
    def check_previous_entry_exists(date, company, period_type):
        # Calculate the previous period based on the type
        if period_type == 'monthly':
            # First day of the previous month
            previous_month = date.replace(day=1) - timedelta(days=1)
            previous_period_date = previous_month.replace(day=1)
        elif period_type == 'quarterly':
            # Calculate the start month of the previous quarter
            previous_quarter_start_month = ((date.month - 1) // 3 * 3) - 3
            if previous_quarter_start_month < 1:
                previous_quarter_start_month = 10
                year = date.year - 1
            else:
                year = date.year
            previous_period_date = datetime(year, previous_quarter_start_month, 1)
        elif period_type == 'yearly':
            # Start of the previous year
            previous_period_date = datetime(date.year - 1, 1, 1)
        
        # Check if the previous period exists in BalanceSheet or IncomeStatement
        # period_exists = (
        #     BalanceSheet.objects.filter(company_id=company, date=previous_period_date).exists() or
        #     IncomeStatement.objects.filter(company_id=company, date=previous_period_date).exists()
        # )
        period_exists = (
            BalanceSheet.objects.filter(company_id=company, date=previous_period_date).exists() and
            IncomeStatement.objects.filter(company_id=company, date=previous_period_date).exists()
        )
        
        return period_exists
    
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')
        



        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)

            # cpee= check_previous_entry_exists(date, company, 'monthly')
            # print(cpee,'cpee')
            
            if not check_previous_entry_exists(date, company, 'monthly'):
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous month.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=month_name 
                )
                cash_flow.save()
                return redirect('cash_flow', id)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')

            quarter_start_months = {
                'Q1': 1,
                'Q2': 4,
                'Q3': 7,
                'Q4': 10
            }
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)
            
            if not check_previous_entry_exists(date, company, 'quarterly'):
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous quarter.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=quarter_value
                )
                cash_flow.save()
                return redirect('cash_flow', id)

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            date = datetime(year, 1, 1)
            
            if not check_previous_entry_exists(date, company, 'yearly'):
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous year.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=year
                )
                cash_flow.save()
                return redirect('cash_flow', id)
    
    cash_flows = CashFlow.objects.filter(company_id=id)
    months, quarters, years = get_months_quarters_years()
    
    context = {
        'company': company,
        'cash_flows': cash_flows,
        'months': months,
        'quarters': quarters,
        'years': years,
        'months_json': months_json,
        'quarters_json': quarters_json,
        'years_json': years_json
    }
    return render(request, 'admin/cash_flow_table.html', context)




def check_previous_entry_exists(date, company, period_type):
    # Calculate the previous period based on the type
    if period_type == 'monthly':
        # First day of the previous month
        previous_month = date.replace(day=1) - timedelta(days=1)
        previous_period_date = previous_month.replace(day=1)
    elif period_type == 'quarterly':
        # Calculate the start month of the previous quarter
        previous_quarter_start_month = ((date.month - 1) // 3 * 3) - 3
        if previous_quarter_start_month < 1:
            previous_quarter_start_month = 10
            year = date.year - 1
        else:
            year = date.year
        previous_period_date = datetime(year, previous_quarter_start_month, 1)
    elif period_type == 'yearly':
        # Start of the previous year
        previous_period_date = datetime(date.year - 1, 1, 1)

    # Retrieve the previous period BalanceSheet and IncomeStatement
    previous_balance_sheet = BalanceSheet.objects.filter(company_id=company, date=previous_period_date).first()
    previous_income_statement = IncomeStatement.objects.filter(company_id=company, date=previous_period_date).first()
    
    # Check if the previous period exists in BalanceSheet and IncomeStatement
    period_exists = previous_balance_sheet and previous_income_statement
    
    return period_exists, previous_period_date, previous_balance_sheet, previous_income_statement



def cashFlowTableNew(request, id):
    company = Company.objects.get(company_id=id)
    
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')

        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)
            
            period_exists, previous_period_date, previous_balance_sheet, previous_income_statement = check_previous_entry_exists(date, company, 'monthly')
            print(previous_period_date,previous_income_statement,'previous_income_statement')
            print(previous_period_date,previous_balance_sheet,'previous_balance_sheet')

            balance_sheet = BalanceSheet.objects.filter(company_id=id,monthly_or_quarterly_or_yearly=select_type_of_data)
            income_statement = IncomeStatement.objects.filter(company_id=id,monthly_or_quarterly_or_yearly=select_type_of_data)
            print('balance_sheet',balance_sheet)
            print('income_statement',income_statement)

            
            if not period_exists:
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous month.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=month_name 
                )
                cash_flow.save()
                return redirect('cash_flow', id)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')

            quarter_start_months = {
                'Q1': 1,
                'Q2': 4,
                'Q3': 7,
                'Q4': 10
            }
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)
            
            period_exists, previous_period_date, previous_balance_sheet, previous_income_statement = check_previous_entry_exists(date, company, 'quarterly')
           
            
            if not period_exists:
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous quarter.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=quarter_value
                )
                cash_flow.save()
                return redirect('cash_flow', id)

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            date = datetime(year, 1, 1)
            
            period_exists, previous_period_date, previous_balance_sheet, previous_income_statement = check_previous_entry_exists(date, company, 'yearly')
            print(previous_period_date,previous_income_statement,'previous_income_statement')
            print(previous_period_date,previous_balance_sheet,'previous_balance_sheet')
            
            if not period_exists:
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous year.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=year
                )
                cash_flow.save()
                return redirect('cash_flow', id)
    
    cash_flows = CashFlow.objects.filter(company_id=id)
    months, quarters, years = get_months_quarters_years()
    
    context = {
        'company': company,
        'cash_flows': cash_flows,
        'months': months,
        'quarters': quarters,
        'years': years,
        'months_json': months_json,
        'quarters_json': quarters_json,
        'years_json': years_json
    }
    return render(request, 'admin/cash_flow_table.html', context)



def get_balance_sheet_and_income_statement(date, company):
    balance_sheet = BalanceSheet.objects.filter(company_id=company, date=date).first()
    income_statement = IncomeStatement.objects.filter(company_id=company, date=date).first()
    return balance_sheet, income_statement

def cashFlowTable11(request, id):
    company = Company.objects.get(company_id=id)
    
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')

        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)
            
            period_exists, previous_period_date, previous_balance_sheet, previous_income_statement = check_previous_entry_exists(date, company, 'monthly')
            current_balance_sheet, current_income_statement = get_balance_sheet_and_income_statement(date, company)

            print(previous_period_date,previous_income_statement,'previous_income_statement')
            print(previous_period_date,previous_balance_sheet,'previous_balance_sheet')
            print(current_balance_sheet,'current_balance_sheet')
            print(current_income_statement,'current_income_statement')

            
            if not period_exists:
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous month.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=month_name 
                )
                cash_flow.save()
                return redirect('cash_flow', id)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')

            quarter_start_months = {
                'Q1': 1,
                'Q2': 4,
                'Q3': 7,
                'Q4': 10
            }
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)
            
            period_exists, previous_period_date, previous_balance_sheet, previous_income_statement = check_previous_entry_exists(date, company, 'quarterly')
            current_balance_sheet, current_income_statement = get_balance_sheet_and_income_statement(date, company)
            
            if not period_exists:
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous quarter.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=quarter_value
                )
                cash_flow.save()
                return redirect('cash_flow', id)

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            date = datetime(year, 1, 1)
            
            period_exists, previous_period_date, previous_balance_sheet, previous_income_statement = check_previous_entry_exists(date, company, 'yearly')
            current_balance_sheet, current_income_statement = get_balance_sheet_and_income_statement(date, company)
            
            if not period_exists:
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous year.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=year
                )
                cash_flow.save()
                return redirect('cash_flow', id)
    
    cash_flows = CashFlow.objects.filter(company_id=id)
    months, quarters, years = get_months_quarters_years()
    
    context = {
        'company': company,
        'cash_flows': cash_flows,
        'months': months,
        'quarters': quarters,
        'years': years,
        'months_json': months_json,
        'quarters_json': quarters_json,
        'years_json': years_json,
        'current_balance_sheet': current_balance_sheet if request.method == 'POST' else None,
        'current_income_statement': current_income_statement if request.method == 'POST' else None,
        'previous_balance_sheet': previous_balance_sheet if request.method == 'POST' else None,
        'previous_income_statement': previous_income_statement if request.method == 'POST' else None,
    }
    return render(request, 'admin/cash_flow_table.html', context)




def get_balance_sheet_and_income_statement(date, company):
    balance_sheet = BalanceSheet.objects.filter(company_id=company, date=date).first()
    income_statement = IncomeStatement.objects.filter(company_id=company, date=date).first()
    return balance_sheet, income_statement

def cashFlowTableNew1(request, id):
    company = Company.objects.get(company_id=id)
    
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')

        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)
            
            period_exists, previous_period_date, previous_balance_sheet, previous_income_statement = check_previous_entry_exists(date, company, 'monthly')
            current_balance_sheet, current_income_statement = get_balance_sheet_and_income_statement(date, company)
            print(previous_balance_sheet,'previous_balance_sheet')
            print(previous_income_statement,'previous_income_statement')
            print(current_balance_sheet,'current_balance_sheet')
            print(current_income_statement,'current_income_statement')
            
            if not current_balance_sheet or not current_income_statement:
                messages.error(request, 'Please fill Income Statement and Balance Sheet for the current period.')
            elif not period_exists:
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous month.')

            

            else:

                net_income_from_continuing_operations = current_income_statement.net_income 
                depreciation_and_amortization = current_income_statement.depreciation_and_amortization
                changes_in_receivables = previous_balance_sheet.receivables - current_balance_sheet.receivables
                change_in_inventory = previous_balance_sheet.inventory - current_balance_sheet.inventory
                change_in_hedging_assets_current = previous_balance_sheet.hedging_current_assets - current_balance_sheet.hedging_current_assets
                change_in_other_current_assets = previous_balance_sheet.other_current_assets - current_balance_sheet.other_current_assets
                change_in_payables_and_accrued_expense =  current_balance_sheet.payables_and_accrued_expenses - previous_balance_sheet.payables_and_accrued_expenses
                change_in_pension_and_other_post_retirement_benefit_plans_current = current_balance_sheet.pension_and_other_post_retirement_benefit_plans_current - previous_balance_sheet.pension_and_other_post_retirement_benefit_plans_current
                change_in_current_debt_and_capital_lease_obligation = current_balance_sheet.current_debt_and_capital_lease_obligation - previous_balance_sheet.current_debt_and_capital_lease_obligation
                change_in_current_deferred_liabilities = current_balance_sheet.current_deferred_liabilities - previous_balance_sheet.current_deferred_liabilities
                change_in_other_current_liabilities = current_balance_sheet.other_current_liabilities - previous_balance_sheet.other_current_liabilities
                change_in_working_capital = ( changes_in_receivables + change_in_inventory + change_in_hedging_assets_current + change_in_other_current_assets + change_in_payables_and_accrued_expense + 
                change_in_pension_and_other_post_retirement_benefit_plans_current + change_in_current_debt_and_capital_lease_obligation + change_in_current_deferred_liabilities + change_in_other_current_liabilities ),
                operating_cash_flow = net_income_from_continuing_operations + depreciation_and_amortization + change_in_working_capital
                net_ppe_purchase_and_sale = previous_balance_sheet.gross_ppe - current_balance_sheet.gross_ppe
                goodwill_and_other_intangible_assets = previous_balance_sheet.goodwill_and_other_intangible_assets - current_balance_sheet.goodwill_and_other_intangible_assets
                investments_and_advances = previous_balance_sheet.investments_and_advances - current_balance_sheet.investments_and_advances
                other_non_current_assets = previous_balance_sheet.other_non_current_assets - current_balance_sheet.other_non_current_assets
                cash_flow_from_continuing_investing_activities = ( net_ppe_purchase_and_sale + goodwill_and_other_intangible_assets + investments_and_advances +  other_non_current_assets )
                investing_cash_flow = cash_flow_from_continuing_investing_activities
                long_term_debt_and_capital_lease_obligation = current_balance_sheet.long_term_capital_lease_obligation - previous_balance_sheet.long_term_capital_lease_obligation
                non_current_deferred_liabilities = current_balance_sheet.non_current_deferred_liabilities - previous_balance_sheet.non_current_deferred_liabilities
                trade_and_other_payables_non_current = current_balance_sheet.trade_and_other_payables_non_current - previous_balance_sheet.trade_and_other_payables_non_current
                other_non_current_liabilities = current_balance_sheet.other_non_current_liabilities - previous_balance_sheet.other_non_current_liabilities
                common_stock_issuance_payments = current_balance_sheet.common_stock - previous_balance_sheet.common_stock
                common_stock_dividend_paid = current_income_statement.equity_share_dividends 
                cash_flow_from_continuing_financing_activities = ( long_term_debt_and_capital_lease_obligation +  non_current_deferred_liabilities + trade_and_other_payables_non_current + other_non_current_liabilities +
                                                                   common_stock_issuance_payments + common_stock_dividend_paid )
                financing_cash_flow = cash_flow_from_continuing_financing_activities
                changes_in_cash = operating_cash_flow + investing_cash_flow + financing_cash_flow
                beginning_cash_position = previous_balance_sheet.cash_cash_equivalents_and_short_term_investments
                end_cash_position = changes_in_cash + beginning_cash_position
                capital_expenditure = net_ppe_purchase_and_sale 
                issuance_repurchase_of_capital_stock = common_stock_issuance_payments
                repayment_of_debt = long_term_debt_and_capital_lease_obligation 
                free_cash_flow = end_cash_position + capital_expenditure + issuance_repurchase_of_capital_stock + repayment_of_debt
 
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    net_income_from_continuing_operations = net_income_from_continuing_operations,
                    depreciation_and_amortization = depreciation_and_amortization,
                    changes_in_receivables = changes_in_receivables,
                    change_in_inventory = change_in_inventory,
                    change_in_hedging_assets_current = change_in_hedging_assets_current,
                    change_in_other_current_assets = change_in_other_current_assets,
                    change_in_payables_and_accrued_expense = change_in_payables_and_accrued_expense,
                    change_in_pension_and_other_post_retirement_benefit_plans_current = change_in_pension_and_other_post_retirement_benefit_plans_current,
                    change_in_current_debt_and_capital_lease_obligation = change_in_current_debt_and_capital_lease_obligation,
                    change_in_current_deferred_liabilities = change_in_current_deferred_liabilities,
                    change_in_other_current_liabilities = change_in_other_current_liabilities,
                    change_in_working_capital = change_in_working_capital,
                    operating_cash_flow = operating_cash_flow,
                    net_ppe_purchase_and_sale = net_ppe_purchase_and_sale,
                    goodwill_and_other_intangible_assets = goodwill_and_other_intangible_assets,
                    investments_and_advances = investments_and_advances,
                    other_non_current_assets = other_non_current_assets,
                    cash_flow_from_continuing_investing_activities = cash_flow_from_continuing_investing_activities,
                    investing_cash_flow = investing_cash_flow,
                    long_term_debt_and_capital_lease_obligation = long_term_debt_and_capital_lease_obligation,
                    non_current_deferred_liabilities = non_current_deferred_liabilities,
                    trade_and_other_payables_non_current = trade_and_other_payables_non_current,
                    other_non_current_liabilities = other_non_current_liabilities,
                    common_stock_issuance_payments = common_stock_issuance_payments,
                    common_stock_dividend_paid = common_stock_dividend_paid,
                    cash_flow_from_continuing_financing_activities = cash_flow_from_continuing_financing_activities,

                    financing_cash_flow = financing_cash_flow,
                    changes_in_cash = changes_in_cash,
                    beginning_cash_position = beginning_cash_position,
                    end_cash_position = end_cash_position,
                    capital_expenditure = capital_expenditure,
                    issuance_repurchase_of_capital_stock = issuance_repurchase_of_capital_stock,
                    repayment_of_debt = repayment_of_debt,
                    free_cash_flow = free_cash_flow,
                    monthly_or_quarterly_or_yearly=month_name 
                )
                cash_flow.save()
                return redirect('cash_flow', id)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')

            quarter_start_months = {
                'Q1': 1,
                'Q2': 4,
                'Q3': 7,
                'Q4': 10
            }
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)
            
            period_exists, previous_period_date, previous_balance_sheet, previous_income_statement = check_previous_entry_exists(date, company, 'quarterly')
            current_balance_sheet, current_income_statement = get_balance_sheet_and_income_statement(date, company)
            
            if not current_balance_sheet or not current_income_statement:
                messages.error(request, 'Please fill Income Statement and Balance Sheet for the current period.')
            elif not period_exists:
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous quarter.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=quarter_value
                )
                cash_flow.save()
                return redirect('cash_flow', id)

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            date = datetime(year, 1, 1)
            
            period_exists, previous_period_date, previous_balance_sheet, previous_income_statement = check_previous_entry_exists(date, company, 'yearly')
            current_balance_sheet, current_income_statement = get_balance_sheet_and_income_statement(date, company)
            
            if not current_balance_sheet or not current_income_statement:
                messages.error(request, 'Please fill Income Statement and Balance Sheet for the current period.')
            elif not period_exists:
                messages.error(request, 'No previous entry exists in BalanceSheet or IncomeStatement for the previous year.')
            else:
                cash_flow = CashFlow(
                    company_id=company,
                    date=date,
                    monthly_or_quarterly_or_yearly=year
                )
                cash_flow.save()
                return redirect('cash_flow', id)
    
    cash_flows = CashFlow.objects.filter(company_id=id)
    months, quarters, years = get_months_quarters_years()
    
    context = {
        'company': company,
        'cash_flows': cash_flows,
        'months': months,
        'quarters': quarters,
        'years': years,
        'months_json': months_json,
        'quarters_json': quarters_json,
        'years_json': years_json,
        'current_balance_sheet': current_balance_sheet if request.method == 'POST' else None,
        'current_income_statement': current_income_statement if request.method == 'POST' else None,
        'previous_balance_sheet': previous_balance_sheet if request.method == 'POST' else None,
        'previous_income_statement': previous_income_statement if request.method == 'POST' else None,
    }
    return render(request, 'admin/cash_flow_table.html', context)








def calculate_cash_flow1(current_balance_sheet, current_income_statement, previous_balance_sheet, previous_income_statement):
    net_income_from_continuing_operations = current_income_statement.net_income 
    depreciation_and_amortization = current_income_statement.depreciation_and_amortization
    changes_in_receivables = previous_balance_sheet.receivables - current_balance_sheet.receivables
    change_in_inventory = previous_balance_sheet.inventory - current_balance_sheet.inventory
    change_in_hedging_assets_current = previous_balance_sheet.hedging_current_assets - current_balance_sheet.hedging_current_assets
    change_in_other_current_assets = previous_balance_sheet.other_current_assets - current_balance_sheet.other_current_assets
    change_in_payables_and_accrued_expense =  current_balance_sheet.payables_and_accrued_expenses - previous_balance_sheet.payables_and_accrued_expenses
    change_in_pension_and_other_post_retirement_benefit_plans_current = current_balance_sheet.pension_and_other_post_retirement_benefit_plans_current - previous_balance_sheet.pension_and_other_post_retirement_benefit_plans_current
    change_in_current_debt_and_capital_lease_obligation = current_balance_sheet.current_debt_and_capital_lease_obligation - previous_balance_sheet.current_debt_and_capital_lease_obligation
    change_in_current_deferred_liabilities = current_balance_sheet.current_deferred_liabilities - previous_balance_sheet.current_deferred_liabilities
    change_in_other_current_liabilities = current_balance_sheet.other_current_liabilities - previous_balance_sheet.other_current_liabilities
    change_in_working_capital = ( changes_in_receivables + change_in_inventory + change_in_hedging_assets_current + change_in_other_current_assets + change_in_payables_and_accrued_expense + 
    change_in_pension_and_other_post_retirement_benefit_plans_current + change_in_current_debt_and_capital_lease_obligation + change_in_current_deferred_liabilities + change_in_other_current_liabilities )
    operating_cash_flow = net_income_from_continuing_operations + depreciation_and_amortization + change_in_working_capital
    net_ppe_purchase_and_sale = previous_balance_sheet.gross_ppe - current_balance_sheet.gross_ppe
    goodwill_and_other_intangible_assets = previous_balance_sheet.goodwill_and_other_intangible_assets - current_balance_sheet.goodwill_and_other_intangible_assets
    investments_and_advances = previous_balance_sheet.investments_and_advances - current_balance_sheet.investments_and_advances
    other_non_current_assets = previous_balance_sheet.other_non_current_assets - current_balance_sheet.other_non_current_assets
    cash_flow_from_continuing_investing_activities = ( net_ppe_purchase_and_sale + goodwill_and_other_intangible_assets + investments_and_advances +  other_non_current_assets )
    investing_cash_flow = cash_flow_from_continuing_investing_activities
    long_term_debt_and_capital_lease_obligation = current_balance_sheet.long_term_capital_lease_obligation - previous_balance_sheet.long_term_capital_lease_obligation
    non_current_deferred_liabilities = current_balance_sheet.non_current_deferred_liabilities - previous_balance_sheet.non_current_deferred_liabilities
    trade_and_other_payables_non_current = current_balance_sheet.trade_and_other_payables_non_current - previous_balance_sheet.trade_and_other_payables_non_current
    other_non_current_liabilities = current_balance_sheet.other_non_current_liabilities - previous_balance_sheet.other_non_current_liabilities
    common_stock_issuance_payments = current_balance_sheet.common_stock - previous_balance_sheet.common_stock
    common_stock_dividend_paid = current_income_statement.equity_share_dividends 
    cash_flow_from_continuing_financing_activities = ( long_term_debt_and_capital_lease_obligation +  non_current_deferred_liabilities + trade_and_other_payables_non_current + other_non_current_liabilities +
                                                       common_stock_issuance_payments + common_stock_dividend_paid )
    financing_cash_flow = cash_flow_from_continuing_financing_activities
    changes_in_cash = operating_cash_flow + investing_cash_flow + financing_cash_flow
    beginning_cash_position = previous_balance_sheet.cash_cash_equivalents_and_short_term_investments
    end_cash_position = changes_in_cash + beginning_cash_position
    capital_expenditure = net_ppe_purchase_and_sale 
    issuance_repurchase_of_capital_stock = common_stock_issuance_payments
    repayment_of_debt = long_term_debt_and_capital_lease_obligation 
    free_cash_flow = end_cash_position + capital_expenditure + issuance_repurchase_of_capital_stock + repayment_of_debt

    return {
        'net_income_from_continuing_operations': net_income_from_continuing_operations,
        'depreciation_and_amortization': depreciation_and_amortization,
        'changes_in_receivables': changes_in_receivables,
        'change_in_inventory': change_in_inventory,
        'change_in_hedging_assets_current': change_in_hedging_assets_current,
        'change_in_other_current_assets': change_in_other_current_assets,
        'change_in_payables_and_accrued_expense': change_in_payables_and_accrued_expense,
        'change_in_pension_and_other_post_retirement_benefit_plans_current': change_in_pension_and_other_post_retirement_benefit_plans_current,
        'change_in_current_debt_and_capital_lease_obligation': change_in_current_debt_and_capital_lease_obligation,
        'change_in_current_deferred_liabilities': change_in_current_deferred_liabilities,
        'change_in_other_current_liabilities': change_in_other_current_liabilities,
        'change_in_working_capital': change_in_working_capital,
        'operating_cash_flow': operating_cash_flow,
        'net_ppe_purchase_and_sale': net_ppe_purchase_and_sale,
        'goodwill_and_other_intangible_assets': goodwill_and_other_intangible_assets,
        'investments_and_advances': investments_and_advances,
        'other_non_current_assets': other_non_current_assets,
        'cash_flow_from_continuing_investing_activities': cash_flow_from_continuing_investing_activities,
        'investing_cash_flow': investing_cash_flow,
        'long_term_debt_and_capital_lease_obligation': long_term_debt_and_capital_lease_obligation,
        'non_current_deferred_liabilities': non_current_deferred_liabilities,
        'trade_and_other_payables_non_current': trade_and_other_payables_non_current,
        'other_non_current_liabilities': other_non_current_liabilities,
        'common_stock_issuance_payments': common_stock_issuance_payments,
        'common_stock_dividend_paid': common_stock_dividend_paid,
        'cash_flow_from_continuing_financing_activities': cash_flow_from_continuing_financing_activities,
        'financing_cash_flow': financing_cash_flow,
        'changes_in_cash': changes_in_cash,
        'beginning_cash_position': beginning_cash_position,
        'end_cash_position': end_cash_position,
        'capital_expenditure': capital_expenditure,
        'issuance_repurchase_of_capital_stock': issuance_repurchase_of_capital_stock,
        'repayment_of_debt': repayment_of_debt,
        'free_cash_flow': free_cash_flow
    }




def calculate_cash_flow(current_balance_sheet, current_income_statement, previous_balance_sheet, previous_income_statement):
    net_income_from_continuing_operations = float(current_income_statement.net_income) 
    depreciation_and_amortization = float(current_income_statement.depreciation_and_amortization)
    changes_in_receivables = float(previous_balance_sheet.receivables) - float(current_balance_sheet.receivables)
    change_in_inventory = float(previous_balance_sheet.inventory) - float(current_balance_sheet.inventory)
    change_in_hedging_assets_current = float(previous_balance_sheet.hedging_current_assets) - float(current_balance_sheet.hedging_current_assets)
    change_in_other_current_assets = float(previous_balance_sheet.other_current_assets) - float(current_balance_sheet.other_current_assets)
    change_in_payables_and_accrued_expense =  float(current_balance_sheet.payables_and_accrued_expenses) - float(previous_balance_sheet.payables_and_accrued_expenses)
    change_in_pension_and_other_post_retirement_benefit_plans_current = float(current_balance_sheet.pension_and_other_post_retirement_benefit_plans_current) - float(previous_balance_sheet.pension_and_other_post_retirement_benefit_plans_current)
    change_in_current_debt_and_capital_lease_obligation = float(current_balance_sheet.current_debt_and_capital_lease_obligation) - float(previous_balance_sheet.current_debt_and_capital_lease_obligation)
    change_in_current_deferred_liabilities = float(current_balance_sheet.current_deferred_liabilities) - float(previous_balance_sheet.current_deferred_liabilities)
    change_in_other_current_liabilities = float(current_balance_sheet.other_current_liabilities) - float(previous_balance_sheet.other_current_liabilities)
    change_in_working_capital = ( changes_in_receivables + change_in_inventory + change_in_hedging_assets_current + change_in_other_current_assets + change_in_payables_and_accrued_expense + 
    change_in_pension_and_other_post_retirement_benefit_plans_current + change_in_current_debt_and_capital_lease_obligation + change_in_current_deferred_liabilities + change_in_other_current_liabilities )
    operating_cash_flow = net_income_from_continuing_operations + depreciation_and_amortization + change_in_working_capital
    net_ppe_purchase_and_sale = float(previous_balance_sheet.gross_ppe) - float(current_balance_sheet.gross_ppe)
    goodwill_and_other_intangible_assets = float(previous_balance_sheet.goodwill_and_other_intangible_assets) - float(current_balance_sheet.goodwill_and_other_intangible_assets)
    investments_and_advances = float(previous_balance_sheet.investments_and_advances) - float(current_balance_sheet.investments_and_advances)
    other_non_current_assets = float(previous_balance_sheet.other_non_current_assets) - float(current_balance_sheet.other_non_current_assets)
    cash_flow_from_continuing_investing_activities = ( net_ppe_purchase_and_sale + goodwill_and_other_intangible_assets + investments_and_advances +  other_non_current_assets )
    investing_cash_flow = cash_flow_from_continuing_investing_activities
    long_term_debt_and_capital_lease_obligation = float(current_balance_sheet.long_term_capital_lease_obligation) - float(previous_balance_sheet.long_term_capital_lease_obligation)
    non_current_deferred_liabilities = float(current_balance_sheet.non_current_deferred_liabilities) - float(previous_balance_sheet.non_current_deferred_liabilities)
    trade_and_other_payables_non_current = float(current_balance_sheet.trade_and_other_payables_non_current) - float(previous_balance_sheet.trade_and_other_payables_non_current)
    other_non_current_liabilities = float(current_balance_sheet.other_non_current_liabilities) - float(previous_balance_sheet.other_non_current_liabilities)
    common_stock_issuance_payments = float(current_balance_sheet.common_stock) - float(previous_balance_sheet.common_stock)
    common_stock_dividend_paid = float(current_income_statement.equity_share_dividends)
    cash_flow_from_continuing_financing_activities = ( long_term_debt_and_capital_lease_obligation +  non_current_deferred_liabilities + trade_and_other_payables_non_current + other_non_current_liabilities +
                                                       common_stock_issuance_payments + common_stock_dividend_paid )
    financing_cash_flow = cash_flow_from_continuing_financing_activities
    changes_in_cash = operating_cash_flow + investing_cash_flow + financing_cash_flow
    beginning_cash_position = float(previous_balance_sheet.cash_cash_equivalents_and_short_term_investments)
    end_cash_position = changes_in_cash + beginning_cash_position
    capital_expenditure = net_ppe_purchase_and_sale 
    issuance_repurchase_of_capital_stock = common_stock_issuance_payments
    repayment_of_debt = long_term_debt_and_capital_lease_obligation 
    free_cash_flow = end_cash_position + capital_expenditure + issuance_repurchase_of_capital_stock + repayment_of_debt

    return {
        'net_income_from_continuing_operations': net_income_from_continuing_operations,
        'depreciation_and_amortization': depreciation_and_amortization,
        'changes_in_receivables': changes_in_receivables,
        'change_in_inventory': change_in_inventory,
        'change_in_hedging_assets_current': change_in_hedging_assets_current,
        'change_in_other_current_assets': change_in_other_current_assets,
        'change_in_payables_and_accrued_expense': change_in_payables_and_accrued_expense,
        'change_in_pension_and_other_post_retirement_benefit_plans_current': change_in_pension_and_other_post_retirement_benefit_plans_current,
        'change_in_current_debt_and_capital_lease_obligation': change_in_current_debt_and_capital_lease_obligation,
        'change_in_current_deferred_liabilities': change_in_current_deferred_liabilities,
        'change_in_other_current_liabilities': change_in_other_current_liabilities,
        'change_in_working_capital': change_in_working_capital,
        'operating_cash_flow': operating_cash_flow,
        'net_ppe_purchase_and_sale': net_ppe_purchase_and_sale,
        'goodwill_and_other_intangible_assets': goodwill_and_other_intangible_assets,
        'investments_and_advances': investments_and_advances,
        'other_non_current_assets': other_non_current_assets,
        'cash_flow_from_continuing_investing_activities': cash_flow_from_continuing_investing_activities,
        'investing_cash_flow': investing_cash_flow,
        'long_term_debt_and_capital_lease_obligation': long_term_debt_and_capital_lease_obligation,
        'non_current_deferred_liabilities': non_current_deferred_liabilities,
        'trade_and_other_payables_non_current': trade_and_other_payables_non_current,
        'other_non_current_liabilities': other_non_current_liabilities,
        'common_stock_issuance_payments': common_stock_issuance_payments,
        'common_stock_dividend_paid': common_stock_dividend_paid,
        'cash_flow_from_continuing_financing_activities': cash_flow_from_continuing_financing_activities,
        'financing_cash_flow': financing_cash_flow,
        'changes_in_cash': changes_in_cash,
        'beginning_cash_position': beginning_cash_position,
        'end_cash_position': end_cash_position,
        'capital_expenditure': capital_expenditure,
        'issuance_repurchase_of_capital_stock': issuance_repurchase_of_capital_stock,
        'repayment_of_debt': repayment_of_debt,
        'free_cash_flow': free_cash_flow
    }


def cashFlowTable(request, id):
    company = Company.objects.get(company_id=id)
    
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')

        if select_type_of_data == 'monthly':
            year = int(request.POST.get('year'))
            month_name = request.POST.get('month')
            month = datetime.strptime(month_name, '%B').month
            date = datetime(year, month, 1)

        elif select_type_of_data == 'quarterly':
            year = int(request.POST.get('year'))
            quarter = request.POST.get('quarter').split()[0]
            quarter_value = request.POST.get('quarter')
            quarter_start_months = {'Q1': 1, 'Q2': 4, 'Q3': 7, 'Q4': 10}
            month = quarter_start_months[quarter]
            date = datetime(year, month, 1)

        elif select_type_of_data == 'yearly':
            year = int(request.POST.get('year'))
            date = datetime(year, 1, 1)

        period_type = select_type_of_data
        period_exists, previous_period_date, previous_balance_sheet, previous_income_statement = check_previous_entry_exists(date, company, period_type)
        current_balance_sheet, current_income_statement = get_balance_sheet_and_income_statement(date, company)

        if not current_balance_sheet or not current_income_statement:
            messages.error(request, f'Please fill Income Statement and Balance Sheet for the current period.')
        elif not period_exists:
            messages.error(request, f'No previous entry exists in BalanceSheet or IncomeStatement for the previous {period_type}.')
        else:
            cash_flow_data = calculate_cash_flow(current_balance_sheet, current_income_statement, previous_balance_sheet, previous_income_statement)
            cash_flow = CashFlow(
                company_id=company,
                date=date,
                **cash_flow_data,
                monthly_or_quarterly_or_yearly=month_name if select_type_of_data == 'monthly' else (quarter_value if select_type_of_data == 'quarterly' else year)
            )
            cash_flow.save()
            return redirect('planning_budgeting_cash_flow_table', id)
    
    cash_flows = CashFlow.objects.filter(company_id=id)
    months, quarters, years = get_months_quarters_years()
    
    context = {
        'company': company,
        'cash_flows': cash_flows,
        'months': months,
        'quarters': quarters,
        'years': years,
        'months_json': months_json,
        'quarters_json': quarters_json,
        'years_json': years_json,
        'current_balance_sheet': current_balance_sheet if request.method == 'POST' else None,
        'current_income_statement': current_income_statement if request.method == 'POST' else None,
        'previous_balance_sheet': previous_balance_sheet if request.method == 'POST' else None,
        'previous_income_statement': previous_income_statement if request.method == 'POST' else None,
    }
    return render(request, 'admin/cash_flow_table.html', context)


def cashFlow(request,id):
    company = Company.objects.get(company_id=id)
    cash_flow = CashFlow.objects.filter(company_id=id).last()
    if request.method == 'POST':
        cash_flow.operating_cash_flow = cash_flow.net_income_from_continuing_operations + cash_flow.depreciation_and_amortization + cash_flow.change_in_working_capital
        
    else:
        context = {'company': company, 'cash_flow': cash_flow}
        return render(request, 'admin/cash_flow.html', context)


    
#Forecasting

def forecastedIncomeStatementTable1(request, id):
        company = Company.objects.get(company_id=id)
        latest_income_statement = IncomeStatement.objects.filter(company_id=id).order_by('-date').first()
        months, quarters, years = get_months_quarters_years()
        if request.method == 'POST':
            select_type_of_data = request.POST.get('select_type_of_data')
            growth_rate = request.POST.get('growth_rate')
            print(select_type_of_data,'select_type_of_data')
            print(growth_rate,'growth_rate')
            return redirect('forecasting_income_statement_table',id)

            
           
        else:
            context = {
                'company': company,
                'income_statement': latest_income_statement,
                'months': months,
                'quarters': quarters,
                'years': years,
                'months_json': months_json,
                'quarters_json': quarters_json,
                'years_json': years_json
            }
            return render(request, 'admin/forecasted_income_statement.html', context)

def forecastedIncomeStatementTable2(request, id):
    company = Company.objects.get(company_id=id)
    latest_income_statement = IncomeStatement.objects.filter(company_id=id).order_by('-date').first()
    months, quarters, years = get_months_quarters_years()
    
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')
        growth_rate = float(request.POST.get('growth_rate')) / 100
        forecasted_data = {}

        if select_type_of_data == 'monthly':
            # Initialize forecasted data with latest income statement values
            forecasted_data['January'] = {
                'total_revenue': latest_income_statement.total_revenue,
                'operating_revenue': latest_income_statement.operating_revenue,
                'cost_of_revenue': latest_income_statement.cost_of_revenue,
                'gross_profit': latest_income_statement.gross_profit,
                'operating_expense': latest_income_statement.operating_expense,
                'selling_general_and_administrative_expense': latest_income_statement.selling_general_and_administrative_expense,
                'general_and_administrative_expenses': latest_income_statement.general_and_administrative_expenses,
                'selling_and_marketing_expense': latest_income_statement.selling_and_marketing_expense,
                'research_and_development_expense': latest_income_statement.research_and_development_expense,
                'operating_income': latest_income_statement.operating_income,
                'net_non_operating_interest_income_expense': latest_income_statement.net_non_operating_interest_income_expense,
                'interest_income_non_operating': latest_income_statement.interest_income_non_operating,
                'interest_expense_non_operating': latest_income_statement.interest_expense_non_operating,
                'other_income_or_expense': latest_income_statement.other_income_or_expense,
                'gain_or_loss_on_sale_of_security': latest_income_statement.gain_or_loss_on_sale_of_security,
                'special_income_or_charges': latest_income_statement.special_income_or_charges,
                'write_off': latest_income_statement.write_off,
                'other_non_operating_income_or_expenses': latest_income_statement.other_non_operating_income_or_expenses,
                'pretax_income': latest_income_statement.pretax_income,
                'tax_provision': latest_income_statement.tax_provision,
                'net_income': latest_income_statement.net_income,
                'preference_share_dividends': latest_income_statement.preference_share_dividends,
                'net_income_to_common_stockholders': latest_income_statement.net_income_to_common_stockholders,
                'equity_share_dividends': latest_income_statement.equity_share_dividends,
                'retained_earnings': latest_income_statement.retained_earnings,
                'basic_eps': latest_income_statement.basic_eps,
                'diluted_eps': latest_income_statement.diluted_eps,
                'depreciation_and_amortization': latest_income_statement.depreciation_and_amortization,
                'ebitda': latest_income_statement.ebitda,
                'no_of_equity_shares': latest_income_statement.no_of_equity_shares,
            }
            
            # Calculate forecast for the next 11 months
            for i in range(1, 12):
                month_name = months[i]
                previous_month_data = forecasted_data[months[i-1]]
                forecasted_data[month_name] = {key: value + value * growth_rate for key, value in previous_month_data.items()}
            
            context = {
                'company': company,
                'income_statement': latest_income_statement,
                'months': months,
                'quarters': quarters,
                'years': years,
                'forecasted_data': forecasted_data,
            }
            return render(request, 'admin/forecasted_income_statement.html', context)

    else:
        context = {
            'company': company,
            'income_statement': latest_income_statement,
            'months': months,
            'quarters': quarters,
            'years': years,
        }
        return render(request, 'admin/forecasted_income_statement.html', context)


from decimal import Decimal

def forecastedIncomeStatementTable(request, id):
    company = Company.objects.get(company_id=id)
    latest_income_statement = IncomeStatement.objects.filter(company_id=id).order_by('-date').first()
    months, quarters, years = get_months_quarters_years()
    
    if request.method == 'POST':
        select_type_of_data = request.POST.get('select_type_of_data')
        growth_rate = Decimal(request.POST.get('growth_rate')) / Decimal(100)
        forecasted_data = {}

        if select_type_of_data == 'monthly':
            # Initialize forecasted data with latest income statement values
            forecasted_data['January'] = {
                'total_revenue': latest_income_statement.total_revenue,
                'operating_revenue': latest_income_statement.operating_revenue,
                'cost_of_revenue': latest_income_statement.cost_of_revenue,
                'gross_profit': latest_income_statement.gross_profit,
                'operating_expense': latest_income_statement.operating_expense,
                'selling_general_and_administrative_expense': latest_income_statement.selling_general_and_administrative_expense,
                'general_and_administrative_expenses': latest_income_statement.general_and_administrative_expenses,
                'selling_and_marketing_expense': latest_income_statement.selling_and_marketing_expense,
                'research_and_development_expense': latest_income_statement.research_and_development_expense,
                'operating_income': latest_income_statement.operating_income,
                'net_non_operating_interest_income_expense': latest_income_statement.net_non_operating_interest_income_expense,
                'interest_income_non_operating': latest_income_statement.interest_income_non_operating,
                'interest_expense_non_operating': latest_income_statement.interest_expense_non_operating,
                'other_income_or_expense': latest_income_statement.other_income_or_expense,
                'gain_or_loss_on_sale_of_security': latest_income_statement.gain_or_loss_on_sale_of_security,
                'special_income_or_charges': latest_income_statement.special_income_or_charges,
                'write_off': latest_income_statement.write_off,
                'other_non_operating_income_or_expenses': latest_income_statement.other_non_operating_income_or_expenses,
                'pretax_income': latest_income_statement.pretax_income,
                'tax_provision': latest_income_statement.tax_provision,
                'net_income': latest_income_statement.net_income,
                'preference_share_dividends': latest_income_statement.preference_share_dividends,
                'net_income_to_common_stockholders': latest_income_statement.net_income_to_common_stockholders,
                'equity_share_dividends': latest_income_statement.equity_share_dividends,
                'retained_earnings': latest_income_statement.retained_earnings,
                'basic_eps': latest_income_statement.basic_eps,
                'diluted_eps': latest_income_statement.diluted_eps,
                'depreciation_and_amortization': latest_income_statement.depreciation_and_amortization,
                'ebitda': latest_income_statement.ebitda,
                'no_of_equity_shares': latest_income_statement.no_of_equity_shares,
            }
            
            # Calculate forecast for the next 11 months
            for i in range(1, 12):
                month_name = months[i]
                previous_month_data = forecasted_data[months[i-1]]
                forecasted_data[month_name] = {key: value + (value * growth_rate) if value is not None else None for key, value in previous_month_data.items()}
            
            context = {
                'company': company,
                'income_statement': latest_income_statement,
                'months': months,
                'quarters': quarters,
                'years': years,
                'forecasted_data': forecasted_data,
            }
            return render(request, 'admin/forecasted_income_statement.html', context)

    else:
        context = {
            'company': company,
            'income_statement': latest_income_statement,
            'months': months,
            'quarters': quarters,
            'years': years,
        }
        return render(request, 'admin/forecasted_income_statement.html', context)

#Investor

def investorDashboard(request):
    users = User.objects.filter(company_type='investor')
    companies = []
    for user in users:
        companies.extend(user.companies.all())
    
    sector=Sector.objects.all()    
    # for company in companies:
    #     print(company.company_type)
    return render(request, 'investor/dashboard.html', {'companies': companies, 'industries':sector})

def investorBase(request,id):
    company=Company.objects.get(company_id=id)
    user=User.objects.get(user_id=company.user_id)
    context={
        'company':company,
        'user':user
    }
    return render(request, 'investor/base.html', context)


def basicInformation(request,id):
    company = Company.objects.get(company_id = id)
    user=User.objects.get(user_id=company.user_id)

    company_profile = CompanyProfile.objects.get(company_id = id)
    founders = Founder.objects.filter(company_id = id)
    clients = Client.objects.filter(company_id = id)

    context = {
        'company':company,
        'user':user,

        'company_profile': company_profile,
        'founders':founders,
        'clients':clients
    }
    return render(request,'investor/basic_information.html',context)



def founderAndTeam(request,id):
    company = Company.objects.get(company_id = id)
    user=User.objects.get(user_id=company.user_id)

    founders = Founder.objects.filter(company_id = id)
    context = { 'company':company,
        'user':user,'founders':founders}
    return render(request,'investor/founders_and_team.html',context)
#New one
def revenueVerticals(request, company_id):
    company_id = Company.objects.get(company_id = company_id)
    if request.method == 'POST':
        # Process homogenous products if any
        homogenous_product_names = request.POST.getlist('homogenous_product_name[]')
        homogenous_selling_prices = request.POST.getlist('homogenous_selling_price_per_unit[]')
        homogenous_units_sold = request.POST.getlist('homogenous_units_sold[]')
        homogenous_growth_rates = request.POST.getlist('homogenous_expected_growth_rate[]')

        for name, price, units, growth in zip(homogenous_product_names, homogenous_selling_prices, homogenous_units_sold, homogenous_growth_rates):
            if name and price and units and growth:
                HomogenousProduct.objects.create(
                   company_id = company_id,
                product_name = name,
                selling_price_per_unit = price,
                units_sold = units,
                expected_growth_rate = growth
                )

        # Process heterogenous products if any
        heterogenous_product_names = request.POST.getlist('heterogenous_product_name[]')
        heterogenous_expected_revenues = request.POST.getlist('heterogenous_expected_revenue[]')
        heterogenous_growth_rates = request.POST.getlist('heterogenous_expected_growth_rate[]')

        for name, revenue, growth in zip(heterogenous_product_names, heterogenous_expected_revenues, heterogenous_growth_rates):
            if name and revenue and growth:
                HeterogenousProduct.objects.create(
                    company_id=company_id,
                    product_name = name,
                expected_revenue = revenue,
                expected_growth_rate = growth
                )
        
        return redirect('revenue_verticals',company_id)  # Change to your desired redirect URL
    else:
        # Handle GET request or any other logic here
        company_profile = CompanyProfile.objects.get(company_id = company_id)
        context ={'company_profile': company_profile}
        return render(request, 'admin/revenue_verticals.html', context)


def expenses(request,company_id):
    if request.method == 'POST':
        pass
    else:
        # Handle GET request or any other logic here
        company_profile = CompanyProfile.objects.get(company_id = company_id)
        context ={'company_profile': company_profile}
        return render(request,'admin/expenses.html',context)
    

#Editor
def editorDashboard(request):
    return render(request,'editor/dashboard.html')

def parent(request):
    subuser_context = custom_subuser(request)
    current_subuser = subuser_context.get('current_subuser') 
    creator_id = current_subuser.creator_id
    creator_data=User.objects.get(user_id = creator_id)
    context ={'creator_data':creator_data}
    return render(request,'editor/parent.html',context)

#User
def userDashboard(request):
    return render(request,'user/dashboard.html')

#Password Reset 
import random
def generate_random_otp():
    otp = ""
    for i in range(5):
        otp += str(random.randint(0, 9))
    return otp
#generate_random_otp()
#print("Generated OTP:", generate_otp())

def forgotPasswordOne(request):
    if request.method == 'POST':
        input_email = request.POST['email']
        print(input_email)
        if User.objects.filter(email=input_email).exists() or Team.objects.filter(email=input_email).exists():
            generated_otp = generate_random_otp()
            request.session['OTP'] = generated_otp
            request.session['email'] = input_email
            # Debug print statements
            # print("OTP set in session:", request.session.get('OTP'))
            # print("Email set in session:", request.session.get('email'))
            # Get the current site domain
            current_site = get_current_site(request)
            domain = current_site.domain

            # Construct the signin URL
            password_reset_url = f'http://{domain}/forgot_password_2'

            subject='Number Leader - Password Reset Link'
            txt='''
                Password Reset Link and OTP :

                OTP: {}
                Domain: {}

                    '''
            message=txt.format(generated_otp,password_reset_url)
            from_email=settings.EMAIL_HOST_USER
            to_list=[input_email]
            send_mail(subject, message,from_email,to_list,fail_silently=True)
            messages.success(request,'we have sent opt to your mail please check')
            return redirect('forgot_password_1')
        else:
            messages.error(request,'please enter the registered email')
            return redirect('forgot_password_1')
    else:
        return render(request,'forgot_password_1.html')


def forgotPasswordTwo(request):
    if request.method == 'POST':
        input_otp = int(request.POST['otp'])
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        session_otp = request.session.get('OTP')
        session_email =request.session.get('email')
        

        if 'OTP' in request.session and 'email' in request.session:
            if input_otp == int(session_otp):
                if User.objects.filter(email=session_email).exists():
                    if new_password == confirm_new_password:
                        user = User.objects.get(email=session_email)
                        user.password = confirm_new_password
                        user.save()
                        del request.session['OTP'] 
                        del request.session['email']
                        messages.error(request,'Password reset completed sucessfully')
                        return redirect('forgot_password_2')

                if Team.objects.filter(email=session_email):
                    if new_password == confirm_new_password:
                        team = Team.objects.get(email=session_email)
                        team.password = confirm_new_password
                        team.save()
                        
                        del request.session['OTP'] 
                        del request.session['email']
                        messages.error(request,'Password reset completed sucessfully')
                        return redirect('forgot_password_2')
                    else:
                        messages.error(request,'Both Password Must be same')
                        return redirect('forgot_password_2')   
                else:
                    messages.error(request,'Please generate OTP first')
                    return redirect('forgot_password_2')
            else:
                messages.error(request,'Please enter correct otp')
                return redirect('forgot_password_2')
        else:
            messages.error(request,'Please generate OTP first')
            return redirect('forgot_password_2')
        
    else:
        return render(request,'forgot_password_2.html')



