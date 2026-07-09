```markdown
# 🏗️ Struct Analyzer

Uma ferramenta inteligente que analisa a estrutura de **qualquer site**, extraindo **todas as tags, classes, IDs, links e textos**, e organiza tudo em uma planilha Excel com **seletores CSS e XPath prontos para uso**.

> 🔥 **Testado e aprovado no Instagram!** Sim, a ferramenta conseguiu mapear um dos sites mais complexos do mundo com React, classes ofuscadas e conteúdo dinâmico.

---

## 🎯 Para que serve?

- **Mapear a estrutura completa** de qualquer site
- **Extrair seletores CSS e XPath** automaticamente
- **Entender a hierarquia** do DOM com profundidade e posição
- **Usar com I.A.** — cole a planilha e peça seletores específicos
- **Economizar horas** de inspeção manual no navegador
- **Funciona em sites com React, Angular, Vue e SPAs**

---

## 📋 O que a planilha te entrega

| Coluna | O que é | Exemplo |
|--------|---------|---------|
| **posicao** | Ordem do elemento na página | `13` |
| **profundidade** | Nível no DOM (0 = raiz) | `3` |
| **tag** | Nome da tag HTML | `h1`, `div`, `a` |
| **classe** | Classes CSS | `title`, `header`, `x1a2a7pz` (classes ofuscadas também!) |
| **id** | ID do elemento | `#app`, `#mount_0_0_0e` |
| **seletor_css** | 🔥 Seletor CSS pronto | `.title`, `#error-code` |
| **xpath** | 🔥 XPath pronto | `//h1[contains(@class, "title")]` |
| **link** | URL (se for um link) | `https://...` |
| **texto** | Conteúdo textual | `"8,506 posts • 685M followers"` |
| **pai** | Tag do elemento pai | `main`, `body`, `section` |

---

## 🧪 Testado em sites reais

| Site | Complexidade | Resultado |
|------|--------------|-----------|
| **UOL** | Conteúdo estático + JS leve | ✅ 100% |
| **Globo** | Conteúdo estático + JS leve | ✅ 100% |
| **Instagram** | React + classes ofuscadas + conteúdo dinâmico | ✅ 100% (233 elementos extraídos) |
| **Magazine Luiza** | Anti-bot forte (Akamai) | ⚠️ Bloqueado (erro 403) |

---

## 🚀 Como usar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/struct-analyzer.git
cd struct-analyzer
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
playwright install
```

### 3. Rode o script
```bash
python main.py
```

### 4. Digite a URL
```
🌐 Qual site você quer analisar? https://www.instagram.com/instagram/
```

### 5. Pronto!
O arquivo `estrutura_20260701_100725.xlsx` será gerado com toda a estrutura do site.

---

## 💬 Como usar com I.A. (ChatGPT, Claude, etc.)

**1. Rode o Struct Analyzer** no site que você quer analisar

**2. Cole a planilha na conversa com a I.A.**

**3. Faça perguntas como:**
> - "Me dá o seletor do menu de navegação"
> - "Qual a classe dos títulos das notícias?"
> - "Como eu pego todos os links da barra preta?"
> - "Qual o XPath do botão de login?"
> - "Me dá o seletor dos posts do Instagram"

**4. A I.A. olha a planilha e te dá os seletores prontos!**

```python
# Exemplo: a I.A. te responde com o seletor
seletor = ".headerDesktop__menu"
elementos = page.query_selector_all(seletor)
```

---

## 📊 Exemplo de saída

### Site simples (UOL):
| posicao | profundidade | tag | classe | seletor_css | texto |
|---------|--------------|-----|--------|-------------|-------|
| 9 | 2 | header | header | .header | |
| 13 | 3 | h1 | title | .title | UOL - Seu universo online |

### Site complexo (Instagram):
| posicao | profundidade | tag | classe | seletor_css | texto |
|---------|--------------|-----|--------|-------------|-------|
| 163 | 1 | body | _ar45 | ._ar45 | 8,506 posts • 685M followers |
| 233 | 5 | div | x9f619 | #scrollview | Discover what's new on Instagram |
| 142 | 2 | title | | title | Instagram (@instagram) • Instagram photos and videos |

---

## 🛠️ Tecnologias

| Tecnologia | Função |
|------------|--------|
| **Python** | Linguagem principal |
| **Playwright** | Navegação e extração de elementos |
| **Pandas** | Manipulação de dados |
| **OpenPyXL** | Geração de planilhas Excel |

---

## 📦 Dependências

```txt
playwright==1.40.0
pandas==2.1.0
openpyxl==3.1.0
```

---

## 🔧 Personalização

Quer mudar algo? O código é modular:

- `analisar_estrutura(url)` → Extrai os dados do site
- `gerar_seletor_css(tag, classe, id)` → Gera seletores CSS
- `gerar_xpath(tag, classe, id, posicao)` → Gera XPath
- `salvar_excel(dados)` → Salva a planilha

---

## ⚠️ Limitações

- Sites com **bloqueio de bot** (ex: Cloudflare, Akamai) podem retornar erro 403
- Conteúdo que exige **login** não será acessado
- Conteúdo **carregado via JavaScript** é capturado (Playwright é headless)
- Textos muito longos são limitados a 300 caracteres
- Classes ofuscadas (ex: `x1a2a7pz`) são capturadas, mas podem ser difíceis de ler

---

## 📝 Licença

MIT - Use à vontade! 🚀

---

## 🤝 Contribuindo

Quer melhorar? Manda um PR ou abre uma issue!

---

## 🏆 Resultados de testes

| Site | Elementos | Profundidade | Status |
|------|-----------|--------------|--------|
| UOL | 200+ | 5 | ✅ |
| Instagram (perfil existe) | 233 | 17 | ✅ |
| Instagram (perfil não existe) | 165 | 17 | ✅ |
| Magazine Luiza | - | - | ⚠️ Bloqueado |

---

**Feito com ❤️ por um dev que cansou de ficar caçando no F12.**

**Aprendeu Python em 1 mês e já criou isso. Imagina o que vem por aí!** 🚀
```