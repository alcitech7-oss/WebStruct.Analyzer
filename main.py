import os
import sys
import webbrowser
import threading
import time
import subprocess

# ============================================
# CONFIGURA O PLAYWRIGHT PARA USAR OS NAVEGADORES INCLUÍDOS
# ============================================


def configurar_playwright():
    """Configura o Playwright para usar os navegadores incluídos no .exe"""

    if getattr(sys, "frozen", False):
        # Estamos no .exe
        browsers_path = os.path.join(sys._MEIPASS, "playwright_browsers")

        if os.path.exists(browsers_path):
            # Configura o Playwright para usar essa pasta
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = browsers_path
            print(f"✅ Navegadores configurados em: {browsers_path}")
        else:
            print("⚠️ Navegadores não encontrados no .exe")
            print("📦 O Playwright vai baixar os navegadores na primeira execução...")
    else:
        # Estamos em desenvolvimento
        browsers_path = os.path.join(os.getcwd(), "playwright_browsers")
        if os.path.exists(browsers_path):
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = browsers_path
            print(f"✅ Navegadores configurados em: {browsers_path}")


# CHAMA ISSO ANTES DE IMPORTAR O PLAYWRIGHT
configurar_playwright()

# ============================================
# IMPORTAÇÕES
# ============================================

from flask import Flask, render_template, jsonify, send_file, request
import pandas as pd
import json
import io
from collections import Counter
import traceback

# ============================================
# CONFIGURA AS PASTAS PARA O .EXE
# ============================================

if getattr(sys, "frozen", False):
    template_folder = os.path.join(sys._MEIPASS, "templates")
    static_folder = os.path.join(sys._MEIPASS, "static")
    core_folder = os.path.join(sys._MEIPASS, "core")
    sys.path.insert(0, core_folder)
else:
    template_folder = "templates"
    static_folder = "static"
    core_folder = "core"
    sys.path.insert(0, core_folder)

# ============================================
# IMPORTA AS FUNÇÕES DO CORE
# ============================================

from mapeador import analisar_estrutura
from processador import processar_estrutura
from gerador_codigo import gerar_codigo

# ============================================
# APP FLASK
# ============================================

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
cache_mapa = {"dados": [], "url": "", "total": 0}


# ============================================
# ⭐ ROTA PRINCIPAL
# ============================================


@app.route("/")
def index():
    """Página inicial - dashboard"""
    return render_template("dashboard.html")


# ============================================
# ROTA DE MAPEAMENTO
# ============================================


@app.route("/mapear", methods=["POST"])
def mapear():
    global cache_mapa
    url = request.json.get("url", "")
    if not url:
        return jsonify({"erro": "URL não fornecida"}), 400
    try:
        dados = analisar_estrutura(url)
        cache_mapa["dados"] = dados
        cache_mapa["url"] = url
        cache_mapa["total"] = len(dados)

        tags = Counter()
        classes = Counter()
        for elem in dados:
            tags[elem.get("tag", "desconhecido")] += 1
            if elem.get("classe"):
                for cls in elem["classe"].split():
                    classes[cls] += 1

        return jsonify(
            {
                "sucesso": True,
                "url": url,
                "total": len(dados),
                "tags": dict(tags.most_common(10)),
                "classes": dict(classes.most_common(5)),
                "todos": dados,
                "primeiros": dados[:10],
            }
        )
    except Exception as e:
        traceback.print_exc()
        return jsonify({"erro": str(e)}), 500


# ============================================
# ROTA DE EXPORTAÇÃO
# ============================================


@app.route("/exportar", methods=["POST"])
def exportar():
    global cache_mapa
    if not cache_mapa["dados"]:
        return jsonify({"erro": "Nenhum mapa para exportar"}), 400
    formato = request.json.get("formato", "excel")
    dados = cache_mapa["dados"]
    if formato == "excel":
        df = pd.DataFrame(dados)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Estrutura")
        output.seek(0)
        return send_file(
            output,
            download_name=f'mapa_{cache_mapa["url"].replace("https://", "").replace("/", "_")}.xlsx',
            as_attachment=True,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    elif formato == "json":
        output = io.BytesIO()
        output.write(json.dumps(dados, indent=2, ensure_ascii=False).encode("utf-8"))
        output.seek(0)
        return send_file(
            output,
            download_name=f'mapa_{cache_mapa["url"].replace("https://", "").replace("/", "_")}.json',
            as_attachment=True,
            mimetype="application/json",
        )
    elif formato == "csv":
        df = pd.DataFrame(dados)
        output = io.BytesIO()
        df.to_csv(output, index=False, encoding="utf-8")
        output.seek(0)
        return send_file(
            output,
            download_name=f'mapa_{cache_mapa["url"].replace("https://", "").replace("/", "_")}.csv',
            as_attachment=True,
            mimetype="text/csv",
        )
    return jsonify({"erro": "Formato não suportado"}), 400


# ============================================
# ROTA PARA GERAR CÓDIGO
# ============================================


@app.route("/gerar_codigo", methods=["POST"])
def gerar():
    dados = request.json
    seletor = dados.get("seletor")
    tipo = dados.get("tipo", "css")
    ferramenta = dados.get("ferramenta", "playwright")
    codigo = gerar_codigo(seletor, tipo, ferramenta)
    return jsonify({"codigo": codigo})


# ============================================
# FUNÇÃO PARA ABRIR O NAVEGADOR (INTELIGENTE)
# ============================================


def abrir_navegador():
    """Abre o navegador no localhost. Se não tiver nenhum aberto, abre um novo."""
    time.sleep(1.5)
    url = "http://127.0.0.1:5000"

    try:
        # Tenta abrir no Chrome (se estiver instalado)
        chrome_paths = [
            "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        ]

        chrome_found = False
        for path in chrome_paths:
            if os.path.exists(path):
                subprocess.Popen([path, "--new-window", url], shell=False)
                chrome_found = True
                print("✅ Chrome aberto com sucesso!")
                break

        if not chrome_found:
            subprocess.Popen(["start", url], shell=True)
            print("✅ Navegador padrão aberto com sucesso!")

    except Exception as e:
        try:
            webbrowser.open(url, new=2)
            print("✅ Tentando com webbrowser...")
        except:
            print(f"❌ Erro ao abrir navegador: {e}")
            print(f"📋 Abra manualmente: {url}")


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("🚀 Struct Analyzer Pro")
    print("🌐 Abrindo navegador...")
    threading.Thread(target=abrir_navegador, daemon=True).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
