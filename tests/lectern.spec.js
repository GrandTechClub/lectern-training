const { test, expect } = require('@playwright/test');
const path = require('path');

const URL = 'file:///' + path.resolve(__dirname, '..', 'index.html').replace(/\\/g, '/');

const DEVICES_LIST  = ['lectern-pc', 'lectern-mac', 'mac', 'windows', 'iphone', 'android'];
const AUDIOS        = ['yes', 'no'];
const MICS          = ['lectern-mic', 'wireless', 'handfree', 'none'];
const SPECIAL_MODES = ['overview', 'shutdown'];

async function walkSteps(page) {
  let count = 0;
  while (count < 30) {
    if (await page.locator('#complete-banner').isVisible()) break;
    const done = page.locator('.nav-btn.done');
    if (await done.isVisible()) { await done.click(); break; }
    await page.locator('#next-btn').click();
    count++;
  }
  if (count >= 30) throw new Error('Possible infinite loop in steps');
}

// ── Special paths ─────────────────────────────────────────────────────────────
for (const mode of SPECIAL_MODES) {
  test(`${mode} path completes`, async ({ page }) => {
    await page.goto(URL);
    await page.click(`[data-q="mode"][data-v="${mode}"]`);
    await expect(page.locator('#show-steps-btn')).toBeEnabled();
    await page.click('#show-steps-btn');
    await expect(page.locator('.step-num-badge')).toBeVisible();
    await walkSteps(page);
    await expect(page.locator('#complete-banner')).toBeVisible();
    await expect(page.locator('#complete-banner')).not.toBeEmpty();
  });
}

// ── Setup paths ───────────────────────────────────────────────────────────────
for (const device of DEVICES_LIST) {
  for (const audio of AUDIOS) {
    for (const mic of MICS) {
      test(`setup: ${device} / audio=${audio} / mic=${mic}`, async ({ page }) => {
        await page.goto(URL);

        await page.click('[data-q="mode"][data-v="setup"]');
        await expect(page.locator('#q-device')).toBeVisible();

        await page.click(`[data-q="device"][data-v="${device}"]`);
        await expect(page.locator('[data-q="audio"]').filter({ visible: true }).first()).toBeVisible();

        await page.click(`[data-q="audio"][data-v="${audio}"]`);
        await expect(page.locator('[data-q="mic"]').filter({ visible: true }).first()).toBeVisible();

        await page.click(`[data-q="mic"][data-v="${mic}"]`);
        await expect(page.locator('#show-steps-btn')).toBeEnabled();

        await page.click('#show-steps-btn');
        await expect(page.locator('.step-num-badge')).toBeVisible();

        await walkSteps(page);
        await expect(page.locator('#complete-banner')).toBeVisible();
        await expect(page.locator('#complete-banner')).not.toBeEmpty();
      });
    }
  }
}
