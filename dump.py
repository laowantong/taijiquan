import json, os
from collections import OrderedDict

HEADER_TEMPLATE = """\
<h2>{french}</h2>\n
<table>
    <thead>
        <tr>
            <th>Chinois simplifié</th>
            <th>Prononciation</th>
            <th>Français</th>
        </tr>
    </thead>
    <tbody>"""

ROW_TEMPLATE = """\
        <tr>
            <td>{simplified}</td>
            <td>
                <audio controls>
                    <source src="audio/{simplified}.m4a">
                </audio>
                <a href="audio/{simplified}.m4a">{pinyin}</a>
            </td>
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
            filename = term["simplified"] + ".m4a"
            if not os.path.isfile("audio/" + filename):
                os.system("say -v Ting-Ting -o 'audio/%s' %s" % (filename, term["simplified"]))

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

if __name__ == "__main__":
    categories = create_categories("lexicon.json")
    generate_audio(categories)
    open("_includes/vocabulary.html", "w").write(html(categories))
    open("README.md", "w").write(markdown())
    
    
