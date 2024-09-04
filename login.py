# login.py
import flet as ft
import sqlite3
from config import RUTA_LOGO, DATABASE_PATH
from serial_utils import verificar_ativacao, salvar_serial, validar_serial, gerar_serial, obter_validade_serial, verificar_expiracao_proxima

def login_page(page: ft.Page):
    from menu_principal import mostrar_menu  # Importação local para evitar circularidade

    # Verificação de ativação
    validade_serial = obter_validade_serial()
    expira_em_breve = verificar_expiracao_proxima()

    if not verificar_ativacao():
        solicitar_ativacao(page)
        return

    # Continuação da lógica da página de login...
    alert_text = ""
    alert_color = ft.colors.GREEN

    if expira_em_breve:
        alert_text = "Sua licença expira em breve! Por favor, renove sua licença."
        alert_color = ft.colors.ORANGE
    elif "Serial inválido" in validade_serial:
        alert_text = "Serial inválido."
        alert_color = ft.colors.RED

    page.clean()
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Image(src=RUTA_LOGO, width=200, height=200),
                        alignment=ft.alignment.top_center,
                        padding=ft.padding.only(top=20, bottom=20)
                    ),
                    ft.Text(
                        value="Bem-vindo à Aplicação de Cronômetro",
                        size=26,
                        weight="bold",
                        text_align=ft.TextAlign.CENTER,
                        color=ft.colors.BLUE_GREY_900
                    ),
                    ft.Text(
                        value=f"Licença válida até: {validade_serial}",
                        size=18,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.colors.GREEN if validade_serial and "Serial inválido" not in validade_serial else ft.colors.RED
                    ),
                    ft.Text(
                        value=alert_text,
                        size=18,
                        text_align=ft.TextAlign.CENTER,
                        color=alert_color
                    ),
                    # Campos de usuário e senha continuam aqui...
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=50,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=5,
                blur_radius=15,
                color=ft.colors.BLACK26,
                offset=ft.Offset(2, 4)
            ),
            alignment=ft.alignment.center
        )
    )
    page.update()

def solicitar_ativacao(page: ft.Page):
    """
    Mostra a interface de solicitação de ativação de licença.
    """
    serial_input = ft.TextField(label="Insira o número serial", width=300)

    def ativar(e):
        usuario_id = "default_user"  # Este é um exemplo; pode ser um ID real ou gerado
        if validar_serial(serial_input.value, usuario_id):
            salvar_serial(serial_input.value)
            page.snack_bar = ft.SnackBar(content=ft.Text("Aplicativo ativado com sucesso!"), open=True)
            login_page(page)  # Redireciona para a tela de login
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Número serial inválido ou expirado. Tente novamente.", color=ft.colors.RED),
                open=True,
                duration=3000
            )
        page.update()

    page.clean()
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Ativação do Aplicativo",
                        size=26,
                        weight="bold",
                        text_align=ft.TextAlign.CENTER,
                        color=ft.colors.BLUE_GREY_900
                    ),
                    serial_input,
                    ft.ElevatedButton(
                        "Ativar",
                        on_click=ativar,
                        bgcolor=ft.colors.BLUE_GREY_700,
                        color=ft.colors.WHITE
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=50,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=5,
                blur_radius=15,
                color=ft.colors.BLACK26,
                offset=ft.Offset(2, 4)
            ),
            alignment=ft.alignment.center
        )
    )
    page.update()
