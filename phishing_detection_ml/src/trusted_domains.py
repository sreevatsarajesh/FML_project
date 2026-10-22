from src.url_utils import canonicalize_url, get_host, registered_domain

TRUSTED_DOMAINS = {
    "google.com", "youtube.com", "gmail.com", "googleapis.com", "gstatic.com",
    "facebook.com", "instagram.com", "whatsapp.com", "messenger.com",
    "twitter.com", "x.com", "linkedin.com", "microsoft.com", "live.com",
    "office.com", "outlook.com", "microsoftonline.com", "bing.com",
    "apple.com", "icloud.com", "amazon.com", "amazon.in", "amazon.co.uk",
    "flipkart.com", "wikipedia.org", "wikimedia.org", "github.com",
    "gitlab.com", "stackoverflow.com", "stackexchange.com", "netflix.com",
    "spotify.com", "zoom.us", "adobe.com", "paypal.com", "ebay.com",
    "yahoo.com", "cloudflare.com", "mozilla.org", "python.org", "pypi.org",
    "npmjs.com", "openai.com", "anthropic.com", "claude.ai", "nytimes.com",
    "bbc.com", "bbc.co.uk", "cnn.com", "theguardian.com", "reuters.com",
    "pinterest.com", "twitch.tv", "discord.com", "slack.com",
    "salesforce.com", "oracle.com", "ibm.com", "intel.com", "nvidia.com",
    "samsung.com", "sony.com", "telegram.org", "tiktok.com", "snapchat.com",
    "vimeo.com", "imdb.com", "booking.com", "airbnb.com", "uber.com",
    "tripadvisor.com", "walmart.com", "target.com", "bestbuy.com",
    "costco.com", "homedepot.com", "chase.com", "bankofamerica.com",
    "wellsfargo.com", "citi.com", "americanexpress.com", "hsbc.com",
    "sbi.co.in", "onlinesbi.sbi", "hdfcbank.com", "icicibank.com",
    "axisbank.com", "irctc.co.in", "incometax.gov.in", "india.gov.in",
    "uidai.gov.in", "nic.in", "sklearn.org", "scikit-learn.org",
    "kaggle.com", "arxiv.org", "nature.com", "science.org", "sciencedirect.com",
    "springer.com", "ieee.org", "acm.org", "nasa.gov", "mit.edu",
    "stanford.edu", "harvard.edu", "berkeley.edu", "ox.ac.uk", "cam.ac.uk",
    "coursera.org", "udemy.com", "edx.org", "khanacademy.org", "w3schools.com",
    "mozilla.com", "docker.com", "kubernetes.io", "tensorflow.org",
    "pytorch.org", "huggingface.co", "jupyter.org", "anaconda.com",
    "ubuntu.com", "debian.org", "linux.org", "apache.org", "wordpress.org",
    "wordpress.com", "shopify.com", "stripe.com", "visa.com", "mastercard.com",
    "fedex.com", "ups.com", "dhl.com", "usps.com", "zoho.com", "atlassian.com",
    "notion.so", "figma.com", "canva.com", "trello.com", "hotstar.com",
    "primevideo.com", "disneyplus.com", "hulu.com", "espn.com", "forbes.com",
    "bloomberg.com", "wsj.com", "washingtonpost.com", "timesofindia.com",
    "indiatimes.com", "hindustantimes.com", "thehindu.com", "ndtv.com",
    "swiggy.com", "zomato.com", "paytm.com", "phonepe.com", "myntra.com",
    "naukri.com", "linkedin.cn", "baidu.com", "qq.com", "taobao.com",
    "alibaba.com", "aliexpress.com", "yandex.ru", "vk.com", "naver.com",
}

UNTRUSTED_HOSTS = {
    "sites.google.com", "docs.google.com", "drive.google.com",
    "forms.google.com", "script.google.com", "translate.google.com",
    "storage.googleapis.com", "groups.google.com", "gist.github.com",
    "pages.github.com",
}


def trusted_domain(url: str):
    """Return an explicitly trusted registered domain, or None."""
    if not isinstance(url, str) or not url.strip():
        return None

    try:
        canon = canonicalize_url(url)
        host = get_host(canon).lower().rstrip(".")
        if not host or host in UNTRUSTED_HOSTS:
            return None

        domain = registered_domain(host)
        if not domain:
            return None

        if domain in TRUSTED_DOMAINS:
            return domain

        return None
    except (ValueError, TypeError, AttributeError):
        return None
