import urllib, re
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

class RFC:

    localRFCs = {}
    recursion = False

    def __init__(self, id, is_ref=False, recursion=False):
        self.recursion = recursion
        self.id = id
        self.url = 'https://tools.ietf.org/html/rfc' + self.id
        self.title = ""
        self.obsoleted = False
        self.references = {}
        if self.id not in self.localRFCs.keys():
            self.localRFCs[self.id] = self
        self.data = "N/A"
        self.parseData(is_ref)

    def parseData(self, is_ref):
        data = self.fetchRFC()
        if data[0] == "text/html":
            self.data = data[1]
            self.title = self.data.title.string
            if not is_ref or self.recursion:
                self.parseReferences()
            for docinfo in self.data.findAll('span', class_='pre noprint docinfo'):
                if re.match('^Obsoleted\ by', docinfo.text) is not None:
                    self.obsoleted = True
                    obsoleted_by_id = re.sub('^Obsoleted\ by:\ ', '', re.sub('\ {2,}.*', '', docinfo.text))
                    if obsoleted_by_id not in self.localRFCs.keys():
                        self.obsoleted_by = RFC(obsoleted_by_id, True, self.recursion)
                    else:
                        self.obsoleted_by = self.localRFCs[obsoleted_by_id]
        elif data[0] == "application/pdf":
            self.title = "Unparseable (Only PDF document was accessible at " + self.url + ")"
        else:
            self.title = "Unparseable (Please check if " + self.url + " is a HTML document)"



    def fetchRFC(self):
        req = urllib.request.Request(self.url)
        try:
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            print("Error: HTTP-Status {:d} while fetching {:s}".format(e.code, self.url))
            return [None, None]
        return [response.info().get_content_type(), BeautifulSoup(response.read(), 'lxml')]

    def parseReferences(self):
        for link in self.data.findAll('a', attrs={'href': re.compile('^\.\/rfc[0-9]{1,4}')}):
            ref = link.get('href')
            ref_id = re.sub('\.\/rfc', '', re.sub('#.*', '', ref))
            if not ref_id == self.id:
                if ref_id not in self.references.keys():
                    if ref_id in self.localRFCs.keys():
                        rfc_reference = self.localRFCs[ref_id]
                    else:
                        rfc_reference = RFC(ref_id, True, self.recursion)
                self.references[ref_id] = rfc_reference

    def getTitle(self):
        return self.title

    def getURL(self):
        return self.url.__str__()

    def getReferences(self):
        return self.references.keys().__str__()

    def getReferenceTitles(self):
        reference_titles = []
        for reference in self.references.values():
            reference_titles.append(reference.getTitle())
        return reference_titles
