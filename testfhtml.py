import json
import spacy
from spacy.util import minibatch, compounding
from spacy.training import Example
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_sm")

# 预加载模型 添加标签
ner = nlp.get_pipe("ner")
for label in ["Time", "Place", "Adjectives", "Verb", "Relationship", "Acts", "People", "Numbers", "OtherNons", "Name", "Adverbs", "Meaningless", "Item", "Images", "Href", "Function", "Class", "Div"]:
    ner.add_label(label)

# 加载训练集
with open("full.jsonl", "r", encoding="utf-8") as f:
    TRAIN_DATA = []
    for line in f:
        data = json.loads(line)
        text = data["text"]
        entities = data["label"]
        annotations = {"entities": entities}
        TRAIN_DATA.append((text, annotations))

# 训练
n_iter = 100
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.begin_training()
    for i in range(n_iter):
        losses = {}
        batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            examples = []
            for i in range(len(texts)):
                examples.append(Example.from_dict(nlp.make_doc(texts[i]), annotations[i]))
            nlp.update(examples, drop=0.2, sgd=optimizer, losses=losses)
        print(f"Iteration {i}: Losses - {losses}")


# # HTML
def read_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        text_test = soup.get_text(separator="\n")
    return text_test

file_path = 'test2.html'
text_test = read_html(file_path)

doc = nlp(text_test)
print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])
