import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import mariadb
import re
from unidecode import unidecode
import builtins

try:
    mydb = mariadb.connect(host='localhost', user='root', password='', database='compara_precos')
except mariadb.Error as e:
    print(f'Ocorreu um erro: {e}')
    exit()

mycursor = mydb.cursor()

inputPesq = input("Digite o nome do celular: \n")

option = Options()

option.add_argument("user-data-dir=C:/Users/marco/AppData/Local/Google/Chrome/User Data")

driver = webdriver.Chrome(options=option)

driver.get("https://www.google.com/search?q=z+fold+4&sxsrf=ALiCzsZ304L3McctoBUC_09bk4OQLg9DNw:1669562492399&source=lnms&tbm=shop&sa=X&ved=2ahUKEwikpaj61M77AhV-q5UCHY51AIcQ_AUoAXoECAIQAw&biw=1366&bih=625&dpr=1")

input = driver.find_element(By.CLASS_NAME, "gLFyf")

input.click()

input.clear()

input.send_keys(inputPesq)

driver.find_element(By.CLASS_NAME, "Tg7LZd").click()

titulo = driver.find_element(By.CLASS_NAME, "center_col")

html_content = titulo.get_attribute('outerHTML')

soup = BeautifulSoup(html_content, 'html.parser')

time.sleep(4)

for t in soup.find_all("div", {"class": "sh-dgr__content"}):
    nome = t.find("h3", {"class": "tAxDx"}).text
    nome = nome.replace("'", "")

    loja = t.find("div", {"class": "aULzUe"}).text
    preco = re.sub('[^0-9\,]', '', t.find("span", {"class": "a8Pemb"}).text)
    
    sql = "insert into dados (loja, nome, preco) values ('{}', '{}', '{}')".format(loja, nome, preco)
    print(sql)
    mycursor.execute(sql)
    mydb.commit()

sql = "select nome, loja, preco from dados ORDER BY preco"

mycursor.execute(sql)

res = mycursor.fetchall()

print("Ordenado por preco")

for x in res:
    print(f"Nome: {x[0]}")
    print(f"Loja: {x[1]}")
    print(f"Preco: R${x[2]}")
    print("-------------------------------------------")

driver.close()

delDados = builtins.input("Deseja apagar os dados salvos do banco de dados? s/n \n")

if delDados == 's':
    mycursor.execute("truncate dados")