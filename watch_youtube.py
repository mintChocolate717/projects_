"""
Suppose that you’d like to extract the URLs of YouTube videos that are embedded in pages (e.g., https://www.youtube.com/embed/xvFZjo5PgG0),
converting them back to shorter, shareable youtu.be URLs (e.g., https://youtu.be/xvFZjo5PgG0) where they can be watched on YouTube itself.

TODO: implement a function called parse...
    - that expects a str of HTML as input,
    ------------------------------------------------------------------------------------------------------------------------------------------------
    | <iframe width="560" height="315" src="https://www.youtube.com/embed/xvFZjo5PgG0" title="YouTube video player"                                  |
    | frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>     |
    ------------------------------------------------------------------------------------------------------------------------------------------------
    - extracts any YouTube URL that’s the value of a src attribute of an iframe element therein,
    - and returns its shorter, shareable youtu.be equivalent as a str.
    # examples:
        # long URL:  http://www.youtube.com/embed/xvFZjo5PgG0
        # short URL: https://youtu.be/xvFZjo5PgG0

    Expect that any such URL will be in one of the formats below.
        http://youtube.com/embed/xvFZjo5PgG0
        https://youtube.com/embed/xvFZjo5PgG0
        https://www.youtube.com/embed/xvFZjo5PgG0
    Assume that the value of src will be surrounded by double quotes.
    And assume that the input will contain no more than one such URL.
    If the input does not contain any such URL at all, return None.
"""
import re


def main():
    p = parse(input("HTML: "))
    print(f"\n{p}")


def parse(s):
    # find the 'src' section and extract the longer URL. ex: http://www.youtube.com/embed/xvFZjo5PgG0
    if match := re.search(
        r'src="(https?://(www\.)?youtube\.com/embed/.+?)"', s.strip()
    ):
        # replace prefixes with "https://youtu.be":
        return re.sub(
            r"https?://(www\.)?youtube\.com/embed", "https://youtu.be", match.group(1)
        )
    # if the src attribute doesn’t point to a YouTube link, return None
    else:
        return None


if __name__ == "__main__":
    main()
