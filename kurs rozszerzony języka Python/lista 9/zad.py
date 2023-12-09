import requests
import matplotlib.pyplot as plt
from prywatne import ApiKEY

plt.rcParams["figure.figsize"] = [11, 7]
plt.rcParams["figure.autolayout"] = True
fig,axs = plt.subplots(3, sharey=True)
fig.suptitle("cena zlota/60 dolarow w latach 2021-22 i ich przewidywana cena w 2023")

def zloto_dzien_na_miesiac(response):
    miesiace_cena = {}
    ile_notowan = {}
    for el in response.json():
        if el['data'][5:7] in miesiace_cena:
            ile_notowan[el['data'][5:7]] = ile_notowan[el['data'][5:7]] + 1
            miesiace_cena[el['data'][5:7]] =  miesiace_cena[el['data'][5:7]] + el['cena']
        else:
            ile_notowan[el['data'][5:7]] = 1
            miesiace_cena[el['data'][5:7]] = el['cena']

    for key in miesiace_cena:
        miesiace_cena[key] = miesiace_cena[key]/ile_notowan[key]
    return miesiace_cena

def dolar_dzien_na_miesiac(response):
    miesiace_cena = {}
    ile_notowan = {}
    for el in response.json()['rates']:
        if el['effectiveDate'][5:7] in miesiace_cena:
            ile_notowan[el['effectiveDate'][5:7]] = ile_notowan[el['effectiveDate'][5:7]] + 1
            miesiace_cena[el['effectiveDate'][5:7]] =  miesiace_cena[el['effectiveDate'][5:7]] + el['mid']
        else:
            ile_notowan[el['effectiveDate'][5:7]] = 1
            miesiace_cena[el['effectiveDate'][5:7]] = el['mid']
    for key in miesiace_cena:
        miesiace_cena[key] = miesiace_cena[key]*60/ile_notowan[key]
    return miesiace_cena

NBPzloto2021 = "http://api.nbp.pl/api/cenyzlota/2021-01-01/2021-12-31"
NBPzloto2022 = "http://api.nbp.pl/api/cenyzlota/2022-01-01/2022-12-31"
NBPzloto2023 = "http://api.nbp.pl/api/cenyzlota/2023-01-01/2023-12-01"

NBPdolar2021 = "http://api.nbp.pl/api/exchangerates/rates/A/USD/2021-01-01/2021-12-31"
NBPdolar2022 = "http://api.nbp.pl/api/exchangerates/rates/A/USD/2022-01-01/2022-12-31"
NBPdolar2023 = "http://api.nbp.pl/api/exchangerates/rates/A/USD/2023-01-01/2023-12-01"

response = requests.get(NBPzloto2021)
miesiace_cena1 = zloto_dzien_na_miesiac(response)
axs[0].plot([miesiac for miesiac in miesiace_cena1], [miesiace_cena1[i] for i in miesiace_cena1], marker='o')

response = requests.get(NBPzloto2022)
miesiace_cena2 = zloto_dzien_na_miesiac(response)
axs[1].plot([miesiac for miesiac in miesiace_cena2], [miesiace_cena2[i] for i in miesiace_cena2], marker='o')

# przewidywana cena zlota na 2023 to zwyczajnie srednia z poprzednich lat dla poszczegolnych miesiecy
miesiace_cena3 = {key:(miesiace_cena1[key]+miesiace_cena2[key])/2 for key in miesiace_cena1}
axs[2].plot([miesiac for miesiac in miesiace_cena3], [miesiace_cena3[i] for i in miesiace_cena3], marker='o')

# i to samo robimy dla dolara
response = requests.get(NBPdolar2021)
miesiace_cena1 = dolar_dzien_na_miesiac(response)
axs[0].plot([miesiac for miesiac in miesiace_cena1], [miesiace_cena1[i] for i in miesiace_cena1], marker='o')

response = requests.get(NBPdolar2022)
miesiace_cena2 = dolar_dzien_na_miesiac(response)
axs[1].plot([miesiac for miesiac in miesiace_cena2], [miesiace_cena2[i] for i in miesiace_cena2], marker='o')

# przewidywana cena dolarow na 2023 to zwyczajnie srednia z poprzednich lat dla poszczegolnych miesiecy
miesiace_cena3 = {key:(miesiace_cena1[key]+miesiace_cena2[key])/2 for key in miesiace_cena1}
axs[2].plot([miesiac for miesiac in miesiace_cena3], [miesiace_cena3[i] for i in miesiace_cena3], marker='o')

# jeszcze faktyczne dane z 2023 do porownania
response = requests.get(NBPzloto2023)
miesiace_cena1 = zloto_dzien_na_miesiac(response)
axs[2].plot([miesiac for miesiac in miesiace_cena1], [miesiace_cena1[i] for i in miesiace_cena1], marker='o')

response = requests.get(NBPdolar2023)
miesiace_cena1 = dolar_dzien_na_miesiac(response)
axs[2].plot([miesiac for miesiac in miesiace_cena1], [miesiace_cena1[i] for i in miesiace_cena1], marker='o')

for i in range(2):
    axs[i].legend(["zloto","60 dolarow"])
    axs[i].set(xlabel="miesiace", ylabel="cena w zł", title=f"ceny w {2021+i}")

axs[2].legend(["przew. zloto","przew. 60 dol", "fakt. zloto", "fakt. 60 dol"])
axs[2].set(xlabel="miesiace", ylabel="cena", title="przewidywane ceny vs faktyczne w 2023")

plt.show()

