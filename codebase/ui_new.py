import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

async def wait_loaded(page):
    try:
        await page.wait_for_selector("[data-testid='stStatusWidget']", state="hidden", timeout=40000)
    except Exception:
        pass
    await asyncio.sleep(4)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-cache"])
        ctx = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await ctx.new_page()
        
        await page.goto("http://localhost:8502", wait_until="networkidle", timeout=45000)
        await wait_loaded(page)
        await page.screenshot(path="ui_new_p1.png")
        print("p1 saved")
        
        # Check CSS is loaded - look for animated gradient
        styles = await page.evaluate("() => { const el = document.querySelector('.main-header'); return el ? window.getComputedStyle(el).animation : 'not found'; }")
        print(f"Header animation CSS: {styles!r}")

        await page.evaluate("() => { const r = document.querySelectorAll('input[type=radio]'); if(r[1]) r[1].click(); }")
        await wait_loaded(page)
        await page.screenshot(path="ui_new_p2.png")
        print("p2 saved")
        
        await page.evaluate("() => { const r = document.querySelectorAll('input[type=radio]'); if(r[2]) r[2].click(); }")
        await wait_loaded(page)
        await page.screenshot(path="ui_new_p3.png")
        print("p3 saved")
        
        await browser.close()

asyncio.run(main())
