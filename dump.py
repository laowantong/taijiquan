import re, os
from collections import OrderedDict

HEADER_TEMPLATE = """\
<h2>{}</h2>
<table>
    <thead>
        <tr>
            <th>Chinois</th>
            <th>Pinyin</th>
            <th>Prononciation</th>
            <th>Littéralement</th>
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

def read_db(filename):
    result = OrderedDict()
    (header, rows) = open(filename).read().split("\n", 1)
    for match in re.finditer(r"(.+?)\t(.+?)(?:\{(.+?)\})?\t(.+?)\t(.*)", rows):
        (pinyin, simplified, reading, french, category) = match.groups()
        if category not in result:
            result[category] = []
        result[category].append({
            "pinyin": pinyin,
            "simplified": simplified,
            "reading": reading if reading else simplified,
            "french": french,
            "category": category
        })
    return result

def generate_audio(data):
    for terms in data.values():
        for term in terms:
            term["filename"] = term["simplified"] + ".m4a"
            if not os.path.isfile("audio/{filename}".format(**term)):
                os.system("say -v Ting-Ting -o 'audio/{filename}' {reading}".format(**term))

def cleanup_obsolete_audio(data):
    audio = set(term["filename"] for terms in data.values() for term in terms)
    obsolete_audio = [filename for filename in os.listdir("audio") if filename.endswith("m4a") and filename not in audio]
    for filename in obsolete_audio:
        os.remove("audio/" + filename)
    
def html(data):
    result = []
    for (category, terms) in data.items():
        result.append(HEADER_TEMPLATE.format(category))
        for term in terms:
            result.append(ROW_TEMPLATE.format(**term))
        result.append('    </tbody>')
        result.append('</table>')
    return "\n".join(result)


if __name__ == "__main__":
    data = read_db("lexicon.tsv")
    generate_audio(data)
    cleanup_obsolete_audio(data)
    open("_includes/vocabulary.html", "w").write(html(data))
