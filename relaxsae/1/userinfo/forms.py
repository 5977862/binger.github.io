#-*- coding:utf-8 -*-
'''
Created on 2012-12-26

@author: Binger
'''
from django import forms
    
class Usereditform(forms.Form):
    email = forms.EmailField(label='邮箱',max_length=40,)
    telephone = forms.CharField(label='手机',max_length=15)
    address = forms.CharField(label='地址',max_length=80,required=False)
    
    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        try:
            assert len(telephone) == 11
            if telephone[0] == '+':
                int(telephone[1:])
            else:
                int(telephone)
        except:
            raise forms.ValidationError('telephone number')
        return telephone
    

class Userform(Usereditform):
    username = forms.CharField(label='用户名',max_length=30)
    passwd1 = forms.CharField(label='用户名',max_length=30,widget = forms.PasswordInput())
    passwd2 = forms.CharField(label='用户名',max_length=30,widget = forms.PasswordInput())
    gender = forms.ChoiceField(label='性别',choices=(('男','男'),('女','女')),widget = forms.RadioSelect())
#    ident = forms.CharField(label='身份证',max_length=20,required=False)
#    email = forms.EmailField(label='邮箱',max_length=40)
#    telephone = forms.CharField(label='手机',max_length=15)
#    address = forms.CharField(label='地址',max_length=80)

#    def clean_ident(self):
#        idnum = self.cleaned_data['ident']
#        if len(idnum) != 18:
#            raise forms.ValidationError('id length error')
#        try:
#            if str(idnum[17]).lower() == 'x':
#                int(idnum[:17])
#            else:
#                int(idnum)
#        except:
#            raise forms.ValidationError('id format error')
#        year = int(idnum[6:10])
#        if not 1900 < year < 2010:
#            raise forms.ValidationError('id date erro')
#        days = [31,28,31,30,31,30,31,31,30,31,30,31]
#        month = int(idnum[10:12])
#        day = int(idnum[12:14])
#        if not 0 < month < 13:
#            raise forms.ValidationError('id date erro')
#        else:
#            if month == 2 and (year%400 == 0 or (year%100!=0 and year%4==0)):
#                if day > 29:
#                    raise forms.ValidationError('id date erro')
#            else:
#                if day > days[month-1]:
#                    raise forms.ValidationError('id date erro')
#        by_num = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
#        ret_num = ['1','0','x','9','8','7','6','5','4','3','2']
#        sum = 0
#        index = 0
#        while index < 17:
#            sum += by_num[index] * int(idnum[index])
#            index += 1
#        if str(idnum[17]).lower() != ret_num[sum%11]:
#            raise forms.ValidationError('id error')
#        return idnum