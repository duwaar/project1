#!/bin/sh

export FLASK_APP=application.py
export FLASK_ENV=development
export DATABASE_URL=postgres://qhutchfxohvldy:06fb88a98fcb777f47b0cf6c3dd38bf8c6ccc0cd22cb540da4e607bd0b431bd8@ec2-54-197-34-207.compute-1.amazonaws.com:5432/d567u6iinhno1a

. ./env/bin/activate
flask run

exit 0
