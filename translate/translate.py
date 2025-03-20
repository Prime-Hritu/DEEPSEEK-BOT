"""
A Translation module.

You can translate text using this module.
"""

import asyncio
import random
import re
import typing

import httpx
from httpx import Response, Timeout
from httpx._types import ProxyTypes

from googletrans import urls, utils
from googletrans.models import Detected, Translated

# -*- coding: utf-8 -*-
import ast
import math
import re
import time
from typing import Any, Callable, Dict, List

import httpx

from googletrans.utils import rshift

from database.lang_settings import get_language


def translate_to_send(text, user_id):
    language = get_language(user_id)
    if language == None:
        language = "en"
    translated = Translator().translate(str(text), dest=str(language))
    return translated.text


class TokenAcquirer:
    """Google Translate API token generator

    translate.google.com uses a token to authorize the requests. If you are
    not Google, you do have this token and will have to pay for use.
    This class is the result of reverse engineering on the obfuscated and
    minified code used by Google to generate such token.

    The token is based on a seed which is updated once per hour and on the
    text that will be translated.
    Both are combined - by some strange math - in order to generate a final
    token (e.g. 744915.856682) which is used by the API to validate the
    request.

    This operation will cause an additional request to get an initial
    token from translate.google.com.

    Example usage:
        >>> from googletrans.gtoken import TokenAcquirer
        >>> acquirer = TokenAcquirer()
        >>> text = 'test'
        >>> tk = acquirer.do(text)
        >>> tk
        950629.577246
    """

    RE_TKK = re.compile(r"tkk:\'(.+?)\'", re.DOTALL)
    RE_RAWTKK = re.compile(r"tkk:\'(.+?)\'", re.DOTALL)

    def __init__(
        self,
        client: httpx.Client,
        tkk: str = "0",
        host: str = "translate.google.com",
    ) -> None:
        self.client = client
        self.tkk = tkk
        self.host = host if "http" in host else "https://" + host

    def _update(self) -> None:
        """update tkk"""
        # we don't need to update the base TKK value when it is still valid
        now = math.floor(int(time.time() * 1000) / 3600000.0)
        if self.tkk and int(self.tkk.split(".")[0]) == now:
            return

        r = self.client.get(self.host)

        raw_tkk = self.RE_TKK.search(r.text)
        if raw_tkk:
            self.tkk = raw_tkk.group(1)
            return

        code = self.RE_TKK.search(r.text)

        if code is not None:
            # this will be the same as python code after stripping out a reserved word 'var'
            code = code.group(1).replace("var ", "")
            # unescape special ascii characters such like a \x3d(=)
            code = code.encode().decode("unicode-escape")

        if code:
            tree = ast.parse(code)
            visit_return = False
            operator = "+"
            n: int = 0
            keys: Dict[str, int] = dict(a=0, b=0)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    name = None
                    if isinstance(node.targets[0], ast.Name):
                        name = node.targets[0].id
                    if name in keys:
                        if isinstance(node.value, ast.Constant):
                            keys[name] = int(node.value.value)
                        # the value can sometimes be negative
                        elif isinstance(node.value, ast.UnaryOp) and isinstance(
                            node.value.op, ast.USub
                        ):  # pragma: nocover
                            if isinstance(node.value.operand, ast.Constant):
                                keys[name] = -int(node.value.operand.value)
                elif isinstance(node, ast.Return):
                    # parameters should be set after this point
                    visit_return = True
                elif visit_return and isinstance(node, ast.Constant):
                    n = int(node.value)
                elif visit_return and isinstance(n, int) and n > 0:
                    # the default operator is '+' but implement some more for
                    # all possible scenarios
                    if isinstance(node, ast.Add):  # pragma: nocover
                        pass
                    elif isinstance(node, ast.Sub):  # pragma: nocover
                        operator = "-"
                    elif isinstance(node, ast.Mult):  # pragma: nocover
                        operator = "*"
                    elif isinstance(node, ast.Pow):  # pragma: nocover
                        operator = "**"
                    elif isinstance(node, ast.BitXor):  # pragma: nocover
                        operator = "^"
            # a safety way to avoid Exceptions
            clause = compile(
                "{1}{0}{2}".format(operator, keys["a"], keys["b"]), "", "eval"
            )
            value = eval(clause, dict(__builtin__={}))
            result = "{}.{}".format(n, value)

            self.tkk = result

    def _lazy(self, value: Any) -> Callable[[], Any]:
        """like lazy evaluation, this method returns a lambda function that
        returns value given.
        We won't be needing this because this seems to have been built for
        code obfuscation.

        the original code of this method is as follows:

           ... code-block: javascript

               var ek = function(a) {
                return function() {
                    return a;
                };
               }
        """
        return lambda: value

    def _xr(self, a: int, b: str) -> int:
        size_b = len(b)
        c = 0
        while c < size_b - 2:
            d = b[c + 2]
            d = ord(d[0]) - 87 if "a" <= d else int(d)
            d = rshift(a, d) if "+" == b[c + 1] else a << d
            a = a + d & 4294967295 if "+" == b[c] else a ^ d

            c += 3
        return a

    def acquire(self, text: str) -> str:
        a: List[int] = []
        # Convert text to ints
        for i in text:
            val = ord(i)
            if val < 0x10000:
                a += [val]
            else:
                # Python doesn't natively use Unicode surrogates, so account for those
                a += [
                    math.floor((val - 0x10000) / 0x400 + 0xD800),
                    math.floor((val - 0x10000) % 0x400 + 0xDC00),
                ]

        b = self.tkk if self.tkk != "0" else ""
        d = b.split(".")
        b_val = int(d[0]) if len(d) > 1 else 0

        # assume e means char code array
        e: List[int] = []
        g = 0
        size = len(a)
        while g < size:
            l = a[g]  # noqa: E741
            # just append if l is less than 128(ascii: DEL)
            if l < 128:
                e.append(l)
            # append calculated value if l is less than 2048
            else:
                if l < 2048:
                    e.append(l >> 6 | 192)
                else:
                    # append calculated value if l matches special condition
                    if (
                        (l & 64512) == 55296
                        and g + 1 < size
                        and a[g + 1] & 64512 == 56320
                    ):
                        g += 1
                        l = (  # noqa: E741
                            65536 + ((l & 1023) << 10) + (a[g] & 1023)
                        )  # This bracket is important
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(l >> 12 | 224)
                    e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)
            g += 1
        a_val = b_val
        for value in e:
            a_val += value
            a_val = self._xr(a_val, "+-a^+6")
        a_val = self._xr(a_val, "+-3^+b+-f")
        a_val ^= int(d[1]) if len(d) > 1 else 0
        if a_val < 0:  # pragma: nocover
            a_val = (a_val & 2147483647) + 2147483648
        a_val %= 1000000  # int(1E6)

        return "{}.{}".format(a_val, a_val ^ b_val)

    def do(self, text: str) -> str:
        self._update()
        tk = self.acquire(text)
        return tk


EXCLUDES = ("en", "ca", "fr")
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
DEFAULT_CLIENT_SERVICE_URLS = ("translate.googleapis.com",)
DEFAULT_SERVICE_URLS = (
    "translate.google.ac",
    "translate.google.ad",
    "translate.google.ae",
    "translate.google.al",
    "translate.google.am",
    "translate.google.as",
    "translate.google.at",
    "translate.google.az",
    "translate.google.ba",
    "translate.google.be",
    "translate.google.bf",
    "translate.google.bg",
    "translate.google.bi",
    "translate.google.bj",
    "translate.google.bs",
    "translate.google.bt",
    "translate.google.by",
    "translate.google.ca",
    "translate.google.cat",
    "translate.google.cc",
    "translate.google.cd",
    "translate.google.cf",
    "translate.google.cg",
    "translate.google.ch",
    "translate.google.ci",
    "translate.google.cl",
    "translate.google.cm",
    "translate.google.cn",
    "translate.google.co.ao",
    "translate.google.co.bw",
    "translate.google.co.ck",
    "translate.google.co.cr",
    "translate.google.co.id",
    "translate.google.co.il",
    "translate.google.co.in",
    "translate.google.co.jp",
    "translate.google.co.ke",
    "translate.google.co.kr",
    "translate.google.co.ls",
    "translate.google.co.ma",
    "translate.google.co.mz",
    "translate.google.co.nz",
    "translate.google.co.th",
    "translate.google.co.tz",
    "translate.google.co.ug",
    "translate.google.co.uk",
    "translate.google.co.uz",
    "translate.google.co.ve",
    "translate.google.co.vi",
    "translate.google.co.za",
    "translate.google.co.zm",
    "translate.google.co.zw",
    "translate.google.com.af",
    "translate.google.com.ag",
    "translate.google.com.ai",
    "translate.google.com.ar",
    "translate.google.com.au",
    "translate.google.com.bd",
    "translate.google.com.bh",
    "translate.google.com.bn",
    "translate.google.com.bo",
    "translate.google.com.br",
    "translate.google.com.bz",
    "translate.google.com.co",
    "translate.google.com.cu",
    "translate.google.com.cy",
    "translate.google.com.do",
    "translate.google.com.ec",
    "translate.google.com.eg",
    "translate.google.com.et",
    "translate.google.com.fj",
    "translate.google.com.gh",
    "translate.google.com.gi",
    "translate.google.com.gt",
    "translate.google.com.hk",
    "translate.google.com.jm",
    "translate.google.com.kh",
    "translate.google.com.kw",
    "translate.google.com.lb",
    "translate.google.com.ly",
    "translate.google.com.mm",
    "translate.google.com.mt",
    "translate.google.com.mx",
    "translate.google.com.my",
    "translate.google.com.na",
    "translate.google.com.ng",
    "translate.google.com.ni",
    "translate.google.com.np",
    "translate.google.com.om",
    "translate.google.com.pa",
    "translate.google.com.pe",
    "translate.google.com.pg",
    "translate.google.com.ph",
    "translate.google.com.pk",
    "translate.google.com.pr",
    "translate.google.com.py",
    "translate.google.com.qa",
    "translate.google.com.sa",
    "translate.google.com.sb",
    "translate.google.com.sg",
    "translate.google.com.sl",
    "translate.google.com.sv",
    "translate.google.com.tj",
    "translate.google.com.tr",
    "translate.google.com.tw",
    "translate.google.com.ua",
    "translate.google.com.uy",
    "translate.google.com.vc",
    "translate.google.com.vn",
    "translate.google.com",
    "translate.google.cv",
    "translate.google.cz",
    "translate.google.de",
    "translate.google.dj",
    "translate.google.dk",
    "translate.google.dm",
    "translate.google.dz",
    "translate.google.ee",
    "translate.google.es",
    "translate.google.eu",
    "translate.google.fi",
    "translate.google.fm",
    "translate.google.fr",
    "translate.google.ga",
    "translate.google.ge",
    "translate.google.gf",
    "translate.google.gg",
    "translate.google.gl",
    "translate.google.gm",
    "translate.google.gp",
    "translate.google.gr",
    "translate.google.gy",
    "translate.google.hn",
    "translate.google.hr",
    "translate.google.ht",
    "translate.google.hu",
    "translate.google.ie",
    "translate.google.im",
    "translate.google.io",
    "translate.google.iq",
    "translate.google.is",
    "translate.google.it",
    "translate.google.je",
    "translate.google.jo",
    "translate.google.kg",
    "translate.google.ki",
    "translate.google.kz",
    "translate.google.la",
    "translate.google.li",
    "translate.google.lk",
    "translate.google.lt",
    "translate.google.lu",
    "translate.google.lv",
    "translate.google.md",
    "translate.google.me",
    "translate.google.mg",
    "translate.google.mk",
    "translate.google.ml",
    "translate.google.mn",
    "translate.google.ms",
    "translate.google.mu",
    "translate.google.mv",
    "translate.google.mw",
    "translate.google.ne",
    "translate.google.nf",
    "translate.google.nl",
    "translate.google.no",
    "translate.google.nr",
    "translate.google.nu",
    "translate.google.pl",
    "translate.google.pn",
    "translate.google.ps",
    "translate.google.pt",
    "translate.google.ro",
    "translate.google.rs",
    "translate.google.ru",
    "translate.google.rw",
    "translate.google.sc",
    "translate.google.se",
    "translate.google.sh",
    "translate.google.si",
    "translate.google.sk",
    "translate.google.sm",
    "translate.google.sn",
    "translate.google.so",
    "translate.google.sr",
    "translate.google.st",
    "translate.google.td",
    "translate.google.tg",
    "translate.google.tk",
    "translate.google.tl",
    "translate.google.tm",
    "translate.google.tn",
    "translate.google.to",
    "translate.google.tt",
    "translate.google.us",
    "translate.google.vg",
    "translate.google.vu",
    "translate.google.ws",
)

SPECIAL_CASES = {
    "ee": "et",
}

LANGUAGES = {
    "abk": "abkhaz",
    "ace": "acehnese",
    "ach": "acholi",
    "aar": "afar",
    "af": "afrikaans",
    "sq": "albanian",
    "alz": "alur",
    "am": "amharic",
    "ar": "arabic",
    "hy": "armenian",
    "as": "assamese",
    "ava": "avar",
    "awa": "awadhi",
    "ay": "aymara",
    "az": "azerbaijani",
    "ban": "balinese",
    "bal": "baluchi",
    "bm": "bambara",
    "bci": "baoulé",
    "bak": "bashkir",
    "eu": "basque",
    "btx": "batak karo",
    "bts": "batak simalungun",
    "bbc": "batak toba",
    "be": "belarusian",
    "bem": "bemba",
    "bn": "bengali",
    "bew": "betawi",
    "bho": "bhojpuri",
    "bik": "bikol",
    "bs": "bosnian",
    "bre": "breton",
    "bg": "bulgarian",
    "bua": "buryat",
    "yue": "cantonese",
    "ca": "catalan",
    "ceb": "cebuano",
    "cha": "chamorro",
    "che": "chechen",
    "zh": "chinese",
    "zh-cn": "chinese (simplified)",
    "zh-tw": "chinese (traditional)",
    "chk": "chuukese",
    "chv": "chuvash",
    "co": "corsican",
    "crh": "crimean tatar",
    "hr": "croatian",
    "cs": "czech",
    "da": "danish",
    "fa-af": "dari",
    "dv": "dhivehi",
    "din": "dinka",
    "doi": "dogri",
    "dom": "dombe",
    "nl": "dutch",
    "dyu": "dyula",
    "dzo": "dzongkha",
    "en": "english",
    "eo": "esperanto",
    "et": "estonian",
    "fao": "faroese",
    "fij": "fijian",
    "fil": "filipino (tagalog)",
    "fi": "finnish",
    "fon": "fon",
    "fr": "french",
    "fy": "frisian",
    "fur": "friulian",
    "ful": "fulani",
    "gaa": "ga",
    "gl": "galician",
    "ka": "georgian",
    "de": "german",
    "el": "greek",
    "gn": "guarani",
    "gu": "gujarati",
    "ht": "haitian creole",
    "cnh": "hakha chin",
    "ha": "hausa",
    "haw": "hawaiian",
    "he": "hebrew",
    "iw": "hebrew",
    "hil": "hiligaynon",
    "hi": "hindi",
    "hmn": "hmong",
    "hu": "hungarian",
    "hrx": "hunsrik",
    "iba": "iban",
    "is": "icelandic",
    "ig": "igbo",
    "ilo": "ilocano",
    "id": "indonesian",
    "ga": "irish",
    "it": "italian",
    "jam": "jamaican patois",
    "ja": "japanese",
    "jv": "javanese",
    "jw": "javanese",
    "kac": "jingpo",
    "kal": "kalaallisut",
    "kn": "kannada",
    "kau": "kanuri",
    "pam": "kapampangan",
    "kk": "kazakh",
    "kha": "khasi",
    "km": "khmer",
    "cgg": "kiga",
    "kik": "kikongo",
    "rw": "kinyarwanda",
    "ktu": "kituba",
    "trp": "kokborok",
    "kom": "komi",
    "gom": "konkani",
    "ko": "korean",
    "kri": "krio",
    "ku": "kurdish",
    "ckb": "kurdish (sorani)",
    "ky": "kyrgyz",
    "lo": "lao",
    "ltg": "latgalian",
    "la": "latin",
    "lv": "latvian",
    "lij": "ligurian",
    "lim": "limburgish",
    "ln": "lingala",
    "lt": "lithuanian",
    "lmo": "lombard",
    "lg": "luganda",
    "luo": "luo",
    "lb": "luxembourgish",
    "mk": "macedonian",
    "mad": "madurese",
    "mai": "maithili",
    "mak": "makassar",
    "mg": "malagasy",
    "ms": "malay",
    "ms-arab": "malay (jawi)",
    "ml": "malayalam",
    "mt": "maltese",
    "mam": "mam",
    "glv": "manx",
    "mi": "maori",
    "mr": "marathi",
    "mah": "marshallese",
    "mwr": "marwadi",
    "mfe": "mauritian creole",
    "mhr": "meadow mari",
    "mni-mtei": "meiteilon (manipuri)",
    "min": "minang",
    "lus": "mizo",
    "mn": "mongolian",
    "my": "myanmar (burmese)",
    "nhe": "nahuatl (eastern huasteca)",
    "ndc-zw": "ndau",
    "nde": "ndebele (south)",
    "new": "nepalbhasa (newari)",
    "ne": "nepali",
    # 'bm-nkoo': 'nko',
    "no": "norwegian",
    "nus": "nuer",
    "ny": "nyanja (chichewa)",
    "oci": "occitan",
    "or": "odia (oriya)",
    "om": "oromo",
    "oss": "ossetian",
    "pag": "pangasinan",
    "pap": "papiamento",
    "ps": "pashto",
    "fa": "persian",
    "pl": "polish",
    "por": "portuguese (portugal)",
    "pt": "portuguese (portugal, brazil)",
    "pa": "punjabi",
    "pa-arab": "punjabi (shahmukhi)",
    "kek": "q'eqchi'",
    "qu": "quechua",
    "rom": "romani",
    "ro": "romanian",
    "run": "rundi",
    "ru": "russian",
    "sme": "sami (north)",
    "sm": "samoan",
    "sag": "sango",
    "sa": "sanskrit",
    "sat": "santali",
    "gd": "scots gaelic",
    "nso": "sepedi",
    "sr": "serbian",
    "st": "sesotho",
    "crs": "seychellois creole",
    "shn": "shan",
    "sn": "shona",
    "scn": "sicilian",
    "szl": "silesian",
    "sd": "sindhi",
    "si": "sinhala (sinhalese)",
    "sk": "slovak",
    "sl": "slovenian",
    "so": "somali",
    "es": "spanish",
    "su": "sundanese",
    "sus": "susu",
    "sw": "swahili",
    "ssw": "swati",
    "sv": "swedish",
    "tl": "tagalog (filipino)",
    "tah": "tahitian",
    "tg": "tajik",
    "ber-atn": "tamazight",
    "ber": "tamazight (tifinagh)",
    "ta": "tamil",
    "tt": "tatar",
    "te": "telugu",
    "tet": "tetum",
    "th": "thai",
    "bod": "tibetan",
    "ti": "tigrinya",
    "tiv": "tiv",
    "tpi": "tok pisin",
    "ton": "tongan",
    "ts": "tsonga",
    "tsn": "tswana",
    "tcy": "tulu",
    "tum": "tumbuka",
    "tr": "turkish",
    "tk": "turkmen",
    "tuk": "tuvan",
    "ak": "twi (akan)",
    "udm": "udmurt",
    "uk": "ukrainian",
    "ur": "urdu",
    "ug": "uyghur",
    "uz": "uzbek",
    "ven": "venda",
    "vec": "venetian",
    "vi": "vietnamese",
    "war": "waray",
    "cy": "welsh",
    "wol": "wolof",
    "xh": "xhosa",
    "sah": "yakut",
    "yi": "yiddish",
    "yo": "yoruba",
    "yua": "yucatec maya",
    "zap": "zapotec",
    "zu": "zulu",
}

LANGCODES = {v: k for k, v in LANGUAGES.items()}
DEFAULT_RAISE_EXCEPTION = False
DUMMY_DATA = [
    [["", None, None, 0]],
    None,
    "en",
    None,
    None,
    None,
    1,
    None,
    [["en"], None, [1], ["en"]],
]


class Translator:
    """Google Translate ajax API implementation class

    You have to create an instance of Translator to use this API

    :param service_urls: google translate url list. URLs will be used randomly.
                         For example ``['translate.google.com', 'translate.google.co.kr']``
                         To preferably use the non webapp api, service url should be translate.googleapis.com
    :type service_urls: a sequence of strings

    :param user_agent: the User-Agent header to send when making requests.
    :type user_agent: :class:`str`

    :param proxy: httpx proxy configuration.

    :param timeout: Definition of timeout for httpx library.
                    Will be used for every request.
    :type timeout: number or a double of numbers
    :param raise_exception: if `True` then raise exception if smth will go wrong
    :type raise_exception: boolean
    """

    def __init__(
        self,
        service_urls: typing.Sequence[str] = DEFAULT_CLIENT_SERVICE_URLS,
        user_agent: str = DEFAULT_USER_AGENT,
        raise_exception: bool = DEFAULT_RAISE_EXCEPTION,
        proxy: typing.Optional[ProxyTypes] = None,
        timeout: typing.Optional[Timeout] = None,
        http2: bool = True,
        list_operation_max_concurrency: int = 2,
    ):
        self.client = httpx.Client(
            http2=http2,
            proxy=proxy,
            headers={
                "User-Agent": user_agent,
            },
        )

        self.service_urls = ["translate.google.com"]
        self.client_type = "webapp"
        self.token_acquirer = TokenAcquirer(
            client=self.client, host=self.service_urls[0]
        )

        if timeout is not None:
            self.client.timeout = timeout

        if service_urls:
            # default way of working: use the defined values from user app
            self.service_urls = service_urls
            self.client_type = "webapp"
            self.token_acquirer = TokenAcquirer(
                client=self.client, host=self.service_urls[0]
            )

            # if we have a service url pointing to client api we force the use of it as defaut client
            for t in enumerate(service_urls):
                api_type = re.search("googleapis", service_urls[0])
                if api_type:
                    self.service_urls = ["translate.googleapis.com"]
                    self.client_type = "gtx"
                    break

        self.raise_exception = raise_exception
        self.list_operation_max_concurrency = list_operation_max_concurrency

    def _pick_service_url(self) -> str:
        if len(self.service_urls) == 1:
            return self.service_urls[0]
        return random.choice(self.service_urls)

    def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.client.aclose()

    def _translate(
        self, text: str, dest: str, src: str, override: typing.Dict[str, typing.Any]
    ) -> typing.Tuple[typing.List[typing.Any], Response]:
        token = "xxxx"  # dummy default value here as it is not used by api client
        if self.client_type == "webapp":
            token = self.token_acquirer.do(text)

        params = utils.build_params(
            client=self.client_type,
            query=text,
            src=src,
            dest=dest,
            token=token,
            override=override,
        )

        url = urls.TRANSLATE.format(host=self._pick_service_url())
        r = self.client.get(url, params=params)

        if r.status_code == 200:
            data = utils.format_json(r.text)
            if not isinstance(data, list):
                data = [data]  # Convert dict to list to match return type
            return data, r

        if self.raise_exception:
            raise Exception(
                'Unexpected status code "{}" from {}'.format(
                    r.status_code, self.service_urls
                )
            )

        DUMMY_DATA[0][0][0] = text
        return DUMMY_DATA, r

    def build_request(
        self, text: str, dest: str, src: str, override: typing.Dict[str, typing.Any]
    ) -> httpx.Request:
        """helper for making the translation request"""
        token = "xxxx"  # dummy default value here as it is not used by api client
        if self.client_type == "webapp":
            token = self.token_acquirer.do(text)

        params = utils.build_params(
            client=self.client_type,
            query=text,
            src=src,
            dest=dest,
            token=token,
            override=override,
        )

        url = urls.TRANSLATE.format(host=self._pick_service_url())

        return self.client.build_request("GET", url, params=params)

    def _parse_extra_data(
        self, data: typing.List[typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        response_parts_name_mapping = {
            0: "translation",
            1: "all-translations",
            2: "original-language",
            5: "possible-translations",
            6: "confidence",
            7: "possible-mistakes",
            8: "language",
            11: "synonyms",
            12: "definitions",
            13: "examples",
            14: "see-also",
        }

        extra = {}

        for index, category in response_parts_name_mapping.items():
            extra[category] = (
                data[index] if (index < len(data) and data[index]) else None
            )

        return extra

    @typing.overload
    def translate(
        self, text: str, dest: str = ..., src: str = ..., **kwargs: typing.Any
    ) -> Translated: ...

    @typing.overload
    def translate(
        self,
        text: typing.List[str],
        dest: str = ...,
        src: str = ...,
        **kwargs: typing.Any,
    ) -> typing.List[Translated]: ...

    def translate(
        self,
        text: typing.Union[str, typing.List[str]],
        dest: str = "en",
        src: str = "auto",
        **kwargs: typing.Any,
    ) -> typing.Union[Translated, typing.List[Translated]]:

        dest = dest.lower().split("_", 1)[0]
        src = src.lower().split("_", 1)[0]

        if src != "auto" and src not in LANGUAGES:
            if src in SPECIAL_CASES:
                src = SPECIAL_CASES[src]
            elif src in LANGCODES:
                src = LANGCODES[src]
            else:
                raise ValueError("invalid source language")

        if dest not in LANGUAGES:
            if dest in SPECIAL_CASES:
                dest = SPECIAL_CASES[dest]
            elif dest in LANGCODES:
                dest = LANGCODES[dest]
            else:
                raise ValueError("invalid destination language")

        if isinstance(text, list):
            concurrency_limit = kwargs.pop(
                "list_operation_max_concurrency", self.list_operation_max_concurrency
            )
            semaphore = asyncio.Semaphore(concurrency_limit)

            def translate_with_semaphore(item):
                with semaphore:
                    return self.translate(item, dest=dest, src=src, **kwargs)

            tasks = [translate_with_semaphore(item) for item in text]
            result = asyncio.gather(*tasks)
            return result

        origin = text
        data, response = self._translate(text, dest, src, kwargs)

        # this code will be updated when the format is changed.
        translated = "".join([d[0] if d[0] else "" for d in data[0]])

        extra_data = self._parse_extra_data(data)

        # actual source language that will be recognized by Google Translator when the
        # src passed is equal to auto.
        try:
            src = data[2]
        except Exception:  # pragma: nocover
            pass

        pron = origin
        try:
            pron = data[0][1][-2]
        except Exception:  # pragma: nocover
            pass

        if pron is None:
            try:
                pron = data[0][1][2]
            except:  # pragma: nocover  # noqa: E722
                pass

        if dest in EXCLUDES and pron == origin:
            pron = translated

        # put final values into a new Translated object
        result = Translated(
            src=src,
            dest=dest,
            origin=origin,
            text=translated,
            pronunciation=pron,
            extra_data=extra_data,
            response=response,
        )

        return result

    @typing.overload
    def detect(self, text: str, **kwargs: typing.Any) -> Detected: ...

    @typing.overload
    def detect(
        self, text: typing.List[str], **kwargs: typing.Any
    ) -> typing.List[Detected]: ...

    def detect(
        self, text: typing.Union[str, typing.List[str]], **kwargs: typing.Any
    ) -> typing.Union[Detected, typing.List[Detected]]:

        if isinstance(text, list):
            concurrency_limit = kwargs.pop(
                "list_operation_max_concurrency", self.list_operation_max_concurrency
            )
            semaphore = asyncio.Semaphore(concurrency_limit)

            def detect_with_semaphore(item):
                with semaphore:
                    return self.detect(item, **kwargs)

            tasks = [detect_with_semaphore(item) for item in text]
            result = asyncio.gather(*tasks)
            return result

        data, response = self._translate(text, "en", "auto", kwargs)

        # actual source language that will be recognized by Google Translator when the
        # src passed is equal to auto.
        src = ""
        confidence = 0.0
        try:
            if len(data[8][0]) > 1:
                src = data[8][0]
                confidence = data[8][-2]
            else:
                src = "".join(data[8][0])
                confidence = data[8][-2][0]
        except Exception:  # pragma: nocover
            pass
        result = Detected(lang=src, confidence=confidence, response=response)

        return result
