import json
import fitz
import re
from bs4 import BeautifulSoup, NavigableString


pdf_file = "test.pdf"
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

incorrect = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAArklEQVR4nGP4TyJgoLOGLYv+pzkiuEA2UASXhr+bFvxOtPm/pgNE/v8PZwPFsWv4Fmnyf0kDCK3p+JHjASQhXJA4Lid9CNT+P60YhICqwQyQCD4//P//ykf1/6T8/5UhQBLExu/pO8ZcILOzXKFoTQdIBJeGa1pMINWx5kD00JwfwgCKgMSxangxpfmiEsP/ED0Q+f8/nA0Ux+mkZxMbzsogRIBsoAgBTxMEg1ADADeCr4y88sA7AAAAAElFTkSuQmCC"

correct = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAACXBIWXMAAA7EAAAOxAGVKw4bAAABWUlEQVR4nGP4TyJgoImG8EV+QXO9iNUQttA3d3Ny5vp4z4mOhDWELvDJ2ZTUf7Gp9URVwrJw+xYLfBpC5ntnbUjoPd/Yfb4+cXmEQ6ulVZ0JVEPW7vj07THIqoPneQOd0XWuvvNcHdBs2yZzy1pjqJOydsWnbYupPJAbvyYUohroxYx1cZ1na9vP1sQvDbNpNLOoMYJ6OnNnXNrW6LaTlb3nGqKWBQK9GDjHM31tTNuZmtbTlbFLQqwbTM2rDeE2M6RuiUreEFm2N3vCpZbWk1VZmxJytyQ3n6xoOl0RszjYqt7ErMoQ2akgJ8WsDAaanbs1Gejc9jPVjafKGk+WRS0KAnrRtNIALSQY4F4MnOWZsia66VR53YmSyAWBQC+aVuhjBh0iWD0nObn3OcQsDgmf7w/0okm5HtawRokHYEjbNpsDvWhchl01ugYgAHrRqFQXl2osGggCAP5JY86bQRXXAAAAAElFTkSuQmCC"

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
foundation_courses = [
        "Maths2",
        "Statistics2",
        "CT",
        "Intro to Python",

        ]


ccd = {}



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
    ccd[sorted_courses[i]] = {}
    ccd[sorted_courses[i]]["soup"] = new_soup
    ccd[sorted_courses[i]]["questions"] = []
    ccd[sorted_courses[i]]["comprehensions"] = []


for course in ccd:
    qn_tags = []
    comp_tags = []
    level = ""
    level_tag = ccd[course]["soup"].find(
            "b",
            string="THIS IS QUESTION PAPER FOR THE SUBJECT"

            ).next_sibling
    if "DEGREE" in level_tag.string:
        level = "Degree"
    elif "DIPLOMA" in level_tag.string:
        level = "Diploma"
    else:
        level = "Foundation"

    ccd[course]["level"] = level

    no_of_qns = ccd[course]["soup"].find(
            "p",
            string="Number of Questions :"
            ).next_sibling.string
    marks = int(ccd[course]["soup"].find(
            "p",
            string="Section Marks :"
            ).next_sibling.string)

    no_of_qns = int(no_of_qns)
    ccd[course]["no_of_qns"] = no_of_qns
    ccd[course]["marks"] = marks
    qid_pattern = re.compile(r"Question Id :.*")
    qn_ids = list(ccd[course]["soup"].find_all("p", string=qid_pattern))
    for i in range(len(qn_ids)):
        q1 = qn_ids[i]
        q2 = qn_ids[i+1] if i+1 < len(qn_ids) else None
        tags = []
        while True:
            if q1 and q1 != q2:
                tags.append(q1)
                q1 = q1.next_sibling
            else:
                # print("one question tags collected for course: ", course, )
                break
        if "COMPREHENSION" in tags[0].string:
            comprehension = {}
            ignore = None
            for tag in tags:
                if tag.string == "Sub-Section Number :":
                    ignore = tags.index(tag)
                    break
            tags = tags[:ignore] if ignore else tags
            for tag in tags:
                if str(tag) == "<p><span></span></p>":
                    tags.remove(tag)
            comp_content = "".join([str(tag) for tag in tags])
            comp_soup = BeautifulSoup(comp_content, "html.parser")
            comprehension["soup"] = comp_soup
            comprehension["images"] = []
            qns = comp_soup.find(
                    "p",
                    string=re.compile(r"Question Numbers :.*")).string
            qns = qns.split(":")[1].strip().strip("(").strip(")").split("to")
            qns = list(range(int(qns[0]), int(qns[1])+1))
            comprehension["qns"] = qns
            start = comp_soup.find(
                    "p",
                    string="Question Label : Comprehension").next_sibling
            end = comp_soup.find("p", string="Sub questions")
            comp_content_strings = []
            while True:
                if start and start != end:
                    if start.name == "p":
                        comp_content_strings.append(start.string)
                        start = start.next_sibling
                    elif start.name == "img":
                        comprehension["images"].append(start["src"])
                        start = start.next_sibling
                else:
                    # print("One Coprehension collected for course: ", course)
                    break
            comp_content_strings = [s for s in comp_content_strings if isinstance(s, str)]
            # print(comp_content_strings)
            comp_content = "".join(comp_content_strings)
            comprehension["content"] = comp_content
            ccd[course]["comprehensions"].append(comprehension)

        else:
            qn = {}
            qn["images"] = []
            ignore = None
            for tag in tags:
                if tag.string == "Sub-Section Number :":
                    ignore = tags.index(tag)
                    break
            tags = tags[:ignore] if ignore else tags
            for tag in tags:
                if str(tag) == "<p><span></span></p>":
                    tags.remove(tag)

            qn_content = "".join([str(tag) for tag in tags])

            qn_soup = BeautifulSoup(qn_content, "html.parser")
            qn["soup"] = qn_soup
            qn["qn_no"] = int(tags[0].string.split(":")[1].split()[0])
            marks = qn_soup.find("b", string=re.compile("Correct Marks :.*")).string.split(":")[1].strip()[0]
            qn["marks"] = int(marks)
            
            if "Question Type : SA" in tags[0].string:
                qn["type"] = "SA"
                start = qn_soup.find(
                        "p",
                        string="Question Label : Short Answer Question"
                        ).next_sibling
                end = qn_soup.find(
                        "b",
                        string="Response Type :"
                        ).parent
                text = []
                while True:
                    if start and start != end:
                        if start.name == "p":
                            text.append(start.string)
                            start = start.next_sibling
                        elif start.name == "img":
                            qn["images"].append(start["src"])
                            start = start.next_sibling
                    else:
                        break
                text = [t for t in text if isinstance(t, str)]
                qn["text"] = "".join(text)

                response_type = qn_soup.find(
                        "b",
                        string="Response Type :").next_sibling.string
                qn["response_type"] = response_type
                answers_type = qn_soup.find(
                        "b",
                        string="Answers Type :")
                qn["answers_type"] = answers_type.next_sibling.string if answers_type else None

                possible_answers_tag = qn_soup.find(
                        "p",
                        string="Possible Answers :"
                        )
                possible_answers = possible_answers_tag.next_sibling.string if possible_answers_tag else None
                # print(possible_answers)

        
                if response_type == "Numeric" and answers_type.next_sibling.string == "Equal":
                    qn["possible_answers"] = float(possible_answers) if possible_answers else None
                elif response_type == "Numeric" and answers_type.next_sibling.string == "Range":
                    qn["possible_answers"] = [
                            float(x.strip()) for x in possible_answers.split("to")
                            ] if possible_answers else None
                elif response_type == "Alphanumeric" and not answers_type:
                    # print(qn_soup.prettify(), course)
                    qn["possible_answers"] = None
                elif response_type == "Alphanumeric" and answers_type.next_sibling.string == "Equal":
                    qn["possible_answers"] = possible_answers if possible_answers else None
                ccd[course]["questions"].append(qn)

            elif "Question Type : MCQ" in tags[0].string:
                qn["type"] = "SCQ"
                start = qn_soup.find(
                        "p",
                        string="Question Label : Multiple Choice Question"
                        ).next_sibling
                end = qn_soup.find(
                        "p",
                        string="Options :"
                        )
                text = []
                while True:
                    if start and start != end:
                        if start.name == "p":
                            text.append(start.string)
                            start = start.next_sibling
                        elif start.name == "img":
                            qn["images"].append(start["src"])
                            start = start.next_sibling
                    else:
                        break
                text = [t for t in text if isinstance(t, str)]
                qn["text"] = "".join(text)
                qn["choices"] = []
                start = qn_soup.find(
                        "p",
                        string="Options :"
                        ).next_sibling

                end = None
                while True:
                    choice = {}
                    if start and start != end:
                        # print(start)
                        if not start.string:
                            break
                        choice["id"] = start.string
                        bool_img = start.next_sibling
                        if not bool_img:
                            print(start, course, start.string)
                            print(qn_soup.prettify())
                            # break
                        # print(bool_img)
                        if bool_img.name == "img" and bool_img["src"] == correct:
                            choice["is_correct"] = True
                        elif bool_img.name == "img" and bool_img["src"] == incorrect:
                            choice["is_correct"] = False
                        else:
                            break
                        choice_content = bool_img.next_sibling
                        while True:
                            if choice_content.name == "p" and choice_content.string:
                                choice["text"] = choice_content.string
                                break
                            elif choice_content.name == "img":
                                choice["image"] = choice_content["src"]
                                break
                            else:
                                choice_content = choice_content.next_sibling
                        # if choice_content.name == "p":
                        #     choice["text"] = choice_content.string
                        # elif choice_content.name == "img":
                        #     choice["image"] = choice_content["src"]
                        # else:
                        #     print(f"choice id = {choice['id']} and type is {choice_content.name}")
                        # print(choice)
                        start = choice_content.next_sibling
                    else:
                        # print("one choice collected")
                        break

                    qn["choices"].append(choice)
                
                ccd[course]["questions"].append(qn)

            elif "Question Type : MSQ" in tags[0].string:
                qn["type"] = "MCQ"
                start = qn_soup.find(
                        "p",
                        string="Question Label : Multiple Select Question"
                        ).next_sibling
                end = qn_soup.find(
                        "p",
                        string="Options :"
                        )
                text = []
                while True:
                    if start and start != end:
                        if start.name == "p":
                            text.append(start.string)
                            start = start.next_sibling
                        elif start.name == "img":
                            qn["images"].append(start["src"])
                            start = start.next_sibling
                    else:
                        break
                text = [t for t in text if isinstance(t, str)]
                qn["text"] = "".join(text)
                qn["choices"] = []
                start = qn_soup.find(
                        "p",
                        string="Options :"
                        ).next_sibling

                end = None
                while True:
                    choice = {}
                    if start and start != end:
                        if not start.string:
                            break
                        choice["id"] = start.string
                        bool_img = start.next_sibling
                        if not bool_img:
                            print(start, course)
                        if bool_img.name == "img" and bool_img["src"] == correct:
                            choice["is_correct"] = True
                        elif bool_img.name == "img" and bool_img["src"] == incorrect:
                            choice["is_correct"] = False
                        else:
                            break
                        choice_content = bool_img.next_sibling
                        if choice_content.name == "p":
                            choice["text"] = choice_content.string
                        elif choice_content.name == "img":
                            choice["image"] = choice_content["src"]
                        start = choice_content.next_sibling
                    else:
                        # print("multiple choice collected")
                        break

                    qn["choices"].append(choice)
                ccd[course]["questions"].append(qn)


class BeautifulSoupEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BeautifulSoup):
            return str(obj)  # Convert BeautifulSoup object to its string representation
        return super().default(obj)


for c in ccd:
    with open(f"json/{c}.json", "w", encoding="utf-8") as f:
        json.dump(ccd[c], f, indent=4, ensure_ascii=False, cls=BeautifulSoupEncoder)











