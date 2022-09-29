# from emoji import UNICODE_EMOJI_PORTUGUESE
import re

from emoji_translate.emoji_translate import Translator


class TweetStr(str):
    def decode_emoji(self):
        emo = Translator(exact_match_only=False, randomize=True)
        self = TweetStr(emo.demojify(self))
        return self

    def remove_mention(self):
        self = TweetStr(
            re.compile(pattern="\s*@\S+\s+").sub(r"", self).replace("\\n", " ")
        )
        return self

    def remove_url(self):
        self = TweetStr(
            re.compile(pattern="\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*")
            .sub(r"", self)
            .strip()
        )
        return self

    def to_string(self):
        return str(self)


def clean(text: str) -> str:
    return TweetStr(text).decode_emoji().remove_mention().remove_url().to_string()
