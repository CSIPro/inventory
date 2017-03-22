# CSinventory

## Requerimientos
 * Django >= 1.10

## Instalación
Den sus clones y sus ward y luego:
```
$ cd /inventory
$ pip install virtualenv
$ virtualenv myvenv
$ source venv/Scripts/activate
$ pip install -r requirements.txt

$ python manage.py migrate
```
No se les olvide el ```python manage.py migrate```. Si no lo hacen van a tener errores (probablemente).

Ésto es para instalar las dependencias en un ambiente virtual. Es opcional, si quieren instalar todo global, ahí está el último comando. Si van a agregar otra cosa, háganlo en otro branch y agreguenlo a ```requirements.txt```.

### Superuser
    username: admin
    pw: cebiche123

## Workflow
```
$ git fetch/pull
$ python manage.py migrate
```
Manden sus PR, etc. Si hacen cambios a los modelos, hagan otro branch y hagan ```python manage.py makemigrations``` y luego ```python manage.py migrate```.

## Mockups for design
* [Home (item list)](http://i.imgur.com/DZYAYog.png)
