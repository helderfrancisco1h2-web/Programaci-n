import gradio as gr
import re
import json
from pathlib import Path


kb_adulto = {
    "malware": """🦠 **Malware**: software malicioso que puede dañar tu equipo o robar información.
Subtipos: troyanos, gusanos, adware, spyware, rootkits, keyloggers, ransomware, bootkits, scareware, dialers.
✅ Acciones recomendadas:
1) Desconectar internet.
2) Analizar con antivirus actualizado.
3) Revisar procesos sospechosos.
4) Cuarentenar archivos infectados.""",

    "phishing": """🎣 **Phishing**: correos, mensajes o sitios web falsos que buscan obtener datos personales.
Subtipos: spear phishing, whaling, pharming, smishing, vishing.
✅ Acciones recomendadas:
1) No abrir enlaces sospechosos.
2) No ingresar datos personales.
3) Verificar remitente.
4) Reportar correo sospechoso.""",

    "ransomware": """💀 **Ransomware**: malware que cifra tus archivos y pide rescate.
Subtipos: CryptoLocker, WannaCry, Petya, Ryuk.
✅ Acciones recomendadas:
1) No pagar rescate.
2) Restaurar desde copia de seguridad.
3) Analizar con antivirus especializado.
4) Mantener sistema actualizado.""",

    "spyware": """🕵️ **Spyware**: software que espía tus actividades.
Subtipos: keyloggers, adware, tracking cookies, monitorización remota.
✅ Acciones recomendadas:
1) Escanear con antivirus.
2) Cambiar contraseñas.
3) Revisar programas instalados.
4) Eliminar software sospechoso.""",

    "enlaces": """🔗 **Enlaces sospechosos**: algunos sitios pueden robar datos o instalar malware.
✅ Acciones recomendadas:
1) No abrir enlaces desconocidos.
2) Analizar URL en páginas seguras.
3) Verificar certificado SSL.
4) Evitar acortar enlaces sospechosos.""",

    "wifi": """📶 **WiFi y redes seguras**:
Subtemas: configuración segura de router, WPA3/WPA2, ocultar SSID, firewall, actualizaciones de firmware, redes públicas, VPN, contraseñas robustas.
✅ Acciones recomendadas:
1) Cambiar contraseña del router regularmente.
2) Usar WPA3 o WPA2.
3) Evitar redes públicas sin VPN.
4) Revisar dispositivos conectados.
5) Mantener firmware actualizado.""",

    "contraseñas": """🔑 **Contraseñas seguras**:
Subtemas: longitud mínima, combinaciones de letras, números y símbolos, gestor de contraseñas, autenticación de dos factores (2FA), no reutilizar contraseñas.
✅ Acciones recomendadas:
1) Crear contraseñas largas y únicas.
2) Usar gestor de contraseñas.
3) Activar 2FA siempre que sea posible.
4) Cambiar contraseñas regularmente."""
}

kb_educativa = {
    "malware": "🦠 **Virus malo**: es un programa que puede romper la computadora o robar cosas. No hagas clic en archivos raros y avisá a un adulto.",
    "phishing": "🎣 **Correo falso**: mensajes que quieren tus datos. No hagas clic ni pongas información personal, contale a un adulto.",
    "ransomware": "💀 **Bloqueo de archivos**: algunos virus bloquean tus archivos y piden dinero. No pagues y avisá a un adulto.",
    "spyware": "🕵️ **Espía**: programas que miran lo que haces en la compu. Avisá a un adulto y pasá antivirus.",
    "enlaces": "🔗 **Link sospechoso**: algunos enlaces pueden ser peligrosos. No los abras y pedí ayuda a un adulto.",
    "wifi": "📶 **WiFi seguro**: no cualquier persona debe usar tu internet. Usá contraseñas fuertes y pedí ayuda a un adulto para configurarlo.",
    "contraseñas": "🔑 **Contraseñas fuertes**: no uses cosas fáciles como '1234' o tu nombre. Pedí ayuda a un adulto para hacer una contraseña segura y guardarla bien."
}

scan_urls = {
    "malware": ["https://www.malwarebytes.com", "https://www.eset.com", "https://www.bitdefender.com"],
    "phishing": ["https://www.phishtank.com", "https://transparencyreport.google.com/safe-browsing/search"],
    "ransomware": ["https://www.nomoreransom.org", "https://id-ransomware.malwarehunterteam.com"],
    "spyware": ["https://www.malwarebytes.com/spyware", "https://www.bitdefender.com"],
    "enlaces": ["https://www.virustotal.com", "https://urlscan.io", "https://sitecheck.sucuri.net"],
    "wifi": ["https://www.speedtest.net", "https://www.routersecurity.org", "https://www.howtogeek.com/"], 
    "contraseñas": ["https://haveibeenpwned.com", "https://www.lastpass.com/password-generator", "https://www.1password.com/password-generator/"]
}

saludos_dict = {
    "hola": "👋 ¡Hola! Soy tu asistente de ciberseguridad, contame qué pasó y te ayudo.",
    "buenas": "👋 ¡Buenas! Puedo ayudarte con temas como phishing, malware, ransomware, spyware, enlaces sospechosos, wifi o contraseñas.",
    "buen día": "👋 ¡Buen día! Estoy aquí para ayudarte a mantener tus dispositivos seguros."
}

despedidas_dict = {
    "gracias": "😊 ¡De nada! Me alegra haberte ayudado. Recordá mantener tu equipo protegido.",
    "chau": "👋 ¡Chau! Que tengas un gran día y navegá siempre con precaución.",
    "adiós": "👋 ¡Adiós! Si necesitás ayuda más tarde, voy a estar acá.",
    "hasta luego": "👋 ¡Hasta luego! Recordá revisar siempre los enlaces antes de hacer clic.",
    "nos vemos": "👋 ¡Nos vemos! Cuidá tu información y usá contraseñas seguras."
}


def detect_category(user_input):
    url_pattern = r"(https?://[^\s]+)"
    urls_found = re.findall(url_pattern, user_input.lower())
    if urls_found:
        return "enlaces", urls_found[0]

    keywords = {
        "phishing": ["phishing", "correo", "estafa", "link", "mensaje sospechoso"],
        "malware": ["virus", "malware", "troyano", "gusano", "infectado"],
        "ransomware": ["ransomware", "rescate", "bloqueo", "archivos cifrados"],
        "spyware": ["espía", "spyware", "seguimiento", "monitor"],
        "wifi": ["wifi", "red", "router", "internet", "conexión"],
        "contraseñas": ["contraseña", "clave", "pw", "password"],
    }
    for category, words in keywords.items():
        if any(re.search(rf"\b{w}\b", user_input.lower()) for w in words):
            return category, None
    return "desconocido", None

def guardar_historial_json(chat_history):
    desktop = Path.home() / "Desktop"
    file_path = desktop / "historial_chat.json"
    try:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                historial_existente = json.load(f)
            historial_existente.extend(chat_history)
            chat_history = historial_existente
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(chat_history, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"No se pudo guardar el historial: {e}")

def limpiar_chat_y_json():
    desktop = Path.home() / "Desktop"
    file_path = desktop / "historial_chat.json"
    try:
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        print(f"No se pudo eliminar el historial: {e}")
    return [], []

def chatbot_response(user_input, show_actions, show_urls, modo_educativa, modo_simple, chat_history):
    mensaje_lower = user_input.lower().strip()

    
    for saludo, respuesta_saludo in saludos_dict.items():
        if saludo in mensaje_lower:
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": respuesta_saludo})
            if not modo_educativa:
                guardar_historial_json(chat_history)
            return chat_history, chat_history

    
    for despedida, respuesta_despedida in despedidas_dict.items():
        if despedida in mensaje_lower:
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": respuesta_despedida})
            if not modo_educativa:
                guardar_historial_json(chat_history)
            return chat_history, chat_history

    
    category, detected_url = detect_category(user_input)

    kb = kb_educativa if modo_educativa else kb_adulto
    response = kb.get(category, None)
    if not response:
        response = ("🤔 No pude determinar el problema exacto. Pega tu enlace o escribí palabras como "
                    "'virus', 'correo sospechoso', 'ransomware', 'spyware', 'wifi', 'contraseña'...")

    
    if show_actions and category in kb_adulto:
        if modo_simple and not modo_educativa:
            
            response += "\n\n✅ **Acciones paso a paso (modo simple):**"
            if category == "malware":
                response += "\n1) Desconectá tu internet para que el virus no se propague."
                response += "\n2) Abrí tu antivirus y hacé un escaneo completo."
                response += "\n3) Mirá los procesos que están corriendo; cerrá los sospechosos."
                response += "\n4) Pone en cuarentena los archivos que el antivirus marque como peligrosos."
            elif category == "phishing":
                response += "\n1) No hagas clic en enlaces sospechosos."
                response += "\n2) No ingreses datos personales en páginas dudosas."
                response += "\n3) Verificá siempre quién te envió el correo."
                response += "\n4) Reportá el correo sospechoso a tu proveedor de email."
            elif category == "ransomware":
                response += "\n1) No pagues rescate."
                response += "\n2) Restaurá tus archivos desde copia de seguridad."
                response += "\n3) Analizá el equipo con un antivirus especializado."
                response += "\n4) Mantené tu sistema actualizado."
            elif category == "spyware":
                response += "\n1) Escaneá tu equipo con antivirus."
                response += "\n2) Cambiá tus contraseñas importantes."
                response += "\n3) Revisá los programas instalados."
                response += "\n4) Eliminá cualquier software sospechoso."
            elif category == "enlaces":
                response += "\n1) No abras enlaces desconocidos."
                response += "\n2) Revisá la URL con páginas seguras como VirusTotal."
                response += "\n3) Evitá acortar enlaces sospechosos."
            elif category == "wifi":
                response += "\n1) Cambiá la contraseña del router."
                response += "\n2) Usá WPA3 o WPA2."
                response += "\n3) Evitá redes públicas sin VPN."
                response += "\n4) Revisá los dispositivos conectados."
                response += "\n5) Mantené el firmware actualizado."
            elif category == "contraseñas":
                response += "\n1) Hacé contraseñas largas y únicas."
                response += "\n2) Usá un gestor de contraseñas."
                response += "\n3) Activá la autenticación de dos pasos (2FA)."
                response += "\n4) Cambiá las contraseñas regularmente."
        else:
            response += "\n\n✅ **Acciones sugeridas activadas**"

    
    if show_urls:
        urls = scan_urls.get(category, [])
        if urls:
            response += "\n\n🌐 **Páginas recomendadas para análisis:**\n" + "\n".join(urls)

    if detected_url and category == "enlaces":
        response += f"\n\n🔎 El enlace detectado fue: {detected_url}\n"
        response += "Podés analizarlo en VirusTotal:\nhttps://www.virustotal.com"

    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response})

    if not modo_educativa:
        guardar_historial_json(chat_history)

    return chat_history, chat_history


with gr.Blocks(title="Chatbot de Ciberseguridad") as demo:
    gr.Markdown("## 🛡️ Chatbot de Ciberseguridad Educativo y de Asistencia Técnica")

    chatbot = gr.Chatbot(label="💬 Chatbot", type="messages")
    chat_history_state = gr.State([])

    with gr.Row():
        user_input = gr.Textbox(label="Escribí tu mensaje", placeholder="Ejemplo: Tengo un virus o sospecho de un enlace raro")
    with gr.Row():
        show_actions = gr.Checkbox(label="✅ Mostrar acciones recomendadas", value=False)
        show_urls = gr.Checkbox(label="🌐 Mostrar páginas de escaneo", value=False)
        modo_educativa = gr.Checkbox(label="🧒 Activar modo educativo (para menores)", value=False)
        modo_simple = gr.Checkbox(label="👴 Activar modo explicación simple", value=False)
    with gr.Row():
        send_button = gr.Button("Enviar")
        clear_button = gr.Button("🗑️ Limpiar chat y eliminar historial JSON")

    send_button.click(chatbot_response,
                      inputs=[user_input, show_actions, show_urls, modo_educativa, modo_simple, chat_history_state],
                      outputs=[chatbot, chat_history_state])

    clear_button.click(limpiar_chat_y_json, outputs=[chatbot, chat_history_state])

if __name__ == "__main__":
    demo.launch()
