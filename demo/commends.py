import click
from demo import app, db
from demo.models import User, Record, Habit
from datetime import date

# 初始化数据库
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')
