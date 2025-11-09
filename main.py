# ===============================================
# BOT COM PERFIL PERSISTENTE DO FIREFOX
# Login manual na 1ª vez → depois automático
# Sem pop-ups, sem erros, 100% seguro
# ===============================================

from playwright.sync_api import sync_playwright
import random
import time
import os

# === CAMINHO DO PERFIL (MUDA SE MUDAR A PASTA) ===
PROFILE_PATH = r"C:\Users\tatia\Documents\Escola\SideProjects\PythonProject1\firefox-profile"

# === CONFIGS ===
HASHTAGS = ["suculentasportugal", "suculentas", "catos", "plantas"]
COMENTARIOS = [
    "Simplesmente linda! Qual é o segredo para ela estar tão viçosa? 😍🌿",
    "Lindo demais!!! Fico inspirada com seu cantinho verde 💚🌱✨",
    "Que lindeza! Um encanto prós meus olhos 👀💖",
    "Que coisa mais fofa! O verde acalma a alma 😌🍃",
    "Preciso de uma planta dessas para alegrar meu dia! ☀️😊",
    "Que espetáculo! Dá pra sentir a energia boa daqui. 💫🙌"
]

MAX_ACOES_POR_DIA = 35
DELAY_MIN = 210  # 5 min
DELAY_MAX = 600  # 10 min

def interage(page):
    acoes_feitas = 0
    hashtag = random.choice(HASHTAGS)
    print(f"\nAbrindo hashtag: #{hashtag}")

    try:
        page.goto(f"https://www.instagram.com/explore/tags/{hashtag}/", wait_until="load", timeout=60000)
        time.sleep(8)

        print("Rolando para carregar posts...")
        for _ in range(6):
            page.evaluate("window.scrollBy(0, 900)")
            time.sleep(3)

        posts = page.query_selector_all('a[href*="/p/"]')
        posts = [p for p in posts if p.is_visible() and "/p/" in (p.get_attribute('href') or "")]

        if not posts:
            print("Nenhum post encontrado.")
            return 0

        print(f"Encontrados {len(posts)} posts.")
        random.shuffle(posts)

        for i, post in enumerate(posts[:10]):
            if acoes_feitas >= MAX_ACOES_POR_DIA:
                break

            try:
                print(f"Abrindo post {i + 1}...")
                post.click()
                time.sleep(random.randint(10, 16))

                if random.random() < 0.7:
                    like = page.query_selector('svg[aria-label="Like"]')
                    if like and like.is_visible():
                        like.click()
                        time.sleep(2)
                        print("Like dado")

                        if random.random() < 0.6:
                            box = page.query_selector('textarea[aria-label="Add a comment..."]')
                            if box:
                                comentario = random.choice(COMENTARIOS)
                                box.click()
                                time.sleep(1)
                                box.fill(comentario)
                                time.sleep(2)
                                page.keyboard.press("Enter")
                                time.sleep(5)
                                print(f"Comentário: {comentario[:40]}...")
                                acoes_feitas += 1

                page.go_back()
                time.sleep(random.randint(DELAY_MIN, DELAY_MAX))

            except Exception as e:
                print(f"Erro: {e}")
                try:
                    page.go_back()
                except:
                    pass
                time.sleep(10)

    except Exception as e:
        print(f"Erro na hashtag: {e}")

    return acoes_feitas


# === INICIA FIREFOX COM PERFIL PERSISTENTE ===
with sync_playwright() as p:
    print("Iniciando Firefox com perfil persistente...")

    # Cria perfil se não existir
    if not os.path.exists(PROFILE_PATH):
        os.makedirs(PROFILE_PATH)

    browser = p.firefox.launch_persistent_context(
        PROFILE_PATH,
        headless=False,
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
        java_script_enabled=True,
        bypass_csp=True
    )

    page = browser.pages[0] if browser.pages else browser.new_page()

    # === PRIMEIRA VEZ: FAZ LOGIN MANUAL ===
    if "login" in page.url or "instagram.com" not in page.url:
        print("\nFAZ LOGIN MANUALMENTE:")
        print("1. Aceita cookies → 'Rejeitar tudo'")
        print("2. Mete username e senha")
        print("3. 2FA se pedir")
        print("4. Clica 'Não agora' em tudo")
        print("5. DEIXA ABERTO COM O FEED!")
        input("Quando estiver logado, aperta ENTER para continuar...")

    # === INTERAGE ===
    total = interage(page)
    print(f"\n{total} interações feitas. Sessão segura!")

    print("Bot finalizado. Podes fechar o Firefox.")
    # browser.close()  # Comenta para manter aberto