from django.shortcuts import render, redirect
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detectUser, send_verification_email
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from vendor.models import Vendor

import datetime


#Restringe vendor acessar a pagina do cliente
def check_role_vendor(user):
  if user.role == 1:
    return True
  else:
    raise PermissionDenied

#Restringe cliente acessar a pagina do vendor
def check_role_customer(user):
  if user.role == 2:
    return True
  else:
    raise PermissionDenied


def registerUser(request):
  if request.user.is_authenticated:
    messages.warning(request, 'Usuário já logado.')
    return redirect('myAccount')
  elif request.method == "POST":
    form = UserForm(request.POST)
        
        
    if form.is_valid():      
      # hash password
      # password = form.cleaned_data['password']
      # user = form.save(commit=False)
      # user.set_password(password)
      # user.role = User.CUSTOMER
      # user.save()
      # end hash password

      # cria usuário utilizando o created método no accounts models
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      username = form.cleaned_data['username']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']

      user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
      user.role = User.CUSTOMER
      user.save()

      # send verification email
      mail_subject = 'Por favor ative sua conta'
      email_template = 'accounts/emails/account_verification_email.html'
      send_verification_email(request, user,  mail_subject, email_template)

      messages.success(request, 'Usuário registrado com sucesso.')
      return redirect('registerUser')
    else:
      print(form.errors)
      messages.error(request, 'Erro no cadastro.')
  else:
    form = UserForm()


  return render(request, 'accounts/registerUser.html', {
    "form": form,
  })


def registerVendor(request):
  if request.user.is_authenticated:
    messages.warning(request, "Usuário já logado.")
    return redirect('myAccount')
  elif request.method == "POST":
    form = UserForm(request.POST)
    v_form = VendorForm(request.POST, request.FILES)
    
    if form.is_valid() and v_form.is_valid():
      password = form.cleaned_data['password']
      user = form.save(commit=False)
      user.set_password(password)
      user.role = User.VENDOR
      user.save()

      #Envia email de verificação
      mail_subject = "Por favor ative a sua conta."
      email_template = 'accounts/emails/account_verification_email.html'
      send_verification_email(request, user, mail_subject, email_template)

      vendor = v_form.save(commit=False)
      vendor.user = user
      vendor_name = v_form.cleaned_data['vendor_name']
      vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
      user_profile = UserProfile.objects.get(user=user)
      vendor.user_profile = user_profile
      vendor.save()

      messages.success(request, "Sua conta foi registrada com sucesso. Por favor ative sua conta e espere pela aprovação.")
      return redirect('login')
    else:
      print("Formulário Inválido")
      print(form.errors)
  else:
    form = UserForm()
    v_form= VendorForm()  
  return render(request, 'accounts/registerVendor.html', {
    "form": form,
    "v_form": v_form,
  })

# Ativa o usuário criado - is_active setado para True
def activate(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)
  
  except(TypeError, OverflowError, User.DoesNotExist):
    user = None
  
  if user is not None and default_token_generator.check_token(user, token):
    user.is_active = True
    user.save()
    messages.success(request, "Sua conta foi ativada com sucesso.")
    return redirect('myAccount')
  else:
    messages.error(request, 'Código de ativação inválido ou expirado.')
    return redirect('myAccount')


def login(request):
  if request.user.is_authenticated:
    messages.warning(request, "Usuário já logado.")
    return redirect('myAccount')
  elif request.method == "POST":
    email = request.POST['email']
    password = request.POST['password']

    user = auth.authenticate(email=email, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, "Usuário logado com sucesso")
      return redirect('myAccount')
    else:
      messages.error(request, "Credenciais invalidas")
      return redirect('login')
  return render(request, 'accounts/login.html')

  
def logout(request):
  auth.logout(request)
  messages.info(request, "Voce saiu com sucesso.")
  return redirect('home')

#detecta tipo de usuario por meio da funcao detectUser no arquivo utils.py
@login_required(login_url='login')
def myAccount(request):
  user = request.user
  redirectUrl = detectUser(user)
  return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def c_dashboard(request):
  # orders = Order.objects.filter(user=request.user, is_ordered=True)
  # recent_orders = orders[:5]
  # orders_count = orders.count()

  return render(request, 'customer/c_dashboard.html', {
    # "orders": orders,
    # "orders_count": orders_count,
    # "recent_orders": recent_orders,
  })



# @login_required(login_url='login')
# @user_passes_test(check_role_vendor)
# def v_dashboard(request):
  
#   vendor = Vendor.objects.get(user=request.user)
  
#   # orders = Order.objects.filter(vendors__in=[vendor.id],  is_ordered=True).order_by('-created_at')
#   # recent_orders = orders[:10]
#   # orders_count = orders.count()

#   # receita no mes
#   # current_month = datetime.datetime.now().month
#   # current_month_orders = orders.filter(vendors__in=[vendor.id], created_at__month=current_month)
#   # current_month_revenue = 0
#   # for i in current_month_orders:
#   #   current_month_revenue += i.get_total_by_vendor()['grand_total']
#   # print(current_month_revenue)


#   # Total faturado
#   # total_revenue = 0
#   # for i in orders:
#   #   total_revenue += i.get_total_by_vendor()['grand_total']
  
  

#   return render(request, 'vendor/v_dashboard.html',{
#     # "orders": orders,
#     # "orders_count": orders_count,
#     # "recent_orders": recent_orders,
#     # "total_revenue": total_revenue,
#     # "current_month_revenue": current_month_revenue,
#   })


def forgot_password(request):
  if request.method == "POST":
    email = request.POST['email']

    if User.objects.filter(email=email).exists():
      user = User.objects.get(email__exact=email)

      #send resset password email
      mail_subject = 'Troque sua senha.'
      email_template = 'accounts/emails/reset_password_email.html'      
      send_verification_email(request, user, mail_subject, email_template)

      messages.success(request, 'Um link para trocar sua senha foi encaminhado por email.')
      return redirect('login')
    else:
      messages.error(request, "Esta email não existe. Por favor tente novamente.l")
      return redirect('forgot_password')
  return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
  # valida o usuario decodificando o token e usuario pk.
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)  
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  
  if user is not None and default_token_generator.check_token(user, token):
    request.session['uid'] = uid
    messages.info(request, "Por favor troque seu password.")
    return redirect('reset_password')
  else:
    messages.error(request, "Link expirado.")
    return redirect('myAccount')

def reset_password(request):
  if request.method == "POST":
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    if password == confirm_password:
      pk = request.session.get('uid')
      user = User.objects.get(pk=pk)
      user.set_password(password)
      user.is_active = True
      user.save()
      messages.success(request, "Senha atualizada com sucesso. Obrigado.")
      return redirect('login')
    else:
      messages.error(request, "As senhas digitadas não são iguais. Tente novamente.")
      return redirect('reset_password')
  return render(request, 'accounts/reset_password.html')