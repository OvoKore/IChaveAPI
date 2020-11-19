## IChave
API do meu tcc

pip3 install pipenv

Flask
flask_sqlalchemy
flask_migrate
flask_marshmallow
marshmallow_sqlalchemy
flask-jwt-extended

## Como rodar esse projeto

export FLASK_APP=app
export FLASK_ENV=Development
export FLASK_DEBUG=True

pipenv shell
flask run --host=0.0.0.0 --reload

## Como fazer as migrações

flask db init
flask db migrate
flask db upgrade

## Maria DB
sudo apt install mariadb-server

mysql
CREATE DATABASE dbchave;
CREATE USER 'ichave'@'192.168.0.59' IDENTIFIED BY 'passchave';
GRANT ALL PRIVILEGES ON dbchave.* TO 'ichave'@'192.168.0.59';
FLUSH PRIVILEGES;
\q

nano /etc/mysql/mariadb.conf.d/50-server.cnf
#bind-address = 0.0.0.0
sudo systemctl restart mysql

DROP DATABASE dbchave;
CREATE DATABASE dbchave;
\q