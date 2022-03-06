#!/bin/bash

RUNTIME_USR=abby
INSTALL_DIR=/opt/abby

if [ "$EUID" -ne 0 ]; then
  echo "You must run this as root!"
  exit
fi

echo "This will be installed to $INSTALL_DIR."
echo "Press enter to begin or CTRL+C to exit."
read

id -u $RUNTIME_USR &>/dev/null || useradd -r -s /bin/false $RUNTIME_USR

chmod +x abby.py
rsync -rpXl --exclude=__pycache__ --exclude=default.config.py . $INSTALL_DIR
chown -R $RUNTIME_USR $INSTALL_DIR

cp --preserve=mode data/abby.service /etc/systemd/system/abby.service
systemctl daemon-reload

echo "Installation is finished!"
