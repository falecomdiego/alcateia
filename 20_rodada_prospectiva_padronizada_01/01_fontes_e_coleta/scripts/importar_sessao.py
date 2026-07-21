#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Importador de sessão do Instagram via arquivo de cookies Netscape.
O arquivo deve ser exportado manualmente pela extensão 'Cookie-Editor' do Chrome
enquanto logado no Instagram, no formato Netscape.
Não expõe senhas ou credenciais.
"""

import sys
import os
import argparse
import http.cookiejar

def parse_args():
    parser = argparse.ArgumentParser(
        description="Importa sessão do Instagram a partir de arquivo de cookies Netscape."
    )
    parser.add_argument(
        "--usuario",
        type=str,
        required=True,
        help="Nome de usuário do Instagram (sem @)."
    )
    parser.add_argument(
        "--cookies",
        type=str,
        default="../preenchidos/instagram_cookies.txt",
        help="Caminho para o arquivo de cookies no formato Netscape."
    )
    return parser.parse_args()

def importar_sessao(usuario, cookies_path):
    """Lê arquivo de cookies Netscape e cria arquivo de sessão do Instaloader."""

    try:
        import instaloader
    except ImportError:
        print("Erro: biblioteca 'instaloader' não instalada.", file=sys.stderr)
        print("Execute: pip install instaloader", file=sys.stderr)
        sys.exit(1)

    import requests

    if not os.path.exists(cookies_path):
        print(f"Erro: arquivo de cookies não encontrado em: {cookies_path}", file=sys.stderr)
        print("Exporte os cookies do Instagram em formato Netscape usando a extensão", file=sys.stderr)
        print("'Cookie-Editor' no Chrome e salve no caminho indicado.", file=sys.stderr)
        sys.exit(1)

    print(f"Lendo arquivo de cookies: {cookies_path}")

    # Carregar cookies via http.cookiejar (nativo do Python, sem dependências extras)
    cj = http.cookiejar.MozillaCookieJar()
    try:
        cj.load(cookies_path, ignore_discard=True, ignore_expires=True)
    except Exception as e:
        print(f"Erro ao carregar arquivo de cookies: {e}", file=sys.stderr)
        print("Verifique se o arquivo está no formato Netscape correto.", file=sys.stderr)
        sys.exit(1)

    cookies_list = list(cj)
    cookie_names = [c.name for c in cookies_list]

    if "sessionid" not in cookie_names:
        print("Erro: cookie 'sessionid' não encontrado no arquivo.", file=sys.stderr)
        print("Certifique-se de que você estava logado no Instagram ao exportar.", file=sys.stderr)
        sys.exit(1)

    print(f"Cookie 'sessionid' encontrado com sucesso ({len(cookies_list)} cookies carregados).")
    print(f"Criando sessão do Instaloader para '{usuario}'...")

    L = instaloader.Instaloader()
    session = requests.Session()

    for c in cookies_list:
        session.cookies.set(c.name, c.value, domain=c.domain)

    L.context._session = session
    L.context.username = usuario

    try:
        L.save_session_to_file(usuario)
        print()
        print(f"Sessão salva com sucesso para o usuário '{usuario}'.")
        print(f"Arquivo de sessão: session-{usuario}")
        print()
        print("Agora execute a coleta com:")
        print(f"  python coletor_instagram.py --session-user {usuario}")
    except Exception as e:
        print(f"Erro ao salvar sessão: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    args = parse_args()
    importar_sessao(args.usuario, args.cookies)

if __name__ == "__main__":
    main()
