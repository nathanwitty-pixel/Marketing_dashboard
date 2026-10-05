/***** Marketing Posting — rewrites the IMPORTRANGE formulas in marketing_posting_monthly and
 * weekly_marketing_posting (spreadsheet 1DYkR0P4…) so each sums only the days of its period.
 * The dashboard reads them through MONTHLY_MARKETING_POST / WEEKLY_MARKETING_POST, so the
 * periods here must match the dashboard's:
 *   Monthly   = today's month, 1st → today         (dashboard "Monthly")
 *   Last week = the last COMPLETE Sun–Sat week     (dashboard "Last week", e.g. 27 Sep – 3 Oct,
 *               all 7 days, even when it straddles two months)
 *****/

/***** SETTINGS *****/
const MP = {
  MONTHLY_SHEET: 'marketing_posting_monthly',
  WEEKLY_SHEET: 'weekly_marketing_posting',
  FORMULA_RANGE: 'E3:J3',   // cells holding the IMPORTRANGE formulas (empty cells are skipped)
  DATE_ROW: 2,              // row in the SOURCE sheet with the dates
  DATE_ROW_FALLBACK: 6,     // if row 2 has no dates, look in rows 1..6
  WEEK_END_DAY: 6,          // 6 = Saturday (weeks run Sunday -> Saturday)
  WEEK: 'last',             // 'last' = last COMPLETE week (on Sat 10 Oct -> 27 Sep - 3 Oct)
                            // 'this' = week ending this coming Saturday
  WEEK_IN_MONTH_ONLY: false,// false = all 7 days of the week (matches the dashboard)
                            // true  = only the week's days inside its month (old behaviour)
  MONTH: 'today'            // 'today' = this calendar month (matches the dashboard)
                            // 'week'  = the month of the week's Saturday (old behaviour)
};

// A formula this script already rewrote
const MP_WRAPPED_RE = /ARRAYFORMULA\(MMULT\(IFERROR\(VALUE\((IMPORTRANGE\([^)]*\))\),0\),\{[^}]*\}\)\)/i;
// IMPORTRANGE("url","Sheet!A3:B1446") — the end row may be left open ("Sheet!A3:B")
const MP_IMPORT_RE = /IMPORTRANGE\(\s*"([^"]+)"\s*,\s*"(.+?)!\$?([A-Z]+)\$?(\d+):\$?([A-Z]+)\$?(\d*)"\s*\)/i;

const MP_MONTHS = { jan:1, feb:2, mar:3, apr:4, may:5, jun:6, jul:7, aug:8, sep:9, oct:10, nov:11, dec:12 };

/***** MENU *****/
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Marketing Posting')
    .addItem('Update monthly + weekly formulas', 'mpUpdateAll')
    .addItem('Check dates (no changes)', 'mpDebugDates')
    .addSeparator()
    .addItem('Install daily auto-update', 'mpInstallTrigger')
    .addToUi();
}

/***** MAIN *****/
function mpUpdateAll() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const w = mpGetWeek_(ss.getSpreadsheetTimeZone());
  const cache = {};
  const log = ['Week: ' + w.start + ' to ' + w.end + '   |   Month: ' + w.month + ' (to ' + w.today + ')', ''];
  const problems = [];

  // Monthly: every day of the month up to today (TOTAL columns skipped)
  log.push('--- ' + MP.MONTHLY_SHEET + ' ---');
  mpUpdateSheet_(ss, MP.MONTHLY_SHEET, w,
    key => key.slice(0, 7) === w.month && key <= w.today, cache, log, problems);

  // Weekly: the whole Sun-Sat week (or only its in-month days if WEEK_IN_MONTH_ONLY)
  log.push('', '--- ' + MP.WEEKLY_SHEET + ' ---');
  mpUpdateSheet_(ss, MP.WEEKLY_SHEET, w,
    key => key >= w.start && key <= w.end && (!MP.WEEK_IN_MONTH_ONLY || key.slice(0, 7) === w.end.slice(0, 7)),
    cache, log, problems);

  if (problems.length) log.unshift('!! ' + problems.length + ' cell(s) NOT updated (still show old numbers): ' +
                                   problems.join(', '), '');
  mpShow_(log);
}

function mpUpdateSheet_(ss, sheetName, w, keepDay, cache, log, problems) {
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) { log.push('sheet not found'); problems.push(sheetName); return; }

  const range = sheet.getRange(MP.FORMULA_RANGE);
  const formulas = range.getFormulas()[0];
  const header = sheet.getRange(1, range.getColumn(), 1, formulas.length).getDisplayValues()[0];

  formulas.forEach((formula, i) => {
    if (!formula) return;
    const cell = range.getCell(1, i + 1);
    const where = cell.getA1Notation() + (header[i] ? ' "' + header[i] + '"' : '');
    const fail = msg => { log.push('!! ' + where + ': ' + msg); problems.push(sheetName + '!' + cell.getA1Notation()); };

    // Find the part to replace (our earlier version, or the original IMPORTRANGE)
    let whole, importCall;
    const wrapped = formula.match(MP_WRAPPED_RE);
    if (wrapped) { whole = wrapped[0]; importCall = wrapped[1]; }
    else {
      const plain = formula.match(MP_IMPORT_RE);
      if (!plain) { fail('no IMPORTRANGE("url","Sheet!A3:B…") found - skipped'); return; }
      whole = importCall = plain[0];
    }

    const m = importCall.match(MP_IMPORT_RE);
    if (!m) { fail('could not read the range - skipped'); return; }
    const url = m[1], sheetPart = m[2], startRow = m[4], endRow = m[6];   // endRow '' = open-ended
    const srcSheet = sheetPart.replace(/^'(.*)'$/, '$1');

    try {
      const key = url + '|' + srcSheet;
      if (!cache[key]) cache[key] = mpReadDateColumns_(url, srcSheet, w);
      const src = cache[key];
      const days = src.dates.filter(d => keepDay(d.key));
      if (!days.length) { fail('[' + src.name + '] SKIPPED - ' + mpWhyNoDates_(src)); return; }

      const first = days[0].col, last = days[days.length - 1].col;
      const keep = {};
      days.forEach(d => keep[d.col] = true);
      const mask = [];
      for (let c = first; c <= last; c++) mask.push(keep[c] ? 1 : 0);

      const rangeA1 = mpColLetter_(first) + startRow + ':' + mpColLetter_(last) + endRow;
      const newExpr = 'ARRAYFORMULA(MMULT(IFERROR(VALUE(IMPORTRANGE("' + url + '","' +
                      sheetPart + '!' + rangeA1 + '")),0),{' + mask.join(';') + '}))';
      // Always the same shape as the Sinza / Uganda cells: one number per product row. (A SUM(…)
      // around it — as weekly E3 had — collapses the column to a single cell, so Kenya read 0.)
      const newFormula = '=ARRAYFORMULA(N(' + newExpr + '))';

      if (newFormula !== formula) cell.setFormula(newFormula);
      const want = mpDaysBetween_(keepDay, w);
      log.push(where + ' [' + src.name + ']: ' + rangeA1 + '  (' + days.length + ' days: ' +
               days[0].key + ' to ' + days[days.length - 1].key + ')' +
               (days.length < want ? '  * only ' + days.length + ' of ' + want + ' days have a column in the source' : '') +
               (src.row !== MP.DATE_ROW ? '  * dates found in row ' + src.row : ''));
    } catch (e) {
      fail('ERROR - ' + e.message);
    }
  });
}

// How many calendar days the period should have (to flag missing source columns)
function mpDaysBetween_(keepDay, w) {
  let n = 0;
  for (let k = mpAddDays_(w.start, -40); k <= w.today; k = mpAddDays_(k, 1)) if (keepDay(k)) n++;
  return n;
}

function mpWhyNoDates_(src) {
  if (!src.dates.length) return 'no dates found in rows 1-' + MP.DATE_ROW_FALLBACK +
                                ' of "' + src.sheet + '" (row 2 starts: ' + src.sample + ')';
  return 'dates found only from ' + src.dates[0].key + ' to ' +
         src.dates[src.dates.length - 1].key + ' (none in this week/month)';
}

/***** DATE CHECK (no changes made) *****/
function mpDebugDates() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const w = mpGetWeek_(ss.getSpreadsheetTimeZone());
  const out = ['Week: ' + w.start + ' to ' + w.end + '   |   Month: ' + w.month + ' (to ' + w.today + ')', ''];
  const seen = {};

  [MP.MONTHLY_SHEET, MP.WEEKLY_SHEET].forEach(sheetName => {
    const sheet = ss.getSheetByName(sheetName);
    if (!sheet) { out.push(sheetName + ': sheet not found'); return; }
    const range = sheet.getRange(MP.FORMULA_RANGE);
    range.getFormulas()[0].forEach((f, i) => {
      if (!f) return;
      const where = sheetName + '!' + range.getCell(1, i + 1).getA1Notation();
      const m = f.match(MP_IMPORT_RE);
      if (!m) { out.push('!! ' + where + ': no IMPORTRANGE found - formula starts: ' + f.slice(0, 80)); return; }
      const srcSheet = m[2].replace(/^'(.*)'$/, '$1');
      const key = m[1] + '|' + srcSheet;
      if (seen[key]) { out.push(where + ': same source as above'); return; }
      seen[key] = true;
      try {
        const src = mpReadDateColumns_(m[1], srcSheet, w);
        const near = src.dates.filter(d =>
          d.key >= mpAddDays_(w.start, -3) && d.key <= mpAddDays_(w.today, 1));
        out.push(where + ' [' + src.name + ' / ' + srcSheet + ', row ' + src.row + ']: ' +
          (near.length ? near.map(d => mpColLetter_(d.col) + '=' + d.key).join(', ')
                       : '!! NO dates near this week - ' + mpWhyNoDates_(src)));
      } catch (e) {
        out.push('!! ' + where + ': ERROR - ' + e.message);
      }
    });
  });

  mpShow_(out);
}

/***** HELPERS *****/

// Opens a spreadsheet from any IMPORTRANGE link format (full URL, URL without /edit, or just the ID)
function mpOpen_(url) {
  const m = url.match(/\/d\/([a-zA-Z0-9_-]+)/);
  return SpreadsheetApp.openById(m ? m[1] : url.trim());
}

// Finds the date row (row 2, else rows 1..6) and returns every column that holds a date
function mpReadDateColumns_(url, sheetName, w) {
  const file = mpOpen_(url);
  const sh = file.getSheetByName(sheetName);
  if (!sh) throw new Error('Sheet "' + sheetName + '" not found in ' + file.getName());
  const tz = file.getSpreadsheetTimeZone();
  const nRows = Math.min(MP.DATE_ROW_FALLBACK, sh.getLastRow());
  const block = sh.getRange(1, 1, nRows, sh.getLastColumn()).getValues();
  const year = Number(w.today.slice(0, 4));

  const parseRow = r => {
    const dates = [];
    block[r - 1].forEach((v, i) => {
      const key = mpToDateKey_(v, tz, year, w.today);
      if (key) dates.push({ col: i + 1, key: key });
    });
    return dates;
  };

  let row = MP.DATE_ROW;
  let dates = nRows >= row ? parseRow(row) : [];
  if (dates.length < 7) {                       // row 2 has no real dates -> try rows 1..6
    for (let r = 1; r <= nRows; r++) {
      if (r === MP.DATE_ROW) continue;
      const d = parseRow(r);
      if (d.length > dates.length) { dates = d; row = r; }
    }
  }

  const sample = (block[MP.DATE_ROW - 1] || []).filter(v => v !== '').slice(0, 4)
                   .map(v => JSON.stringify(v)).join(', ');
  return { name: file.getName(), sheet: sheetName, tz: tz, row: row, dates: dates, sample: sample };
}

// Turns a cell value into 'yyyy-MM-dd', or null if it is not a date. A date written without a
// year takes the year that puts it nearest today (so "30 Dec" read on 2 Jan is last year).
function mpToDateKey_(v, tz, year, today) {
  if (v instanceof Date && !isNaN(v)) return Utilities.formatDate(v, tz, 'yyyy-MM-dd');
  if (typeof v === 'number' && v > 40000 && v < 60000) {        // date stored as a plain number
    return Utilities.formatDate(new Date(Math.round((v - 25569) * 86400000)), 'UTC', 'yyyy-MM-dd');
  }
  if (typeof v !== 'string') return null;
  const s = v.trim();
  if (!s || /total/i.test(s)) return null;

  const pad = n => ('0' + n).slice(-2);
  const ok = (y, mo, d) => (mo >= 1 && mo <= 12 && d >= 1 && d <= 31) ? y + '-' + pad(mo) + '-' + pad(d) : null;
  const noYear = (mo, d) => {                                   // nearest year to today
    let best = null;
    [year - 1, year, year + 1].forEach(y => {
      const k = ok(y, mo, d);
      if (k && (!best || Math.abs(mpDiff_(k, today)) < Math.abs(mpDiff_(best, today)))) best = k;
    });
    return best;
  };
  let m;

  if ((m = s.match(/^(\d{4})[\/\-.](\d{1,2})[\/\-.](\d{1,2})/)))            // 2026-10-01
    return ok(m[1], +m[2], +m[3]);
  if ((m = s.match(/^(\d{1,2})[\/\-.](\d{1,2})[\/\-.](\d{2,4})/)))          // 01/10/2026 (day first)
    return ok(m[3].length === 2 ? '20' + m[3] : m[3], +m[2], +m[1]);
  if ((m = s.match(/^(\d{1,2})[\/\-.](\d{1,2})$/)))                         // 01/10 (day first, no year)
    return noYear(+m[2], +m[1]);

  const y4 = s.match(/\b(20\d{2})\b/);
  if ((m = s.match(/(\d{1,2})(?:st|nd|rd|th)?[\s\-\/]*([A-Za-z]{3,})/))) {  // 1 Oct, Thu 01-Oct
    const mo = MP_MONTHS[m[2].slice(0, 3).toLowerCase()];
    if (mo) return y4 ? ok(y4[1], mo, +m[1]) : noYear(mo, +m[1]);
  }
  if ((m = s.match(/([A-Za-z]{3,})[\s\-\/]*(\d{1,2})\b/))) {                 // Oct 1, October 01
    const mo = MP_MONTHS[m[1].slice(0, 3).toLowerCase()];
    if (mo) return y4 ? ok(y4[1], mo, +m[2]) : noYear(mo, +m[2]);
  }
  return null;
}

// The week (Sunday-Saturday), this month and today
function mpGetWeek_(tz) {
  const now = new Date();
  const today = Utilities.formatDate(now, tz, 'yyyy-MM-dd');
  const dow = Number(Utilities.formatDate(now, tz, 'u'));         // 1=Mon ... 7=Sun
  const shift = MP.WEEK === 'this'
    ? (MP.WEEK_END_DAY - dow + 7) % 7                             // forward to coming Saturday
    : -(((dow - MP.WEEK_END_DAY + 6) % 7) + 1);                   // back to the last COMPLETE Saturday
                                                                  // (on a Saturday: a week ago)
  const end = mpAddDays_(today, shift);
  return { start: mpAddDays_(end, -6), end: end, today: today,
           month: MP.MONTH === 'week' ? end.slice(0, 7) : today.slice(0, 7) };
}

function mpAddDays_(key, n) {
  const d = new Date(key + 'T12:00:00Z');
  d.setUTCDate(d.getUTCDate() + n);
  return Utilities.formatDate(d, 'UTC', 'yyyy-MM-dd');
}

function mpDiff_(a, b) {
  return (new Date(a + 'T12:00:00Z') - new Date(b + 'T12:00:00Z')) / 86400000;
}

function mpColLetter_(col) {
  let s = '';
  while (col > 0) {
    const r = (col - 1) % 26;
    s = String.fromCharCode(65 + r) + s;
    col = Math.floor((col - 1) / 26);
  }
  return s;
}

function mpShow_(lines) {
  Logger.log(lines.join('\n'));
  try { SpreadsheetApp.getUi().alert(lines.join('\n')); } catch (e) { /* trigger run */ }
}

/***** DAILY TRIGGER *****/
function mpInstallTrigger() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'mpUpdateAll')
    .forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('mpUpdateAll').timeBased().everyDays(1).atHour(1).create();
  mpShow_(['Auto-update installed: every day ~1am.']);
}
