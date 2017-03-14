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
            if not os.path.isfile(filename):
                os.system("say -v Ting-Ting -o 'audio/%s' %s" % (filename, term["simplified"]))

def markdown(categories):
    result = ["# Vocabulaire du _taiji quan_"]
    for category in categories.values():
        result.append("## " + category["french"])
        result.append("Chinois simplifié | Prononciation | Français")
        result.append("|".join(["---"] * 3))
        for term in category["terms"]:
            result.append("{simplified} | [{pinyin}](https://raw.githubusercontent.com/laowantong/taijiquan/audio/{simplified}.mp4) | {french}".format(**term))
    return "\n".join(result)

if __name__ == "__main__":
    categories = create_categories("lexicon.json")
    generate_audio(categories)
    open("README.md", "w").write(markdown(categories))
    
    
