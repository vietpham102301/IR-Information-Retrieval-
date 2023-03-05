from query import intersect_with_skip_pointer


class Doc:
    def __init__(self, doc_id, terms):
        self.doc_id = doc_id
        self.terms = terms


class TermIndex:
    def __init__(self, term, num_of_docs):
        self.term = term
        self.num_of_docs = num_of_docs


if __name__ == "__main__":
    f = open("resource/doc-text", "r")
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
    # print(all_terms_setilize)
    reversed_index = {}
    for term in all_terms_setilize:
        for doc in docs_list:
            if term in doc.terms:
                if term in reversed_index.keys():
                    reversed_index[term].append(doc.doc_id)
                else:
                    reversed_index[term] = [doc.doc_id]

    # print(reversed_index)

    query_words = []

    query = True
    print("Enter words to query (enter each word seperated by enter, press 'q' to quit): ")
    while query:
        input_val = str(input())
        if input_val != 'q':
            query_words.append(input_val.lower())
        else:
            break

    sorted_query_words = []
    for word in query_words:
        term = word
        num_of_docs = len(reversed_index[word])
        sorted_query_words.append(TermIndex(term, num_of_docs))

    sorted_query_words = sorted(sorted_query_words, key=lambda term_index: term_index.num_of_docs)
    sorted_query_words = [term_index.term for term_index in sorted_query_words]

    if len(query_words) >= 1:
        first_term = query_words[0] #catch key that doesn't exist
        # p1 = []
        p1_with_optimize = []
        for i in range(len(query_words)-1):
            # p1 = reversed_index[first_term]
            p1_with_optimize = reversed_index[first_term]
            p2 = reversed_index[query_words[i+1]]
            # p1 = intersect(p1, p2)
            p1_with_optimize = intersect_with_skip_pointer(p1_with_optimize, p2)
        if len(query_words) == 1:
            p1 = reversed_index[first_term]
        # print(p1)
        # for id in p1:
        #     print(f"{docs_list[int(id)-1].doc_id}: {docs_list[int(id)-1].terms}")
        for i in p1_with_optimize:
            print(f"{docs_list[int(i) - 1].doc_id}: {docs_list[int(i) - 1].terms}")
            print("goes here")
        print("smt")
