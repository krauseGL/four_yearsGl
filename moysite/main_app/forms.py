from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, FileExtensionValidator

from .models import User, University, Specialization

"""
    Формы которые обрабатываются и возвращаются.
"""


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Эл.почта', widget=forms.EmailInput, max_length=30)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')


class ApplicationForm(forms.Form):
    """
    Форма подачи анкеты. Описанны поля и валидаторы к ним.
    """
    # Левая колонка
    first_name = forms.CharField(label='Фамилия', max_length=22)
    last_name = forms.CharField(label='Имя', max_length=22)

    patronymic = forms.CharField(label='Отчество', max_length=22, validators=[
        RegexValidator(r'^[а-яА-ЯёЁ\s]+$', message="Отчество должно содержать только кириллицу!", code="invalid")])

    series_passport = forms.CharField(label='Серия паспорта', max_length=4, validators=[
        RegexValidator(r'^\d{1,10}$', message="Серия паспорта должна содержать только цифры!", code="invalid"),
        MinLengthValidator(4)])

    number_passport = forms.CharField(label='Номер паспорта', max_length=6, validators=[
        RegexValidator(r'^\d{1,10}$', message="Номер паспорта должен содержать только цифры!", code="invalid"),
        MinLengthValidator(6)])

    date_of_birth = forms.DateField(label="Дата рождения",
                                    widget=forms.SelectDateWidget(
                                        years=list(map(str, ([x for x in range(1940, 2020)])))))

    school = forms.CharField(label='Школа', max_length=150, validators=[
        RegexValidator(r'^[а-яА-ЯёЁ\s]+$', message="Школа должна содержать только кириллицу!", code="invalid")])

    # Правая колонка
    region = forms.CharField(label='Регион', max_length=22, validators=[
        RegexValidator(r'^[а-яА-ЯёЁ\s]+$', message="Регион должен содержать только кириллицу!", code="invalid")])

    locality = forms.CharField(label='Населенный пункт', max_length=100, validators=[
        RegexValidator(r'^[а-яА-ЯёЁ\s]+$', message="Населенный пункт должен содержать только кириллицу!",
                       code="invalid")])

    street = forms.CharField(label='Улица', max_length=100, validators=[
        RegexValidator(r'^[а-яА-ЯёЁ0-9\s]+$', message="Улица должна содержать только кириллицу и цифру!",
                       code="invalid")])

    house = forms.CharField(label='Дом', max_length=20, validators=[
        RegexValidator(r'^[а-яА-ЯёЁ0-9\s]+$', message="Дом должен содержать только кириллицу и цифры!",
                       code="invalid")])

    housing = forms.CharField(label='Корпус', max_length=20, validators=[
        RegexValidator(r'^[а-яА-ЯёЁ0-9\s]+$', message="Копус должен содержать только кириллицу и цифры!",
                       code="invalid")])

    index = forms.CharField(label='Индекс', max_length=6, validators=[MinLengthValidator(6),
                                                                      RegexValidator(r'^\d{1,10}$',
                                                                                     message="Индекс должен содержать только цифры!",
                                                                                     code="invalid")])

    numbers_house = forms.CharField(label='Номер квартиры', max_length=3, validators=[
        RegexValidator(r'^\d{1,10}$', message="Номер квартиры должна содержать только цифры!", code="invalid")])

    # ОСП
    university = forms.ModelChoiceField(label='Университет', queryset=University.objects.all())
    specialization = forms.ModelChoiceField(label='Специальность', queryset=Specialization.objects.all())

    # Файлы
    file_passport = forms.FileField(label='Паспорт', widget=forms.FileInput(attrs={'accept': '.pdf'}), validators=[
        FileExtensionValidator(allowed_extensions=['pdf'],
                               message='Файл пасспорта должен быть с расширением pdf!')])
    file_certificate = forms.FileField(label='Атестат', widget=forms.FileInput(attrs={'accept': '.pdf'}), validators=[
        FileExtensionValidator(allowed_extensions=['pdf'],
                               message='Файл атестата должен быть с расширением pdf!')])
    file_statement = forms.FileField(label='Заявление', widget=forms.FileInput(attrs={'accept': '.pdf'}), validators=[
        FileExtensionValidator(allowed_extensions=['pdf'],
                               message='Файл заявления должен быть с расширением pdf!')])
    file_other = forms.FileField(label='Другие документы', allow_empty_file=True, required=False,
                                 widget=forms.FileInput(attrs={'accept': '.pdf'}), validators=[
            FileExtensionValidator(allowed_extensions=['pdf'],
                                   message='Другой файл  должен быть с расширением pdf!')])

    def clean_file_passport(self):
        """
        Валидация расширения файла и его размера, иначе кидаем исключение с сообщением.
        """
        file = self.cleaned_data.get('file_passport', False)
        if file:
            if file.size > 1 * 1024 * 1024:
                raise ValidationError('Размер файла должен не более 1мб!')
            return file
        else:
            raise ValidationError('Невозможно прочитать файл!')

    def clean_file_certificate(self):
        """
        Валидация расширения файла и его размера, иначе кидаем исключение с сообщением.
        """
        file = self.cleaned_data.get('file_certificate', False)
        if file:
            if file.size > 1 * 1024 * 1024:
                raise ValidationError('Размер файла должен не более 1мб!')
            return file
        else:
            raise ValidationError('Невозможно прочитать файл!')

    def clean_file_statement(self):
        """
        Валидация расширения файла и его размера, иначе кидаем исключение с сообщением.
        """
        file = self.cleaned_data.get('file_statement', False)
        if file:
            if file.size > 1 * 1024 * 1024:
                raise ValidationError('Размер файла должен не более 1мб!')
            return file
        else:
            raise ValidationError('Невозможно прочитать файл!')

    def clean_file_other(self):
        """
        Валидация расширения файла и его размера, иначе кидаем исключение с сообщением.
        """
        file = self.cleaned_data.get('file_other', False)
        if file:
            if file.size > 1 * 1024 * 1024:
                raise ValidationError('Размер файла должен не более 1мб!')
            return file
        else:
            return None
