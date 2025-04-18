from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import User

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        widget = forms.PasswordInput(
            )
    )

    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'palceholder': '비밀번호 확인',
            }
        )
    )




    FAVORITE_CATEGORIES = [
        ('Novel,Poem,Drama','소설, 시, 희곡'),
        ('Economy','경제, 경영'),
        ('Self-development','자기계발'),
        ('Humanities','인문/교양'),
        ('Science','과학'),
        ('Hobby','취미/실용'),
        ('Teenager','어린이/청소년'),
    ]

    category = forms.MultipleChoiceField(
        choices = FAVORITE_CATEGORIES,
        widget = forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        # 비밀번호 안뜨게 만들고 싶습니다.
        model=User
        fields = ('username', 'password1', 'password2', 'email', 'last_name', 'first_name',  'gender','age','weekly_avg_reading_time','yearly_read_count','profile','category')
        labels = {
            'username': '아이디',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
            'email': '이메일',
            'last_name': '성',
            'first_name': '이름',
            'gender': '성별',  # 원하는 라벨
            'age': '나이',
            'weekly_avg_reading_time': '주간 평균 독서 시간',
            'yearly_read_count': '연간 독서량',
            'profile': '프로필 사진',
        }




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].help_text = ''
        self.fields['password2'].label = '비밀번호 확인'
        self.fields['password2'].help_text = ''
        self.fields['username'].help_text = ''
        
class CustomUserChangeForm(UserChangeForm):

    FAVORITE_CATEGORIES = [
        ('Novel,Poem,Drama','소설, 시, 희곡'),
        ('Economy','경제, 경영'),
        ('Self-development','자기계발'),
        ('Humanities','인문/교양'),
        ('Science','과학'),
        ('Hobby','취미/실용'),
        ('Teenager','어린이/청소년'),
    ]

    category = forms.MultipleChoiceField(
        choices = FAVORITE_CATEGORIES,
        widget = forms.CheckboxSelectMultiple,
        required=False,
    )



    class Meta:
        model=User
        fields = ('username', 'email', 'first_name', 'last_name', 'gender','age','weekly_avg_reading_time','yearly_read_count','profile', 'category')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 메시지 커스터마이징
        self.fields['password'].help_text = ('비밀번호 변경')
        self.fields['username'].help_text = ''

        if self.instance and self.instance.pk:
            if self.instance.category:
                self.fields['category'].initial = self.instance.category.split(',')
            else:
                self.fields['category'].initial = []