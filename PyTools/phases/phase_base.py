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
        self._overwrite_html_by_selector(soup, f"#{element_id}", html_string)

    def overwrite_html_by_class(self, soup: BeautifulSoup, class_name: str, html_string: str):
        self._overwrite_html_by_selector(soup, f".{class_name}", html_string)

    def append_html_by_id(self, soup: BeautifulSoup, element_id: str, html_string: str):
        self._append_html_by_selector(soup, f"#{element_id}", html_string)

    def append_html_by_class(self, soup: BeautifulSoup, class_name: str, html_string: str):
        self._append_html_by_selector(soup, f"#{class_name}", html_string)

    def set_text_by_class(self, soup: BeautifulSoup, class_name: str, text: str) -> bool:
        """
        Finds the first element with the given class and replaces its inner content with text.
        Returns True if successful, False if element not found.
        """
        tag = soup.select_one(f".{class_name}")
        if tag:
            tag.clear()
            tag.append(text)
            return True
        return False

    def report(self) -> str:
        return "No report available."

    def enter(self):
        raise NotImplementedError(f"{self.name} must implement enter()")

    def exit(self):
        pass
    
    def _overwrite_html_by_selector(self, soup: BeautifulSoup, selector: str, html_string: str, before=False, after=False):
        tag = soup.select_one(selector)
        if not tag:
            raise ValueError(f"[{self.name}] Could not find element with selector '{selector}'")

        new_html = BeautifulSoup(html_string, "html.parser")

        if before:
            tag.insert_before(new_html)
        elif after:
            tag.insert_after(new_html)
        else:
            tag.clear()
            tag.append(new_html)

    def _append_html_by_selector(self, soup: BeautifulSoup, selector: str, html_string: str, before=False, after=False):
        tag = soup.select_one(selector)
        if not tag:
            raise ValueError(f"[{self.name}] Could not find element with selector '{selector}'")

        new_html = BeautifulSoup(html_string, "html.parser")

        if before:
            tag.insert_before(new_html)
        elif after:
            tag.insert_after(new_html)
        else:
            tag.append(new_html)
