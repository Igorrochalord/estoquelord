from selenium import webdriver
from selenium.webdriver.common.by import By

# Configurações do Selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Executar em modo headless
chrome_options.add_argument('--disable-gpu')  # Desabilitar aceleração de GPU
chrome_options.add_argument('--no-sandbox')  # Desabilitar sandbox
driver = webdriver.Chrome('/caminho/para/chromedriver', options=chrome_options)

# URL da loja online
url = 'https://www.google.com/search?q=banana&source=lmns&tbm=shop&client=opera-gx&hs=bHZ&hl=pt-BR&sa=X&ved=2ahUKEwjxyuTGwuv-AhU-B7kGHf6-DyMQ_AUoAnoECAEQAg'

# Navegar para a página da loja online
driver.get(url)

# Extrair os nomes e preços dos produtos
produtos = driver.find_elements(By.XPATH, '//div[@class="produto"]')
for produto in produtos:
    nome = produto.find_element(By.XPATH, './/h2').text
    preco = produto.find_element(By.XPATH, './/span[@class="preco"]').text
    print(nome, preco)

# Fechar o navegador
driver.quit()
