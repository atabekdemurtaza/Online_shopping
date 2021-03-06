from django.contrib import admin
from .models import User 
import datetime 
from .utilities import send_activation_notification
from .models import SuperRubric, SubRubric 
from .forms import SubRubricForm
from .models import AdditionalImage, Post
from .models import Comment
from .utilities import send_new_comment_notification

#Отправляем письма для активации 
def send_activation_notifications(modeladmin, request, queryset):  

	for rec in queryset:
		if not rec.is_activated:
			send_activation_notification(rec)
	modeladmin.message_user(request, 'Письма с требованиями отправлены')
send_activation_notifications.short_description = 'Отправка писем с требованиями активации'


"""class NonactivatedFilter(admin.SimpleListFilter):

	title = 'Прошли активацию?'
	parameter_name = 'actstate'

	def lookups(self, request, model_admin):

		return (
					('activated', 'Прошли'),
					('threedays', 'Не прошли более 3 дней'),
					('week', 'Не прошли более недели'),
		)

	def get_queryset(self, request, queryset):

		val = self.value()
		if val == 'activated':
			return queryset.filter(is_active=True, is_activated=True)
		elif val == 'threedays':
			day = datetime.date.today() - datetime.timedelta(days=3)
			return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=day)
		elif val == 'week':
			day = datetime.date.today() - datetime.timedelta(weeks=1)
			return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=day)"""


class UserAdmin(admin.ModelAdmin):

	list_display = ('__str__', 'is_activated', 'date_joined')
	search_fields = ('username','email','first_name', 'last_name')
	#list_filter = (NonactivatedFilter,)
	fields = (
				('username','email'),('first_name','last_name'),
				('send_messages', 'is_active', 'is_activated'),
				('is_staff', 'is_superuser'),
				'groups', 'user_permissions',
				('last_login', 'date_joined')
	)
	readonly_fields = ('last_login', 'date_joined')
	actions = (send_activation_notifications, )

class SubRubricInline(admin.TabularInline):

	model = SubRubric

class SuperRubricAdmin(admin.ModelAdmin):

	exclude = ('super_rubric',)
	inlines = (SubRubricInline,)

class SubRubricAdmin(admin.ModelAdmin):

	form = SubRubricForm

class AdditionalImageInline(admin.TabularInline):

	model = AdditionalImage

class PostAdmin(admin.ModelAdmin):

	list_display = ('rubric', 'title', 'author', 'created_at')
	fields = (('rubric', 'author'), 'title', 'content', 'price', 'contacts', 'image', 'is_active')
	inlines = (AdditionalImageInline,)

#Отправляем письма пользователю о том что коммент добавился
def send_new_comment_notifications(modeladmin, request, queryset):

	for rec in queryset:
		if not rec.is_active:
			send_activation_notification(rec)
	modeladmin.message_user(request, 'Комменты отправлены')
send_activation_notifications.short_description = 'Отправка комменты'

class Comments(admin.ModelAdmin):

	list_display = ('author', 'content', 'created_at')
	search_fields = ('created_at',)

admin.site.register(User, UserAdmin)
admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, Comments)