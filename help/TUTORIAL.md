📄 TUTORIAL

# 🌐 WebStruct Analyzer Pro — Mapeamento Estrutural com IA

**Versão:** 1.0.0  
**Status:** ✅ Estável e validado com casos reais  
**Autor:** [Alcitech7-oss](https://github.com/alcitech7-oss)

---

## 🧠 O QUE É ISSO?

**WebStruct Analyzer Pro** é uma ferramenta desktop que mapeia a estrutura HTML de qualquer site, gera seletores CSS e XPath automaticamente, e exporta os dados em Excel, JSON ou CSV.

Além disso, você pode usar o mapa gerado com **Inteligência Artificial** para extrair informações específicas, como o valor do dólar, preços de produtos ou qualquer outro dado dinâmico.

---

## 🎯 OBJETIVO DESTE POST

1. Demonstrar como a ferramenta funciona na prática
2. Mostrar como usar IA para interpretar os mapas gerados
3. Comparar respostas de diferentes IAs (ChatGPT, Gemini, Claude)
4. Ensinar a **perguntar do jeito certo** para obter os melhores resultados

---

## 🧪 LABORATÓRIO 1: MAPEANDO O UOL

### Entrada

```bash
URL: https://www.uol.com.br/
Ferramenta: WebStruct Analyzer Pro (.exe)
```

### Saída

Arquivo Excel com **mais de 4.000 elementos** mapeados, incluindo:

| posicao | tag   | classe                              | texto         |
|---------|-------|-------------------------------------|---------------|
| 188     | div   | exchangeBarHeader                   | (container)   |
| 191     | div   | exchangeBarHeader__container        | (container)   |
| 194     | span  | exchangeBarHeader__loading          | (loading)     |

> ⚠️ **Observação:** O valor do dólar (`5,203`) **não apareceu** no mapa porque é carregado via JavaScript após o mapeamento.

---

## 🔍 LABORATÓRIO 2: USANDO IA PARA EXTRAIR O DÓLAR

### O Problema

O mapa não mostrou o valor do dólar, mas mostrou a **estrutura** onde ele vai aparecer.

### A Pergunta Certa

> *"Analise este mapa do UOL. Quero capturar o valor do dólar (ex: 5,203). O mapa mostra a estrutura `exchangeBarHeader__container`. Me dê o seletor CSS, XPath e o código para capturar o valor, considerando que ele é carregado via JavaScript."*

---

## 📊 LABORATÓRIO 3: COMPARANDO IAs

### Resultados Obtidos

| IA           | Resposta                                                                                      | Funcionou? 
| ------------ | --------------------------------------------------------------------------------------------- | ---------- 
| **Claude**   | Explicou o padrão, deu o seletor e sugeriu `wait_for_selector` imediatamente.                 | ✅ |        
| **Gemini**   | Na 3ª tentativa, entendeu após mudar a forma de perguntar, e deu os seletores corretos.       | ✅ |         
| **ChatGPT**  | Leu o mapa, viu que a classe não existia, explicou o motivo e deu a solução.                  | ✅ |        

### 🏆 Melhor Performance

| Critério                    | Melhor IA |
| --------------------------- | --------- |
| Análise do mapa             | ChatGPT   |
| Entendimento do padrão      | Claude    |
| Explicação do motivo        | ChatGPT   |
| Sugestão de código          | Claude    |
| Dicas de automação          | Gemini    |

---

## 💡 O QUE APRENDEMOS

### 1. O mapa é imbatível para estrutura

Mesmo sem mostrar o valor do dólar, o mapa revelou:

- O container da barra de câmbio (`.exchangeBarHeader`)
- O container interno (`.exchangeBarHeader__container`)
- O padrão de nomenclatura (`.exchangeBarHeader__item__value`)

### 2. A IA precisa de boas perguntas

| Pergunta Vaga                         | Pergunta Específica                                   |
| ------------------------------------- | ----------------------------------------------------- |
| "Acha o dólar"                        | "Acha o VALOR NUMÉRICO do dólar (ex: 5,203)"          |
| "Me dá o seletor"                     | "Me dá o seletor CSS e XPath do elemento com o valor" |
| "Como faço?"                          | "Código em Python com Selenium, com espera implícita" |

### 3. A IA aprende com tentativas

- **Gemini:** Acertou na 3ª tentativa
- **ChatGPT:** Acertou de primeira
- **Claude:** Acertou de primeira com análise aprofundada

---

## 🛠️ CÓDIGO FINAL

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Aguarda o JavaScript carregar o valor
dolar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR,
        ".exchangeBarHeader__item__value"))
)

valor = dolar.text
print(f"💵 Dólar: R$ {valor}")
```

Ou com Playwright:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.uol.com.br")

    page.wait_for_selector(".exchangeBarHeader__item__value", timeout=10000)
    dolar = page.locator(".exchangeBarHeader__item__value")
    valor = dolar.text_content()

    print(f"💵 Dólar: R$ {valor}")
    browser.close()
```

---

## 🎯 CONCLUSÃO

> **O WebStruct Analyzer Pro entrega a estrutura. A IA entrega a inteligência. Juntas, são imbatíveis.**

### Com este workflow você pode:

- ✅ Mapear qualquer site
- ✅ Extrair dados estáticos e dinâmicos
- ✅ Usar IA para interpretar os mapas
- ✅ Obter seletores precisos
- ✅ Automatizar a captura de dados

---

## 📦 REPOSITÓRIO

🔗 [github.com/alcitech7-oss/Webstruct.Analyzer](https://github.com/alcitech7-oss/Webstruct.Analyzer)

---

## 🤝 CONTRIBUIÇÕES

Contribuições são bem-vindas! Abra uma issue ou pull request.

---

## 📄 LICENÇA

MIT License — Use, modifique e compartilhe!

---

**Feito com 💜, café ☕ e determinação.**

---