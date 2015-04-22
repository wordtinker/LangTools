# -*- coding: utf-8 -*-

from yattag import Doc


def _wrap_with_mark(token):
    """
    Wrap singe word with tag mark
    :param token:
    :return:
    """
    token_text, description = token
    if description["type"] == "word":
        token_text = "<span class=" + description['class'] + ">" +\
                     token_text + "</span>"

    return token_text


def print_page(name, lexi_text, style=""):
    """
    :param name: title of the HTML page
    :param lexi_text: text with marked words
    :return: HTML page
    """
    # Prepare text
    lexi_text = "".join([_wrap_with_mark(token)
                         for token in lexi_text])

    # Convert text to html
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        doc.stag('meta', charset='utf-8')
        with tag('title'):
            text(name)
        with tag('body'):
            with tag('article'):
                lines = lexi_text.split('\n')
                for line in lines:
                    with tag('p'):
                        doc.asis(line)
            if style:  # Use user defined style
                with tag('style'):
                    text(style)
            else:  # Use default style
                with tag('style'):
                    text('body {font-family:sans-serif; \
                         line-height: 1.5;}')
                    text('span.known \
                         {background-color: white; \
                         font-weight: normal;font-style: normal; \
                         border-bottom: 3px solid green;}')
                    text('span.maybe \
                         {background-color: white; \
                         font-weight: normal;font-style: normal; \
                         border-bottom: 3px solid yellowgreen;}')

    return doc.getvalue()
