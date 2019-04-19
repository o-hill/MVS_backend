
from mongoengine import *

class Dish(Document):
    dish_number = IntField()
    experiment = ReferenceField(Experiment)

class Experiment(Document):
    start_date = DateTimeField()
    end_date = DatetimeField()

