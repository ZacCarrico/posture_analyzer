Notes about the raspberry pi this is being run on:

pi@rpi:~ $ cat /etc/os-release 
PRETTY_NAME="Debian GNU/Linux 11 (bullseye)"
NAME="Debian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"

pi@rpi:~ $ uname -m
aarch64

pi@rpi:~ $ grep MemTotal /proc/meminfo
MemTotal:         931460 kB

pi@rpi:~ $ df -H
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        63G  3.4G   57G   6% /
devtmpfs        341M     0  341M   0% /dev
tmpfs           477M     0  477M   0% /dev/shm
tmpfs           191M  1.1M  190M   1% /run
tmpfs           5.3M  4.1k  5.3M   1% /run/lock
/dev/mmcblk0p1  268M   33M  236M  13% /boot
tmpfs            96M     0   96M   0% /run/user/1000

# Install Docker
sudo apt-get update && sudo apt-get upgrade
sudo reboot
docker install following these instructions: https://docs.docker.com/engine/install/debian/#install-using-the-convenience-script
sudo docker pull mxnet/python:1.9.1_aarch64_cpu_py3
