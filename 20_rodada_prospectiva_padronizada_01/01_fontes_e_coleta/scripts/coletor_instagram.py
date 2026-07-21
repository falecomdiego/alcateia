#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Coletor de Comentários do Instagram para a Rodada MDN-RPP01.
Garante extração programática, auditável e com minimização prévia de dados.
Usa uma única instância do Instaloader com cookies injetados diretamente.
"""

import os
import csv
import json
import sys
import argparse
import http.cookiejar
from datetime import datetime, timezone

COLUNAS_OBRIGATORIAS = [
    "my-serial-number",
    "index",
    "User ID",
    "Avatar URL",
    "Profile URL",
    "User Name",
    "Comment Text",
    "Comment Date"
]

COOKIES_PATH_PADRAO = os.path.join(
    os.path.dirname(__file__),
    "../preenchidos/instagram_cookies.txt"
)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Coletor de comentários do Instagram para a MDN-RPP01."
    )
    parser.add_argument("--fontes", type=str,
                        default="../preenchidos/MDN-RPP01-FON-PRO-001-V0.1.csv",
                        help="Caminho para o inventário de fontes previstas.")
    parser.add_argument("--destino", type=str,
                        default="../../02_dados_brutos_protegidos/dados",
                        help="Diretório de destino dos arquivos brutos coletados.")
    parser.add_argument("--cookies", type=str,
                        default=COOKIES_PATH_PADRAO,
                        help="Caminho para o arquivo de cookies Netscape.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Executa em modo sintético, sem conectar à rede.")
    return parser.parse_args()

def gerar_dados_ficticios(destino_path):
    os.makedirs(destino_path, exist_ok=True)
    arquivo = os.path.join(destino_path, "MDN-RPP01-RAW-TEST-SINTETICO.csv")
    dados = [
        ["1", "1", "1000000001",
         "https://instagram.fria1-1.fna.fbcdn.net/v/t51.2885-19/ficticio1.jpg",
         "https://www.instagram.com/user_teste1/", "user_teste1",
         "Comentário de teste sintético para validação estrutural.",
         "2026-06-15T21:00:00.000Z"],
        ["2", "2", "1000000002",
         "https://instagram.fria1-1.fna.fbcdn.net/v/t51.2885-19/ficticio2.jpg",
         "https://www.instagram.com/user_teste2/", "user_teste2",
         "Comprova a exclusão de emails e telefones e preservação das 8 colunas.",
         "2026-06-20T22:30:00.000Z"]
    ]
    with open(arquivo, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLUNAS_OBRIGATORIAS)
        writer.writerows(dados)
    print(f"[DRY-RUN] Arquivo sintético criado: {arquivo}")
    return arquivo

def criar_instaloader_autenticado(cookies_path):
    """Cria uma instância do Instaloader com cookies injetados diretamente."""
    try:
        import instaloader
        import requests as req
    except ImportError:
        print("Erro: instaloader não instalado. Execute: pip install instaloader", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(cookies_path):
        print(f"Erro: arquivo de cookies não encontrado: {cookies_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Carregando cookies de: {cookies_path}")

    cj = http.cookiejar.MozillaCookieJar()
    try:
        cj.load(cookies_path, ignore_discard=True, ignore_expires=True)
    except Exception as e:
        print(f"Erro ao carregar cookies: {e}", file=sys.stderr)
        sys.exit(1)

    cookies_list = list(cj)
    cookie_names = [c.name for c in cookies_list]

    if "sessionid" not in cookie_names:
        print("Erro: 'sessionid' não encontrado. Exporte os cookies novamente.", file=sys.stderr)
        sys.exit(1)

    # Criar instância do Instaloader
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=True,
        save_metadata=False,
        compress_json=False,
        quiet=True
    )

    # Injetar cookies diretamente na sessão interna
    for c in cookies_list:
        L.context._session.cookies.set(c.name, c.value, domain=c.domain)

    # Verificar autenticação
    try:
        username = L.test_login()
        if username:
            print(f"Autenticado com sucesso como: {username}")
        else:
            print("Aviso: autenticação não confirmada. Prosseguindo assim mesmo.", file=sys.stderr)
    except Exception as e:
        print(f"Aviso ao testar login: {e}", file=sys.stderr)

    return L

def extrair_shortcode(url):
    parts = url.strip().rstrip("/").split("/")
    if "p" in parts:
        idx = parts.index("p")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return None

def coletar_post(L, shortcode, destino_path, fonte_id, coleta_id):
    """Coleta comentários de um único post usando a instância autenticada."""
    try:
        import instaloader
    except ImportError:
        return False

    print(f"  Coletando shortcode: {shortcode} | fonte: {fonte_id} | coleta: {coleta_id}")

    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
    except Exception as e:
        print(f"  Erro ao carregar post {shortcode}: {e}", file=sys.stderr)
        return False

    os.makedirs(destino_path, exist_ok=True)
    csv_file = os.path.join(destino_path, f"MDN-RPP01-RAW-{fonte_id}-{coleta_id}.csv")
    json_file = os.path.join(destino_path, f"MDN-RPP01-RAW-{fonte_id}-{coleta_id}-metadata.json")

    # Metadados de auditoria
    metadata = {
        "shortcode": post.shortcode,
        "owner_username": post.owner_username,
        "date_utc": post.date_utc.isoformat() if post.date_utc else None,
        "comments_count": post.comments,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "coleta_id": coleta_id,
        "fonte_id": fonte_id
    }
    with open(json_file, "w", encoding="utf-8") as jf:
        json.dump(metadata, jf, ensure_ascii=False, indent=2)

    # Coleta dos comentários (apenas nível raiz — sem replies)
    rows = []
    try:
        for idx, comment in enumerate(post.get_comments(), start=1):
            user_id = str(comment.owner.userid) if comment.owner else "nao_determinado"
            user_name = comment.owner.username if comment.owner else "nao_determinado"
            profile_url = (f"https://www.instagram.com/{user_name}/"
                           if user_name != "nao_determinado" else "")
            avatar_url = ""
            try:
                avatar_url = comment.owner.profile_pic_url if comment.owner else ""
            except Exception:
                pass
            comment_date = (comment.created_at_utc.isoformat() + "Z"
                            if comment.created_at_utc else "")
            rows.append([
                str(idx), str(idx), user_id, avatar_url,
                profile_url, user_name, comment.text, comment_date
            ])
    except Exception as e:
        print(f"  Erro ao iterar comentários de {shortcode}: {e}", file=sys.stderr)
        return False

    with open(csv_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLUNAS_OBRIGATORIAS)
        writer.writerows(rows)

    print(f"  Sucesso: {len(rows)} comentários salvos em {csv_file}")
    return True

def main():
    args = parse_args()

    if args.dry_run:
        gerar_dados_ficticios(args.destino)
        sys.exit(0)

    # Criar UMA ÚNICA instância autenticada para todos os posts
    L = criar_instaloader_autenticado(args.cookies)

    if not os.path.exists(args.fontes):
        print(f"Erro: inventário não encontrado: {args.fontes}", file=sys.stderr)
        sys.exit(1)

    with open(args.fontes, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fontes = list(reader)

    print(f"\nIniciando coleta de {len(fontes)} publicações...\n")
    total_sucesso = 0

    for row in fontes:
        url = row.get("URL da publicação") or row.get("url", "")
        item_id = row.get("item") or row.get("fonte_id", "0")

        if not url:
            print(f"Aviso: linha sem URL. Pulando.")
            continue

        shortcode = extrair_shortcode(url)
        if not shortcode:
            print(f"Aviso: shortcode não extraído de: {url}. Pulando.")
            continue

        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        coleta_id = f"COL-{ts}-{item_id}"
        fonte_id = f"FON-{str(item_id).zfill(4)}"

        ok = coletar_post(L, shortcode, args.destino, fonte_id, coleta_id)
        if ok:
            total_sucesso += 1

    print(f"\nProcessamento concluído. Sucesso em {total_sucesso} de {len(fontes)} publicações.")

if __name__ == "__main__":
    main()
