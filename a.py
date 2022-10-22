from matplotlib import pyplot as plt
import datetime
registro = [{'x': datetime.date(2022, 2, 1), 'y': 100}, {'x': datetime.date(2022, 2, 2), 'y': 100}, {'x': datetime.date(2022, 2, 2), 'y': 100}, {'x': datetime.date(2022, 2, 3), 'y': -100}, {'x': datetime.date(2022, 2, 3), 'y': -100}, {'x': datetime.date(2022, 2, 4), 'y': 100}]
largo = len(registro)



registro_x = [x['x'] for x in registro]
registro_y = [x['y'] for x in registro]




for i in range(largo):
    registro_x = []
    registro_y = []
    last_month = registro[largo-(1)]["x"].month
    last_day = registro[largo-(1)]["x"].day
    day_plata = 0
    if(registro[largo-(i+1)]['x'].month == last_month):
        break
    else:
        if(registro[largo-(i+1)]['x'].day == last_day):
            registro_x.append(last_day)
            registro_y.append(day_plata)
            day_plata = 0
        else:
            day_plata += registro[largo-(i+1)]['y']
        last_day = registro[largo-(i+1)]['x'].day
print(registro_x)
print(registro_y)
plt.plot(registro_x, registro_y)
plt.show()