import http from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';

const root = path.resolve('dist');
const port = Number(process.env.PORT || 4187);
const mime = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.webp': 'image/webp', '.woff2': 'font/woff2', '.txt': 'text/plain; charset=utf-8', '.xml': 'application/xml; charset=utf-8' };

// Local preview only. Cloud hosting serves the checked-in dist directory.
http.createServer(async (req, res) => {
  if (!['GET', 'HEAD'].includes(req.method)) {
    res.writeHead(405, { Allow: 'GET, HEAD' }).end();
    return;
  }
  let pathname;
  let query;
  try {
    const url = new URL(req.url, 'http://localhost');
    pathname = decodeURIComponent(url.pathname);
    query = url.searchParams;
  }
  catch { res.writeHead(400).end('Invalid URL'); return; }
  const file = path.resolve(root, `.${pathname === '/' ? '/index.html' : pathname}`);
  if (!file.startsWith(root + path.sep)) { res.writeHead(403).end('Forbidden'); return; }
  // Local QA fixtures keep the shipped files untouched.
  if (pathname === '/__qa__/text-200.css') {
    res.writeHead(200, { 'Content-Type': mime['.css'] }).end('html{font-size:200%}');
    return;
  }
  try {
    let data = await readFile(file);
    if (path.extname(file) === '.html' && query.get('qa') === 'text200') {
      data = Buffer.from(data.toString().replace('</head>', '<link rel="stylesheet" href="/__qa__/text-200.css"></head>'));
    }
    if (path.extname(file) === '.html' && query.get('qa') === 'nojs') {
      data = Buffer.from(data.toString().replace('<script src="site.js" defer></script>', ''));
    }
    res.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'application/octet-stream', 'X-Content-Type-Options': 'nosniff', 'Cache-Control': 'no-store' });
    res.end(req.method === 'HEAD' ? undefined : data);
  } catch {
    const data = await readFile(path.join(root, '404.html'));
    res.writeHead(404, { 'Content-Type': mime['.html'] });
    res.end(req.method === 'HEAD' ? undefined : data);
  }
}).listen(port, '127.0.0.1', () => console.log(`Local URL: http://127.0.0.1:${port}/`));
