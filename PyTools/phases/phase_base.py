from bs4 import BeautifulSoup
import os

class Phase:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.html_files = {}
        self.soups = {}
    
    def open_htmls(self, labels):
        soups = []
        for label in labels:
            path = self.html_files[label]

            os.makedirs(os.path.dirname(path), exist_ok=True)
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
        os.makedirs(os.path.dirname(path), exist_ok=True) 
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(soup))

    def overwrite_html_by_id(self, soup: BeautifulSoup, element_id: str, html_string: str):
        target = soup.find(id=element_id)
        if not target:
            raise ValueError(f"[{self.name}] Could not find element with id='{element_id}'")
        target.clear()
        target.append(BeautifulSoup(html_string, "html.parser"))

    def append_html_by_id(self, soup: BeautifulSoup, element_id: str, html_string: str):
        target = soup.find(id=element_id)
        if not target:
            raise ValueError(f"[{self.name}] Could not find element with id='{element_id}'")
        target.append(BeautifulSoup(html_string, "html.parser"))

    def report(self) -> str:
        return "No report available."

    def enter(self):
        raise NotImplementedError(f"{self.name} must implement enter()")

    def exit(self):
        pass
