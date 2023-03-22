import os
import time


class Doc:
    def __init__(self, doc_id, terms):
        self.doc_id = doc_id
        self.terms = terms


def load_to_ram(path):
    start_loading_time = time.time()
    f = open(path, "r")
    # print(f.read())
    docs = f.read()
    docs = docs.split("\n")
    pointers = docs[0].split(", ")
    pointers.pop()
    extract = []
    i = 0
    for p in pointers:
        extract.append(docs[1][i:int(p)])
        i = int(p)
    end_loading_time = time.time()
    print(f"loading time: {end_loading_time - start_loading_time}")
    return extract


def compress(path):
    f = open(path, "r")
    # print(f.read())
    docs = f.read()
    docs = docs.split("/")
    docs_list = []
    all_terms = []
    for doc in docs:
        id = doc.strip().split("\n")[0]
        content = ' '.join(doc.strip().split("\n")[1:])
        terms = list(filter(None, content.split(" ")))
        terms_normalize = [word.lower() for word in terms]
        doc_item = Doc(id, terms_normalize)
        # print(doc_item.doc_id)
        all_terms.extend(terms_normalize)
        docs_list.append(doc_item)

    docs_list.pop()
    all_terms.sort()
    # print(all_terms)
    all_terms_setilize = sorted(set(all_terms))
    pointers = []
    all_terms_in_a_string = ''
    file = open("dictionary_as_a_string.txt", "w")
    for term in all_terms_setilize:
        all_terms_in_a_string += term
        file.write(str(len(all_terms_in_a_string)) + ", ")
    file.write("\n")
    file.write(all_terms_in_a_string)
    file.close()


def size_after_compress(path):
    return os.path.getsize(path)

if __name__ == "__main__":
    compress(path="resource/doc-text")
    extract = load_to_ram(path="./dictionary_as_a_string.txt")
    print(extract)
    print(size_after_compress(path="./dictionary_as_a_string.txt"))


