// Vercel serverless function — /api/refresh
//
// The dashboard's Refresh button calls this. It kicks off the GitHub Actions
// workflow that regenerates the pages from live Odoo + Sheets (which a static
// host can't do itself). If a ?dashboard=<file> is passed, only that page's
// generators run (fast); otherwise every page is rebuilt.
//
// Vercel env vars (Project → Settings → Environment Variables):
//   GH_DISPATCH_TOKEN  fine-grained PAT for THIS repo with "Actions: Read and write"
//                      (or a classic PAT with the `workflow` scope)
//   GH_REPO            "owner/repo"  e.g. "nathanwitty-pixel/marketing-dashboard"
//   GH_WORKFLOW        optional, defaults to "refresh-dashboard.yml"
//   GH_REF             optional, defaults to "main"
//
// The GitHub token lives ONLY here (server-side) — never in the page.

export default async function handler(req, res) {
  if (req.method !== 'GET' && req.method !== 'POST') {
    return res.status(405).json({ ok: false, error: 'Method not allowed' });
  }

  const token = process.env.GH_DISPATCH_TOKEN;
  const repo  = process.env.GH_REPO;
  const wf    = process.env.GH_WORKFLOW || 'refresh-dashboard.yml';
  const ref   = process.env.GH_REF || 'main';
  if (!token || !repo) {
    return res.status(500).json({
      ok: false,
      error: 'Server not configured — set GH_DISPATCH_TOKEN and GH_REPO in Vercel.',
    });
  }

  // Which page was the user on? (from ?dashboard= or a JSON body)
  let dashboard = '';
  try {
    if (req.query && req.query.dashboard) dashboard = String(req.query.dashboard);
    else if (req.body && req.body.dashboard) dashboard = String(req.body.dashboard);
  } catch (_) { /* ignore */ }
  dashboard = dashboard.split('?')[0].trim();          // strip any cache-buster
  const singlePage = !!dashboard;

  try {
    const gh = await fetch(
      `https://api.github.com/repos/${repo}/actions/workflows/${encodeURIComponent(wf)}/dispatches`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: 'application/vnd.github+json',
          'X-GitHub-Api-Version': '2022-11-28',
          'User-Agent': 'denri-dashboard-refresh',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ref, inputs: { dashboard } }),
      }
    );

    if (gh.status === 204) {
      return res.status(200).json({
        ok: true,
        dispatched: true,
        page: dashboard || 'all',
        // rough time until the run + Vercel redeploy make new data live
        etaSeconds: singlePage ? 210 : 480,
        message: singlePage
          ? 'Refreshing this page from Odoo…'
          : 'Refreshing every dashboard from Odoo…',
      });
    }
    const txt = await gh.text();
    return res.status(502).json({ ok: false, error: `GitHub API ${gh.status}: ${txt.slice(0, 200)}` });
  } catch (e) {
    return res.status(500).json({ ok: false, error: String(e) });
  }
}
