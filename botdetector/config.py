LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
CONF_OPT_DB_NAME = "DB_NAME"
CONF_OPT_DB_HOST = "DB_HOST"
CONF_OPT_DB_PORT = "DB_PORT"
CONF_OPT_DB_USER = "DB_USER"
CONF_OPT_DB_PASSWORD = "DB_PASSWORD"
CONF_OPT_SECRET_KEY = "SECRET_KEY"
CONF_OPT_PROMETHEUS_URL = "PROMETHEUS_URL"
BROWSER_SIGNATURES = ["Mozilla", "Chrome", "Safari", "Edge", "Firefox", "Opera"]
HTTP_COMMON_HEADERS = [
    "Accept", "Accept-CH", "Accept-CH-Lifetime", "Accept-Charset", "Accept-Encoding",
    "Accept-Language", "Accept-Patch", "Accept-Post", "Accept-Ranges",
    "Access-Control-Allow-Credentials", "Access-Control-Allow-Headers",
    "Access-Control-Allow-Methods", "Access-Control-Allow-Origin",
    "Access-Control-Expose-Headers", "Access-Control-Max-Age",
    "Access-Control-Request-Headers", "Access-Control-Request-Method", "Age",
    "Allow", "Alt-Svc", "Alt-Used", "Authorization", "Cache-Control",
    "Clear-Site-Data", "Connection", "Content-Disposition", "Content-DPR",
    "Content-Encoding", "Content-Language", "Content-Length", "Content-Location",
    "Content-Range", "Content-Security-Policy", "Content-Security-Policy-Report-Only",
    "Content-Type", "Cookie", "Critical-CH", "Cross-Origin-Embedder-Policy",
    "Cross-Origin-Opener-Policy", "Cross-Origin-Resource-Policy", "Date",
    "Device-Memory", "Digest", "DNT", "Downlink", "DPR", "Early-Data", "ECT",
    "ETag", "Expect", "Expect-CT", "Expires", "Forwarded", "From", "Host",
    "If-Match", "If-Modified-Since", "If-None-Match", "If-Range",
    "If-Unmodified-Since", "Keep-Alive", "Large-Allocation", "Last-Modified",
    "Link", "Location", "Max-Forwards", "NEL", "Origin", "Origin-Agent-Cluster",
    "Permissions-Policy", "Pragma", "Proxy-Authenticate", "Proxy-Authorization",
    "Range", "Referer", "Referrer-Policy", "Retry-After", "RTT", "Save-Data",
    "Sec-CH-Prefers-Color-Scheme", "Sec-CH-Prefers-Reduced-Motion",
    "Sec-CH-Prefers-Reduced-Transparency", "Sec-CH-UA", "Sec-CH-UA-Arch",
    "Sec-CH-UA-Bitness", "Sec-CH-UA-Full-Version", "Sec-CH-UA-Full-Version-List",
    "Sec-CH-UA-Mobile", "Sec-CH-UA-Model", "Sec-CH-UA-Platform",
    "Sec-CH-UA-Platform-Version", "Sec-Fetch-Dest", "Sec-Fetch-Mode",
    "Sec-Fetch-Site", "Sec-Fetch-User", "Sec-GPC", "Sec-Purpose",
    "Sec-WebSocket-Accept", "Server", "Server-Timing",
    "Service-Worker-Navigation-Preload", "Set-Cookie", "SourceMap",
    "Strict-Transport-Security", "Supports-Loading-Mode", "TE",
    "Timing-Allow-Origin", "Tk", "Trailer", "Transfer-Encoding", "Upgrade",
    "Upgrade-Insecure-Requests", "User-Agent", "Vary", "Via", "Viewport-Width",
    "Want-Digest", "Warning", "Width", "WWW-Authenticate"
]

