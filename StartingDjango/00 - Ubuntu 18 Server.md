Релізи Ubuntu перелічені тут:<br>
https://wiki.ubuntu.com/Releases<br>
Дали все будемо робити з `Ubuntu 18.04.5 LTS`, якщо інше не зазначено додатково.

Install image можна знайти тут:<br>
https://releases.ubuntu.com/18.04/<br>
Краще брати серверну версію, буде встановлено меньше всякого непотребу<br>
https://releases.ubuntu.com/18.04/ubuntu-18.04.5-live-server-amd64.iso<br>

Параметри VM(Віртуальної машини) відносно скромні:
* RAM = 1-2 GB
* HDD = 15-20 GB
* Network 
  * VM повинна мати доступ до Інтернет, для інсталяції купи додоткових пакетів.
  * Необхідно мати статичну IP адресу на VM, яка буде доступна з Хостової машини.

Машинка на якій RAM = 3GB, HDD = 25GB та встановлено Django + Postgresql показує наступне:
````
dasha@ubun18:~/mysite$ top
Tasks: 117 total,   1 running,  73 sleeping,   0 stopped,   0 zombie
%Cpu0  :  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
%Cpu1  :  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  3045708 total,  1624672 free,   229220 used,  1191816 buff/cache
KiB Swap:  4032508 total,  4032508 free,        0 used.  2612412 avail Mem
...
dasha@ubun18:~/mysite$ df
Filesystem     1K-blocks    Used Available Use% Mounted on
udev             1491160       0   1491160   0% /dev
tmpfs             304572     728    303844   1% /run
/dev/xvda2      24636752 7424112  15938120  32% /
tmpfs            1522852       8   1522844   1% /dev/shm
tmpfs               5120       0      5120   0% /run/lock
tmpfs            1522852       0   1522852   0% /sys/fs/cgroup
tmpfs             304568       0    304568   0% /run/user/1001
dasha@ubun18:~/mysite$
````
Якщо на початку інсталяції вчасно натиснути `Esc` подальші дії будуть проходити без графічної оболонки.
Під час інсталяції простіше зразу встановити статичну IP адресу, а з потрібних пакетів вибираємо тільки `sshd`.

Інсталяція `Ubuntu 18.04.5 LTS` чомусь зависа на етапі онавлення/скасуванні оновлення пакетів.
В такому випадку потрібно кільнути процесс оновлення з сусіднього терміналу, або відмонтувати .iso диск та примусово перезавантажити машину.

Для встановлення нових пакетів використовуємо `sudo apt`. На свіжій Ubuntu зразу робимо
````
sudo apt update
sudo apt upgrade
````

Іноді виникає необхіднісь скористатись свіжими версіями пакетів, ніж доступні через `sudo apt`,
в такому випадку користуємось `sudo snap`. Наприклад, для отримання https сертифікату сайту, необхідно
було встановити `certbot` наступним чином:
````
snap --help
sudo snap install certbot
sudo snap --classic install certbot
sudo snap install certbot --classic
````

Налаштування мережі знаходяться в файлах `/etc/netplan/` і виглядають приблизно так:
````
dasha@ubun18:~/mysite$ cd /etc/netplan/
dasha@ubun18:/etc/netplan$ ll
total 12
drwxr-xr-x   2 root root 4096 Jan 24 12:56 ./
drwxr-xr-x 100 root root 4096 Jan 28 06:11 ../
-rw-r--r--   1 root root  225 Jan 24 12:56 00-installer-config.yaml
dasha@ubun18:/etc/netplan$ cat 00-installer-config.yaml
# This is the network config written by 'subiquity'
network:
  ethernets:
    eth0:
      addresses:
      - 192.168.1.3/24
      gateway4: 192.168.1.1
      nameservers:
        addresses:
        - 192.168.0.1
  version: 2
dasha@ubun18:/etc/netplan$
````

TODO: розібратись з `iptables` vs `ufw`, та `systemctl` vs `service`
````
dasha@ubun18:/etc/netplan$ systemctl status ufw
● ufw.service - Uncomplicated firewall
   Loaded: loaded (/lib/systemd/system/ufw.service; enabled; vendor preset: enabled)
   Active: active (exited) since Sun 2021-01-24 12:57:48 UTC; 3 days ago
     Docs: man:ufw(8)
  Process: 418 ExecStart=/lib/ufw/ufw-init start quiet (code=exited, status=0/SUCCESS)
 Main PID: 418 (code=exited, status=0/SUCCESS)

Warning: Journal has been rotated since unit was started. Log output is incomplete or unavailable.
dasha@ubun18:/etc/netplan$ service ufw status
● ufw.service - Uncomplicated firewall
   Loaded: loaded (/lib/systemd/system/ufw.service; enabled; vendor preset: enabled)
   Active: active (exited) since Sun 2021-01-24 12:57:48 UTC; 3 days ago
     Docs: man:ufw(8)
  Process: 418 ExecStart=/lib/ufw/ufw-init start quiet (code=exited, status=0/SUCCESS)
 Main PID: 418 (code=exited, status=0/SUCCESS)

Warning: Journal has been rotated since unit was started. Log output is incomplete or unavailable.
dasha@ubun18:/etc/netplan$
````
