from matplotlib import pyplot as plt
import datetime

registro_holder = []

def CreatePlot(registro):
    mes = registro[-1]['x'].month
    registro_t = [[x['x'].day,x['y']] for x in registro if x['x'].month == mes]


    registro_final = []
    for i in range(len(registro_t)):
        if i == 0:
            registro_final.append(registro_t[i])
        else:
            if registro_final[-1][0] == registro_t[i][0]:
                registro_final[-1][1] = registro_final[-1][1] + registro_t[i][1]
            else:
                registro_final.append(registro_t[i])

    return registro_final

#GRAFICO DE BARRAS
def CreateBarPlot(registro):
    x = []
    y = []
    for i in registro:
        x.append(i["nombre"])
        y.append(i["porcentaje"])

    plt.bar(x,y, color=("purple", "grey", "red", "blue", "brown",  "yellow", "black"))
    plt.savefig('R.png')
    plt.figure().clear()

#TODOS GASTOS
def CreatePlotPT(registro):
    registro_holder = CreatePlot(registro)
    plt.plot([x[0] for x in registro_holder], [x[1] for x in registro_holder])
    plt.savefig('PT.png')
    plt.figure().clear()


#INGRESOS Y GASTOS
def CreatePlotIE(registro, registro2):
    registro_holder = CreatePlot(registro)
    plt.plot([x[0] for x in registro_holder], [x[1] for x in registro_holder])
    registro_holder = CreatePlot(registro2)
    plt.plot([x[0] for x in registro_holder], [x[1] for x in registro_holder])
    plt.savefig('IE.png')
    plt.figure().clear()

registro_PT = [{'x': datetime.date(2022, 5, 1), 'y': 500}, {'x': datetime.date(2022, 5, 1), 'y': -500}, {'x': datetime.date(2022, 8, 3), 'y': 1000}, {'x': datetime.date(2022, 10, 20), 'y': 400}, {'x': datetime.date(2022, 10, 21), 'y': -266}, {'x': datetime.date(2022, 10, 21), 'y': -499}, {'x': datetime.date(2022, 10, 21), 'y': 5001}]

registro_I = [{'x': datetime.date(2022, 3, 10), 'y': 500}, {'x': datetime.date(2022, 8, 21), 'y': 1500}, {'x': datetime.date(2022, 8, 22), 'y': 5500}]

registro_E = [{'x': datetime.date(2022, 5, 21), 'y': 1000}, {'x': datetime.date(2022, 5, 21), 'y': 600}, {'x': datetime.date(2022, 5, 22), 'y': 666}, {'x': datetime.date(2022, 5, 22), 'y': 233}]

registro_R = [{'nombre': 'OCIO', 'porcentaje': 0.0}, {'nombre': 'IMPUESTOS', 'porcentaje': 0.0}, {'nombre': 'SALUD', 'porcentaje': 98.96}, {'nombre': 'SERVICIOS', 'porcentaje': 0.0}, {'nombre': 'GASTRONOMIA', 'porcentaje': 0.41}, {'nombre': 'COMPRAS', 'porcentaje': 0.09}, {'nombre': 'OTROS', 'porcentaje': 0.52}]

CreatePlotPT(registro_PT)
CreatePlotIE(registro_I, registro_E)
CreateBarPlot(registro_R)