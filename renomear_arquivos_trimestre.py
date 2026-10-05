"""Prefixa arquivos das pastas do primeiro semestre com "1° trimestre - "."""

import argparse
from pathlib import Path


PREFIX = "1° trimestre - "
FOLDERS = (
    Path(
        r"C:\Users\Ulysson Fontenele\Desktop\Curso de Engenharia\1° Semestre"
        r"\Formação Cidadã Contemporãnea"
    ),
    Path(
        r"C:\Users\Ulysson Fontenele\Desktop\Curso de Engenharia\1° Semestre"
        r"\Formação Inicial em Educação a Distância"
    ),
    Path(
        r"C:\Users\Ulysson Fontenele\Desktop\Curso de Engenharia\1° Semestre"
        r"\Fundamentos de Sistemas da Informação"
    ),
    Path(
        r"C:\Users\Ulysson Fontenele\Desktop\Curso de Engenharia\1° Semestre"
        r"\Matemática Elementar"
    ),
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Adiciona '1° trimestre - ' ao início dos nomes dos arquivos "
            "nas quatro pastas do primeiro semestre."
        )
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="renomeia os arquivos; sem esta opção, apenas exibe a simulação",
    )
    args = parser.parse_args()

    errors = 0
    renamed = 0
    unchanged = 0

    for folder in FOLDERS:
        if not folder.is_dir():
            print(f"ERRO: pasta não encontrada ou inacessível: {folder}")
            errors += 1
            continue

        print(f"\nPasta: {folder}")
        try:
            files = sorted(
                (item for item in folder.iterdir() if item.is_file()),
                key=lambda item: item.name.casefold(),
            )
        except OSError as error:
            print(f"ERRO: não foi possível listar a pasta: {error}")
            errors += 1
            continue

        for source in files:
            if source.name.casefold().startswith(PREFIX.casefold()):
                print(f"Já está prefixado: {source.name}")
                unchanged += 1
                continue

            target = source.with_name(f"{PREFIX}{source.name}")
            if target.exists():
                print(f"CONFLITO: destino já existe; ignorado: {target.name}")
                errors += 1
                continue

            if args.apply:
                try:
                    source.rename(target)
                except OSError as error:
                    print(f"ERRO: não foi possível renomear {source.name}: {error}")
                    errors += 1
                    continue
                print(f"Renomeado: {source.name} -> {target.name}")
            else:
                print(f"Simulação: {source.name} -> {target.name}")
            renamed += 1

    action = "Renomeados" if args.apply else "A renomear"
    print(f"\n{action}: {renamed} | Já prefixados: {unchanged} | Erros/conflitos: {errors}")
    if not args.apply:
        print("Nenhum arquivo foi alterado. Execute com --apply para renomear.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())


#py "C:\Users\Ulysson Fontenele\Desktop\Curso de Engenharia\renomear_arquivos_trimestre.py" --apply