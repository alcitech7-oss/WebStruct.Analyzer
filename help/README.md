# 🌐 WebStruct Analyzer Pro

**Versão:** 1.0.0  
**Status:** ✅ Estável  
**Autor:** [Alcitech7-oss](https://github.com/alcitech7-oss)  
**Repositório:** [github.com/alcitech7-oss/Webstruct.Analyzer](https://github.com/alcitech7-oss/Webstruct.Analyzer)

---

## 📖 SOBRE O PROJETO

**WebStruct Analyzer Pro** é uma ferramenta desktop para mapeamento estrutural de sites. Ela extrai todos os elementos HTML de uma página, gera seletores CSS e XPath automaticamente, e exporta os dados em Excel, JSON ou CSV.

Ideal para:

- 🧪 Automação de testes (QA)
- 🕷️ Web scraping e extração de dados
- 🔍 Análise de estrutura de sites
- 📊 Monitoramento de preços e cotações
- 🤖 Integração com Inteligência Artificial

---

## 🛠️ TECNOLOGIAS E FERRAMENTAS

| Ferramenta/Biblioteca | Versão | Finalidade |
|------------------------|--------|------------|
| **Python** | 3.10+ | Linguagem principal |
| **Flask** | 2.3.3 | Servidor web embutido |
| **Playwright** | 1.39.0 | Navegação e extração de elementos |
| **Pandas** | 2.0.3 | Manipulação e exportação de dados |
| **OpenPyXL** | 3.1.2 | Exportação para Excel |
| **PyInstaller** | 5.13.0 | Geração do executável (.exe) |
| **HTML5/CSS3/JavaScript** | - | Interface do dashboard |
| **Google Fonts (Inter)** | - | Tipografia da interface |

---

## 📦 BIBLIOTECAS E DEPENDÊNCIAS

### `requirements.txt`

```txt
Flask==2.3.3
pandas==2.0.3
openpyxl==3.1.2
playwright==1.39.0
selenium==4.15.0
webdriver-manager==4.0.1
```

### Instalação das Dependências

```bash
# Instala todas as dependências
pip install -r requirements.txt

# Instala os navegadores do Playwright
playwright install

# OU instala apenas os navegadores necessários (Chromium)
playwright install chromium
```

---

## 🗂️ ESTRUTURA DO PROJETO

```
📁 Webstruct.Analyzer/
├── 📁 core/                      # Núcleo da aplicação
│   ├── mapeador.py               # Mapeamento de sites com Playwright
│   ├── processador.py            # Processamento e estatísticas
│   └── gerador_codigo.py         # Geração de código (CSS, XPath, Playwright)
│
├── 📁 static/                    # Arquivos estáticos
│   ├── style.css                 # Estilos da interface
│   ├── script.js                 # Interatividade do dashboard
│   ├── fundo.jpg                 # Imagem de fundo
│   └── gif1.gif                  # Logo animado
│
├── 📁 templates/                 # Templates HTML
│   └── dashboard.html            # Interface principal
│
├── 📁 exports/                   # Pasta de exportação 
│
├── main.py                       # Ponto de entrada e launcher
├── requirements.txt              # Dependências do projeto
├── README.md                     # Documentação completa
└── TUTORIAL.md                   # Tutorial com exemplos práticos
```

---

## ⚙️ INSTALAÇÃO E CONFIGURAÇÃO

### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/alcitech7-oss/Webstruct.Analyzer.git
cd Webstruct.Analyzer
```

### 2️⃣ Crie um Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Instale os Navegadores do Playwright

```bash
pip install playwright

# Apenas Chromium
python -m playwright install chromium

# Apenas Firefox
python -m playwright install firefox

# Apenas WebKit (Safari)
python -m playwright install webkit
```

### 5️⃣ Execute o Projeto

```bash
# pelo launcher
python main.py
```

### 6️⃣ Acesse no Navegador

```
http://127.0.0.1:5000
```

---


### Como usar:


> ⚠️ **Requisitos:** Windows 10/11, navegador (Chrome/Edge/Firefox)

---

## 🧪 COMO USAR

### Passo 1: Digite a URL

```
https://www.uol.com.br/
```

### Passo 2: Clique em "Mapear"

### Passo 3: Confirme o mapeamento

### Passo 4: Aguarde o processamento

### Passo 5: Visualize os resultados

### Passo 6: Exporte para Excel, JSON ou CSV

### Passo 7: Copie seletores com 1 clique


---

## 🎯 EXEMPLO PRÁTICO: CAPTURANDO O DÓLAR

### Mapeamento do UOL

| posicao | tag   | classe                              | texto         |
| ------- | ----- | ----------------------------------- | ------------- |
| 188     | div   | exchangeBarHeader                   | (container)   |
| 191     | div   | exchangeBarHeader__container        | (container)   |
| 194     | span  | exchangeBarHeader__loading          | (loading)     |

### Código Gerado

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

---

## 🤖 USANDO COM INTELIGÊNCIA ARTIFICIAL

### Pergunta Recomendada:

> *"Analise este mapa do UOL. Quero capturar o valor do dólar (ex: 5,203). O mapa mostra a estrutura `exchangeBarHeader__container`. Me dê o seletor CSS, XPath e o código para capturar o valor, considerando que ele é carregado via JavaScript."*

### Seletores Encontrados:

| Tipo   | Seletor                                                         |
| ------ | --------------------------------------------------------------- |
| **CSS**  | `.exchangeBarHeader__item__value`                               |
| **CSS Alternativo** | `[class*="exchangeBarHeader"][class*="value"]`                  |
| **XPath** | `//span[contains(@class, "exchangeBarHeader__item__value")]`    |
| **XPath Alternativo** | `//*[contains(@class, "exchangeBarHeader__item__value")]` |

---

## 📊 COMPARAÇÃO DE IAs

| IA           | Desempenho                                                                        |
| ------------ | --------------------------------------------------------------------------------- |
| **Claude**   | ✅ Explicou o padrão e sugeriu `wait_for_selector` imediatamente                  |
| **Gemini**   | ✅ Na 3ª tentativa, entendeu o padrão e deu os seletores corretos                 |
| **ChatGPT**  | ✅ Leu o mapa, viu que a classe não existia, explicou o motivo e deu a solução   |

---

## 🛠️ GERANDO O EXECUTÁVEL (.EXE)

### Comando PyInstaller

```bash
pyinstaller --name "StructAnalyzer" --onefile --windowed --add-data "core;core" --add-data "static;static" --add-data "templates;templates" --add-data "playwright_browsers;playwright_browsers" --hidden-import flask --hidden-import openpyxl --hidden-import playwright --hidden-import playwright.sync_api --hidden-import pandas main.py
```

### O que cada parâmetro faz:

| Parâmetro | Função |
|-----------|--------|
| `--name` | Nome do executável |
| `--onefile` | Gera um único arquivo .exe |
| `--windowed` | Não exibe terminal (só o navegador) |
| `--add-data` | Inclui pastas no executável |
| `--hidden-import` | Inclui bibliotecas ocultas |

### Tem um arquivo TUTORIAL.md para mais detalhes de uso 
---

## 🔧 PERSONALIZAÇÃO

### Alterar o Logo (GIF)

1. Substitua o arquivo `static/gif1.gif` pelo seu GIF
2. Atualize o nome no `dashboard.html` se necessário

### Alterar a Imagem de Fundo

1. Substitua o arquivo `static/fundo.jpg` pela sua imagem
2. Ajuste o CSS se necessário

### Alterar Cores e Estilos

Edite o arquivo `static/style.css`:

```css
/* Cores principais */
body {
    background: #0a0e17;  /* Fundo escuro */
    color: #e6edf3;       /* Texto claro */
}

/* Gradiente do título */
.logo h1 {
    background: linear-gradient(135deg, #58a6ff, #a371f7);
}
```

---

## 📄 LICENÇA

MIT License — Use, modifique e compartilhe!

---

## 🤝 CONTRIBUIÇÕES

Contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📬 CONTATO

- **Autor:** [Alcitech7-oss](https://github.com/alcitech7-oss)
- **GitHub:** [github.com/alcitech7-oss/Webstruct.Analyzer](https://github.com/alcitech7-oss/Webstruct.Analyzer)

---

## ⭐ SE ESTE PROJETO TE AJUDOU

Considere dar uma estrela no GitHub! ⭐

---

**Feito com 💜, café ☕ e muita determinação.**
