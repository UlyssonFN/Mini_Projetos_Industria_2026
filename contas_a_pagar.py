"""
Sistema de Controle de Contas a Pagar
Desktop app em Python + CustomTkinter + SQLite3.
Execute com: python app.py
"""

# ======================================================================
# IMPORTS
# ======================================================================
import os
import re
import shutil
import sqlite3
import hashlib
import platform
import subprocess
from datetime import datetime, date

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

try:
    import customtkinter as ctk
except ImportError:
    raise SystemExit(
        "A biblioteca 'customtkinter' nao esta instalada.\n"
        "Instale com: pip install customtkinter"
    )

# ======================================================================
# CONFIGURACOES / CONSTANTES
# ======================================================================
APP_TITLE = "Sistema de Controle de Contas a Pagar"
DB_NAME = "contas_pagar.db"
COMPROVANTES_DIR = "comprovantes"
EXTENSOES_PERMITIDAS = {".pdf", ".png", ".jpg", ".jpeg"}

COLORS = {
    "fundo": "#1E1E1E",
    "sidebar": "#121212",
    "card": "#252525",
    "campo": "#2B2B2B",
    "texto": "#FFFFFF",
    "texto_sec": "#B0B0B0",
    "destaque": "#2FA572",
    "destaque_hover": "#248a5f",
    "pago": "#2ECC71",
    "pendente": "#F1C40F",
    "vencido": "#E74C3C",
    "vencendo": "#E67E22",
    "erro": "#E74C3C",
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

MESES_PT = [
    "Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]


# ======================================================================
# INICIALIZACAO DO BANCO DE DADOS
# ======================================================================
def get_connection():
    """Retorna uma conexao SQLite com foreign_keys ativado e row_factory."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabelas(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            perfil TEXT NOT NULL DEFAULT 'comum',
            ativo INTEGER NOT NULL DEFAULT 1,
            data_criacao TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            data_vencimento TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            caminho_comprovante TEXT,
            data_pagamento TEXT,
            usuario_id INTEGER NOT NULL,
            data_criacao TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_contas_status ON contas(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_contas_vencimento ON contas(data_vencimento)")
    conn.commit()


def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def criar_admin_padrao(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
    total = cursor.fetchone()["total"]
    if total == 0:
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash, perfil, ativo, data_criacao) "
            "VALUES (?, ?, ?, ?, ?)",
            ("admin", hash_senha("admin123"), "admin", 1, agora),
        )
        conn.commit()
        return True
    return False


def inicializar_banco():
    os.makedirs(COMPROVANTES_DIR, exist_ok=True)
    conn = get_connection()
    try:
        criar_tabelas(conn)
        criar_admin_padrao(conn)
    finally:
        conn.close()


# ======================================================================
# FUNCOES DE AUTENTICACAO
# ======================================================================
def autenticar_usuario(username: str, senha: str):
    """Retorna (usuario_dict, None) em caso de sucesso ou (None, mensagem_erro)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        usuario = cursor.fetchone()
        if usuario is None:
            return None, "Usuario ou senha invalidos."
        if usuario["ativo"] != 1:
            return None, "Usuario desativado. Contate o administrador."
        if usuario["password_hash"] != hash_senha(senha):
            return None, "Usuario ou senha invalidos."
        return dict(usuario), None
    except sqlite3.Error as e:
        return None, f"Erro ao acessar o banco de dados: {e}"
    finally:
        conn.close()


# ======================================================================
# FUNCOES DE USUARIOS (GESTAO - somente admin)
# ======================================================================
def listar_usuarios():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY username")
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error:
        return []
    finally:
        conn.close()


def cadastrar_usuario(username: str, senha: str, perfil: str):
    username = (username or "").strip()
    if not username or not senha:
        return False, "Informe usuario e senha."
    if len(senha) < 4:
        return False, "A senha deve possuir ao menos 4 caracteres."
    if perfil not in ("admin", "comum"):
        return False, "Perfil invalido."
    conn = get_connection()
    try:
        cursor = conn.cursor()
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash, perfil, ativo, data_criacao) "
            "VALUES (?, ?, ?, 1, ?)",
            (username, hash_senha(senha), perfil, agora),
        )
        conn.commit()
        return True, "Usuario cadastrado com sucesso."
    except sqlite3.IntegrityError:
        return False, "Ja existe um usuario com esse nome."
    except sqlite3.Error as e:
        return False, f"Erro ao cadastrar usuario: {e}"
    finally:
        conn.close()


def alterar_senha_usuario(user_id: int, nova_senha: str):
    if not nova_senha or len(nova_senha) < 4:
        return False, "A nova senha deve possuir ao menos 4 caracteres."
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET password_hash = ? WHERE id = ?",
            (hash_senha(nova_senha), user_id),
        )
        conn.commit()
        return True, "Senha alterada com sucesso."
    except sqlite3.Error as e:
        return False, f"Erro ao alterar senha: {e}"
    finally:
        conn.close()


def alterar_perfil_usuario(user_id: int, perfil: str):
    if perfil not in ("admin", "comum"):
        return False, "Perfil invalido."
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET perfil = ? WHERE id = ?", (perfil, user_id))
        conn.commit()
        return True, "Perfil atualizado com sucesso."
    except sqlite3.Error as e:
        return False, f"Erro ao atualizar perfil: {e}"
    finally:
        conn.close()


def alterar_status_usuario(user_id: int, ativo: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET ativo = ? WHERE id = ?", (ativo, user_id))
        conn.commit()
        return True, "Status atualizado com sucesso."
    except sqlite3.Error as e:
        return False, f"Erro ao atualizar status: {e}"
    finally:
        conn.close()


# ======================================================================
# FUNCOES AUXILIARES (formatacao e validacao)
# ======================================================================
def formatar_moeda(valor: float) -> str:
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def parse_valor(texto: str) -> float:
    """Converte texto no formato brasileiro (1.250,50) para float. Lanca ValueError se invalido."""
    texto = (texto or "").strip().replace("R$", "").strip()
    if not texto:
        raise ValueError("Valor vazio.")
    texto = texto.replace(".", "").replace(",", ".")
    valor = float(texto)
    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")
    return valor


def data_br_para_iso(data_br: str) -> str:
    """Converte dd/mm/aaaa para aaaa-mm-dd. Lanca ValueError se invalido."""
    data_br = (data_br or "").strip()
    dt = datetime.strptime(data_br, "%d/%m/%Y")
    return dt.strftime("%Y-%m-%d")


def data_iso_para_br(data_iso: str) -> str:
    if not data_iso:
        return "-"
    try:
        dt = datetime.strptime(data_iso[:10], "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return data_iso


def datahora_iso_para_br(data_iso: str) -> str:
    if not data_iso:
        return "-"
    try:
        dt = datetime.strptime(data_iso, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return data_iso


def sanitizar_nome_arquivo(nome: str) -> str:
    nome = re.sub(r"[^A-Za-z0-9_.\-]", "_", nome)
    return nome


def obter_status_exibicao(status: str, data_vencimento: str) -> str:
    """Calcula o status visual (Pago / Vencida / Vencendo hoje / Pendente)."""
    if status == "Pago":
        return "Pago"
    try:
        venc = datetime.strptime(data_vencimento[:10], "%Y-%m-%d").date()
    except ValueError:
        return status
    hoje = date.today()
    if venc < hoje:
        return "Vencida"
    if venc == hoje:
        return "Vencendo hoje"
    return "Pendente"


# ======================================================================
# FUNCOES DE CONTAS
# ======================================================================
def cadastrar_conta(descricao: str, valor_texto: str, data_venc_br: str, usuario_id: int):
    descricao = (descricao or "").strip()
    if not descricao:
        return False, "A descricao e obrigatoria."
    try:
        valor = parse_valor(valor_texto)
    except ValueError:
        return False, "Informe um valor numerico valido e maior que zero."
    try:
        data_iso = data_br_para_iso(data_venc_br)
    except ValueError:
        return False, "Informe a data de vencimento no formato dd/mm/aaaa."

    conn = get_connection()
    try:
        cursor = conn.cursor()
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO contas (descricao, valor, data_vencimento, status, usuario_id, data_criacao) "
            "VALUES (?, ?, ?, 'Pendente', ?, ?)",
            (descricao, valor, data_iso, usuario_id, agora),
        )
        conn.commit()
        return True, "Conta cadastrada com sucesso."
    except sqlite3.Error as e:
        return False, f"Erro ao cadastrar conta: {e}"
    finally:
        conn.close()


def listar_contas(status_filtro="Todas", mes=None, ano=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        query = """
            SELECT contas.*, usuarios.username AS usuario_nome
            FROM contas
            LEFT JOIN usuarios ON usuarios.id = contas.usuario_id
        """
        condicoes = []
        parametros = []

        if mes and ano:
            condicoes.append("strftime('%m', data_vencimento) = ? AND strftime('%Y', data_vencimento) = ?")
            parametros.extend([f"{mes:02d}", str(ano)])

        if condicoes:
            query += " WHERE " + " AND ".join(condicoes)
        query += " ORDER BY data_vencimento ASC"

        cursor.execute(query, parametros)
        linhas = [dict(row) for row in cursor.fetchall()]

        # Filtro por status calculado (feito em Python pois depende da data atual)
        if status_filtro == "Pendentes":
            linhas = [c for c in linhas if obter_status_exibicao(c["status"], c["data_vencimento"]) == "Pendente"]
        elif status_filtro == "Pagas":
            linhas = [c for c in linhas if c["status"] == "Pago"]
        elif status_filtro == "Vencidas":
            linhas = [c for c in linhas if obter_status_exibicao(c["status"], c["data_vencimento"]) == "Vencida"]
        elif status_filtro == "Vencendo hoje":
            linhas = [c for c in linhas if obter_status_exibicao(c["status"], c["data_vencimento"]) == "Vencendo hoje"]

        return linhas
    except sqlite3.Error:
        return []
    finally:
        conn.close()


def obter_conta(conta_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contas WHERE id = ?", (conta_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    except sqlite3.Error:
        return None
    finally:
        conn.close()


def editar_conta(conta_id: int, descricao: str, valor_texto: str, data_venc_br: str):
    descricao = (descricao or "").strip()
    if not descricao:
        return False, "A descricao e obrigatoria."
    try:
        valor = parse_valor(valor_texto)
    except ValueError:
        return False, "Informe um valor numerico valido e maior que zero."
    try:
        data_iso = data_br_para_iso(data_venc_br)
    except ValueError:
        return False, "Informe a data de vencimento no formato dd/mm/aaaa."

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE contas SET descricao = ?, valor = ?, data_vencimento = ? WHERE id = ?",
            (descricao, valor, data_iso, conta_id),
        )
        conn.commit()
        return True, "Conta atualizada com sucesso."
    except sqlite3.Error as e:
        return False, f"Erro ao atualizar conta: {e}"
    finally:
        conn.close()


def excluir_conta(conta_id: int, perfil_usuario: str):
    conta = obter_conta(conta_id)
    if conta is None:
        return False, "Conta nao encontrada."
    if conta["status"] == "Pago" and perfil_usuario != "admin":
        return False, "Apenas administradores podem excluir contas ja pagas."

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contas WHERE id = ?", (conta_id,))
        conn.commit()
        return True, "Conta excluida com sucesso."
    except sqlite3.Error as e:
        return False, f"Erro ao excluir conta: {e}"
    finally:
        conn.close()


def realizar_baixa(conta_id: int):
    conta = obter_conta(conta_id)
    if conta is None:
        return False, "Conta nao encontrada."
    if conta["status"] == "Pago":
        return False, "Esta conta ja esta paga."

    conn = get_connection()
    try:
        cursor = conn.cursor()
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "UPDATE contas SET status = 'Pago', data_pagamento = ? WHERE id = ?",
            (agora, conta_id),
        )
        conn.commit()
        return True, "Baixa realizada com sucesso."
    except sqlite3.Error as e:
        return False, f"Erro ao realizar baixa: {e}"
    finally:
        conn.close()


def desfazer_baixa(conta_id: int, perfil_usuario: str):
    if perfil_usuario != "admin":
        return False, "Apenas administradores podem desfazer uma baixa."
    conta = obter_conta(conta_id)
    if conta is None:
        return False, "Conta nao encontrada."
    if conta["status"] != "Pago":
        return False, "Esta conta nao esta paga."

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE contas SET status = 'Pendente', data_pagamento = NULL WHERE id = ?",
            (conta_id,),
        )
        conn.commit()
        return True, "Baixa desfeita com sucesso."
    except sqlite3.Error as e:
        return False, f"Erro ao desfazer baixa: {e}"
    finally:
        conn.close()


def calcular_indicadores():
    contas = listar_contas("Todas", mes=None, ano=None)
    total = len(contas)
    pendentes = [c for c in contas if obter_status_exibicao(c["status"], c["data_vencimento"]) == "Pendente"]
    pagas = [c for c in contas if c["status"] == "Pago"]
    vencidas = [c for c in contas if obter_status_exibicao(c["status"], c["data_vencimento"]) == "Vencida"]
    vencendo_hoje = [c for c in contas if obter_status_exibicao(c["status"], c["data_vencimento"]) == "Vencendo hoje"]

    return {
        "total": total,
        "qtd_pendentes": len(pendentes) + len(vencidas) + len(vencendo_hoje),
        "qtd_pagas": len(pagas),
        "qtd_vencidas": len(vencidas),
        "qtd_vencendo_hoje": len(vencendo_hoje),
        "valor_pendente": sum(c["valor"] for c in pendentes) + sum(c["valor"] for c in vencidas) + sum(c["valor"] for c in vencendo_hoje),
        "valor_pago": sum(c["valor"] for c in pagas),
    }


# ======================================================================
# FUNCOES DE COMPROVANTES
# ======================================================================
def anexar_comprovante(conta_id: int, caminho_origem: str):
    if not caminho_origem:
        return False, "Nenhum arquivo selecionado."
    if not os.path.isfile(caminho_origem):
        return False, "Arquivo selecionado nao encontrado."

    extensao = os.path.splitext(caminho_origem)[1].lower()
    if extensao not in EXTENSOES_PERMITIDAS:
        return False, "Formato invalido. Utilize PDF, PNG, JPG ou JPEG."

    try:
        os.makedirs(COMPROVANTES_DIR, exist_ok=True)
        nome_base = sanitizar_nome_arquivo(os.path.splitext(os.path.basename(caminho_origem))[0])
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        nome_destino = f"conta{conta_id}_{nome_base}_{timestamp}{extensao}"
        caminho_destino = os.path.join(COMPROVANTES_DIR, nome_destino)

        contador = 1
        while os.path.exists(caminho_destino):
            nome_destino = f"conta{conta_id}_{nome_base}_{timestamp}_{contador}{extensao}"
            caminho_destino = os.path.join(COMPROVANTES_DIR, nome_destino)
            contador += 1

        shutil.copy2(caminho_origem, caminho_destino)
    except OSError as e:
        return False, f"Erro ao copiar o arquivo: {e}"

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE contas SET caminho_comprovante = ? WHERE id = ?",
            (caminho_destino, conta_id),
        )
        conn.commit()
        return True, "Comprovante anexado com sucesso."
    except sqlite3.Error as e:
        return False, f"Erro ao salvar referencia do comprovante: {e}"
    finally:
        conn.close()


def abrir_comprovante(caminho: str):
    if not caminho or not os.path.exists(caminho):
        return False, "O arquivo de comprovante nao foi encontrado."
    try:
        sistema = platform.system()
        if sistema == "Windows":
            os.startfile(caminho)  # type: ignore[attr-defined]
        elif sistema == "Darwin":
            subprocess.run(["open", caminho], check=False)
        else:
            subprocess.run(["xdg-open", caminho], check=False)
        return True, ""
    except OSError as e:
        return False, f"Nao foi possivel abrir o comprovante: {e}"


# ======================================================================
# COMPONENTES REUTILIZAVEIS DA INTERFACE
# ======================================================================
class CardIndicador(ctk.CTkFrame):
    def __init__(self, master, titulo, valor, cor_valor=COLORS["texto"], **kwargs):
        super().__init__(master, fg_color=COLORS["card"], corner_radius=10, **kwargs)
        self.label_titulo = ctk.CTkLabel(
            self, text=titulo, font=ctk.CTkFont(size=13),
            text_color=COLORS["texto_sec"], anchor="w",
        )
        self.label_titulo.pack(fill="x", padx=16, pady=(14, 2))
        self.label_valor = ctk.CTkLabel(
            self, text=valor, font=ctk.CTkFont(size=22, weight="bold"),
            text_color=cor_valor, anchor="w",
        )
        self.label_valor.pack(fill="x", padx=16, pady=(0, 14))

    def atualizar(self, valor):
        self.label_valor.configure(text=valor)


def estilizar_treeview():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Custom.Treeview",
        background=COLORS["campo"],
        fieldbackground=COLORS["campo"],
        foreground=COLORS["texto"],
        rowheight=28,
        borderwidth=0,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Custom.Treeview.Heading",
        background=COLORS["sidebar"],
        foreground=COLORS["texto"],
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
    )
    style.map(
        "Custom.Treeview",
        background=[("selected", COLORS["destaque"])],
        foreground=[("selected", "#FFFFFF")],
    )


# ======================================================================
# APLICACAO PRINCIPAL
# ======================================================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.usuario_atual = None
        self.conta_selecionada_id = None
        self.title(APP_TITLE)
        self.configure(fg_color=COLORS["fundo"])
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        estilizar_treeview()
        self.mostrar_login()

    def _on_close(self):
        self.destroy()

    def limpar_janela(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ------------------------------------------------------------------
    # TELA DE LOGIN
    # ------------------------------------------------------------------
    def mostrar_login(self):
        self.usuario_atual = None
        self.limpar_janela()
        self.resizable(False, False)
        largura, altura = 420, 480
        self.geometry(f"{largura}x{altura}")
        self.eval("tk::PlaceWindow . center")

        container = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=16)
        container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.8)

        ctk.CTkLabel(
            container, text="Contas a Pagar", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["texto"],
        ).pack(pady=(36, 4))
        ctk.CTkLabel(
            container, text="Acesse com seu usuario e senha",
            font=ctk.CTkFont(size=12), text_color=COLORS["texto_sec"],
        ).pack(pady=(0, 24))

        self.entry_login_usuario = ctk.CTkEntry(
            container, placeholder_text="Usuario", width=260,
            fg_color=COLORS["campo"], border_width=0,
        )
        self.entry_login_usuario.pack(pady=8)

        self.entry_login_senha = ctk.CTkEntry(
            container, placeholder_text="Senha", show="*", width=260,
            fg_color=COLORS["campo"], border_width=0,
        )
        self.entry_login_senha.pack(pady=8)
        self.entry_login_senha.bind("<Return>", lambda e: self._tentar_login())

        ctk.CTkButton(
            container, text="Entrar", width=260, fg_color=COLORS["destaque"],
            hover_color=COLORS["destaque_hover"], command=self._tentar_login,
        ).pack(pady=(20, 8))

        ctk.CTkLabel(
            container, text="Primeiro acesso: admin / admin123",
            font=ctk.CTkFont(size=11), text_color=COLORS["texto_sec"],
        ).pack(pady=(10, 0))

        self.entry_login_usuario.focus_set()

    def _tentar_login(self):
        username = self.entry_login_usuario.get().strip()
        senha = self.entry_login_senha.get()
        if not username or not senha:
            messagebox.showwarning("Atencao", "Informe usuario e senha.")
            return

        usuario, erro = autenticar_usuario(username, senha)
        if erro:
            messagebox.showerror("Erro de login", erro)
            return

        self.usuario_atual = usuario
        if username == "admin" and senha == "admin123":
            messagebox.showinfo(
                "Recomendacao de seguranca",
                "Voce esta usando a senha padrao. Por seguranca, altere-a em 'Usuarios'.",
            )
        self.mostrar_principal()

    # ------------------------------------------------------------------
    # TELA PRINCIPAL (SIDEBAR + CONTEUDO)
    # ------------------------------------------------------------------
    def mostrar_principal(self):
        self.limpar_janela()
        self.resizable(True, True)
        self.geometry("1200x720")
        self.minsize(1024, 640)

        sidebar = ctk.CTkFrame(self, fg_color=COLORS["sidebar"], width=220, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(
            sidebar, text="Contas a Pagar", font=ctk.CTkFont(size=17, weight="bold"),
            text_color=COLORS["texto"],
        ).pack(pady=(28, 4), padx=16, anchor="w")
        ctk.CTkLabel(
            sidebar, text=f"Ola, {self.usuario_atual['username']}",
            font=ctk.CTkFont(size=12), text_color=COLORS["texto_sec"],
        ).pack(pady=(0, 24), padx=16, anchor="w")

        botoes = [
            ("Dashboard", self.mostrar_dashboard),
            ("Nova Conta", self.mostrar_cadastro_conta),
            ("Consultar Contas", self.mostrar_contas),
        ]
        if self.usuario_atual["perfil"] == "admin":
            botoes.append(("Usuarios", self.mostrar_usuarios))

        for texto, comando in botoes:
            ctk.CTkButton(
                sidebar, text=texto, anchor="w", fg_color="transparent",
                hover_color=COLORS["card"], text_color=COLORS["texto"],
                font=ctk.CTkFont(size=13), height=38, command=comando,
            ).pack(fill="x", padx=12, pady=3)

        ctk.CTkButton(
            sidebar, text="Sair (Logout)", anchor="w", fg_color="transparent",
            hover_color=COLORS["vencido"], text_color=COLORS["texto"],
            font=ctk.CTkFont(size=13), height=38, command=self._logout,
        ).pack(fill="x", padx=12, pady=(30, 12), side="bottom")

        self.content_frame = ctk.CTkFrame(self, fg_color=COLORS["fundo"], corner_radius=0)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.mostrar_dashboard()

    def _logout(self):
        if messagebox.askyesno("Logout", "Deseja realmente sair do sistema?"):
            self.mostrar_login()

    def _limpar_conteudo(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ------------------------------------------------------------------
    # DASHBOARD
    # ------------------------------------------------------------------
    def mostrar_dashboard(self):
        self._limpar_conteudo()
        indicadores = calcular_indicadores()

        ctk.CTkLabel(
            self.content_frame, text="Dashboard", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["texto"],
        ).pack(anchor="w", padx=30, pady=(24, 16))

        grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        grid.pack(fill="x", padx=30)
        for i in range(4):
            grid.columnconfigure(i, weight=1)

        cards_info = [
            ("Total de contas", str(indicadores["total"]), COLORS["texto"]),
            ("Contas pendentes", str(indicadores["qtd_pendentes"]), COLORS["pendente"]),
            ("Contas pagas", str(indicadores["qtd_pagas"]), COLORS["pago"]),
            ("Contas vencidas", str(indicadores["qtd_vencidas"]), COLORS["vencido"]),
            ("Vencendo hoje", str(indicadores["qtd_vencendo_hoje"]), COLORS["vencendo"]),
            ("Valor pendente", formatar_moeda(indicadores["valor_pendente"]), COLORS["pendente"]),
            ("Valor pago", formatar_moeda(indicadores["valor_pago"]), COLORS["pago"]),
        ]
        for idx, (titulo, valor, cor) in enumerate(cards_info):
            linha, coluna = divmod(idx, 4)
            card = CardIndicador(grid, titulo, valor, cor_valor=cor)
            card.grid(row=linha, column=coluna, sticky="nsew", padx=8, pady=8)

        # Grafico simples de barras (sem dependencias externas)
        grafico_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["card"], corner_radius=10)
        grafico_frame.pack(fill="both", expand=True, padx=30, pady=(20, 24))

        ctk.CTkLabel(
            grafico_frame, text="Resumo de contas", font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["texto"],
        ).pack(anchor="w", padx=20, pady=(16, 4))

        canvas = tk.Canvas(grafico_frame, bg=COLORS["card"], highlightthickness=0, height=220)
        canvas.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        dados_grafico = [
            ("Pagas", indicadores["qtd_pagas"], COLORS["pago"]),
            ("Pendentes", indicadores["qtd_pendentes"] - indicadores["qtd_vencidas"] - indicadores["qtd_vencendo_hoje"], COLORS["pendente"]),
            ("Vencidas", indicadores["qtd_vencidas"], COLORS["vencido"]),
        ]

        def desenhar_grafico(event=None):
            canvas.delete("all")
            largura = canvas.winfo_width() or 600
            altura = canvas.winfo_height() or 220
            maximo = max([v for _, v, _ in dados_grafico] + [1])
            largura_barra = largura // (len(dados_grafico) * 2)
            base_y = altura - 30

            for i, (rotulo, valor, cor) in enumerate(dados_grafico):
                altura_barra = int((valor / maximo) * (altura - 60)) if maximo else 0
                x0 = 40 + i * (largura_barra * 2 + 20)
                x1 = x0 + largura_barra
                y1 = base_y
                y0 = base_y - altura_barra
                canvas.create_rectangle(x0, y0, x1, y1, fill=cor, outline="")
                canvas.create_text((x0 + x1) / 2, y0 - 12, text=str(valor), fill=COLORS["texto"], font=("Segoe UI", 10, "bold"))
                canvas.create_text((x0 + x1) / 2, base_y + 14, text=rotulo, fill=COLORS["texto_sec"], font=("Segoe UI", 9))

        canvas.bind("<Configure>", desenhar_grafico)

    # ------------------------------------------------------------------
    # CADASTRO DE CONTA
    # ------------------------------------------------------------------
    def mostrar_cadastro_conta(self):
        self._limpar_conteudo()

        ctk.CTkLabel(
            self.content_frame, text="Nova Conta", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["texto"],
        ).pack(anchor="w", padx=30, pady=(24, 16))

        formulario = ctk.CTkFrame(self.content_frame, fg_color=COLORS["card"], corner_radius=10)
        formulario.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(formulario, text="Descricao", text_color=COLORS["texto_sec"]).pack(
            anchor="w", padx=24, pady=(20, 4))
        self.entry_conta_descricao = ctk.CTkEntry(
            formulario, width=400, fg_color=COLORS["campo"], border_width=0)
        self.entry_conta_descricao.pack(anchor="w", padx=24)

        ctk.CTkLabel(formulario, text="Valor (ex: 1250,50)", text_color=COLORS["texto_sec"]).pack(
            anchor="w", padx=24, pady=(16, 4))
        self.entry_conta_valor = ctk.CTkEntry(
            formulario, width=250, fg_color=COLORS["campo"], border_width=0)
        self.entry_conta_valor.pack(anchor="w", padx=24)

        ctk.CTkLabel(formulario, text="Data de vencimento (dd/mm/aaaa)", text_color=COLORS["texto_sec"]).pack(
            anchor="w", padx=24, pady=(16, 4))
        self.entry_conta_data = ctk.CTkEntry(
            formulario, width=250, fg_color=COLORS["campo"], border_width=0)
        self.entry_conta_data.pack(anchor="w", padx=24)

        ctk.CTkButton(
            formulario, text="Salvar Conta", fg_color=COLORS["destaque"],
            hover_color=COLORS["destaque_hover"], width=200,
            command=self._salvar_nova_conta,
        ).pack(anchor="w", padx=24, pady=24)

    def _salvar_nova_conta(self):
        sucesso, mensagem = cadastrar_conta(
            self.entry_conta_descricao.get(),
            self.entry_conta_valor.get(),
            self.entry_conta_data.get(),
            self.usuario_atual["id"],
        )
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.entry_conta_descricao.delete(0, "end")
            self.entry_conta_valor.delete(0, "end")
            self.entry_conta_data.delete(0, "end")
            self.mostrar_contas()
        else:
            messagebox.showerror("Erro", mensagem)

    # ------------------------------------------------------------------
    # CONSULTA DE CONTAS
    # ------------------------------------------------------------------
    def mostrar_contas(self):
        self._limpar_conteudo()
        self.conta_selecionada_id = None
        hoje = date.today()
        self.filtro_status_var = tk.StringVar(value="Todas")
        self.filtro_mes_var = tk.IntVar(value=hoje.month)
        self.filtro_ano_var = tk.IntVar(value=hoje.year)

        ctk.CTkLabel(
            self.content_frame, text="Consultar Contas", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["texto"],
        ).pack(anchor="w", padx=30, pady=(24, 12))

        barra_filtros = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        barra_filtros.pack(fill="x", padx=30)

        for opcao in ["Todas", "Pendentes", "Pagas", "Vencidas", "Vencendo hoje"]:
            ctk.CTkRadioButton(
                barra_filtros, text=opcao, variable=self.filtro_status_var, value=opcao,
                text_color=COLORS["texto"], command=self._atualizar_tabela_contas,
            ).pack(side="left", padx=(0, 14))

        meses_opcoes = ["Todos"] + [f"{i:02d} - {MESES_PT[i-1]}" for i in range(1, 13)]
        self.combo_mes = ctk.CTkOptionMenu(
            barra_filtros, values=meses_opcoes, width=150,
            fg_color=COLORS["campo"], button_color=COLORS["campo"],
            command=self._mudar_filtro_mes,
        )
        self.combo_mes.set(f"{hoje.month:02d} - {MESES_PT[hoje.month - 1]}")
        self.combo_mes.pack(side="left", padx=(20, 8))

        anos_opcoes = [str(ano) for ano in range(hoje.year - 3, hoje.year + 2)]
        self.combo_ano = ctk.CTkOptionMenu(
            barra_filtros, values=anos_opcoes, width=90,
            fg_color=COLORS["campo"], button_color=COLORS["campo"],
            command=self._mudar_filtro_ano,
        )
        self.combo_ano.set(str(hoje.year))
        self.combo_ano.pack(side="left")

        # Tabela
        tabela_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["card"], corner_radius=10)
        tabela_frame.pack(fill="both", expand=True, padx=30, pady=16)

        colunas = ("id", "descricao", "valor", "vencimento", "status", "pagamento", "comprovante", "usuario")
        self.tabela_contas = ttk.Treeview(
            tabela_frame, columns=colunas, show="headings", style="Custom.Treeview", height=14,
        )
        titulos = {
            "id": "ID", "descricao": "Descricao", "valor": "Valor",
            "vencimento": "Vencimento", "status": "Status", "pagamento": "Pagamento",
            "comprovante": "Comprovante", "usuario": "Usuario",
        }
        larguras = {
            "id": 40, "descricao": 240, "valor": 110, "vencimento": 100,
            "status": 110, "pagamento": 130, "comprovante": 100, "usuario": 100,
        }
        for coluna in colunas:
            self.tabela_contas.heading(coluna, text=titulos[coluna],
                                        command=lambda c=coluna: self._ordenar_tabela(c))
            self.tabela_contas.column(coluna, width=larguras[coluna], anchor="w")

        self.tabela_contas.tag_configure("pago", foreground=COLORS["pago"])
        self.tabela_contas.tag_configure("vencida", foreground=COLORS["vencido"])
        self.tabela_contas.tag_configure("vencendo", foreground=COLORS["vencendo"])
        self.tabela_contas.tag_configure("pendente", foreground=COLORS["pendente"])

        scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tabela_contas.yview)
        self.tabela_contas.configure(yscrollcommand=scroll.set)
        self.tabela_contas.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=12)
        scroll.pack(side="left", fill="y", pady=12)

        self.tabela_contas.bind("<<TreeviewSelect>>", self._selecionar_conta)

        # Botoes de acao
        acoes_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        acoes_frame.pack(fill="x", padx=30, pady=(0, 24))

        botoes_acao = [
            ("Realizar Baixa", self._acao_realizar_baixa, COLORS["destaque"]),
            ("Desfazer Baixa", self._acao_desfazer_baixa, COLORS["texto_sec"]),
            ("Anexar Comprovante", self._acao_anexar_comprovante, COLORS["destaque"]),
            ("Abrir Comprovante", self._acao_abrir_comprovante, COLORS["texto_sec"]),
            ("Editar", self._acao_editar_conta, COLORS["destaque"]),
            ("Excluir", self._acao_excluir_conta, COLORS["vencido"]),
            ("Atualizar", self._atualizar_tabela_contas, COLORS["texto_sec"]),
        ]
        for texto, comando, cor in botoes_acao:
            ctk.CTkButton(
                acoes_frame, text=texto, fg_color=cor, hover_color=COLORS["destaque_hover"],
                width=150, command=comando,
            ).pack(side="left", padx=(0, 8), pady=4)

        self._ordenacao_atual = {"coluna": None, "reverso": False}
        self._atualizar_tabela_contas()

    def _mudar_filtro_mes(self, valor):
        if valor == "Todos":
            self.filtro_mes_var.set(0)
        else:
            self.filtro_mes_var.set(int(valor.split(" - ")[0]))
        self._atualizar_tabela_contas()

    def _mudar_filtro_ano(self, valor):
        self.filtro_ano_var.set(int(valor))
        self._atualizar_tabela_contas()

    def _atualizar_tabela_contas(self):
        status_filtro = self.filtro_status_var.get()
        mes = self.filtro_mes_var.get() or None
        ano = self.filtro_ano_var.get() if mes else None
        contas = listar_contas(status_filtro, mes=mes, ano=ano)

        for item in self.tabela_contas.get_children():
            self.tabela_contas.delete(item)

        for conta in contas:
            status_exibicao = obter_status_exibicao(conta["status"], conta["data_vencimento"])
            tag = {
                "Pago": "pago", "Vencida": "vencida",
                "Vencendo hoje": "vencendo", "Pendente": "pendente",
            }.get(status_exibicao, "pendente")

            comprovante_texto = "Sim" if conta.get("caminho_comprovante") else "Nao"
            self.tabela_contas.insert(
                "", "end", iid=str(conta["id"]),
                values=(
                    conta["id"],
                    conta["descricao"],
                    formatar_moeda(conta["valor"]),
                    data_iso_para_br(conta["data_vencimento"]),
                    status_exibicao,
                    datahora_iso_para_br(conta.get("data_pagamento")),
                    comprovante_texto,
                    conta.get("usuario_nome") or "-",
                ),
                tags=(tag,),
            )

    def _ordenar_tabela(self, coluna):
        itens = [(self.tabela_contas.set(k, coluna), k) for k in self.tabela_contas.get_children("")]
        reverso = self._ordenacao_atual["coluna"] == coluna and not self._ordenacao_atual["reverso"]
        try:
            itens.sort(key=lambda t: float(re.sub(r"[^\d,.-]", "", t[0]).replace(".", "").replace(",", ".") or 0), reverse=reverso)
        except ValueError:
            itens.sort(key=lambda t: t[0], reverse=reverso)
        for indice, (_, k) in enumerate(itens):
            self.tabela_contas.move(k, "", indice)
        self._ordenacao_atual = {"coluna": coluna, "reverso": reverso}

    def _selecionar_conta(self, event=None):
        selecao = self.tabela_contas.selection()
        self.conta_selecionada_id = int(selecao[0]) if selecao else None

    def _exigir_selecao(self):
        if not self.conta_selecionada_id:
            messagebox.showwarning("Atencao", "Selecione uma conta na tabela.")
            return False
        return True

    def _acao_realizar_baixa(self):
        if not self._exigir_selecao():
            return
        if not messagebox.askyesno("Confirmar baixa", "Confirmar o pagamento desta conta?"):
            return
        sucesso, mensagem = realizar_baixa(self.conta_selecionada_id)
        (messagebox.showinfo if sucesso else messagebox.showerror)(
            "Sucesso" if sucesso else "Erro", mensagem)
        if sucesso:
            self._atualizar_tabela_contas()

    def _acao_desfazer_baixa(self):
        if not self._exigir_selecao():
            return
        if not messagebox.askyesno("Confirmar", "Deseja desfazer a baixa desta conta?"):
            return
        sucesso, mensagem = desfazer_baixa(self.conta_selecionada_id, self.usuario_atual["perfil"])
        (messagebox.showinfo if sucesso else messagebox.showerror)(
            "Sucesso" if sucesso else "Erro", mensagem)
        if sucesso:
            self._atualizar_tabela_contas()

    def _acao_anexar_comprovante(self):
        if not self._exigir_selecao():
            return
        caminho = filedialog.askopenfilename(
            title="Selecionar comprovante",
            filetypes=[("Arquivos suportados", "*.pdf *.png *.jpg *.jpeg")],
        )
        if not caminho:
            return
        sucesso, mensagem = anexar_comprovante(self.conta_selecionada_id, caminho)
        (messagebox.showinfo if sucesso else messagebox.showerror)(
            "Sucesso" if sucesso else "Erro", mensagem)
        if sucesso:
            self._atualizar_tabela_contas()

    def _acao_abrir_comprovante(self):
        if not self._exigir_selecao():
            return
        conta = obter_conta(self.conta_selecionada_id)
        if not conta or not conta.get("caminho_comprovante"):
            messagebox.showwarning("Atencao", "Esta conta nao possui comprovante anexado.")
            return
        sucesso, mensagem = abrir_comprovante(conta["caminho_comprovante"])
        if not sucesso:
            messagebox.showerror("Erro", mensagem)

    def _acao_editar_conta(self):
        if not self._exigir_selecao():
            return
        conta = obter_conta(self.conta_selecionada_id)
        if not conta:
            messagebox.showerror("Erro", "Conta nao encontrada.")
            return
        self._abrir_janela_edicao(conta)

    def _abrir_janela_edicao(self, conta):
        janela = ctk.CTkToplevel(self)
        janela.title("Editar Conta")
        janela.geometry("420x340")
        janela.configure(fg_color=COLORS["card"])
        janela.grab_set()
        janela.transient(self)

        ctk.CTkLabel(janela, text="Descricao", text_color=COLORS["texto_sec"]).pack(anchor="w", padx=24, pady=(20, 4))
        entry_descricao = ctk.CTkEntry(janela, width=350, fg_color=COLORS["campo"], border_width=0)
        entry_descricao.insert(0, conta["descricao"])
        entry_descricao.pack(padx=24)

        ctk.CTkLabel(janela, text="Valor", text_color=COLORS["texto_sec"]).pack(anchor="w", padx=24, pady=(16, 4))
        entry_valor = ctk.CTkEntry(janela, width=250, fg_color=COLORS["campo"], border_width=0)
        entry_valor.insert(0, formatar_moeda(conta["valor"]).replace("R$ ", ""))
        entry_valor.pack(padx=24, anchor="w")

        ctk.CTkLabel(janela, text="Vencimento (dd/mm/aaaa)", text_color=COLORS["texto_sec"]).pack(
            anchor="w", padx=24, pady=(16, 4))
        entry_data = ctk.CTkEntry(janela, width=250, fg_color=COLORS["campo"], border_width=0)
        entry_data.insert(0, data_iso_para_br(conta["data_vencimento"]))
        entry_data.pack(padx=24, anchor="w")

        def salvar():
            sucesso, mensagem = editar_conta(
                conta["id"], entry_descricao.get(), entry_valor.get(), entry_data.get())
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                janela.destroy()
                self._atualizar_tabela_contas()
            else:
                messagebox.showerror("Erro", mensagem)

        ctk.CTkButton(
            janela, text="Salvar alteracoes", fg_color=COLORS["destaque"],
            hover_color=COLORS["destaque_hover"], command=salvar,
        ).pack(pady=24)

    def _acao_excluir_conta(self):
        if not self._exigir_selecao():
            return
        if not messagebox.askyesno("Confirmar exclusao", "Deseja realmente excluir esta conta?"):
            return
        sucesso, mensagem = excluir_conta(self.conta_selecionada_id, self.usuario_atual["perfil"])
        (messagebox.showinfo if sucesso else messagebox.showerror)(
            "Sucesso" if sucesso else "Erro", mensagem)
        if sucesso:
            self.conta_selecionada_id = None
            self._atualizar_tabela_contas()

    # ------------------------------------------------------------------
    # GESTAO DE USUARIOS (somente admin)
    # ------------------------------------------------------------------
    def mostrar_usuarios(self):
        if self.usuario_atual["perfil"] != "admin":
            messagebox.showerror("Acesso negado", "Apenas administradores podem acessar esta area.")
            return

        self._limpar_conteudo()
        self.usuario_selecionado_id = None

        ctk.CTkLabel(
            self.content_frame, text="Gestao de Usuarios", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["texto"],
        ).pack(anchor="w", padx=30, pady=(24, 16))

        corpo = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=30, pady=(0, 24))
        corpo.columnconfigure(0, weight=2)
        corpo.columnconfigure(1, weight=1)
        corpo.rowconfigure(0, weight=1)

        # Tabela de usuarios
        tabela_frame = ctk.CTkFrame(corpo, fg_color=COLORS["card"], corner_radius=10)
        tabela_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        colunas = ("id", "username", "perfil", "ativo", "criado_em")
        self.tabela_usuarios = ttk.Treeview(
            tabela_frame, columns=colunas, show="headings", style="Custom.Treeview", height=14,
        )
        titulos = {"id": "ID", "username": "Usuario", "perfil": "Perfil", "ativo": "Status", "criado_em": "Criado em"}
        for coluna in colunas:
            self.tabela_usuarios.heading(coluna, text=titulos[coluna])
            self.tabela_usuarios.column(coluna, width=100, anchor="w")
        self.tabela_usuarios.tag_configure("inativo", foreground=COLORS["vencido"])
        self.tabela_usuarios.pack(fill="both", expand=True, padx=12, pady=12)
        self.tabela_usuarios.bind("<<TreeviewSelect>>", self._selecionar_usuario)

        # Painel lateral: cadastro e acoes
        painel = ctk.CTkFrame(corpo, fg_color=COLORS["card"], corner_radius=10)
        painel.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(painel, text="Novo usuario", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=COLORS["texto"]).pack(anchor="w", padx=20, pady=(16, 8))

        self.entry_novo_usuario = ctk.CTkEntry(painel, placeholder_text="Usuario", fg_color=COLORS["campo"], border_width=0)
        self.entry_novo_usuario.pack(fill="x", padx=20, pady=4)

        self.entry_nova_senha_usuario = ctk.CTkEntry(painel, placeholder_text="Senha", show="*", fg_color=COLORS["campo"], border_width=0)
        self.entry_nova_senha_usuario.pack(fill="x", padx=20, pady=4)

        self.combo_novo_perfil = ctk.CTkOptionMenu(painel, values=["comum", "admin"], fg_color=COLORS["campo"], button_color=COLORS["campo"])
        self.combo_novo_perfil.pack(fill="x", padx=20, pady=4)

        ctk.CTkButton(
            painel, text="Cadastrar usuario", fg_color=COLORS["destaque"],
            hover_color=COLORS["destaque_hover"], command=self._acao_cadastrar_usuario,
        ).pack(fill="x", padx=20, pady=(8, 20))

        ctk.CTkLabel(painel, text="Usuario selecionado", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=COLORS["texto"]).pack(anchor="w", padx=20, pady=(0, 8))

        self.entry_nova_senha_alterar = ctk.CTkEntry(painel, placeholder_text="Nova senha", show="*", fg_color=COLORS["campo"], border_width=0)
        self.entry_nova_senha_alterar.pack(fill="x", padx=20, pady=4)
        ctk.CTkButton(
            painel, text="Alterar senha", fg_color=COLORS["texto_sec"],
            hover_color=COLORS["destaque_hover"], command=self._acao_alterar_senha_usuario,
        ).pack(fill="x", padx=20, pady=4)

        self.combo_alterar_perfil = ctk.CTkOptionMenu(painel, values=["comum", "admin"], fg_color=COLORS["campo"], button_color=COLORS["campo"])
        self.combo_alterar_perfil.pack(fill="x", padx=20, pady=(12, 4))
        ctk.CTkButton(
            painel, text="Alterar perfil", fg_color=COLORS["texto_sec"],
            hover_color=COLORS["destaque_hover"], command=self._acao_alterar_perfil_usuario,
        ).pack(fill="x", padx=20, pady=4)

        linha_ativo = ctk.CTkFrame(painel, fg_color="transparent")
        linha_ativo.pack(fill="x", padx=20, pady=(12, 20))
        ctk.CTkButton(
            linha_ativo, text="Ativar", fg_color=COLORS["pago"],
            command=lambda: self._acao_definir_status_usuario(1), width=100,
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            linha_ativo, text="Desativar", fg_color=COLORS["vencido"],
            command=lambda: self._acao_definir_status_usuario(0), width=100,
        ).pack(side="left")

        self._atualizar_tabela_usuarios()

    def _atualizar_tabela_usuarios(self):
        for item in self.tabela_usuarios.get_children():
            self.tabela_usuarios.delete(item)
        for usuario in listar_usuarios():
            tag = "inativo" if usuario["ativo"] == 0 else ""
            self.tabela_usuarios.insert(
                "", "end", iid=str(usuario["id"]),
                values=(
                    usuario["id"], usuario["username"], usuario["perfil"],
                    "Ativo" if usuario["ativo"] == 1 else "Inativo",
                    datahora_iso_para_br(usuario["data_criacao"]),
                ),
                tags=(tag,) if tag else (),
            )

    def _selecionar_usuario(self, event=None):
        selecao = self.tabela_usuarios.selection()
        self.usuario_selecionado_id = int(selecao[0]) if selecao else None

    def _acao_cadastrar_usuario(self):
        sucesso, mensagem = cadastrar_usuario(
            self.entry_novo_usuario.get(),
            self.entry_nova_senha_usuario.get(),
            self.combo_novo_perfil.get(),
        )
        (messagebox.showinfo if sucesso else messagebox.showerror)(
            "Sucesso" if sucesso else "Erro", mensagem)
        if sucesso:
            self.entry_novo_usuario.delete(0, "end")
            self.entry_nova_senha_usuario.delete(0, "end")
            self._atualizar_tabela_usuarios()

    def _acao_alterar_senha_usuario(self):
        if not self.usuario_selecionado_id:
            messagebox.showwarning("Atencao", "Selecione um usuario na tabela.")
            return
        sucesso, mensagem = alterar_senha_usuario(
            self.usuario_selecionado_id, self.entry_nova_senha_alterar.get())
        (messagebox.showinfo if sucesso else messagebox.showerror)(
            "Sucesso" if sucesso else "Erro", mensagem)
        if sucesso:
            self.entry_nova_senha_alterar.delete(0, "end")

    def _acao_alterar_perfil_usuario(self):
        if not self.usuario_selecionado_id:
            messagebox.showwarning("Atencao", "Selecione um usuario na tabela.")
            return
        sucesso, mensagem = alterar_perfil_usuario(
            self.usuario_selecionado_id, self.combo_alterar_perfil.get())
        (messagebox.showinfo if sucesso else messagebox.showerror)(
            "Sucesso" if sucesso else "Erro", mensagem)
        if sucesso:
            self._atualizar_tabela_usuarios()

    def _acao_definir_status_usuario(self, ativo: int):
        if not self.usuario_selecionado_id:
            messagebox.showwarning("Atencao", "Selecione um usuario na tabela.")
            return
        if ativo == 0 and self.usuario_selecionado_id == self.usuario_atual["id"]:
            messagebox.showerror("Erro", "Voce nao pode desativar o proprio usuario enquanto estiver logado.")
            return
        sucesso, mensagem = alterar_status_usuario(self.usuario_selecionado_id, ativo)
        (messagebox.showinfo if sucesso else messagebox.showerror)(
            "Sucesso" if sucesso else "Erro", mensagem)
        if sucesso:
            self._atualizar_tabela_usuarios()


# ======================================================================
# INICIALIZACAO DA APLICACAO
# ======================================================================
def main():
    try:
        inicializar_banco()
    except sqlite3.Error as e:
        messagebox.showerror("Erro critico", f"Nao foi possivel inicializar o banco de dados:\n{e}")
        return

    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
