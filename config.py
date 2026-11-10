"""
ReconMail - Configuration Module
Author: Imran Pasha (https://github.com/Imranpasha30)
"""

VERSION = "2.1.0"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

DEFAULT_TIMEOUT = 10

# Search Engines URL Templates
SEARCH_ENGINES = {
    "google": "https://www.google.com/search?q={query}&num=50",
    "bing": "https://www.bing.com/search?q={query}&count=50",
    "yahoo": "https://search.yahoo.com/search?p={query}&n=50",
    "duckduckgo": "https://html.duckduckgo.com/html/?q={query}",
}

# Public PGP Key Servers (Using machine-readable options=mr for reliable API responses)
PGP_KEYSERVERS = [
    "https://keyserver.ubuntu.com/pks/lookup?search={query}&op=index&options=mr",
]

BANNER = r"""
  ____                      __  __       _ _ 
 |  _ \ ___  ___ ___  _ __ |  \/  | __ _(_) |
 | |_) / _ \/ __/ _ \| '_ \| |\/| |/ _` | | |
 |  _ <  __/ (_| (_) | | | | |  | | (_| | | |
 |_| \_\___|\___\___/|_| |_|_|  |_|\__,_|_|_|
                                             
 ReconMail - Email OSINT & Threat Reconnaissance Framework
 Version: {version} | Author: Imran Pasha
"""
