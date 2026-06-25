#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================
#   TRITON FINDER - by MR_TRITON
#   OSINT Username Finder Tool
#   Compatible: Kali Linux & Termux
# ================================================

import requests
import sys
import json
import os
import threading
from datetime import datetime

try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:
    os.system("pip install colorama -q")
    from colorama import Fore, Back, Style, init
    init(autoreset=True)

# ─── COULEURS ───────────────────────────────────
G  = Fore.GREEN
BG = Fore.LIGHTGREEN_EX
W  = Fore.WHITE
R  = Fore.RED
Y  = Fore.YELLOW
C  = Fore.CYAN
M  = Fore.MAGENTA
B  = Fore.LIGHTBLACK_EX
RS = Style.RESET_ALL
BD = Style.BRIGHT

# ─── BANNIÈRE ASCII ─────────────────────────────
def banner():
    os.system("clear" if os.name != "nt" else "cls")
    print(BD + G + r"""
    ███╗   ███╗██████╗      ████████╗██████╗ ██╗████████╗ ██████╗ ███╗   ██╗
    ████╗ ████║██╔══██╗     ╚══██╔══╝██╔══██╗██║╚══██╔══╝██╔═══██╗████╗  ██║
    ██╔████╔██║██████╔╝        ██║   ██████╔╝██║   ██║   ██║   ██║██╔██╗ ██║
    ██║╚██╔╝██║██╔══██╗        ██║   ██╔══██╗██║   ██║   ██║   ██║██║╚██╗██║
    ██║ ╚═╝ ██║██║  ██║        ██║   ██║  ██║██║   ██║   ╚██████╔╝██║ ╚████║
    ╚═╝     ╚═╝╚═╝  ╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝
    """ + RS)

    print(BG + BD + r"""
                    ≋≋≋  ╔╦╗╦═╗  ╔╦╗╦═╗╦╔╦╗╔═╗╔╗╔  ≋≋≋
                          ║║├╦╝   ║ ╠╦╝║ ║ ║ ║║║║
                         ═╩╝╩╚═   ╩ ╩╚═╩ ╩ ╚═╝╝╚╝
    """ + RS)

    print(G  + "    " + "─" * 70)
    print(BG + "    " + "⚡  TRITON FINDER  ⚡".center(68))
    print(W  + "    " + "Username OSINT Tool — by MR_TRITON".center(68))
    print(G  + "    " + "─" * 70)
    print(B  + f"    Version : 2.0  |  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(G  + "    " + "─" * 70 + RS)
    print()

# ─── LISTE COMPLÈTE DES SITES (100+) ────────────
SITES = {
    # ── Réseaux Sociaux Principaux ──
    "Facebook"        : "https://www.facebook.com/{}",
    "Instagram"       : "https://www.instagram.com/{}",
    "Twitter/X"       : "https://twitter.com/{}",
    "TikTok"          : "https://www.tiktok.com/@{}",
    "Snapchat"        : "https://www.snapchat.com/add/{}",
    "Pinterest"       : "https://www.pinterest.com/{}",
    "LinkedIn"        : "https://www.linkedin.com/in/{}",
    "Reddit"          : "https://www.reddit.com/user/{}",
    "Tumblr"          : "https://{}.tumblr.com",
    "Telegram"        : "https://t.me/{}",
    "WhatsApp"        : "https://wa.me/{}",
    "Skype"           : "https://www.skype.com/en/search/#people/{}",
    "VKontakte"       : "https://vk.com/{}",
    "MeWe"            : "https://mewe.com/i/{}",
    "Mastodon"        : "https://mastodon.social/@{}",
    "Minds"           : "https://www.minds.com/{}",
    "Parler"          : "https://parler.com/{}",
    "Gab"             : "https://gab.com/{}",
    "Clubhouse"       : "https://www.joinclubhouse.com/@{}",
    "BeReal"          : "https://bere.al/{}",
    "Threads"         : "https://www.threads.net/@{}",
    "Bluesky"         : "https://bsky.app/profile/{}",

    # ── Vidéo & Streaming ──
    "YouTube"         : "https://www.youtube.com/@{}",
    "Twitch"          : "https://www.twitch.tv/{}",
    "Vimeo"           : "https://vimeo.com/{}",
    "Dailymotion"     : "https://www.dailymotion.com/{}",
    "Periscope"       : "https://www.pscp.tv/{}",
    "Rumble"          : "https://rumble.com/c/{}",
    "Odysee"          : "https://odysee.com/@{}",
    "Kick"            : "https://kick.com/{}",
    "Trovo"           : "https://trovo.live/{}",
    "Bilibili"        : "https://space.bilibili.com/{}",

    # ── Musique ──
    "SoundCloud"      : "https://soundcloud.com/{}",
    "Spotify"         : "https://open.spotify.com/user/{}",
    "Last.fm"         : "https://www.last.fm/user/{}",
    "Bandcamp"        : "https://{}.bandcamp.com",
    "Audiomack"       : "https://audiomack.com/{}",
    "Mixcloud"        : "https://www.mixcloud.com/{}",
    "ReverbNation"    : "https://www.reverbnation.com/{}",

    # ── Gaming ──
    "Steam"           : "https://steamcommunity.com/id/{}",
    "Roblox"          : "https://www.roblox.com/user.aspx?username={}",
    "Chess"           : "https://www.chess.com/member/{}",
    "Minecraft"       : "https://namemc.com/profile/{}",
    "PSN"             : "https://psnprofiles.com/{}",
    "Xbox"            : "https://xboxgamertag.com/search/{}",
    "Fortnite"        : "https://fortnitetracker.com/profile/all/{}",
    "Valorant"        : "https://tracker.gg/valorant/profile/riot/{}/overview",
    "Leetcode"        : "https://leetcode.com/{}",
    "HackerRank"      : "https://www.hackerrank.com/{}",

    # ── Dev & Tech ──
    "GitHub"          : "https://github.com/{}",
    "GitLab"          : "https://gitlab.com/{}",
    "Replit"          : "https://replit.com/@{}",
    "Codecademy"      : "https://www.codecademy.com/profiles/{}",
    "HackerNews"      : "https://news.ycombinator.com/user?id={}",
    "ProductHunt"     : "https://www.producthunt.com/@{}",
    "Keybase"         : "https://keybase.io/{}",
    "StackOverflow"   : "https://stackoverflow.com/users/{}",
    "Dev.to"          : "https://dev.to/{}",
    "Codepen"         : "https://codepen.io/{}",
    "Bitbucket"       : "https://bitbucket.org/{}",
    "NPM"             : "https://www.npmjs.com/~{}",
    "PyPI"            : "https://pypi.org/user/{}",

    # ── Design & Art ──
    "Behance"         : "https://www.behance.net/{}",
    "Dribbble"        : "https://dribbble.com/{}",
    "DeviantArt"      : "https://www.deviantart.com/{}",
    "ArtStation"      : "https://www.artstation.com/{}",
    "Flickr"          : "https://www.flickr.com/people/{}",
    "500px"           : "https://500px.com/p/{}",
    "Unsplash"        : "https://unsplash.com/@{}",
    "Pixiv"           : "https://www.pixiv.net/en/users/{}",

    # ── Blogging & Écriture ──
    "Medium"          : "https://medium.com/@{}",
    "WordPress"       : "https://en.wordpress.com/profiles/{}",
    "Wattpad"         : "https://www.wattpad.com/user/{}",
    "Goodreads"       : "https://www.goodreads.com/{}",
    "Quora"           : "https://www.quora.com/profile/{}",
    "Substack"        : "https://{}.substack.com",
    "Ghost"           : "https://{}.ghost.io",

    # ── Commerce & Finance ──
    "Ebay"            : "https://www.ebay.com/usr/{}",
    "Etsy"            : "https://www.etsy.com/shop/{}",
    "Fiverr"          : "https://www.fiverr.com/{}",
    "Patreon"         : "https://www.patreon.com/{}",
    "CashApp"         : "https://cash.app/${}",
    "Venmo"           : "https://venmo.com/{}",
    "PayPal"          : "https://www.paypal.com/paypalme/{}",
    "Ko-fi"           : "https://ko-fi.com/{}",
    "BuyMeACoffee"    : "https://www.buymeacoffee.com/{}",

    # ── Identité & Profil ──
    "Gravatar"        : "https://en.gravatar.com/{}",
    "AboutMe"         : "https://about.me/{}",
    "Linktree"        : "https://linktr.ee/{}",
    "Carrd"           : "https://{}.carrd.co",
    "Genius"          : "https://genius.com/{}",
    "Foursquare"      : "https://foursquare.com/{}",
    "Mix"             : "https://mix.com/{}",
    "Trakt"           : "https://trakt.tv/users/{}",
    "Duolingo"        : "https://www.duolingo.com/profile/{}",
    "Strava"          : "https://www.strava.com/athletes/{}",
    "Letterboxd"      : "https://letterboxd.com/{}",
    "MyAnimeList"     : "https://myanimelist.net/profile/{}",
    "Imgur"           : "https://imgur.com/user/{}",
    "9GAG"            : "https://9gag.com/u/{}",
    "Giphy"           : "https://giphy.com/{}",
    "Houzz"           : "https://www.houzz.com/user/{}",
    "Poshmark"        : "https://poshmark.com/closet/{}",
    "Depop"           : "https://www.depop.com/{}",
    "Vinted"          : "https://www.vinted.fr/member/{}",
    "AngelList"       : "https://angel.co/u/{}",
    "Crunchbase"      : "https://www.crunchbase.com/person/{}",
    "ResearchGate"    : "https://www.researchgate.net/profile/{}",
    "Academia"        : "https://independent.academia.edu/{}",
    "Slideshare"      : "https://www.slideshare.net/{}",
    "Scribd"          : "https://www.scribd.com/{}",
}

# ─── RÉSULTATS ──────────────────────────────────
results_found = []
results_lock  = threading.Lock()

# ─── VÉRIFICATION D'UN SITE ─────────────────────
def check_site(site, url, username):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        r = requests.get(url, timeout=15, headers=headers, allow_redirects=True)
        if r.status_code == 200:
            with results_lock:
                results_found.append({"site": site, "url": url})
            print(f"  {G}{BD}[✔]{RS}  {BG}{site:<20}{RS}  {W}{url}")
        else:
            print(f"  {R}[✘]{RS}  {B}{site:<20}{RS}  {B}HTTP {r.status_code}")
    except requests.exceptions.Timeout:
        print(f"  {Y}[⏱]{RS}  {B}{site:<20}{RS}  {Y}Timeout")
    except requests.exceptions.RequestException:
        print(f"  {Y}[!]{RS}  {B}{site:<20}{RS}  {Y}Erreur connexion")

# ─── RECHERCHE PRINCIPALE ───────────────────────
def search_username(username):
    global results_found
    results_found = []

    print()
    print(G + "  " + "─" * 68)
    print(BD + BG + f"  🔱  Recherche de : {username}".ljust(68) + RS)
    print(G + "  " + "─" * 68 + RS)
    print()

    threads = []
    for site, url_template in SITES.items():
        url = url_template.format(username)
        t = threading.Thread(target=check_site, args=(site, url, username))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results_found

# ─── EXPORT RÉSULTATS ───────────────────────────
def export_results(username, found):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"triton_{username}_{timestamp}"

    with open(f"{filename}.txt", "w") as f:
        f.write(f"TRITON FINDER — Résultats pour : {username}\n")
        f.write(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        for item in found:
            f.write(f"[✔] {item['site']}\n    {item['url']}\n\n")
        f.write(f"\nTotal : {len(found)} profil(s) trouvé(s)\n")

    with open(f"{filename}.json", "w") as f:
        json.dump({
            "username" : username,
            "date"     : datetime.now().isoformat(),
            "total"    : len(found),
            "results"  : found
        }, f, indent=4, ensure_ascii=False)

    print()
    print(G + "  " + "─" * 68)
    print(BD + G + f"  💾  Exporté : {filename}.txt")
    print(BD + G + f"  💾  Exporté : {filename}.json" + RS)

# ─── RÉSUMÉ FINAL ───────────────────────────────
def summary(username, found):
    print()
    print(G + "  " + "═" * 68)
    print(BD + BG + f"  🔱  RÉSUMÉ — {username}".ljust(68) + RS)
    print(G + "  " + "═" * 68)
    print(BD + G  + f"  ✅  Profils trouvés  : {len(found)}")
    print(BD + R  + f"  ❌  Non trouvés      : {len(SITES) - len(found)}")
    print(BD + W  + f"  🌐  Sites vérifiés   : {len(SITES)}")
    print(G + "  " + "═" * 68 + RS)

# ─── MENU PRINCIPAL ─────────────────────────────
def main():
    banner()

    while True:
        print(BD + G + "  🔱  TRITON FINDER" + RS)
        print(G  + "  ─" * 34)
        print(W  + "  [1]  Rechercher un username")
        print(W  + "  [2]  Quitter")
        print(G  + "  ─" * 34)
        choice = input(BD + G + "\n  triton > " + RS).strip()

        if choice == "1":
            username = input(BD + C + "\n  ⚡ Entrez le nom d'utilisateur : " + RS).strip()
            if not username:
                print(R + "\n  [!] Nom d'utilisateur vide !\n")
                continue

            found = search_username(username)
            summary(username, found)

            if found:
                save = input(BD + Y + "\n  💾 Exporter les résultats ? (o/n) : " + RS).strip().lower()
                if save == "o":
                    export_results(username, found)

            print()

        elif choice == "2":
            print(BD + G + "\n  🔱 MR_TRITON — À bientôt !\n" + RS)
            sys.exit(0)

        else:
            print(R + "\n  [!] Option invalide\n")

# ─── LANCEMENT ──────────────────────────────────
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(BD + G + "\n\n  🔱 Interruption — À bientôt !\n" + RS)
        sys.exit(0)
