# -*- coding: utf-8 -*-

from yattag import Doc


def __wrap_with_mark(token):
    """
    Wrap singe word with tag mark
    :param token:
    :return:
    """
    token_text = token[0]
    description = token[1]
    if description["type"] == "word":
        if description["class"] == "known":
            token_text = "<mark class=known>" + token_text + "</mark>"
        elif description["class"] == "maybe":
            token_text = "<mark>" + token_text + "</mark>"

    return token_text


def print_page(name, lexi_text):
    """
    :param name: title of the HTML page
    :param lexi_text: text with marked words
    :return: HTML page
    """
    # Prepare text
    lexi_text = "".join([__wrap_with_mark(token)
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
            with tag('style'):
                text('mark.known \
                     {background-color: white; \
                     font-weight: normal;font-style: normal; \
                     border-bottom: 3px solid green;}')
                text('mark \
                     {background-color: white; \
                     font-weight: normal;font-style: normal; \
                     border-bottom: 3px solid yellowgreen;}')

    return doc.getvalue()