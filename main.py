from playwright.sync_api import sync_playwright
import random
import time
import os

# === PROFILE PATH ===
PROFILE_PATH = r"C:\Users\tatia\Documents\Escola\SideProjects\PythonProject1\firefox-profile"

# === CONFIGS ===
HASHTAGS = ["suculentasportugal", "catosportugal", "plantasportugal"]
COMMENTS = [
    "Simplesmente linda! Qual é o segredo para ela estar tão viçosa? 😍🌿",
    "Lindo demais!!! Fico inspirada com seu cantinho verde 💚🌱✨",
    "Que lindeza! Um encanto prós meus olhos 👀💖",
    "Que coisa mais fofa! O verde acalma a alma 😌🍃",
    "Preciso de uma planta dessas para alegrar meu dia! ☀️😊",
    "Que espetáculo! Dá pra sentir a energia boa daqui. 💫🙌"
]

MAX_ACTIONS_PER_DAY = 35
DELAY_MIN = 210  # 3.5 minutes
DELAY_MAX = 600  # 10 minutes


def collect_post_urls(page, hashtag):
    """Collect /p/ URLs from hashtag page"""
    print(f"Collecting posts from #{hashtag}...")
    page.goto(f"https://www.instagram.com/explore/tags/{hashtag}/", wait_until="load", timeout=60000)
    time.sleep(10)

    urls = set()
    for _ in range(12):  # More scrolls = more posts
        page.evaluate("window.scrollBy(0, 1200)")
        time.sleep(3)

        links = page.query_selector_all('a[href*="/p/"]')
        for link in links:
            href = link.get_attribute('href')
            if href and "/p/" in href:
                urls.add(f"https://www.instagram.com{href}")

    print(f"Collected {len(urls)} unique post URLs.")
    return list(urls)


def interact(page):
    actions_done = 0
    hashtag = random.choice(HASHTAGS)
    post_urls = collect_post_urls(page, hashtag)
    random.shuffle(post_urls)

    for i, post_url in enumerate(post_urls[:MAX_ACTIONS_PER_DAY]):
        if actions_done >= MAX_ACTIONS_PER_DAY:
            break

        try:
            print(f"\nOpening post {i + 1}: {post_url}")
            page.goto(post_url, wait_until="load", timeout=60000)
            time.sleep(random.randint(12, 18))

            # Wait for like button
            page.wait_for_selector('svg[aria-label="Like"]', timeout=20000)

            # LIKE
            if random.random() < 0.7:
                like_btn = page.query_selector('svg[aria-label="Like"]')
                if like_btn:
                    like_btn.click(force=True)
                    time.sleep(2)
                    print("Like given")

                    # COMMENT
                    if random.random() < 0.6:
                        comment_box = page.query_selector('textarea[aria-label="Add a comment..."]')
                        if comment_box:
                            comment = random.choice(COMMENTS)
                            comment_box.click()
                            time.sleep(1)
                            comment_box.fill(comment)
                            time.sleep(2)
                            page.keyboard.press("Enter")
                            time.sleep(5)
                            print(f"Comment: {comment[:40]}...")
                            actions_done += 1

            # Back to hashtag (reload to avoid stale elements)
            page.goto(f"https://www.instagram.com/explore/tags/{hashtag}/", wait_until="load", timeout=60000)
            time.sleep(5)

            # Human delay
            delay = random.randint(DELAY_MIN, DELAY_MAX)
            print(f"Waiting {delay//60} min before next post...")
            time.sleep(delay)

        except Exception as e:
            print(f"Error on post {i+1}: {e}")
            try:
                page.goto(f"https://www.instagram.com/explore/tags/{hashtag}/")
                time.sleep(5)
            except:
                pass
            time.sleep(10)
            continue

    return actions_done


# === START FIREFOX ===
with sync_playwright() as p:
    print("Starting Firefox with persistent profile...")

    if not os.path.exists(PROFILE_PATH):
        os.makedirs(PROFILE_PATH)

    browser = p.firefox.launch_persistent_context(
        PROFILE_PATH,
        headless=False,
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"
    )

    page = browser.pages[0] if browser.pages else browser.new_page()

    # MANUAL LOGIN
    if "login" in page.url.lower() or "instagram.com" not in page.url:
        print("\nMANUAL LOGIN REQUIRED:")
        print("1. Reject cookies")
        print("2. Enter credentials")
        print("3. 2FA if needed")
        print("4. 'Not now' on pop-ups")
        input("Press ENTER when on feed...")

    total = interact(page)
    print(f"\n{total} interactions done. Safe session!")

    print("Bot finished. Close Firefox when ready.")