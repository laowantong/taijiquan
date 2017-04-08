import json, os
from collections import OrderedDict

HEADER_TEMPLATE = """\
<h2>{french}</h2>\n
<table>
    <thead>
        <tr>
            <th>Chinois simplifié</th>
            <th>Pinyin</th>
            <th>Prononciation</th>
            <th>Français</th>
        </tr>
    </thead>
    <tbody>"""

ROW_TEMPLATE = """\
        <tr>
            <td>{simplified}</td>
            <td>{pinyin}</td>
            <td><audio controls><source src="audio/{simplified}.m4a"></audio></td>
            <td>{french}</td>
        </tr>"""

def create_categories(filename):
    db = json.loads(open(filename).read())
    categories = OrderedDict((category["id"], category) for category in db["categories"])
    for term in db["terms"]:
        for category in term["categories"]:
            categories[category]["terms"] = categories[category].get("terms", []) + [term]
    return categories

def generate_audio(categories):
    for category in categories.values():
        for term in category["terms"]:
            term["filename"] = term["simplified"] + ".m4a"
            if not os.path.isfile("audio/{filename}".format(**term)):
                if "correct_pronunciation" not in term:
                    term["correct_pronunciation"] = term["simplified"]
                os.system("say -v Ting-Ting -o 'audio/{filename}' {correct_pronunciation}".format(**term))

def html(categories):
    result = []
    for category in categories.values():
        result.append(HEADER_TEMPLATE.format(**category))
        for term in category["terms"]:
            result.append(ROW_TEMPLATE.format(**term))
        result.append('    </tbody>')
        result.append('</table>')
    return "\n".join(result)

def markdown():
    result = ["# Vocabulaire du _taiji quan_\n"]
    result.append("{% include vocabulary.html %}")
    return "\n".join(result)

def flashcards_deluxe(categories):
    result = ["\t".join(["Text 1", "Text 2", "Text 3", "Category 1"])]
    for category in categories.values():
        for term in category["terms"]:
            row = []
            row.append(term["pinyin"])
            row.append(term["simplified"] + "{{}}".format(term.get("correct_pronunciation", "")).replace("{}", ""))
            row.append(term["french"])
            row.append(category["id"])
            result.append("\t".join(row))
    return "\n".join(result)

if __name__ == "__main__":
    categories = create_categories("lexicon.json")
    generate_audio(categories)
    open("lexicon.tsv", "w").write(flashcards_deluxe(categories))
    # open(os.path.expanduser("~/Dropbox/Flashcards Deluxe/taiji.txt"), "w").write(flashcards_deluxe(categories))
    open("_includes/vocabulary.html", "w").write(html(categories))
    open("README.md", "w").write(markdown())
