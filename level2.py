import fitz
import re
from bs4 import BeautifulSoup, NavigableString


pdf_file = "diploma_paper.pdf"
doc = fitz.open(pdf_file)
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
        "Maths2",
        "Statistics2",
        "CT",
        "Intro to Python",
        "DBMS",
        "PDSA",
        "AppDev1",
        "MLF",
        "Java",
        "AppDev2",
        "MLT",
        "MLP",
        "BDM",
        "Business Analytics",
        "System Commands",
        ]

# courses = [
#         "SPG",
#         "Sw Testing",
#         "Industry 4.0",
#         "SW Engg",
#         "AI",
#         "Deep learning",
#         "PSM",
#         "Algo Thinking",
#         "BBN",
#         "Fin Forensics",
#         "Data Viz",
#         "Market Research",
#         "LSM",
#         "Intro to BigData",
#         "Design Thinking",
#
#
#
#         ]

html_content = ""
for page in doc:
    page_html = page.get_text("html")
    page_soup = BeautifulSoup(page_html, "html.parser")
    tags = page_soup.find_all(True)

    for tag in tags:
        tag.attrs.pop("style", None)

    html_content += str(page_soup)

tsoup = BeautifulSoup(html_content, "html.parser")
html_str = str(tsoup.prettify())

html_list = html_str.split("\n")
html_list.append("<p>end_of_paper</p>")
while True:
    try:
        html_list.remove("<div id=\"page0\">")
        html_list.remove("</div>")
    except ValueError:
        break

html_content = "".join(html_list)
html_content = re.sub(r">[\s]+<", "><", html_content)


final_html = template.format(title="All Courses", content=html_content)
full_soup = BeautifulSoup(final_html, "html.parser")
strings = full_soup.find_all(string=True)
for string in strings:
    if string.strip():
        string.replace_with(string.strip())

strings = full_soup.find_all(string=True)


sorted_courses = sorted(courses, key=lambda x: list(strings).index(x))
sorted_courses.append("end_of_paper")
# print(sorted_courses)

for i in range(len(sorted_courses)-1):
    c1 = full_soup.find("p", string=sorted_courses[i])
    c2 = full_soup.find("p", string=sorted_courses[i+1])
    tags = []
    while True:
        if c1 and c1 != c2:
            tags.append(c1)
            c1 = c1.next_sibling
        else:
            break
    content = "".join([str(tag) for tag in tags])
    new_soup = BeautifulSoup(content, "html.parser")
    with open(f"{sorted_courses[i]}.html", "w", encoding="utf-8") as f:
        f.write(new_soup.prettify())
