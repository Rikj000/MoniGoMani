#!/usr/bin/env node

// Disco is like disco. 🥳 👯‍️
// Like, disable your brain and have fun!
//
// But what it does? Well, login to Discord and send a message.
// So, configure, lean back and prepare to go to the Disco.
//
// :: github.com/topscoder

//# Required libs
const puppeteer = require('puppeteer-extra');
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
const headless = true;

console.info("[DISCO] Let's get this party started...")

//# Let's dance!
(async () => {

    // throw debug info to stdout
    console.info('[DISCO] dcu: ' + discord_channel_url.substring(0,5) + '******')
    console.info('[DISCO] du: ' + discord_channel_url.substring(0,4) + '******')
    console.info('[DISCO] dp: ' + discord_channel_url.substring(0,4) + '******')
    console.info('[DISCO] dm: ' + discord_channel_url.substring(0,5) + '******')
    console.info('[DISCO] dts: ' + discord_channel_url.substring(0,5) + '******')
    console.info('[DISCO] 🤯: ' + discord_channel_url.substring(0,5) + '******')
    //////////

    const browser = await puppeteer.launch({
        headless: headless
    });
    console.log('[DISCO] Navigating to https://discord.com/login')
    const page = await browser.newPage();
    await page.goto('https://discord.com/login', {
        waitUntil: 'networkidle2',
        timeout: 60
    })

    // login
    console.log('[DISCO] Entering login information')
    await page.type('input[name=email]', discord_username);
    await page.type('input[name=password]', discord_password);

    await page.evaluate(() => {
        document.querySelector('button[type=submit]').click();
    });

    // wait for 3 seconds. We are not in a hurry
    await page.waitForTimeout(3000);
    await page.screenshot({ path: "disco-runner/screenshots/1-click-submit.png" })

    console.log('[DISCO] Checking if we are logged in')

    // check if login is successful
    if (page.url().includes('discord.com/login')) {
        await page.screenshot({ path: "disco-runner/screenshots/2-failed-login.png" })
        await browser.close();
        console.error('[DISCO] Sorry, but failed to log in')
        process.exit(1)
    }

    await page.screenshot({ path: "disco-runner/screenshots/2-login-success.png" })

    // enter target discord server/channel
    console.log('[DISCO] Navigating to the Discord channel')
    await page.goto(discord_channel_url, {
        waitUntil: 'networkidle2',
        timeout: 60
    })

    // DO NOT CREATE ANY SCREENSHOTS FROM HERE TO
    // KEEP THE CHANNEL, MEMBERS AND MESSAGES PRIVATE.

    await page.waitForTimeout(5000); // wait for 5 seconds

    console.log('[DISCO] Enter message in Discord channel')
    await page.type(discord_textbox_selector, the_message)
    await page.waitForTimeout(2000); // wait for 2 seconds
    await (await page.$(discord_textbox_selector)).press('Enter');

    await page.waitForNavigation()

    console.log("[DISCO] And we are done. Let's go to the disco! 👯 ")

    // and let's dance! 👯‍
    await page.waitForTimeout(3000); // wait for 3 seconds
    await browser.close();

    process.exit(0)
  })();
