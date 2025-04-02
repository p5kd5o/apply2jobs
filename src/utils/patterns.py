# $¢£¤¥ƒ֏؋৲৳૱௹฿៛ℳ元円圆圓﷼₠₡₢₣₤₥₦₧₨₩₪₫€₭₮₯₰₱₲₳₴₵₶₷₸₹₺₻₼₽₾₿⃀
CURRENCY_CHARS = tuple(map(chr, [
    0x0024, 0x00a2, 0x00a3, 0x00a4, 0x00a5, 0x0192, 0x058f,
    0x060b, 0x09f2, 0x09f3, 0x0af1, 0x0bf9, 0x0e3f, 0x17db,
    0x2133, 0x5143, 0x5186, 0x5706, 0x5713, 0xfdfc, 0x20a0,
    0x20a1, 0x20a2, 0x20a3, 0x20a4, 0x20a5, 0x20a6, 0x20a7,
    0x20a8, 0x20a9, 0x20aa, 0x20ab, 0x20ac, 0x20ad, 0x20ae,
    0x20af, 0x20b0, 0x20b1, 0x20b2, 0x20b3, 0x20b4, 0x20b5,
    0x20b6, 0x20b7, 0x20b8, 0x20b9, 0x20ba, 0x20bb, 0x20bc,
    0x20bd, 0x20be, 0x20bf, 0x20c0
]))
CURRENCY_CLASS = f"[{''.join(CURRENCY_CHARS)}]"

NOSEP_NUMBER_PATTERN = f"({'|'.join([
    r'\d+([,.]\d+)?',
    r'[,.]\d+'
])})"
SPACE_NUMBER_PATTERN = f"({'|'.join([
    r'\d{1,3}( \d{3})*([,.]\d+)?',
    r'[,.]\d+'
])})"
COMMA_NUMBER_PATTERN = f"({'|'.join([
    r'\d{1,3}(,\d{3})*(\.\d+)?',
    r'\.\d+'
])})"
PERIOD_NUMBER_PATTERN = f"({'|'.join([
    r'\d{1,3}(\.\d{3})*(,\d+)?',
    r',\d+'
])})"
TWOSEP_NUMBER_PATTERN = f"({'|'.join([
    r'\d{1,3}(( \d{3})*(\.\d{3}))?(,\d+)?',
    r'\d{1,3}(( \d{3})*(,\d{3}))?(\.\d+)?',
    r'[,.]\d+'
])})"
NUMBER_PATTERN = f"({'|'.join([
    NOSEP_NUMBER_PATTERN,
    SPACE_NUMBER_PATTERN,
    COMMA_NUMBER_PATTERN,
    PERIOD_NUMBER_PATTERN,
    TWOSEP_NUMBER_PATTERN
])})"

CURRENCY_PATTERN = f"{CURRENCY_CLASS}{NUMBER_PATTERN}"
