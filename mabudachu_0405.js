const { chromium } = require("playwright");
const fs = require("fs");

const user_data_dir = "C:\\Default";

const ticket_name = "mabudachu_0405";
const ticket_site = "https://ticketdive.com/event/mabudachu_0405";
const ticket_btn_bunki = "";
const ticket_bunki = "";
const ticket_tuika = "";
const ticket_option = "Vチケット";
const ticket_quantity = "1";
const ticket_omeate = "T";
const shiharai = "c";
const cvc_num = "979";

const RELOAD_TIME = "";

function sleep(ms) {
return new Promise(resolve => setTimeout(resolve, ms));
}

async function wait_until_reload_time(time_str, plus_second) {

const now = new Date();

const [h, m, s] = time_str.split(":").map(Number);
let target = new Date();
target.setHours(h, m, s, 0);

if (plus_second === 0) {

if (target <= now) {
target.setDate(target.getDate() + 1);
}

const wait = target - now;
console.log(`${time_str}まで ${Math.floor(wait/1000)} 秒待機します`);
await sleep(wait);

} else {

target.setSeconds(target.getSeconds() + plus_second);

if (target > now) {
const wait = target - now;
console.log(`${Math.floor(wait/1000)} 秒待機します`);
await sleep(wait);
}
}
}

(async () => {

const browser = await chromium.launchPersistentContext(
user_data_dir,
{ headless:false }
);

const page = browser.pages()[0];

await page.goto(ticket_site);

if (RELOAD_TIME !== "") {

await wait_until_reload_time(RELOAD_TIME,0);

await page.waitForTimeout(500);

await page.reload();
}

if (ticket_btn_bunki !== "") {

await page
.locator("div.Card_card__aQ73q", { hasText: ticket_btn_bunki })
.locator("button:has-text('選択する')")
.click();
}

if (ticket_bunki !== "") {

await page
.locator("div.Card_card__aQ73q", { hasText: ticket_bunki })
.click();
}

if (ticket_tuika !== "") {

const additional_sale_card = page.locator(
"div.Card_card__aQ73q",
{ has: page.locator(`span:has-text('${ticket_tuika}')`) }
).first();

const ticket_container = additional_sale_card
.locator("span", { hasText: ticket_option })
.locator("xpath=ancestor::div[contains(@class,'TicketTypeCard_ticketTypeContainer')]");

const select_box = ticket_container.locator(
"select.TicketTypeCard_numberSelector__UcNLO"
);

await select_box.scrollIntoViewIfNeeded();
await select_box.hover();
await select_box.click({force:true});

for(let i=0;i<parseInt(ticket_quantity);i++){
await page.keyboard.press("ArrowDown");
}

await page.keyboard.press("Enter");

const apply_button = additional_sale_card.locator(
"button.Button_xl__GlZ43:has-text('申し込みをする')"
);

await page.waitForSelector(
"div.PhoneVerificationNavigator_container__59q_4",
{ state:"detached" }
);

await apply_button.scrollIntoViewIfNeeded();
await apply_button.hover();
await apply_button.click();

} else {

const select_box = page
.locator(`text=${ticket_option}`)
.locator("xpath=ancestor::div[contains(@class,'TicketTypeCard_ticketTypeContainer')]")
.locator("select.TicketTypeCard_numberSelector__UcNLO");

await select_box.scrollIntoViewIfNeeded();
await select_box.hover();

await select_box.click();

for(let i=0;i<parseInt(ticket_quantity);i++){
await page.keyboard.press("ArrowDown");
}

await page.keyboard.press("Enter");

const apply_button = page.locator(
"button.Button_xl__GlZ43:has-text('申し込みをする')"
);

await page.waitForSelector(
"div.PhoneVerificationNavigator_container__59q_4",
{ state:"detached" }
);

await apply_button.scrollIntoViewIfNeeded();
await apply_button.hover();
await apply_button.click();
}

if(ticket_omeate !== ""){

const select_box = page.locator("select.Select_select__Wa03B");

await select_box.waitFor();

await select_box.scrollIntoViewIfNeeded();
await select_box.hover();
await select_box.click({force:true});

await page.keyboard.press("ArrowDown");
await page.keyboard.press("Enter");
}

if(shiharai === "k"){

await page.locator("text=コンビニ決済（前払い）").waitFor();
await page.locator("text=コンビニ決済（前払い）").click();

await page.fill('input[placeholder="姓"]','山田');
await page.fill('input[placeholder="名"]','太郎');
await page.fill('input[name="phoneNumber"]','09012345679');

}else{

const frame = page.frameLocator("div#card-cvc iframe");

await frame.locator("input").waitFor();
await frame.locator("input").click();
await frame.locator("input").fill(cvc_num);
}

const submit = page.locator("button.Button_xl__GlZ43");

await submit.scrollIntoViewIfNeeded();
await submit.hover();
await submit.click();

const now = new Date();
const click_time = now.toISOString();

fs.appendFileSync(
"ticket_log.txt",
`${ticket_name}の申込クリック時刻: ${click_time}\n`,
"utf8"
);

await page.waitForTimeout(300000);

await browser.close();

})();