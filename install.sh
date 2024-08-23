#!/bin/bash

logfile="/tmp/qar-install.log"

qar-install() {
  here=$(realpath $(dirname "$0"))
  cd "$here"
  rm -f "$logfile" "$logfile.err"
  step "Checking if root"     qar-check-root
  step "Disabling SELinux"    qar-disable-selinux
  step "Removing old files"   qar-files-remove
  step "Copying files"        qar-files-copy
  step "Installing docker"    qar-docker
  step "Installing service"   qar-install-service
  step "Configuring firewall" qar-firewall
  step "Install Apache"       qar-httpd
  step "Install Python"       qar-python
  step "Install mDNS"         qar-install-mdns
  step "Restart Apache"       systemctl restart httpd
}

step() {
  msg="$1"
  shift
  echo -n "$msg..."
  "$@" >> "$logfile" 2>> "$logfile.err"

  if [ $? -ne 0 ]; then
    echo "FAILED!"
    echo ""
    echo " Installation failed!"
    echo " Check '$logfile' for more information"
    echo " Here is a snippet: "
    echo "---------------------------------"
    tail -n 5 "$logfile"
    echo "---------------------------------"
    tail -n 5 "$logfile.err"
    echo "---------------------------------"
    exit 1
  fi
  
  echo "OK"
}

qar-dnf() {
  dnf install -y "$@"
}

qar-check-root() {
  if [ "$EUID" -ne 0 ]
    then echo "Must run as root"
    exit 1
  fi
}

qar-disable-selinux() {
  sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
}

qar-files-remove() {
  rm -rf /usr/local/bin/qar* || return 1
  rm -rf /usr/local/share/qar/ || return 1
  rm -rf /qar/www || return 1
}

qar-files-copy() {
  mkdir -p /qar || return 1
  cp bin/qar* /usr/local/bin/ || return 1
  cp -r www/ /qar/www || return 1
  mkdir -p /qar/www/instance || return 1
  chown -R apache:apache /qar/www/instance || return 1
}

qar-docker() {
  if [ -x "$(command -v docker)" ]; then
    echo "Docker is already installed"
    return
  fi

  curl -fsSL https://get.docker.com | sh
}

qar-install-service() {
  cp etc/systemd/qar.service /etc/systemd/system/qar.service
  systemctl enable --now qar
}

qar-firewall() {
  firewall-cmd --permanent --add-port=80/tcp
  firewall-cmd --permanent --add-port=443/tcp
  firewall-cmd --reload
}

qar-httpd() {
  qar-dnf httpd
  rm -f /etc/httpd/conf.d/welcome.conf
  cp etc/httpd/qar.conf /etc/httpd/conf.d/qar.conf
  systemctl enable --now httpd
}

qar-python() {
  qar-dnf python3 python3-pip httpd mod_ssl python3-mod_wsgi
  pip3 install flask pip Flask-Migrate speedtest-cli psutil docker 1337x
}

qar-install-mdns() {
  qar-dnf avahi avahi-tools nss-mdns
  sed -i 's/mdns4_minimal/mdns4/' /etc/nsswitch.conf
  systemctl enable avahi-daemon
  systemctl start avahi-daemon
}

qar-install