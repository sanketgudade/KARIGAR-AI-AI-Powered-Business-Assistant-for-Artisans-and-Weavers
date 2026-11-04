import re
from html.parser import HTMLParser

with open('frontend/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

class TagValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in self.void_tags:
            self.stack.append((tag.lower(), self.getpos()))

    def handle_endtag(self, tag):
        t = tag.lower()
        if t in self.void_tags:
            return
        if not self.stack:
            self.errors.append(f"Unexpected closing tag </{t}> at line {self.getpos()[0]}")
            return
        top, pos = self.stack.pop()
        if top != t:
            self.errors.append(f"Mismatched tag: expected </{top}> (opened line {pos[0]}), got </{t}> at line {self.getpos()[0]}")

v = TagValidator()
v.feed(content)
print(f"HTML Validation completed. Errors: {len(v.errors)}")
for err in v.errors[:10]:
    print(" ", err)
if v.stack:
    print(f"Unclosed tags count: {len(v.stack)}")
    for tag, pos in v.stack[:5]:
        print(f"  <{tag}> opened at line {pos[0]}")
else:
    print("All HTML tags closed properly!")
