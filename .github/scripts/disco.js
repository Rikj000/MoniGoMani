#!/usr/bin/env node

// Disco is like disco. 🥳 👯‍️
// Like, disable your brain and have fun!
//
// But what it does? Well, login to Discord and send a message.
// So, configure, lean back and prepare to go to the Disco.
//
// :: github.com/topscoder

//# Required libs
const core = require('@actions/core');
const puppeteer = require('puppeteer-extra');
const randomUseragent = require('random-useragent');
const StealthPlugin = require('puppeteer-extra-plugin-stealth')
puppeteer.use(StealthPlugin())


//# Some settings
const discord_channel_url = process.env.DISCORD_CHANNEL_URL
const discord_username = process.env.DISCORD_USERNAME
const discord_password = process.env.DISCORD_PASSWORD
const the_message = process.env.DISCORD_MESSAGE
const discord_textbox_selector = process.env.DISCORD_TEXTBOX_SELECTOR
// True if it should run in an invisible browser window. False to see all magic happen.
// Use only at local testing.
const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36';
const headless = true;
let failure = false;

console.log("[DISCO] Let's get this party started...")

//# Let's dance!
async function run() {

    // throw debug info to stdout
    dcu = discord_channel_url.substring(0,5)
    du = discord_username.substring(0,4)
    dp = discord_password.substring(0,4)
    dm = the_message.substring(0,5)
    dts = discord_textbox_selector.substring(0,5)

    console.log(`[DISCO] dcu: ${dcu}******`)
    console.log(`[DISCO] du: ${du}******`)
    console.log(`[DISCO] dp: ${dp}******`)
    console.log(`[DISCO] dm: ${dm}******`)
    console.log(`[DISCO] dts: ${dts}******`)
    //////////

    console.log("[DISCO] Navigating to https://discord.com/login")
    try {
        const browser = await puppeteer.launch({
            headless: headless
        });

        page = await createPage(browser, 'https://discord.com/login?')

        await shot_screen(page, '1-browser-started.png')

        // login
        console.log("[DISCO] Entering login information")

        await page.type('input[name=email]', discord_username);
        await page.type('input[name=password]', discord_password);

        await page.evaluate(() => {
            document.querySelector('button[type=submit]').click();
        });

        // wait for 3 seconds. We are not in a hurry
        await page.waitForTimeout(3000);
        await shot_screen(page, "1-click-submit.png")

        console.log("[DISCO] Checking if we are logged in")

        // check if login is successful
        if (page.url().includes('discord.com/login')) {
            await shot_screen(page, "2-failed-login.png")
            await browser.close();
            core.setFailed("[DISCO] Sorry, but failed to log in")
        }

        await shot_screen(page, "2-login-success.png")

        console.log("[DISCO] Navigating to the Discord channel")

        // enter target discord server/channel
        await page.goto(discord_channel_url, {
            waitUntil: 'networkidle2',
            timeout: 5000
        })

        // DO NOT CREATE ANY SCREENSHOTS FROM HERE TO
        // KEEP THE CHANNEL, MEMBERS AND MESSAGES PRIVATE.

        console.log("[DISCO] Enter message in Discord channel")
        await page.waitForTimeout(3000); // wait for 3 seconds
        await page.type(discord_textbox_selector, the_message)
        await page.waitForTimeout(2000); // wait for 2 seconds
        await (await page.$(discord_textbox_selector)).press('Enter');

        await page.waitForNavigation()

    } catch (error) {
        dumpStack(error)
        core.setFailed(`[DISCO] Failed to send message in Discord channel. ${error.message}`)
        failure = true
    }

    if (! failure )
        console.log("[DISCO] And we are done. Let's go to the disco! 👯 ")
        await page.waitForTimeout(3000); // wait for 3 seconds

    if (browser)
        await browser.close();
}

async function shot_screen(page, filename) {
    return await page.screenshot({ path: `screenshots/${filename}` })
}

dumpStack = function(err) {
    if (err.stack) {
      console.log('\nStacktrace:')
      console.log('====================')
      console.log(err.stack);
      console.log('====================\n')
    }
}

async function createPage(browser, url) {

    // Randomize User agent or Set a valid one
    const userAgent = randomUseragent.getRandom();
    const UA = userAgent || USER_AGENT;
    const page = await browser.newPage();

    // Randomize viewport size
    await page.setViewport({
        width: 1920 + Math.floor(Math.random() * 100),
        height: 3000 + Math.floor(Math.random() * 100),
        deviceScaleFactor: 1,
        hasTouch: false,
        isLandscape: false,
        isMobile: false,
    });

    await page.setUserAgent(UA);
    await page.setJavaScriptEnabled(true);
    await page.setDefaultNavigationTimeout(0);

    // Skip images/styles/fonts loading for performance
    await page.setRequestInterception(true);
    page.on('request', (req) => {
        if(req.resourceType() == 'stylesheet' || req.resourceType() == 'font' || req.resourceType() == 'image'){
            req.abort();
        } else {
            req.continue();
        }
    });

    await page.evaluateOnNewDocument(() => {
        // Pass webdriver check
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
        });
    });

    await page.evaluateOnNewDocument(() => {
        // Pass chrome check
        window.chrome = {
            runtime: {},
            // etc.
        };
    });

    await page.evaluateOnNewDocument(() => {
        // Pass notifications check
        const originalQuery = window.navigator.permissions.query;
        return window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
    });

    await page.evaluateOnNewDocument(() => {
        // Overwrite the `plugins` property to use a custom getter.
        Object.defineProperty(navigator, 'plugins', {
            // This just needs to have `length > 0` for the current test,
            // but we could mock the plugins too if necessary.
            get: () => [1, 2, 3, 4, 5],
        });
    });

    await page.evaluateOnNewDocument(() => {
        // Overwrite the `languages` property to use a custom getter.
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });
    });

    await page.goto(url, { waitUntil: 'networkidle2',timeout: 0 } );
    return page;
}

run()
