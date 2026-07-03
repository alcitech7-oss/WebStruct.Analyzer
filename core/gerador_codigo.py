"""
GERADOR DE CÓDIGO - WebStruct Analyzer
Gera código pronto pra copiar em diferentes ferramentas de automação
"""


def gerar_codigo(seletor, tipo_seletor, ferramenta):
    """
    Gera código baseado no seletor e ferramenta escolhida

    Args:
        seletor (str): O seletor CSS ou XPath
        tipo_seletor (str): 'css' ou 'xpath'
        ferramenta (str): 'selenium', 'playwright', 'beautifulsoup'

    Returns:
        str: Código formatado pronto pra copiar
    """
    if tipo_seletor == "css":
        return _gerar_css(seletor, ferramenta)
    elif tipo_seletor == "xpath":
        return _gerar_xpath(seletor, ferramenta)
    return "# Tipo de seletor não suportado"


def _gerar_css(seletor, ferramenta):
    templates = {
        "selenium": f"""from selenium.webdriver.common.by import By

elemento = driver.find_element(By.CSS_SELECTOR, "{seletor}")
texto = elemento.text
elemento.click()
""",
        "playwright": f"""from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("URL_AQUI")
    elemento = page.query_selector("{seletor}")
    texto = elemento.text_content()
    elemento.click()
    browser.close()
""",
        "beautifulsoup": f"""from bs4 import BeautifulSoup
import requests

response = requests.get("URL_AQUI")
soup = BeautifulSoup(response.text, 'html.parser')
elemento = soup.select_one("{seletor}")
texto = elemento.text
""",
    }
    return templates.get(ferramenta, "# Ferramenta não suportada")


def _gerar_xpath(seletor, ferramenta):
    templates = {
        "selenium": f"""from selenium.webdriver.common.by import By

elemento = driver.find_element(By.XPATH, "{seletor}")
texto = elemento.text
elemento.click()
""",
        "playwright": f"""from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("URL_AQUI")
    elemento = page.query_selector("xpath={seletor}")
    texto = elemento.text_content()
    elemento.click()
    browser.close()
""",
        "beautifulsoup": f"""# BeautifulSoup não suporta XPath nativamente
# Use Selenium ou Playwright para XPath

from selenium.webdriver.common.by import By
elemento = driver.find_element(By.XPATH, "{seletor}")
""",
    }
    return templates.get(ferramenta, "# Ferramenta não suportada")
