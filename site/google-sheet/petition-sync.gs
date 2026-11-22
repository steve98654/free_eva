/**
 * Free Eva petition -> Google Sheet, refreshed daily.
 *
 * Setup (one time, about 3 minutes):
 *  1. Open the Google Sheet. Extensions > Apps Script. Delete what is there and paste this whole file.
 *  2. Project Settings (gear icon) > Script Properties > Add property:
 *       EXPORT_TOKEN = the same value you saved as the EXPORT_TOKEN secret on the Cloudflare Worker.
 *  3. Back in the editor, choose the function `setup` in the toolbar and click Run.
 *     Approve the permissions (it needs to edit this sheet and fetch evaxie.us).
 *  That writes the sheet now and schedules a refresh every day around 6 AM (sheet's time zone).
 *  Run `syncSignatures` any time for an immediate refresh.
 */

const EXPORT_URL = 'https://evaxie.us/api/petition/export';
const SHEET_NAME = 'Signers';
// Email and phone are included so the team can contact signers. Set to false to leave them out.
const INCLUDE_CONTACT = true;

function setup() {
  ScriptApp.getProjectTriggers()
    .filter((t) => t.getHandlerFunction() === 'syncSignatures')
    .forEach((t) => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('syncSignatures').timeBased().everyDays(1).atHour(6).create();
  syncSignatures();
}

function syncSignatures() {
  const token = PropertiesService.getScriptProperties().getProperty('EXPORT_TOKEN');
  if (!token) throw new Error('Add the EXPORT_TOKEN script property first (Project Settings > Script Properties).');

  const res = UrlFetchApp.fetch(EXPORT_URL, {
    headers: { Authorization: 'Bearer ' + token },
    muteHttpExceptions: true,
  });
  if (res.getResponseCode() !== 200) {
    throw new Error('Export failed: HTTP ' + res.getResponseCode() + ' ' + res.getContentText().slice(0, 200));
  }
  const data = JSON.parse(res.getContentText());

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME, 0);
  const tz = ss.getSpreadsheetTimeZone();

  const header = ['#', 'Name', 'Signed (date)', 'Signed (time)', 'Public?', 'City', 'State', 'ZIP',
    'Princeton connection', 'How they heard', 'Why I\'m signing', 'OK to contact?'];
  if (INCLUDE_CONTACT) header.splice(5, 0, 'Email', 'Phone');

  const rows = data.signers.map((s, i) => {
    const d = new Date(s.signedAt);
    const row = [
      i + 1,
      s.name,
      Utilities.formatDate(d, tz, 'yyyy-MM-dd'),
      Utilities.formatDate(d, tz, 'h:mm a'),
      s.public ? 'Yes' : 'No',
      s.city || '',
      s.state || '',
      s.zip || '',
      s.affiliation || '',
      s.heardFrom || '',
      s.comment || '',
      s.wantsUpdates ? 'Yes' : '',
    ];
    if (INCLUDE_CONTACT) row.splice(5, 0, s.email || '', s.phone || '');
    return row;
  });

  sheet.clearContents();
  sheet.getRange(1, 1, 1, header.length).setValues([header]).setFontWeight('bold');
  // Keep ZIP codes as text so leading zeros (08540) survive. Must be set before writing.
  const zipCol = header.indexOf('ZIP') + 1;
  sheet.getRange(2, zipCol, Math.max(rows.length, 1), 1).setNumberFormat('@');
  if (rows.length) sheet.getRange(2, 1, rows.length, header.length).setValues(rows);
  sheet.setFrozenRows(1);
  sheet.getRange(1, header.length + 2).setValue(
    'Last updated ' + Utilities.formatDate(new Date(), tz, 'yyyy-MM-dd h:mm a z') + ' · ' + rows.length + ' signers');
}
