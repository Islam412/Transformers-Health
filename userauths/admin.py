from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from userauths.models import User , Account , KYC

# Register your models here.


class UserCustomAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','username', 'email', 'phone']
    search_fields = ['first_name','last_name','username', 'email','phone']
    list_filter = ['email']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('first_name','last_name','username', 'email','phone','company','date_of_birth', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('user_permissions',)



class AccountAdminModel(ImportExportModelAdmin):
    list_editable = ['account_status', 'kyc_submitted', 'kyc_confirmed'] 
    list_display = ['user', 'account_number','user__phone' ,'account_status', 'kyc_submitted', 'kyc_confirmed'] 
    list_filter = ['account_status']
    search_fields = ['user__username', 'user__email', 'account_number']



class KYCAdmin(ImportExportModelAdmin):
    search_fields = ["user__first_name" , "user__last_name" , "account"]
    list_display = ['user', 'user__first_name' , 'user__last_name' , 'date'] 


admin.site.register(User, UserCustomAdmin)
admin.site.register(Account, AccountAdminModel)
admin.site.register(KYC, KYCAdmin)