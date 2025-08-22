from bs4 import BeautifulSoup

class Phase:
    def __init__(self, name):
        self.name = name
        self.html_files = {}      # e.g., {"index": "../docs/index.html"}
        self.soups = {}           # {"index": BeautifulSoup instance}

    def open_htmls(self, labels):
        """Opens and parses HTML files by label. Returns list of soups in order."""
        soups = []
        for label in labels:
            path = self.html_files[label]
            with open(path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                self.soups[label] = soup
                soups.append(soup)
        return soups


    def write_html(self, label):
        path = self.html_files.get(label)
        soup = self.soups.get(label)
        if not path or not soup:
            print(f"[{self.name}] ERROR: Cannot write HTML for '{label}'")
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(soup))

    def overwrite_html_by_id(self, soup: BeautifulSoup, element_id: str, new_html: str):
        target = soup.find(id=element_id)
        if target:
            target.clear()
            new_soup = BeautifulSoup(new_html, "html.parser")
            for child in new_soup.contents:
                target.append(child)
        else:
            print(f"[{self.name}] WARN: Element with id='{element_id}' not found.")

    def enter(self):
        raise NotImplementedError(f"{self.name} must implement enter()")

    def exit(self):
        pass

    def overwrite_html_by_id(self, soup: BeautifulSoup, element_id: str, html_string: str):
        target = soup.find(id=element_id)
        if not target:
            raise ValueError(f"Could not find element with id='{element_id}'")
        target.clear()
        target.append(BeautifulSoup(html_string, "html.parser"))

    def append_html_by_id(self, soup: BeautifulSoup, element_id: str, html_string: str):
        target = soup.find(id=element_id)
        if not target:
            raise ValueError(f"Could not find element with id='{element_id}'")
        target.append(BeautifulSoup(html_string, "html.parser"))
