import crypto from 'node:crypto';

const SOURCE_URL = 'https://raw.githubusercontent.com/hieu-TQS/ENC/main/playlist.enc';

export default async function handler(req, res) {
  try {
    const token = process.env.SUPEROK_TOKEN;
    if (!token) {
      res.status(500).send('Missing server configuration');
      return;
    }

    const upstreamUrl = new URL(SOURCE_URL);
    upstreamUrl.searchParams.set('_nm7_reload', Date.now().toString());

    const upstream = await fetch(upstreamUrl, {
      cache: 'no-store',
      headers: {
        'Cache-Control': 'no-cache, no-store, max-age=0',
        'Pragma': 'no-cache',
        'User-Agent': 'SuperOK-Live-Playlist/1.0'
      }
    });
    if (!upstream.ok) throw new Error(`Upstream HTTP ${upstream.status}`);

    const encodedText = (await upstream.text()).trim();
    const payload = Buffer.from(encodedText, 'base64');
    if (payload.length <= 16) throw new Error('Encrypted payload too short');

    const iv = payload.subarray(0, 16);
    const ciphertext = payload.subarray(16);
    const key = crypto.createHash('sha256').update(token, 'utf8').digest();
    const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
    const plaintext = Buffer.concat([decipher.update(ciphertext), decipher.final()]).toString('utf8');
    if (!plaintext.includes('#EXTM3U')) throw new Error('Decrypted content is not M3U');

    res.setHeader('Content-Type', 'application/vnd.apple.mpegurl; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0, s-maxage=0');
    res.setHeader('CDN-Cache-Control', 'no-store');
    res.setHeader('Vercel-CDN-Cache-Control', 'no-store');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    res.setHeader('X-SuperOK-Source-Fetched-At', new Date().toISOString());
    res.status(200).send(plaintext);
  } catch (err) {
    console.error(err);
    res.setHeader('Cache-Control', 'no-store');
    res.status(502).send('Unable to refresh playlist');
  }
}
