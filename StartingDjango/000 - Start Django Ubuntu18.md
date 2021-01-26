Мабуть це було так:

````
sudo apt install mc
sudo apt install python3-pip
sudo apt install python3-venv
````

Тобто інсталяція `mc` потягла за собою `python3`. В результаті маємо наступне:

````
dasha@ubun18:~$ apt list python3 --installed -a
Listing... Done
python3/bionic-updates,now 3.6.7-1~18.04 amd64 [installed,automatic]
python3/bionic 3.6.5-3 amd64
dasha@ubun18:~$
dasha@ubun18:~$ apt list *-pip* --installed
Listing... Done
python-pip-whl/bionic-updates,bionic-security,now 9.0.1-2.3~ubuntu1.18.04.4 all [installed,automatic]
python3-pip/bionic-updates,bionic-security,now 9.0.1-2.3~ubuntu1.18.04.4 all [installed]
dasha@ubun18:~$
dasha@ubun18:~$ python3 -m pip --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)
dasha@ubun18:~$
````

Потрібно більш детально розбиратись з Virtual Environment<br>
venv VS virtualenv<br>
https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe<br>
але схоже - потрібно ставити `python3-venv` і не заморочуватись

````
dasha@ubun18:~$ apt list *venv* --installed
Listing... Done
python3-venv/bionic-updates,now 3.6.7-1~18.04 amd64 [installed]
python3.6-venv/bionic-updates,bionic-security,now 3.6.9-1~18.04ubuntu1.3 amd64 [installed,automatic]
dasha@ubun18:~$ apt list *virtualenv* --installed
Listing... Done
dasha@ubun18:~$
dasha@ubun18:~$ apt list *django* --installed
Listing... Done
dasha@ubun18:~$
````

Django не варто ставити через apt, його треба ПІПати в venv поточного проєкту

    python3 -m venv tutorial-env

створить в поточній директорію `tutorial-env` в яку буде складатись все напіпане. Треба активувати потрібні Virtual Environment командою:

    source tutorial-env/bin/activate

запрошення повинено змінитись, далі все робимо в активованому venv
````
dasha@ubun18:~$ source tutorial-env/bin/activate
(tutorial-env) dasha@ubun18:~$ python -m pip install Django
(tutorial-env) dasha@ubun18:~$ django-admin startproject mysite
````

TODO: розібратись з venv, щоб мати можливісь відновлювати Virtual Environment з іншого компа.


````
dasha@ubun18:~$ source tutorial-env/bin/activate
(tutorial-env) dasha@ubun18:~$ python -m pip freeze > requirements.txt
(tutorial-env) dasha@ubun18:~$ cat requirements.txt
asgiref==3.3.1
Django==3.1.5
pkg-resources==0.0.0
pytz==2020.5
sqlparse==0.4.1
(tutorial-env) dasha@ubun18:~$ deactivate
dasha@ubun18:~$
dasha@ubun18:~$
dasha@ubun18:~$ python -m pip freeze > requirements2.txt
Command 'python' not found, but can be installed with:
dasha@ubun18:~$ python3 -m pip freeze > requirements2.txt
dasha@ubun18:~$ cat requirements2.txt
asgiref==3.3.1
asn1crypto==0.24.0
attrs==17.4.0
Automat==0.6.0
....
....
unattended-upgrades==0.1
urllib3==1.22
zope.interface==4.3.2
dasha@ubun18:~$
````

щоб відновити треба дати команду

    (tutorial-env) dasha@ubun18:~$ python -m pip install -r requirements.txt

більш детально тут:<br>
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/<br>
https://pip.pypa.io/en/latest/user_guide/#requirements-files<br>


