#!/bin/bash
echo -n "BEGIN:" >> /home/tobi/backup.log
date >> /home/tobi/backup.log
rsync -a /mnt/nas/Data rsync://192.168.0.166/rsync/ubuntu-nas/
echo -n "END:" >> /home/tobi/backup.log
date >> /home/tobi/backup.log
