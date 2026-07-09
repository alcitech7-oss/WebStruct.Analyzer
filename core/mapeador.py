from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os
import time


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


def analisar_estrutura(url):
    """
    Versão com Playwright - Janela visível durante todo o mapeamento.
    """
    print(f"🔍 Analisando: {url}")

    dados = []

    try:
        with sync_playwright() as p:
            # ============================================================
            # PASSO 1: ABRE A JANELA COM A PÁGINA
            # ============================================================
            browser = p.chromium.launch(headless=False, args=["--no-sandbox"])
            page = browser.new_page()
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.bring_to_front()

            print("✅ Janela aberta! A página está visível.")
            print("ℹ️ Você pode minimizar a janela se quiser.")

            # ============================================================
            # PASSO 2: MOSTRA A PÁGINA POR 3 SEGUNDOS
            # ============================================================
            print("👀 Mostrando a página por 3 segundos...")
            page.wait_for_timeout(3000)

            # ============================================================
            # PASSO 3: VERIFICA SE O USUÁRIO FECHOU A JANELA
            # ============================================================
            try:
                page.title()
            except Exception:
                print("❌ Você fechou a página! Mapeamento cancelado.")
                browser.close()
                return []

            # ============================================================
            # PASSO 4: SCROLL PARA CARREGAR CONTEÚDO DINÂMICO
            # ============================================================
            print("⏳ Rolando a página para carregar conteúdo dinâmico...")

            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.3)")
            page.wait_for_timeout(1500)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.6)")
            page.wait_for_timeout(1500)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)

            # ============================================================
            # PASSO 5: ESPERA O CONTEÚDO DINÂMICO
            # ============================================================
            print("⏳ Aguardando conteúdo dinâmico...")
            try:
                page.wait_for_selector(".exchangeBarHeader__item__value", timeout=10000)
                print("✅ Conteúdo dinâmico carregado com sucesso!")
            except:
                print("⚠️ Conteúdo dinâmico não encontrado (pode não estar na página).")

            # ============================================================
            # PASSO 6: MAPEIA TODOS OS ELEMENTOS
            # ============================================================
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

            return dados

    except Exception as e:
        print(f"❌ Erro no mapeamento: {e}")
        return []


# ============================================
# FUNÇÃO PARA SALVAR MAPA NO BANCO
# ============================================


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
