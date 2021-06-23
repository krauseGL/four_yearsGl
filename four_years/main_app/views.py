from django.contrib import auth
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.views import View

from .forms import CustomUserCreationForm, CustomAuthenticationForm, ApplicationForm
from .models import Application, Specialization, University, Address, User

"""
    Представления. Подробнее можно почитать про MVT - model, VIEW, template.  
"""

def index(request):
    return render(request, 'index.html', {'user': auth.get_user(request)})


def logout(request):
    """
    Представление для выхода из учетной записи
    """
    template_name = 'logout.html'
    user = auth.get_user(request)
    if user.is_authenticated:
        auth.logout(request)
        return render(request, template_name, {'user': user})
    else:
        return redirect('main_app:index')


class AuthView(View):
    """
    Представление для авторизации пользователя
    """
    template_name = 'auth.html'
    form_class = CustomAuthenticationForm

    errors_msg = {
        'email': 'Пользователя с таким email не существует!',
        'password': 'Неправильный пароль!'
    }

    def get(self, request, *args, **kwargs):
        if auth.get_user(request).is_authenticated:
            return redirect('main_app:index')
        else:
            form = self.form_class(initial={'key': 'value'})
            context = {'form': form}
            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(request.POST)
        if form.is_valid():
            if User.objects.filter(email=(request.POST['email'])).exists():
                user = auth.authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('main_app:index')
                else:
                    form.add_error('password', self.errors_msg['password'])
            else:
                form.add_error('email', self.errors_msg['email'])
        return render(request, self.template_name, {'form': form})


class ApplicationView(View):
    """
    Представление для подачи анкеты. Проверяются все поля на валидность, если все поля валидны мы сохраняем файл.
    """
    template_name = 'application.html'
    form_class = ApplicationForm

    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)
        if user.is_authenticated:
            form = self.form_class(initial={
                'first_name': user.first_name,
                'last_name': user.last_name
            })
            context = {'form': form}

            return render(request, self.template_name, context)
        else:
            return redirect('main_app:auth')

    def post(self, request, *args, **kwargs):
        user = auth.get_user(request)
        if user.is_authenticated \
                and request.FILES['file_passport'] \
                and request.FILES['file_certificate'] \
                and request.FILES['file_statement']:
            # print(type(request.FILES.get('file_passport')))

            form = self.form_class(request.POST, request.FILES)

            print(form.is_valid())
            # print(form.errors.as_data())

            context = {'form': form}

            if form.is_valid():
                c = form.cleaned_data
                address = Address(region=c['region'], locality=c['locality'], street=c['street'], house=c['house'],
                        housing=c['housing'], index=c['index'], numbers_house=c['numbers_house'])
                address.save()

                application = Application(id_user=user, id_address=address,
                                          file_passport=request.FILES['file_passport'],
                                          file_certificate=request.FILES['file_certificate'],
                                          file_statement=request.FILES['file_statement'],
                                          file_other=request.FILES['file_other']
                                          )
                application.save()

                user.series_passport = c['series_passport']
                user.number_passport = c['number_passport']
                user.school = c['school']
                user.choice = c['specialization']
                print(application)
                return redirect('main_app:account')
            else:
                return render(request, self.template_name, context)
        else:
            return redirect('main_app:auth')


class AccountView(View):
    """
    Представление личного кабинета. Получаем объект пользователя если он авторизован,
    иначе редиректим его на страницу авторизации.
    """
    template_name = 'account.html'

    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)
        if user.is_authenticated:
            try:
                application = Application.objects.get(id_user=user.pk)
            except Application.DoesNotExist:
                application = None
            context = {'application': application}
            return render(request, self.template_name, context)
        else:
            return redirect('main_app:index')


class RegistrationView(View):
    """
    Представление для регистрации пользователя. Проверяется сущ. пользователь или нет,
    если нет то мы его регистрируем.
    """
    template_name = 'registration.html'
    form_class = CustomUserCreationForm

    def get(self, request):
        form = self.form_class(initial={'key': 'value'})
        context = {'form': form}
        print(form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.save()
            user = auth.authenticate(request, email=user.email, password=form.cleaned_data['password1'])
            login(request, user)
            print('DONE!')
            return redirect('main_app:index')
        return render(request, self.template_name, {'form': form})


def get_specializations(request):
    """
    Возвращает json со списоком специальностей университета
    """
    print(request.GET)
    university = request.GET.get('university', None)

    if university:
        university = get_object_or_404(University, pk=university)
        response = {
            'result': list(Specialization.objects.filter(university=university).values())
        }
    else:
        response = {
            'result': [{'specialization': 'Выберете университет!', 'id': 0}]
        }

    return JsonResponse(response)
