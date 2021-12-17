#HOW TO INSTALL 

#Создайте виртуальную машину сперва 

	py -m venv myenv

#Затем установите пакеты 

	pip install -r requirements.txt 

#Запускайте сервер
	
	py manage.py runserver 

#Для активации frontend 
	
	Установите npm (node.js)

#Установка Angular(TypeScript)

	npm install -g @angular/cli

#Компонент списка обьявлений PostListComponent;
	
	ng generate component post-list --flat

#Флаг --flat задает размещение файлов с модулем непосредственно в папке src\app, а не во вложенной папке (проект у нас несложный, и разностить его код)

#Компонент сведений о выбранном обьявлении PostDetailComponent(он же выведет список комментариев и форму для добавляения нового комментария):
	
	ng generate component post-detail --flat 

#Служба PostService - для "общения" с бэкендом, написанным
	
	ng generate service post  

#postclient/src/app/app.module.ts
	
declorations - массив классов компоненотов, регистрируемых в метамодуле.
Отметим, что там уже присутвтуют, помимо компонента приложения AppComponent, еще и созданные вручную компоненты PostListComponent и PostDetailComponent.
Их добавила туда утилита ng сразу при их создания.