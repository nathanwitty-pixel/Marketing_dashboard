/**
 * sheet_trigger.gs — paste this into the dashboard spreadsheet's Apps Script
 * editor (Extensions → Apps Script). It pings GitHub whenever the sheet's data
 * changes, which runs the "Refresh dashboard" workflow → Vercel redeploys.
 *
 * ── ONE-TIME SETUP ────────────────────────────────────────────────────────
 * 1. GitHub → Settings → Developer settings → Fine-grained tokens →
 *    Generate new token:
 *      • Repository access: Only select repositories → Marketing_dashboard
 *      • Permissions → Repository → Contents: Read and write
 *      • Copy the token (starts with github_pat_…).
 * 2. In the Apps Script editor: Project Settings (gear) → Script properties →
 *    Add property:  name = GH_TOKEN   value = <the token>
 *    (Keeping it here, not in code, keeps the token out of the source.)
 * 3. Back in the editor, run once:  setup   (authorize when prompted).
 *    That installs a trigger that checks every 5 minutes and pings GitHub only
 *    when the sheet has actually changed since the last check.
 *
 * To ping GitHub immediately for a test, run:  notifyGitHub
 * ──────────────────────────────────────────────────────────────────────────
 */

var GITHUB_OWNER = 'nathanwitty-pixel';
var GITHUB_REPO  = 'Marketing_dashboard';
var EVENT_TYPE   = 'sheet-updated';

/** Installs the 5-minute change-check trigger (run this once). */
function setup() {
  // Clear any existing copies of our trigger so re-running doesn't stack them.
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'checkAndNotify') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('checkAndNotify').timeBased().everyMinutes(5).create();
  // Seed the baseline so the first check doesn't fire a needless run.
  PropertiesService.getScriptProperties()
    .setProperty('lastUpdated', String(currentUpdatedMs()));
  Logger.log('Trigger installed — checking every 5 minutes.');
}

/** The spreadsheet's last-modified time, in ms. */
function currentUpdatedMs() {
  var id = SpreadsheetApp.getActiveSpreadsheet().getId();
  return DriveApp.getFileById(id).getLastUpdated().getTime();
}

/** Runs on the timer: ping GitHub only if the sheet changed since last check. */
function checkAndNotify() {
  var props   = PropertiesService.getScriptProperties();
  var updated = currentUpdatedMs();
  var last    = Number(props.getProperty('lastUpdated') || 0);
  if (updated > last) {
    notifyGitHub();
    props.setProperty('lastUpdated', String(updated));
  }
}

/** Fires the repository_dispatch event that triggers the GitHub workflow. */
function notifyGitHub() {
  var token = PropertiesService.getScriptProperties().getProperty('GH_TOKEN');
  if (!token) throw new Error('Set the GH_TOKEN script property first (see setup notes).');
  var url = 'https://api.github.com/repos/' + GITHUB_OWNER + '/' + GITHUB_REPO + '/dispatches';
  var res = UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    headers: { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json' },
    payload: JSON.stringify({ event_type: EVENT_TYPE }),
    muteHttpExceptions: true
  });
  var code = res.getResponseCode();
  if (code !== 204) {
    throw new Error('GitHub dispatch failed (' + code + '): ' + res.getContentText());
  }
  Logger.log('GitHub notified — dashboard refresh triggered.');
}
