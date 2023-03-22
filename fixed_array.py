class Doc:
    def __init__(self, doc_id, terms):
        self.doc_id = doc_id
        self.terms = terms

if __name__ == "__main__":
    f = open("resource/sample_text.txt", "r")
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
    print(all_terms_setilize)
    # reversed_index = {}
    # for term in all_terms_setilize:
    #     for doc in docs_list:
    #         if term in doc.terms:
    #             if term in reversed_index.keys():
    #                 reversed_index[term].append(doc.doc_id)
    #             else:
    #                 reversed_index[term] = [doc.doc_id]
    #
    # print(reversed_index)