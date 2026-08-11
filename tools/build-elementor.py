#!/usr/bin/env python3
"""
Gera a versão autocontida do app para embutir no Elementor (ou em qualquer CMS).

Fonte da verdade continua sendo o index.html da raiz: este script apenas embute
GLOBO.png e LETTERING.png como data URI, de modo que o resultado seja UM arquivo
só, sem nenhum arquivo companheiro para subir junto.

    python3 tools/build-elementor.py

Saída: elementor/esquenta-privateday.html

As imagens entram uma única vez, num objeto `window.__ASSETS`, e os `<img>` são
preenchidos a partir dele. Embutir o data URI direto em cada `src` repetiria
~360 KB por ocorrência (são cinco) e inflaria o arquivo para vários megabytes.

Continuam vindo de CDN (não há como embutir, e o app não funciona sem rede de
qualquer forma): Tailwind, Google Fonts, SDK do Firebase, DiceBear e o YouTube.
"""

import base64
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "index.html"
SAIDA = RAIZ / "elementor" / "esquenta-privateday.html"

AVISO = """<!--
  ARQUIVO GERADO — não edite à mão.
  Origem: index.html · gerado por tools/build-elementor.py
  Versão autocontida (imagens embutidas em base64) para embutir no Elementor.
  Como usar: docs/elementor.md
-->
"""


def data_uri(caminho: pathlib.Path) -> str:
    return "data:image/png;base64," + base64.b64encode(caminho.read_bytes()).decode()


def troca_unica(html: str, de: str, para: str, esperado: int = 1) -> str:
    """Troca exigindo a quantidade esperada de ocorrências — se o index.html mudar
    de forma incompatível, o build falha alto em vez de gerar um arquivo quebrado."""
    achados = html.count(de)
    if achados != esperado:
        sys.exit(f"ERRO: esperava {esperado} ocorrência(s) de {de!r}, encontrei {achados}. "
                 f"O index.html mudou — ajuste tools/build-elementor.py.")
    return html.replace(de, para)


def main() -> None:
    html = ENTRADA.read_text(encoding="utf-8")
    globo = data_uri(RAIZ / "GLOBO.png")
    lettering = data_uri(RAIZ / "LETTERING.png")

    # 1) a tela de "Firebase não configurado" monta o <img> por template string:
    #    lá o data URI entra por interpolação, não por data-img (o elemento nasce
    #    depois que o preenchimento inicial já rodou)
    html = troca_unica(
        html,
        '<img src="GLOBO.png" class="w-20 h-20 mb-5 opacity-50 object-contain">',
        '<img src="${window.__ASSETS.globo}" class="w-20 h-20 mb-5 opacity-50 object-contain">',
    )

    # 2) imagens estáticas: marcadas para preenchimento a partir de window.__ASSETS
    html = troca_unica(html, 'src="GLOBO.png"', 'data-img="globo" src=""', esperado=3)
    html = troca_unica(html, 'src="LETTERING.png"', 'data-img="lettering" src=""')

    # 3) lista de pré-carregamento: as mesmas URLs, agora data URI
    html = troca_unica(
        html,
        "                'GLOBO.png', 'LETTERING.png',",
        "                window.__ASSETS.globo, window.__ASSETS.lettering,",
    )

    # 4) as imagens em si, uma única vez, antes do módulo (script clássico roda
    #    primeiro: módulos são adiados até o fim do parse)
    injecao = (
        "    <script>\n"
        "        // imagens da marca embutidas — versão autocontida, sem arquivos ao lado\n"
        "        window.__ASSETS = {\n"
        f'            globo: "{globo}",\n'
        f'            lettering: "{lettering}"\n'
        "        };\n"
        "        document.querySelectorAll('[data-img]').forEach(function (el) {\n"
        "            el.src = window.__ASSETS[el.dataset.img];\n"
        "        });\n"
        "    </script>\n\n"
    )
    html = troca_unica(html, '    <script type="module">', injecao + '    <script type="module">')

    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_text(AVISO + html, encoding="utf-8")
    print(f"OK  {SAIDA.relative_to(RAIZ)}  ({SAIDA.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
