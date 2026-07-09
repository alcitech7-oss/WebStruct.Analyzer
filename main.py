"""
🏗️ STRUCT ANALYZER - Versão Simples
Abre qualquer site e extrai a estrutura básica
"""

from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os


def analisar_estrutura(url):
    """
    Versão simples: Abre a página, extrai a estrutura e salva em Excel
    """
    print(f"\n🔍 Tentando abrir: {url}")

    with sync_playwright() as p:
        # Navegador COM interface (pra você ver o que acontece)
        browser = p.chromium.launch(
            headless=False, args=["--no-sandbox"]  # 👈 MOSTRA O NAVEGADOR
        )

        page = browser.new_page()

        try:
            # Tenta abrir a página
            print("⏳ Carregando página...")
            page.goto(url, timeout=30000, wait_until="domcontentloaded")

            # Espera um pouco
            page.wait_for_timeout(2000)

            # Pega o título
            titulo = page.title()
            print(f"📌 Título: {titulo}")

            # Pega todos os elementos
            elementos = page.query_selector_all("*")
            print(f"✅ {len(elementos)} elementos encontrados na página")

            # Extrai informações básicas
            dados = []
            for posicao, elem in enumerate(elementos, 1):
                try:
                    tag = elem.evaluate("el => el.tagName.toLowerCase()")
                    classe = elem.get_attribute("class") or ""
                    id_elem = elem.get_attribute("id") or ""
                    texto = (
                        elem.inner_text().strip()[:100]
                        if elem.inner_text().strip()
                        else ""
                    )

                    # Só salva se tiver algo relevante
                    if texto or classe or id_elem:
                        dados.append(
                            {
                                "posicao": posicao,
                                "tag": tag,
                                "classe": classe,
                                "id": id_elem,
                                "texto": texto[:50],
                            }
                        )
                except:
                    pass

            print(f"✅ {len(dados)} elementos com dados relevantes")

            # Salva em Excel
            if dados:
                os.makedirs("exports", exist_ok=True)
                nome_arquivo = (
                    f"exports/estrutura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                )
                df = pd.DataFrame(dados)
                df.to_excel(nome_arquivo, index=False)
                print(f"📁 Arquivo salvo: {nome_arquivo}")
            else:
                print("❌ Nenhum dado encontrado!")

            # Mostra estatísticas básicas
            tags = {}
            for item in dados:
                tag = item["tag"]
                tags[tag] = tags.get(tag, 0) + 1

            print("\n📊 ESTATÍSTICAS:")
            for tag, count in sorted(tags.items(), key=lambda x: x[1], reverse=True)[
                :5
            ]:
                print(f"   {tag}: {count}")

            # Espera o usuário ver
            input("\n⏸️ Pressione Enter para fechar o navegador...")

            browser.close()
            return dados

        except Exception as e:
            print(f"❌ ERRO: {e}")
            input("\n⏸️ Pressione Enter para fechar o navegador...")
            browser.close()
            return []


def main():
    print("=" * 60)
    print("🏗️ STRUCT ANALYZER - Versão Simples")
    print("Abre qualquer site e extrai a estrutura básica")
    print("=" * 60)

    # Pede a URL
    url = input("\n🌐 URL do site: ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Analisa
    dados = analisar_estrutura(url)

    if dados:
        print(f"\n✅ Análise concluída! {len(dados)} elementos salvos.")
    else:
        print("\n❌ Falha na análise. Verifique a URL e tente novamente.")


if __name__ == "__main__":
    main()
