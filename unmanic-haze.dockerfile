FROM archlinux:base

WORKDIR /saveme

RUN pacman -Syyu

RUN pacman -S python3 python-pip git nodejs npm ffmpeg

#Creating user with PERMS
RUN groupadd -g 1000 user \
  && useradd -d /home/user -m -u 1000 -g 1000 user

#Living on the bleeding edge
RUN git clone https://github.com/Unmanic/unmanic

CMD cd /saveme/unmanic
CMD git submodule update --init --recursive
CMD python3 -m pip install -r requirements.txt requirements-dev.txt
CMD sed -i 's/library_count = 2/library_count = 20/g' ./unmanic/libs/session.py
CMD sed -i 's/link_count = 5/link_count = 50/g' ./unmanic/libs/session.py
CMD python3 ./setup.py install
CMD runuser -l linux -c "export HOME_DIR=/saveme/ && unmanic"
