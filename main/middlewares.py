from .models import SubRubric 

#То есть пагинация
#Создадим обработчик контекста, в котором и будет формироваться список подрубрик.
def bboard_context_processor(request):

	context = {}
	context['rubrics'] = SubRubric.objects.all()
	#В файле explainin.txt я показал обьяснение для этого кода
	context['keyword'] = ''
	context['all'] = ''
	if 'keyword' in request.GET:
		keyword = request.GET['keyword']
		if keyword:
			context['keyword'] = '?keyword=' + keyword
			context['all'] = context['keyword']
	if 'page' in request.GET:
		page = request.GET['page']
		if page != '1':
			if context['all']:
				context['all'] += '&page=' + page
			else:
				context['all'] = '&page=' + page
	return context 