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
                    return redirect('admin_dashboard')
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
        founder_photo = request.FILES.get('founder_email')

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



def basicInformation(request,id):
    company = Company.objects.get(company_id = id)
    company_profile = CompanyProfile.objects.get(company_id = id)
    founders = Founder.objects.filter(company_id = id)
    clients = Client.objects.filter(company_id = id)


   
    context = {
        'company':company,
        'company_profile': company_profile,
        'founders':founders,
        'clients':clients
    }
    return render(request,'admin/basic_information.html',context)

def businessPlan(request, id):
    company_profile = CompanyProfile.objects.get(company_id = id)
    
   
    context = {
        'company_profile': company_profile,
    }

    return render(request, 'admin/business_plan.html', context)

def capTable(request, id):
    company_profile = CompanyProfile.objects.get(company_id = id)
    cap_table = CapTable.objects.filter(company_id = id)
    context = {'company_profile': company_profile,'cap_table': cap_table }
   

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
        context ={'company_profile': company_profile}
    
        context = {
            'company_profile': company_profile,
        }

        return render(request, 'admin/cap_table_form.html', context)



def financialStatement(request,id):
    company_profile = CompanyProfile.objects.get(company_id = id)
    homogenous_products = HomogenousProduct.objects.filter(company_id = id)
    heterogenous_products = HeterogenousProduct.objects.filter(company_id = id)
    context ={'company_profile': company_profile,'homogenous_products':homogenous_products,'heterogenous_products':heterogenous_products}

    return render(request,'admin/financial_statement.html',context)


def incomeStatement(request,id):
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


def balanceSheet(request,id):
    company = Company.objects.get(company_id = id)

    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        begin_date = request.POST.get('begin_date')
        end_date = request.POST.get('end_date')
        #current assets
        total_current_assets = request.POST.get('total_current_assets')
        ca_cash = request.POST.get('ca_cash')
        ca_accounts_receivables = request.POST.get('ca_accounts_receivables')
        ca_prepaid_expenses = request.POST.get('ca_prepaid_expenses')
        ca_inventory = request.POST.get('ca_inventory')
        ca_other = request.POST.get('ca_other')
        #non current assets
        total_non_current_assets = request.POST.get('total_non_current_assets')
        nca_property = request.POST.get('nca_property')
        nca_charity = request.POST.get('nca_charity')
        nca_equipment = request.POST.get('nca_equipment')
        nca_leases = request.POST.get('nca_leases')
        nca_other = request.POST.get('nca_other')
        #current liabilities
        total_current_liabilities = request.POST.get('total_current_liabilities')
        cl_accounts_payable = request.POST.get('cl_accounts_payable')
        cl_accrued_expenses = request.POST.get('cl_accrued_expenses')
        cl_unearned_revenue = request.POST.get('cl_unearned_revenue')
        cl_other = request.POST.get('cl_other')
        #non current liabilities
        total_non_current_liabilities = request.POST.get('total_non_current_liabilities')
        ncl_longterm_debt = request.POST.get('ncl_longterm_debt')
        ncl_other = request.POST.get('ncl_other')
        #equity
        shareholder_equity = request.POST.get('shareholder_equity')
        equity_investment_capital = request.POST.get('equity_investment_capital')
        equity_retained_earnings = request.POST.get('equity_retained_earnings')

        user_context = custom_user(request)
        current_user = user_context.get('current_user') 

        

        balance_sheet = BalanceSheet(
            company_id = company,
            begin_date = begin_date,
            end_date = end_date,

            total_current_assets = total_current_assets,
            ca_cash = ca_cash,
            ca_accounts_receivables = ca_accounts_receivables,
            ca_prepaid_expenses = ca_prepaid_expenses,
            ca_inventory = ca_inventory,
            ca_other = ca_other,

            total_non_current_assets = total_non_current_assets,
            nca_property = nca_property,
            nca_charity = nca_charity,
            nca_equipment = nca_equipment,
            nca_leases = nca_leases,
            nca_other = nca_other,

            total_current_liabilities = total_current_liabilities,
            cl_accounts_payable = cl_accounts_payable,
            cl_accrued_expenses = cl_accrued_expenses,
            cl_unearned_revenue = cl_unearned_revenue,
            cl_other = cl_other,

            total_non_current_liabilities = total_non_current_liabilities,
            ncl_longterm_debt = ncl_longterm_debt,
            ncl_other = ncl_other,

            shareholder_equity = shareholder_equity,
            equity_investment_capital = equity_investment_capital,
            equity_retained_earnings = equity_retained_earnings,

            creator_id = current_user.user_id,
            #modifier_id = modifier_id,
            

        )
        balance_sheet.save()
        return redirect('planning_budgeting_balance_sheet_table',company.company_id)



        
    else:
        context = {'company':company}
        return render(request,'admin/balance_sheet.html',context)

def cashFlow(request,id):
    company = Company.objects.get(company_id = id)

    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        begin_date = request.POST.get('begin_date')
        end_date = request.POST.get('end_date')
        #financing
        net_financing = request.POST.get('net_financing')
        cf_finance_inflow_drawing = request.POST.get('cf_finance_inflow_drawing')
        cf_finance_inflow_distribution = request.POST.get('cf_finance_inflow_distribution')
        cf_finance_inflow_other = request.POST.get('cf_finance_inflow_other')
        cf_finance_outflow_loan_payments = request.POST.get('cf_finance_outflow_loan_payments')
        cf_finance_outflow_other = request.POST.get('cf_finance_outflow_other')
        #investments
        net_investments = request.POST.get('net_investments')
        cf_invest_inflow_loans = request.POST.get('cf_invest_inflow_loans')
        cf_invest_inflow_sell_property = request.POST.get('cf_invest_inflow_sell_property')
        cf_invest_inflow_sell_equip = request.POST.get('cf_invest_inflow_sell_equip')
        cf_invest_inflow_other = request.POST.get('cf_invest_inflow_other')
        cf_invest_outflow_buy_property = request.POST.get('cf_invest_outflow_buy_property')
        cf_invest_outflow_buy_equip = request.POST.get('cf_invest_outflow_buy_equip')
        cf_invest_outflow_other = request.POST.get('cf_invest_outflow_other')
        #operations
        net_operations = request.POST.get('net_operations')
        cf_ops_inflow_customers = request.POST.get('cf_ops_inflow_customers')
        cf_ops_inflow_depreciation = request.POST.get('cf_ops_inflow_depreciation')
        cf_ops_inflow_amortization = request.POST.get('cf_ops_inflow_amortization')
        cf_ops_inflow_other = request.POST.get('cf_ops_inflow_other')
        cf_ops_outflow_wages = request.POST.get('cf_ops_outflow_wages')
        cf_ops_outflow_overhead = request.POST.get('cf_ops_outflow_overhead')
        cf_ops_outflow_interest = request.POST.get('cf_ops_outflow_interest')
        cf_ops_outflow_taxes = request.POST.get('cf_ops_outflow_taxes')
        cf_ops_outflow_accounts_receivable = request.POST.get('cf_ops_outflow_accounts_receivable')
        cf_ops_outflow_inventory_increase = request.POST.get('cf_ops_outflow_inventory_increase')
        cf_ops_outflow_other = request.POST.get('cf_ops_outflow_other')
        #cash flow
        cf_beginning_balance = request.POST.get('cf_beginning_balance')
        cf_change_in_cash = request.POST.get('cf_change_in_cash')
        user_context = custom_user(request)
        current_user = user_context.get('current_user') 
       
        cash_flow = CashFlow(
           company_id = company,
           begin_date = begin_date,
           end_date = end_date,

           net_financing = net_financing,
           cf_finance_inflow_drawing = cf_finance_inflow_drawing,
           cf_finance_inflow_distribution = cf_finance_inflow_distribution,
           cf_finance_inflow_other = cf_finance_inflow_other,
           cf_finance_outflow_loan_payments = cf_finance_outflow_loan_payments,
           cf_finance_outflow_other = cf_finance_outflow_other,

           net_investments = net_investments,
           cf_invest_inflow_loans = cf_invest_inflow_loans,
           cf_invest_inflow_sell_property = cf_invest_inflow_sell_property,
           cf_invest_inflow_sell_equip = cf_invest_inflow_sell_equip,
           cf_invest_inflow_other = cf_invest_inflow_other,
           cf_invest_outflow_buy_property = cf_invest_outflow_buy_property,
           cf_invest_outflow_buy_equip = cf_invest_outflow_buy_equip,
           cf_invest_outflow_other = cf_invest_outflow_other,

           net_operations = net_operations,
           cf_ops_inflow_customers = cf_ops_inflow_customers,
           cf_ops_inflow_depreciation = cf_ops_inflow_depreciation,
           cf_ops_inflow_amortization = cf_ops_inflow_amortization,
           cf_ops_inflow_other = cf_ops_inflow_other,
           cf_ops_outflow_wages = cf_ops_outflow_wages,
           cf_ops_outflow_overhead = cf_ops_outflow_overhead,
           cf_ops_outflow_interest = cf_ops_outflow_interest,
           cf_ops_outflow_taxes = cf_ops_outflow_taxes,
           cf_ops_outflow_accounts_receivable = cf_ops_outflow_accounts_receivable,
           cf_ops_outflow_inventory_increase = cf_ops_outflow_inventory_increase,
           cf_ops_outflow_other = cf_ops_outflow_other,

           cf_beginning_balance = cf_beginning_balance,
           cf_change_in_cash = cf_change_in_cash,

           creator_id = current_user.user_id,
           #modifier_id = modifier_id
            
       )
        cash_flow.save()
        return redirect('planning_budgeting_cash_flow_table',company.company_id)


    else:
        context = {'company':company}
        return render(request,'admin/cash_flow.html',context)


from calendar import month_abbr

# def get_period_label(begin_date, end_date):
#     # Define financial quarters
#     quarters = {
#         'Q1': (1, 3),  # January to March
#         'Q2': (4, 6),  # April to June
#         'Q3': (7, 9),  # July to September
#         'Q4': (10, 12)  # October to December
#     }

#     if begin_date.month == end_date.month:
#         # Same month
#         return month_abbr[begin_date.month],f'Monthly Data'
#     for quarter, (start_month, end_month) in quarters.items():
#         if begin_date.month == start_month and end_date.month == end_month:
#             months = [month_abbr[m] for m in range(start_month, end_month + 1)]
#             return f'{quarter} ({", ".join(months)})',f'Quarterly Data'
#     # Custom or irregular period
#     return f'{begin_date.strftime("%b %d, %Y")} - {end_date.strftime("%b %d, %Y")}',f'irregular data'



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


def incomeStatementTable(request,id):
    company = Company.objects.get(company_id = id)
    income_statements = IncomeStatement.objects.filter(company_id = id)
    for income_statement in income_statements:
        income_statement.period_label,income_statement.data_name = get_period_label(income_statement.begin_date, income_statement.end_date)
    context = {'company':company,'income_statements':income_statements}
    return render(request,'admin/income_statement_table.html',context)

def balanceSheetTable(request,id):
    company = Company.objects.get(company_id = id)
    balance_sheets = BalanceSheet.objects.filter(company_id = id)
    for balance_sheet in balance_sheets:
        balance_sheet.period_label,balance_sheet.data_name = get_period_label(balance_sheet.begin_date, balance_sheet.end_date)
    context = {'company':company,'balance_sheets':balance_sheets}
    return render(request,'admin/balance_sheet_table.html',context)

def cashFlowTable(request,id):
    company = Company.objects.get(company_id = id)
    cash_flows = CashFlow.objects.filter(company_id = id)
    for cash_flow in cash_flows:
        cash_flow.period_label,cash_flow.data_name = get_period_label(cash_flow.begin_date, cash_flow.end_date)
    context = {'company':company,'cash_flows':cash_flows}
    return render(request,'admin/cash_flow_table.html',context)


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




