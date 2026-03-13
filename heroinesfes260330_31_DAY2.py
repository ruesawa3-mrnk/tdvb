from playwright.sync_api import sync_playwright
import time
from datetime import datetime, timedelta

user_data_dir = r"C:\Default"

ticket_name = "heroinesfes260330_31_DAY1" #ログ表示名
ticket_site = "https://ticketdive.com/event/heroinesfes260330_31" #チケットサイトURL
ticket_btn_bunki = "" #公演チケ選択分岐(選択するボタン有り)用(ツアーなど)
ticket_bunki = "" #公演チケ選択分岐用(ツアーなど)
ticket_tuika = "" #チケ分類分岐用(追加公演など)
ticket_option = "前方エリア" #チケ種類(コピペ推奨)
ticket_quantity = "1" #チケ枚数
ticket_omeate = "T" #お目当て有無
shiharai = 'c' #c=カード、k=コンビニ
cvc_num = "979" #カードの場合のセキュリティコード

RELOAD_TIME = "22:29:59"  # チケ発1秒前

def wait_until_reload_time(time_str,plus_second):
    now = datetime.now()

    try:
        target_time = datetime.strptime(time_str, "%H:%M:%S").replace(
            year=now.year, month=now.month, day=now.day
        )
    except ValueError:
        raise ValueError("RELOAD_TIME は 'HH:MM:SS' 形式で指定してください。")

    if plus_second==0:
        if target_time <= now:
            target_time += timedelta(days=1)

        wait_seconds = (target_time - now).total_seconds()
        print(f"{time_str} まで {int(wait_seconds)} 秒待機します。")
        time.sleep(wait_seconds)
    else:
        target_time_plus = target_time + timedelta(seconds=plus_second)
        if target_time_plus > now:
            comp_wait_seconds = (target_time_plus - now).total_seconds()
            print(f"{int(comp_wait_seconds)} 秒待機します。")
            time.sleep(comp_wait_seconds)

def main():
    with sync_playwright() as p:

        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,  # 既存のログイン済みデータを使用
            headless=False,               # ブラウザを表示する
        )
        
        page = browser.pages[0]
        
        page.goto(ticket_site)
        
        if RELOAD_TIME != "":
            wait_until_reload_time(RELOAD_TIME,0)
            page.wait_for_timeout(300)
            page.reload()

        

        if ticket_btn_bunki != "":
            page.locator("div.Card_card__aQ73q", has_text=ticket_btn_bunki).locator("button:has-text('選択する')").click()

        if ticket_bunki != "":
            page.locator("div.Card_card__aQ73q", has_text=ticket_bunki).click()

        if ticket_tuika != "":
            additional_sale_card = page.locator(
                "div.Card_card__aQ73q",
                has=page.locator(f"span:has-text('{ticket_tuika}')")
            ).first
            
            ticket_container = additional_sale_card.locator(
                "span",
                has_text=ticket_option
            ).locator(
                "xpath=ancestor::div[contains(@class,'TicketTypeCard_ticketTypeContainer')]"
            )

            select_box = ticket_container.locator(
                "select.TicketTypeCard_numberSelector__UcNLO"
            )
            
            select_box.scroll_into_view_if_needed()
            select_box.hover()
            select_box.click(force=True)

            for _ in range(int(ticket_quantity)):
                page.keyboard.press("ArrowDown")

            page.keyboard.press("Enter")
            
            apply_button = additional_sale_card.locator("button.Button_xl__GlZ43:has-text('申し込みをする')")
            #page.wait_for_function("""btn => !btn.disabled""",apply_button,timeout=5000)
            page.wait_for_selector("div.PhoneVerificationNavigator_container__59q_4", state="detached")
            
            apply_button.scroll_into_view_if_needed()
            apply_button.hover()
            apply_button.click()
            
        elif ticket_tuika == "":
            select_box = page.locator(
            "text="+ticket_option
            ).locator(
                "xpath=ancestor::div[contains(@class,'TicketTypeCard_ticketTypeContainer')]"
            ).locator(
                "select.TicketTypeCard_numberSelector__UcNLO"
            )
            select_box.scroll_into_view_if_needed()
            select_box.hover()
            page.wait_for_timeout(500)
            select_box.click()

            for _ in range(int(ticket_quantity)):
                page.keyboard.press("ArrowDown")

            page.keyboard.press("Enter")
            
            apply_button = page.locator("button.Button_xl__GlZ43:has-text('申し込みをする')")
            #page.wait_for_function("""btn => !btn.disabled""",apply_button,timeout=5000)
            page.wait_for_selector("div.PhoneVerificationNavigator_container__59q_4", state="detached")
            
            apply_button.scroll_into_view_if_needed()
            apply_button.hover()
            apply_button.click()
        
        if ticket_omeate != '':
            page.wait_for_selector('select.Select_select__Wa03B')
            # page.locator('select.Select_select__Wa03B').click()
            # page.select_option('select.Select_select__Wa03B', value=ticket_omeate)

            select_box = page.locator("select.Select_select__Wa03B")
            select_box.scroll_into_view_if_needed()
            select_box.hover()
            select_box.click(force=True)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")
            
        if shiharai == 'k':
            page.locator("text=コンビニ決済（前払い）").wait_for()
            page.locator("text=コンビニ決済（前払い）").hover()
            page.locator("text=コンビニ決済（前払い）").click()
            page.fill('input[placeholder="姓"]', '山田')
            page.fill('input[placeholder="名"]', '太郎')
            page.fill('input[name="phoneNumber"]', '09012345679')
        else:
            page.frame_locator('div#card-cvc iframe').locator('input').wait_for()
            frame = page.frame_locator('div#card-cvc iframe')
            frame.locator('input').wait_for()
            frame.locator('input').click()
            frame.locator('input').fill(f"{cvc_num}")
            frame.locator('input').click()

        #wait_until_reload_time(RELOAD_TIME,5)
        page.locator('button.Button_xl__GlZ43').scroll_into_view_if_needed()
        page.locator('button.Button_xl__GlZ43').hover()
        page.locator('button.Button_xl__GlZ43').click()
        # page.wait_for_timeout(3000)
        # page.click('button.Button_xl__GlZ43')
        
        # 現在時刻を取得（例：23:59:59'123）
        click_time = datetime.now().strftime("%H:%M:%S'%f")[:-3]  # ミリ秒まで表示

        # ログファイルに追記
        with open("ticket_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{ticket_name}の申込クリック時刻: {click_time}\n")
        
        
        # 結果画面が見たい場合の一時停止
        page.wait_for_timeout(300000)

        browser.close()


if __name__ == "__main__":
    main()