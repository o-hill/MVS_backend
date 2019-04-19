from datetime import datetime
from database import MongoDatabase

db = MongoDatabase()
experiments = db.experiments

format = '%Y-%m-%d'

available_times = []

for a in range(1):

    dish = list(db.experiments.find({'dishNumber': str(a + 1)}))

    for b in range(1):

        start_date = list(dish)[b]['startDate']
        start_experiment = start_date

        end_date = list(dish)[b]['endDate']
        end_experiment = end_date

        start_experiment = datetime.strptime(start_experiment, format)
        end_experiment = datetime.strptime(end_experiment, format)

        start_experiment = int(datetime.timestamp(start_experiment))
        end_experiment = int(datetime.timestamp(end_experiment))

        print(start_experiment, type(start_experiment))
        print(end_experiment, type(end_experiment))

        available_times.append(range(start_experiment, end_experiment))

print(len(available_times))

# if statement to see if new experiments can fit in the schedule
# need to repopulate list every time with all the experiments
# need to black out space on the front end when time/date not available
# maybe a for loop for the repopulattion
# need to strip seconds when sending dates/times to front end
