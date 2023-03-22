import math


class Doc:
    def __init__(self, doc_id, terms):
        self.score = None
        self.doc_id = doc_id
        self.terms = terms

    def set_score(self, score):
        self.score = score


class QueryWord:
    def __init__(self, word, frequency):
        self.word = word
        self.frequency = frequency


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

    docs_freq_dic = {}
    term_freq = []
    for term in all_terms_setilize:
        list_freq_of_term = []
        for doc in docs_list:
            if term in doc.terms:
                if term in docs_freq_dic.keys():
                    docs_freq_dic[term] += 1
                else:
                    docs_freq_dic[term] = 1

            freq = 0
            for word in doc.terms:
                if word == term:
                    freq += 1
            list_freq_of_term.append(freq)
        term_freq.append(list_freq_of_term)

    dic_for_IDF = {}
    for key in all_terms_setilize:
        dic_for_IDF[key] = math.log(len(docs_list) / docs_freq_dic[key], 10)

    query_vector = [0] * len(all_terms_setilize)
    weight_matrix = []
    i = 0
    for list_i in term_freq:
        list_temp = []
        term_i = all_terms_setilize[i]
        for tf in list_i:
            list_temp.append(tf * dic_for_IDF[term_i])
        weight_matrix.append(list_temp)
        i += 1

    print("enter the search keywords seperated by space: ")
    query_words = str(input())
    input_words = query_words.split()
    input_words_setilize = set(input_words)
    input_list = []

    for word in input_words_setilize:
        count = 0
        for w in input_words:
            if word == w:
                count += 1
        qw = QueryWord(word, count)
        input_list.append(qw)

    j = 0
    for term in all_terms_setilize:
        for word in input_list:
            if term == word.word:
                query_vector[j] = word.frequency * dic_for_IDF[term]
        j += 1

    # matrix transposition
    matrix = []
    for i in range(len(docs_list)):
        temp = []
        for list_i in weight_matrix:
            temp.append(list_i[i])
        matrix.append(temp)

    # cal the sim
    k = 0
    for doc_vec in matrix:
        numerator = 0
        denominator = 0
        score = 0
        pre_denom_1 = 0
        pre_denom_2 = 0

        for i in range(len(doc_vec)):
            numerator += doc_vec[i]*query_vector[i]
            pre_denom_1 += doc_vec[i]**2
            pre_denom_2 += query_vector[i]**2

        denominator = math.sqrt(pre_denom_1) * math.sqrt(pre_denom_2)
        score = numerator / denominator

        docs_list[k].set_score(score)
        k += 1
    print(k)
    print(len(docs_list))
    docs_list_sorted = sorted(docs_list, key=lambda d: d.score, reverse=True)
    print("here are the top 4 search results")
    for i in range(4):
        print(f"id: {docs_list_sorted[i].doc_id}, score: {docs_list_sorted[i].score}")