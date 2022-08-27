# from emoji import UNICODE_EMOJI_PORTUGUESE
import re


# def _remove_emoji(text):
#     allchars = [str for str in text]
#     emoji_list = [c for c in allchars if c in UNICODE_EMOJI_PORTUGUESE]
#     clean_text = " ".join(
#         [str for str in text.split() if not any(i in str for i in emoji_list)]
#     )
#     return clean_text


def clean(text):

    emoji_cleaned = re.compile(
        pattern="(\u00a9|\u00ae|"
        + "[\u2000-\u3300]|"
        + "\ud83c[\ud000-\udfff]|"
        + "\ud83d[\ud000-\udfff]|"
        + "\ud83e[\ud000-\udfff])"
    ).sub(r"", text)
    mention_cleaned = (
        re.compile(pattern="\s*@\S+\s+").sub(r"", emoji_cleaned).replace("\\n", " ")
    )
    return (
        re.compile(pattern="\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*")
        .sub(r"", mention_cleaned)
        .strip()
    )
