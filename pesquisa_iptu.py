from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from google.colab import auth
import gspread
from google.auth import default
import time
import random

# 1. Autenticação e acesso ao Google Sheets
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)
sh = gc.open('InscricIPTU')
worksheet = sh.sheet1
inscricoes = worksheet.col_values(1)[2:] # Obtém inscrições da coluna A, a partir da linha 3

# 2. Configuração do Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36") # Adiciona user-agent
driver = webdriver.Chrome(options=options)
driver.get("https://grpfordam.sefin.fortaleza.ce.gov.br/grpfor/pagesPublic/iptu/damIptu/imprimirDamIptu.seam")

# 3. Loop para cada inscrição
for i, inscricao in enumerate(inscricoes):
    if inscricao:
        tentativas = 0
        while tentativas < 3: # Tenta 3 vezes em caso de erro
            try:
                # Pausa aleatória antes de inserir a inscrição
                time.sleep(random.uniform(3, 7))

                # Insere inscrição e clica em Pesquisar
                inscricao_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pmfInclude:cadastroForm:inscricaoImovelDec:inscricao"]')))
                inscricao_input.clear()
                inscricao_input.send_keys(inscricao)

                # Pausa aleatória antes de clicar em Pesquisar
                time.sleep(random.uniform(2, 5))

                driver.find_element(By.XPATH, '//*[@id="pmfInclude:cadastroForm:inscricaoImovelDec:botaoRecuperarImovelNaoLogado"]').click()

                # Pausa aleatória antes de extrair os dados
                time.sleep(random.uniform(5, 10))

                # Extrai dados
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pmfInclude:cadastroForm:mensagens"]/dt/span[2]')))
                    print(f"Inscrição {inscricao} não encontrada.")
                    break # Sai do loop de tentativas
                except:
                    localizacao = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pmfInclude:cadastroForm:dadosImovel"]/fieldset/table[2]/tbody/tr/td[1]/table/tbody/tr/td[2]'))).text
                    cartografia = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pmfInclude:cadastroForm:dadosImovel"]/fieldset/table[1]/tbody/tr/td[2]/table/tbody/tr/td[2]'))).text
                    try:
                        possuidor = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pmfInclude:cadastroForm:dadosImovel"]/fieldset/table[3]/tbody/tr[1]/td/table/tbody/tr/td'))).text
                    except:
                        possuidor = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pmfInclude:cadastroForm:dadosImovel"]/fieldset/table[3]/tbody/tr[2]/td/table/tbody/tr/td/span'))).text
                    correspondencia = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pmfInclude:cadastroForm:dadosImovel"]/fieldset/table[2]/tbody/tr/td[2]/table/tbody/tr/td[3]'))).text

                    # Atualiza planilha
                    worksheet.update_cell(i + 3, 5, localizacao)
                    worksheet.update_cell(i + 3, 6, cartografia)
                    worksheet.update_cell(i + 3, 7, possuidor)
                    worksheet.update_cell(i + 3, 8, correspondencia)

                    # Pausa aleatória antes de limpar
                    time.sleep(random.uniform(3, 6))

                    # Limpa e espera
                    driver.find_element(By.XPATH, '//*[@id="pmfInclude:cadastroForm:inscricaoImovelDec:limparPublic"]').click()

                    # Pausa aleatória antes de recarregar a página
                    time.sleep(random.uniform(6, 12))

                    driver.get("https://grpfordam.sefin.fortaleza.ce.gov.br/grpfor/pagesPublic/iptu/damIptu/imprimirDamIptu.seam") #Recarrega a página
                    break # Sai do loop de tentativas
            except Exception as e:
                print(f"Erro ao processar {inscricao}: {e}")
                tentativas += 1
                time.sleep(5) # Espera antes de tentar novamente

driver.quit()