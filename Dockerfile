FROM python:3.10-slim

WORKDIR /app

# ⭐ INSTALA DEPENDÊNCIAS BÁSICAS ⭐
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ⭐ INSTALA O CHROME (MÉTODO ATUALIZADO - SEM apt-key) ⭐
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# ⭐ COPIA E INSTALA AS BIBLIOTECAS PYTHON ⭐
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ⭐ INSTALA O CHROMIUM DO PLAYWRIGHT (OPCIONAL, MAS GARANTE COMPATIBILIDADE) ⭐
RUN playwright install chromium

# ⭐ COPIA O RESTO DO CÓDIGO ⭐
COPY . .

CMD ["python", "main.py"]