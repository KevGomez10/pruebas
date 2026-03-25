import random
import time
from playwright.sync_api import sync_playwright

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdCCqEaQYC1CZqJmFzHKQ7nvZp2degdbvUwaV2Ql1TpZBVeLQ/viewform"

# --- RESPUESTAS DE PRUEBA ---

respuestas_felicidad = [
    "Estar tranquilo",
    "Lograr mis metas",
    "Salud para mi familia",
    "Viajar mucho",
    "Paz mental"
]

respuestas_genz = [
    "Es muy digital",
    "Depende de redes sociales",
    "Buscan autenticidad",
    "Inmediatez",
    "Salud mental primero"
]

respuestas_que_cosas = [
    "Comida rica",
    "Ropa nueva",
    "Escuchar música",
    "Videojuegos",
    "Dulces",
    "Salir con amigos"
]

opciones_consumo = [
    "Redes sociales",
    "Entretenimiento",
    "Compras",
    "Comida o bebida",
    "Relaciones",
    "Tiempo libre / ocio",
    "Logros personales"
]


def llenar_form(page):

    # --- P1 CHECKBOX ---
    seleccion = random.sample(opciones_consumo, random.randint(1, 3))

    for opcion in seleccion:
        checkbox = page.get_by_label(opcion)
        checkbox.wait_for(state="visible")
        checkbox.click()

    page.wait_for_timeout(400)

    # --- P2 TEXTO ---
    page.locator("textarea").nth(0).fill(random.choice(respuestas_felicidad))

    page.wait_for_timeout(400)

    # Obtener grupos de radios
    grupos_radio = page.locator("div[role='radiogroup']")

    # --- P3 RADIO ---
    p3 = grupos_radio.nth(0)

    factores = [
        "Más de factores internos",
        "Más de factores externos",
        "Ambos por igual"
    ]

    p3.get_by_role(
        "radio",
        name=random.choice(factores)
    ).click()

    page.wait_for_timeout(400)

    # --- P4 RADIO ---
    p4 = grupos_radio.nth(1)

    influencia = ["Mucho", "Bastante", "Poco", "Nada"]

    p4.get_by_role(
        "radio",
        name=random.choice(influencia)
    ).click()

    page.wait_for_timeout(400)

    # --- P5 TEXTO ---
    page.locator("textarea").nth(1).fill(random.choice(respuestas_genz))

    page.wait_for_timeout(400)

    # --- P6 RADIO ---
    p6 = grupos_radio.nth(2)

    necesidad = ["Sí", "No", "A veces"]

    p6.get_by_role(
        "radio",
        name=random.choice(necesidad)
    ).click()

    page.wait_for_timeout(400)

    # --- P7 TEXTO ---
    campo = page.locator("textarea").nth(2)

    campo.scroll_into_view_if_needed()
    campo.fill(random.choice(respuestas_que_cosas))

    page.wait_for_timeout(400)


def enviar(page):

    boton = page.get_by_role("button", name="Enviar")

    boton.wait_for(state="visible")
    boton.scroll_into_view_if_needed()

    boton.click()

    page.wait_for_url("**/formResponse", timeout=10000)


def ejecutar_bot():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )

        context = browser.new_context()

        page = context.new_page()

        for i in range(80):

            try:

                print(f"🚀 Envío #{i+1}")

                page.goto(FORM_URL)

                page.wait_for_load_state("domcontentloaded")

                llenar_form(page)

                print("📨 Enviando respuesta...")

                enviar(page)

                print(f"✅ Respuesta #{i+1} enviada")

                time.sleep(2)

            except Exception as e:

                print(f"❌ Error en envío {i+1}: {e}")

                page.close()
                page = context.new_page()

        browser.close()


if __name__ == "__main__":
    ejecutar_bot()