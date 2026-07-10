from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os
import time
import base64
import json


def gerar_seletor_css(tag, classe, id_elem):
    if id_elem:
        return f"#{id_elem}"
    if classe:
        classes = classe.strip().split()
        if len(classes) == 1:
            return f".{classes[0]}"
        else:
            return f".{'.'.join(classes)}"
    return tag


def gerar_xpath(tag, classe, id_elem, posicao):
    if id_elem:
        return f'//{tag}[@id="{id_elem}"]'
    if classe:
        classes = classe.strip().split()
        return f'//{tag}[contains(@class, "{classes[0]}")]'
    return f"//{tag}[{posicao}]"


# ============================================
# ⭐ FUNÇÃO PARA TIRAR FOTO RÁPIDA (CORRIGIDA) ⭐
# ============================================


def tirar_foto_rapida(url):
    """Tira um screenshot rápido da página (com scroll leve)"""
    print(f"📸 Tirando foto rápida de: {url}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            page = browser.new_page()
            page.goto(url, timeout=30000, wait_until="domcontentloaded")

            # ⭐ ADICIONA UM SCROLL LEVE (igual ao que funciona)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.3)")
            page.wait_for_timeout(1000)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(1000)

            # Tira a foto
            screenshot = page.screenshot(full_page=False)
            screenshot_base64 = base64.b64encode(screenshot).decode("utf-8")
            browser.close()
            print("📸 Foto rápida capturada com sucesso!")
            return screenshot_base64
    except Exception as e:
        print(f"❌ Erro ao tirar foto rápida: {e}")
        return None


# ============================================
# ⭐ FUNÇÃO DE MAPEAMENTO COM PROGRESSO ⭐
# ============================================


def analisar_estrutura_com_progresso(url):
    """
    Mapeia a estrutura de um site e retorna o progresso via generator.
    """
    print(f"🔍 Analisando: {url}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

            page = browser.new_page()
            page.goto(url, timeout=30000, wait_until="domcontentloaded")

            yield json.dumps({"status": "carregando", "mensagem": "Página carregada!"})

            # Scroll
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.5)")
            page.wait_for_timeout(1500)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(1000)

            yield json.dumps({"status": "scroll", "mensagem": "Scroll concluído!"})

            # Espera conteúdo dinâmico
            try:
                page.wait_for_selector(".exchangeBarHeader__item__value", timeout=5000)
                print("✅ Conteúdo dinâmico carregado com sucesso!")
            except:
                print("⚠️ Conteúdo dinâmico não encontrado (pode não estar na página).")

            # ⭐ MAPEIA OS ELEMENTOS COM PROGRESSO ⭐
            elementos = page.query_selector_all("*")
            total = len(elementos)

            dados = []

            for i, elem in enumerate(elementos, 1):
                try:
                    tag = elem.evaluate("el => el.tagName.toLowerCase()")
                    classe = elem.get_attribute("class") or ""
                    id_elem = elem.get_attribute("id") or ""
                    link = elem.get_attribute("href") or ""
                    texto = (
                        elem.inner_text().strip()[:300]
                        if elem.inner_text().strip()
                        else ""
                    )

                    profundidade = elem.evaluate("""
                        (el) => {
                            let depth = 0;
                            let parent = el.parentElement;
                            while (parent) {
                                depth++;
                                parent = parent.parentElement;
                            }
                            return depth;
                        }
                    """)

                    pai = elem.evaluate(
                        "el => el.parentElement ? el.parentElement.tagName.toLowerCase() : ''"
                    )

                    dados.append(
                        {
                            "posicao": i,
                            "profundidade": profundidade,
                            "tag": tag,
                            "classe": classe,
                            "id": id_elem,
                            "link": link,
                            "texto": texto,
                            "pai": pai,
                            "seletor_css": gerar_seletor_css(tag, classe, id_elem),
                            "xpath": gerar_xpath(tag, classe, id_elem, i),
                        }
                    )

                    # ⭐ ENVIA O PROGRESSO A CADA 10 ELEMENTOS ⭐
                    if i % 10 == 0 or i == total:
                        pct = int((i / total) * 100)
                        yield json.dumps(
                            {
                                "status": "progresso",
                                "atual": i,
                                "total": total,
                                "percentual": pct,
                                "mensagem": f"Coletando elementos... {i} / {total}",
                            }
                        )

                except Exception:
                    pass

            browser.close()

            yield json.dumps(
                {
                    "status": "concluido",
                    "total": len(dados),
                    "dados": dados,
                    "mensagem": f"✅ {len(dados)} elementos mapeados!",
                }
            )

    except Exception as e:
        yield json.dumps({"status": "erro", "mensagem": str(e)})


# ============================================
# ⭐ FUNÇÃO DE MAPEAMENTO COMPLETO ⭐
# ============================================


def analisar_estrutura(url, pegar_screenshot=False):
    """
    Mapeia a estrutura de um site (completo, com scroll).
    Se `pegar_screenshot` for True, retorna também um screenshot da página.
    """
    print(f"🔍 Analisando: {url}")

    dados = []
    screenshot_base64 = None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

            page = browser.new_page()
            page.goto(url, timeout=30000, wait_until="domcontentloaded")

            if pegar_screenshot:
                page.wait_for_timeout(2000)
                screenshot = page.screenshot(full_page=True)
                screenshot_base64 = base64.b64encode(screenshot).decode("utf-8")
                print("📸 Screenshot capturado!")

            print("⏳ Rolando a página para carregar conteúdo dinâmico...")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.5)")
            page.wait_for_timeout(1500)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(1000)

            print("⏳ Aguardando conteúdo dinâmico...")
            try:
                page.wait_for_selector(".exchangeBarHeader__item__value", timeout=5000)
                print("✅ Conteúdo dinâmico carregado com sucesso!")
            except:
                print("⚠️ Conteúdo dinâmico não encontrado (pode não estar na página).")

            print("⏳ Coletando todos os elementos...")
            elementos = page.query_selector_all("*")

            for posicao, elem in enumerate(elementos, 1):
                try:
                    tag = elem.evaluate("el => el.tagName.toLowerCase()")
                    classe = elem.get_attribute("class") or ""
                    id_elem = elem.get_attribute("id") or ""
                    link = elem.get_attribute("href") or ""
                    texto = (
                        elem.inner_text().strip()[:300]
                        if elem.inner_text().strip()
                        else ""
                    )

                    profundidade = elem.evaluate("""
                        (el) => {
                            let depth = 0;
                            let parent = el.parentElement;
                            while (parent) {
                                depth++;
                                parent = parent.parentElement;
                            }
                            return depth;
                        }
                    """)

                    pai = elem.evaluate(
                        "el => el.parentElement ? el.parentElement.tagName.toLowerCase() : ''"
                    )

                    dados.append(
                        {
                            "posicao": posicao,
                            "profundidade": profundidade,
                            "tag": tag,
                            "classe": classe,
                            "id": id_elem,
                            "link": link,
                            "texto": texto,
                            "pai": pai,
                            "seletor_css": gerar_seletor_css(tag, classe, id_elem),
                            "xpath": gerar_xpath(tag, classe, id_elem, posicao),
                        }
                    )
                except Exception:
                    pass

            print(f"✅ {len(dados)} elementos mapeados!")

            browser.close()
            print("✅ Processo concluído!")

            if pegar_screenshot:
                return dados, screenshot_base64
            else:
                return dados

    except Exception as e:
        print(f"❌ Erro no mapeamento: {e}")
        if pegar_screenshot:
            return [], None
        else:
            return []


def salvar_mapa_atual(dados, url, descricao=None):
    """
    Salva o mapa atual no banco de dados.
    """
    try:
        from database import salvar_mapa

        mapa = salvar_mapa(dados, url, descricao)
        return mapa
    except Exception as e:
        print(f"⚠️ Não foi possível salvar no banco: {e}")
        return None
