from datetime import datetime
from database import MongoDatabase

db = MongoDatabase()
experiments = db.experiments

format = '%Y-%m-%d %H:%M'

for i in range(6):
    

dish_1 = list(db.experiments.find({'dishNumber': '1'}))

start_time = list(dish_1)[0]['startTime']
start_date = list(dish_1)[0]['startDate']
start_experiment = start_date + ' ' + start_time

end_time = list(dish_1)[0]['endTime']
end_date = list(dish_1)[0]['endDate']
end_experiment = end_date + ' ' + end_time

start_experiment = datetime.strptime(start_experiment, format)
end_experiment = datetime.strptime(end_experiment, format)

start_experiment = int(datetime.timestamp(start_experiment))
end_experiment = int(datetime.timestamp(end_experiment))

print(start_experiment, type(start_experiment))
print(end_experiment, type(end_experiment))

available_times = []

available_times.append(list(range(start_experiment, end_experiment)))

print(available_times, type(available_times))

# if statement to see if new experiments can fit in the schedule
# need to repopulate list every time with all the experiments
# need to black out space on the front end when time/date not available
# maybe a for loop for the repopulattion
