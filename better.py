from typing import final
import fitz
from bs4 import BeautifulSoup

print("imported")

pdf_file = "test.pdf"
doc = fitz.open(pdf_file)
print("pdf loaded")
template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
</head>
<body>
    {content}
</body>
</html>
"""


courses = [
        "SPG",
        "Sw Testing",
        "Industry 4.0",
        "SW Engg",
        "AI",
        "Deep learning",
        "PSM",
        "Algo Thinking",
        "BBN",
        "Fin Forensics",
        "Data Viz",
        "Market Research",
        "LSM",
        "Intro to BigData",
        "Design Thinking",



        ]



html_content = ""
for page in doc:
    page_html = page.get_text("html")
    page_soup = BeautifulSoup(page_html, "html.parser")
    tags = page_soup.find_all(True)
    for tag in tags:
        tag.attrs.pop("style", None)
    html_content += str(page_soup)
    cc = 0
    for tag in tags:
        course = ""
        html_content = ""
        csoup = BeautifulSoup(html_content, "html.parser")
        if tag.text in courses:
            csoup.append(tag)
            cc += 1
            course = tag.text
        if cc <= 1:
            csoup.append(tag)
        else:
            break
    html_content += str(csoup)
    print(html_content)
    final_html = template.format(title=course, content=html_content)
    with open(f"{course}.html", "w", encoding="utf-8") as f:
        f.write(final_html)





# Create the final HTML document using the template
# title = "Example Document"
#
#
# final_html = template.format(title=title, content=html_content)
#
#
# # Write the final HTML document to a file
# with open("output2.html", "w", encoding="utf-8") as file:
#     file.write(final_html)
