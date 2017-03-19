import json, os
from collections import OrderedDict

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
        result.append('<h2>%s</h2>\n' % category["french"])
        result.append('<table>')
        result.append('    <thead>')
        result.append('        <tr>')
        result.append('            <th>Chinous simplifié</th>')
        result.append('            <th>Prononciation</th>')
        result.append('            <th>Français</th>')
        result.append('        </tr>')
        result.append('    </thead>')
        result.append('    <tbody>')

        for term in category["terms"]:
            result.append('        <tr>')
            result.append('            <td>{simplified}</td>'.format(**term))
            result.append('            <td>')
            result.append('                <a href="audio/{simplified}.m4a">{pinyin}</a>'.format(**term))
            result.append('                <br/>')
            result.append('                <audio controls>')
            result.append('                    <source src="audio/{simplified}.m4a">'.format(**term))
            result.append('                </audio>')
            result.append('            </td>')
            result.append('            <td>{french}</td>'.format(**term))
            result.append('        </tr>')

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
    
    
