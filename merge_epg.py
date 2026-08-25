#!/usr/bin/env python3
"""
JP_Merged_fixed.m3u 向けのEPG統合スクリプト
ベース: skinred78/jp-iptv-epg の統合済みXMLTV
補完  : animenosekai/japanterebi-xmltv から、ベースに無い分だけ追加
出力  : merged_guide.xml
"""
import urllib.request
import xml.etree.ElementTree as ET
import gzip

BASE_URL = "https://raw.githubusercontent.com/skinred78/jp-iptv-epg/dist/jp-epg-merged.xml"
SUPPLEMENT_URL = "https://raw.githubusercontent.com/animenosekai/japanterebi-xmltv/main/guide.xml"

# JP_Merged_fixed.m3u のtvg-idと突き合わせ済みの補完対象チャンネルID
SUPPLEMENT_CHANNEL_IDS = {
    "QVC.jp", "KidsStation.jp", "DiscoveryChannelSoutheastAsia.sg@Japan",
    "DisneyJunior.jp", "DisneyChannel.jp", "NitteleGPlus.jp", "WOWOWCinema.jp",
    "SkyA.jp", "KayoPops.jp", "FishingVision.jp", "BBCNews.uk@AsiaPacific",
    "ShopChannelPlus.jp",
}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data

def main():
    print(f"[1/3] ベース取得: {BASE_URL}")
    base_root = ET.fromstring(fetch(BASE_URL))

    print(f"[2/3] 補完取得: {SUPPLEMENT_URL}")
    supp_root = ET.fromstring(fetch(SUPPLEMENT_URL))

    added_ch = added_pr = 0
    for ch in supp_root.findall("channel"):
        if ch.get("id") in SUPPLEMENT_CHANNEL_IDS:
            base_root.append(ch); added_ch += 1
    for pr in supp_root.findall("programme"):
        if pr.get("channel") in SUPPLEMENT_CHANNEL_IDS:
            base_root.append(pr); added_pr += 1
    print(f"    追加 channel: {added_ch} / programme: {added_pr}")

    tree = ET.ElementTree(base_root)
    ET.indent(tree, space="  ")
    tree.write("merged_guide.xml", encoding="UTF-8", xml_declaration=True)
    print("[3/3] merged_guide.xml 出力完了")

if __name__ == "__main__":
    main()
