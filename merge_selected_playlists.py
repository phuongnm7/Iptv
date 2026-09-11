#!/usr/bin/env python3
import re
import urllib.request
from urllib.parse import urljoin

SOURCES = [
    (
        "https://raw.githubusercontent.com/phuongnm7/Iptv/main/SuperOK_playlist.m3u",
        {
            "VTV", "VTVcab", "SCTV", "HTV", "Sự Kiện FPT PLAY", "Thiết yếu",
            "🇸🇬 Mediacorp", "🌟SPORTS VIP🌟"
        },
    ),
    (
        "https://raw.githubusercontent.com/vuminhthanh12/vuminhthanh12/refs/heads/main/vmttv",
        {"Sự Kiện TV360"},
    ),
    (
        "https://tinyurl.com/ttthethao2",
        {"Giờ Vàng TV", "Gà Vàng 33 TV", "Xôi Lạc Z TV", "Gà Vàng TV"},
    ),
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 IPTV-playlist-updater"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8-sig", errors="replace")


def group_of(extinf):
    m = re.search(r'group-title="([^"]*)"', extinf, flags=re.I)
    return m.group(1).strip() if m else ""


def entries(text):
    lines = text.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    current = []
    for line in lines:
        if line.startswith("#EXTINF:"):
            if current:
                yield current
            current = [line]
        elif current:
            current.append(line)
    if current:
        yield current


def main():
    selected = []
    seen = set()
    source_errors = []

    for url, groups in SOURCES:
        try:
            text = fetch(url)
            for entry in entries(text):
                g = group_of(entry[0])
                if g not in groups:
                    continue
                # De-duplicate identical stream entries while preserving order.
                stream = next((x.strip() for x in reversed(entry[1:]) if x.strip() and not x.startswith("#")), "")
                key = (g, stream, entry[0])
                if key in seen:
                    continue
                seen.add(key)
                selected.append(entry)
        except Exception as exc:
            source_errors.append(f"{url}: {exc}")

    if not selected:
        raise SystemExit("No matching channels were found. Sources: " + "; ".join(source_errors))

    out = [
        '#EXTM3U x-tvg-url=""',
        '#PLAYLIST: PhuongNM7 - Selected IPTV',
        '# This playlist is generated automatically from the configured source playlists.',
    ]
    for entry in selected:
        out.extend(entry)

    with open("Iptv_selected.m3u", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")

    print(f"Generated {len(selected)} channels.")
    if source_errors:
        print("WARNING: " + " | ".join(source_errors))


if __name__ == "__main__":
    main()
