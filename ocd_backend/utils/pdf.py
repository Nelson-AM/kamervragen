import os
import subprocess
import tempfile
import re
from cStringIO import StringIO
from urllib2 import HTTPError

from OpenSSL.SSL import ZeroReturnError

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import requests

from ocd_backend import settings

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        print "Start processing page %s" % (page,)
        # For some reason PDFMiner chokes on pages that have a single,
        # but detailed image in them. Work around by skipping pages with
        # a large media box
        mediabox = [0, 0, 0, 0]
        try:
            mediabox = page.mediabox
        except AttributeError as e:
            pass
        try:
            mediabox_pixels = mediabox[2] * mediabox[3]
        except IndexError as e:
            mediabox_pixels = 0

        print "Page has %s pixels" % (mediabox_pixels,)
        if mediabox_pixels <= settings.PDF_MAX_MEDIABOX_PIXELS:
            print "Processed page %s" % (page,)
            interpreter.process_page(page)
        else:
            print "Skipped page %s" % (page,)

    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text


class PDFToTextMixin(object):
    """
    Interface for converting a PDF file into text format using pdftotext
    """

    def pdf_clean_text(self, text):
        return text
        # return re.sub(r'\s+', u' ', text)

    def pdf_get_contents(self, url, max_pages=20):
        """
        Convenience method to download a PDF file and converting it to text.
        """
        tf = self.pdf_download(url)
        if tf is not None:
            print "Download went ok, now trying to convert ..."
            result = self.pdf_to_text(tf.name, max_pages)
            print "Conversion was ok ..."
            return result
        else:
            print "Download did not go ok ..."
            return u''  # FIXME: should be something else ...

    def pdf_download(self, url):
        """
        Downloads a given url to a tempfile.
        """

        print "Downloading %s" % (url,)
        try:
            # GO has no wildcard domain for SSL
            r = self.http_session.get(url, verify=False)
            tf = tempfile.NamedTemporaryFile()
            tf.write(r.content)
            tf.seek(0)
            return tf
        except HTTPError as e:
            print "Something went wrong downloading %s" % (url,)
        except ZeroReturnError as e:
            print "SSL Zero return error %s" % (url,)
        except Exception as e:
            print "Some other exception %s" % (url,)

    def pdf_to_text(self, path, max_pages=20):
        """
        Method to convert a given PDF file into text file using a subprocess
        """

        if max_pages > 0:
            content = convert(path, range(0, max_pages))
        else:
            content = convert(path)

        return unicode(self.pdf_clean_text(content.decode('utf-8')))
