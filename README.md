# CSinventory

## Requerimientos
 * Django 1.10

## Instalación
Den sus clones y sus ward y luego:
```
$ cd /inventory
$ pip install virtualenv
$ python -m venv myvenv
$ venv/Scripts/activate
$ pip install -r requirements.txt
```
Ésto es para instalar las dependencias en un ambiente virtual. Es opcional, si quieren instalar todo global, ahí está el último comando. Si van a agregar otra cosa, háganlo en otro branch y agreguenlo a ```requirements.txt```

## Workflow
```
$ git fetch/pull
$ python manage.py migrate
```
Manden sus PR, etc. Si hacen cambios a los modelos, hagan otro branch y hagan ```python manage.py makemigrations``` y luego ```python manage.py migrate```.
