"""Prefixa arquivos das pastas do primeiro semestre com "1° trimestre - "."""

# Importa a biblioteca para receber argumentos da linha de comando.
import argparse
# Importa a classe Path para trabalhar com caminhos de arquivos e pastas.
from pathlib import Path


# Texto que será adicionado no início de cada nome de arquivo.
# Exemplo: "aula.pdf" vira "2° trimestre - aula.pdf".
PREFIX = "2° trimestre - "

# Lista das pastas onde os arquivos serão analisados e renomeados.
FOLDERS = (
    Path(
        r"C:\Users\Ulysson Fontenele\Desktop\Curso de Engenharia\2° Trimestre"
        r"\Fundamentos de Sistemas Operacionais"
    ),
    Path(
        r"C:\Users\Ulysson Fontenele\Desktop\Curso de Engenharia\2° Trimestre"
        r"\Lógica de Programação e Algoritmos"
    ),
)


def main() -> int:
    # Cria um parser para interpretar os argumentos passados ao script.
    parser = argparse.ArgumentParser(
        description=(
            "Adiciona '1° trimestre - ' ao início dos nomes dos arquivos "
            "nas quatro pastas do primeiro semestre."
        )
    )

    # Adiciona a opção --apply.
    # Se ela estiver presente, os arquivos serão realmente renomeados.
    # Se não estiver, o programa apenas mostra uma simulação.
    parser.add_argument(
        "--apply",
        action="store_true",
        help="renomeia os arquivos; sem esta opção, apenas exibe a simulação",
    )

    # Lê os argumentos informados pelo usuário.
    args = parser.parse_args()

    # Contadores para resumo final da execução.
    errors = 0
    renamed = 0
    unchanged = 0

    # Percorre cada pasta da lista FOLDERS.
    for folder in FOLDERS:
        # Verifica se a pasta existe e é acessível.
        if not folder.is_dir():
            print(f"ERRO: pasta não encontrada ou inacessível: {folder}")
            errors += 1
            continue

        print(f"\nPasta: {folder}")

        # Tenta listar os arquivos da pasta e ordena por nome, ignorando letras maiúsculas/minúsculas.
        try:
            files = sorted(
                (item for item in folder.iterdir() if item.is_file()),
                key=lambda item: item.name.casefold(),
            )
        except OSError as error:
            print(f"ERRO: não foi possível listar a pasta: {error}")
            errors += 1
            continue

        # Percorre cada arquivo da pasta.
        for source in files:
            # Se o nome do arquivo já começa com o prefixo, ignora.
            if source.name.casefold().startswith(PREFIX.casefold()):
                print(f"Já está prefixado: {source.name}")
                unchanged += 1
                continue

            # Cria o nome final do arquivo com o prefixo adicionado.
            target = source.with_name(f"{PREFIX}{source.name}")

            # Se já existir um arquivo com esse nome, não sobrescreve.
            if target.exists():
                print(f"CONFLITO: destino já existe; ignorado: {target.name}")
                errors += 1
                continue

            # Se --apply foi passado, renomeia o arquivo.
            if args.apply:
                try:
                    source.rename(target)
                except OSError as error:
                    print(f"ERRO: não foi possível renomear {source.name}: {error}")
                    errors += 1
                    continue
                print(f"Renomeado: {source.name} -> {target.name}")
            else:
                # Caso contrário, apenas mostra a mudança que seria feita.
                print(f"Simulação: {source.name} -> {target.name}")

            # Conta cada arquivo que foi ou seria renomeado.
            renamed += 1

    # Mostra o resumo final da execução.
    action = "Renomeados" if args.apply else "A renomear"
    print(f"\n{action}: {renamed} | Já prefixados: {unchanged} | Erros/conflitos: {errors}")

    # Se o usuário não usou --apply, informa que nada foi alterado.
    if not args.apply:
        print("Nenhum arquivo foi alterado. Execute com --apply para renomear.")

    # Retorna 1 se houve erros, ou 0 se tudo ocorreu sem problemas.
    return 1 if errors else 0


# Bloco principal do programa.
# Garante que o código dentro da função main() será executado somente quando o arquivo for rodado diretamente.
if __name__ == "__main__":
    raise SystemExit(main())


# Exemplo de uso:
# py "C:\Users\Ulysson Fontenele\Desktop\Curso de Engenharia\renomear_arquivos_trimestre.py" --apply