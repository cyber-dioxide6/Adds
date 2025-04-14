import asyncio
from playwright.async_api import async_playwright
import random

async def simulate_valid_click(url, unique_id):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=300)
        context = await browser.new_context(
            viewport={"width": random.randint(800, 1200), "height": random.randint(600, 1000)},
            user_agent=f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{random.randint(90, 120)}.0) Gecko/20100101 Firefox/{random.randint(90, 120)}.0"
        )
        page = await context.new_page()

        await page.goto(url)
        await asyncio.sleep(5)  # Wait for page and JS to load

        ad_container = await page.query_selector("#container-ce15f5ed07b67d44812c9ae8563a04e3")
        if ad_container:
            box = await ad_container.bounding_box()
            if box and box["width"] > 10 and box["height"] > 10:
                x = box["x"] + random.randint(5, int(box["width"] - 5))
                y = box["y"] + random.randint(5, int(box["height"] - 5))
                await page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.5, 1.5))
                await page.mouse.click(x, y)
                print(f"[{unique_id}] ✅ Clicked inside ad container at ({x:.1f}, {y:.1f})")
            else:
                print(f"[{unique_id}] ❌ Ad container too small or invalid bounding box")
        else:
            print(f"[{unique_id}] ❌ Ad container not found")

        await asyncio.sleep(random.uniform(2, 4))
        await browser.close()

async def main():
    url = input("🔗 Enter the URL to simulate click on: ").strip()
    count = input("🔁 How many simulations to run? ").strip()

    try:
        simulations = int(count)
    except ValueError:
        print("❌ Invalid number. Exiting.")
        return

    for i in range(1, simulations + 1):
        print(f"\n🔄 Running simulation {i}/{simulations}")
        await simulate_valid_click(url, i)

asyncio.run(main())
