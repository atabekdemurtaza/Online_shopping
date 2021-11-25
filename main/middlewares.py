from .models import SubRubric 

#То есть пагинация
#Создадим обработчик контекста, в котором и будет формироваться список подрубрик.
def bboard_context_processor(request):

	context = {}
	context['rubrics'] = SubRubric.objects.all()
	return context 