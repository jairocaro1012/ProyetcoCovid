
import requests
from bs4 import BeautifulSoup
import pymysql
import datetime
from matplotlib import pyplot


fecha = datetime.datetime.now()
fecha = str(fecha.date())
url='https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Colombia'
req=requests.get(url)
soup=BeautifulSoup(req.content,'html.parser')
datos=soup.find_all('th')
total=list()

for i in datos:
    total.append(i.text)

Casos=str(total[89])
Recuperados=str(total[50])
Hospitalizados=str(total[56])
Unidades=str(total[59])
Muertes=str(total[62])

print(Casos,Recuperados,Hospitalizados,Unidades,Muertes)

connection = pymysql.connect(host='localhost',user='root',password='1234',db='seguimineto',charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        sql = "select fecha from total where fecha="+fecha+";"
        cursor.execute(sql)
        result = cursor.fetchone()
    if result == None:
        with connection.cursor() as cursor:
            sql = "insert into total values("+fecha+","+Casos+","+Recuperados+","+Hospitalizados+","+Unidades+","+Muertes+");"
            cursor.execute(sql)
            connection.commit()
finally:
    connection.close()

estado=('Recuperado','Hospitalizados','UCI',"Muertos")
slices=(Recuperados,Hospitalizados,Unidades,Muertes)
colores=('red','blue','black','green')
Valores=(0.1,0,0,0)
pyplot.pie(slices,colors=colores,labels=estado,autopct='%1.1f%%',explode=Valores,shadow=True)
pyplot.axis('equal')
pyplot.title('Numero de casos de Covid en colombia = '+Casos)
pyplot.show()

slices1=(Recuperados,Hospitalizados,Unidades,Muertes)

pyplot.title('Numero de casos de Covid en colombia = '+Casos)
pyplot.bar(estado,slices1,color=colores)
pyplot.axis('equal')
pyplot.show()


pyplot.title('Numero de casos de Covid en colombia = '+Casos)
pyplot.barh(range(4),slices1,color=colores)
pyplot.yticks(range(4),estado, rotation=60)
pyplot.axis('equal')
pyplot.show()
