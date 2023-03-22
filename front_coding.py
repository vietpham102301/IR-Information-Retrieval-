import os
import time


def blocked_storage(path):
    f = open(path, "r")
    # print(f.read())
    docs = f.read()
    docs = docs.split("/")
    all_terms = []
    for doc in docs:
        content = ' '.join(doc.strip().split("\n")[1:])
        terms = list(filter(None, content.split(" ")))
        terms_normalize = [word.lower() for word in terms]
        # print(doc_item.doc_id)
        all_terms.extend(terms_normalize)

    all_terms.sort()
    # print(all_terms)
    all_terms_setilize = sorted(set(all_terms))
    print(all_terms_setilize)
    count = 0
    file = open("step1_blocked_storage.txt", "w")
    result = ''
    for term in all_terms_setilize:
        if count % 4 == 0:
            file.write(str(len(result)) + ", ")
            count = 0
        result += (str(len(term)) + term)
        count += 1

    file.write("\n")
    file.write(result)
    file.close()


def compress(path):
    f = open(path, "r")
    # print(f.read())
    docs = f.read()
    docs = docs.split("\n")
    print(docs[0])
    print(docs[1])
    prefixes = []
    extract = []
    k = 0
    for i in range(len(docs[1])):
        if (k + 1 < len(docs[1])) and (docs[1][k] + docs[1][k + 1]).isdigit():
            word = ''
            start_index = k + 2
            for j in range(int(docs[1][k] + docs[1][k + 1])):
                word += docs[1][start_index + j]
            extract.append(word)
            k += 1
        elif (docs[1][k]).isdigit():
            word = ''
            start_index = k + 1
            for j in range(int(docs[1][k])):
                word += docs[1][start_index + j]
            extract.append(word)
        k += 1
        if k == len(docs[1]):
            break

    print(extract)
    count = 0
    sub_list = []
    temp_list = []
    for i in range(len(extract)):
        temp_list.append(extract[i])
        count += 1
        if count % 4 == 0:
            sub_list.append(temp_list)
            temp_list = []
        elif i == len(extract) - 1 and count % 4 != 0:
            sub_list.append(temp_list)
    print(sub_list)
    for ele in sub_list:
        prefixes.append(find_prefix(ele))

    print(prefixes)
    m = 0
    res = ''
    file = open("front_coding_res.txt", "w")
    for block in sub_list:
        n = 0
        for ele in block:
            if n == 0 and prefixes[m] != '':
                res += (str(len(ele)) + prefixes[m] + '*' + word_without_prefix(prefix=prefixes[m], word=ele))
            else:
                if prefixes[m] != '':
                    res += (str(len(word_without_prefix(prefixes[m], ele))) + '-' + word_without_prefix(
                        prefix=prefixes[m], word=ele))
                else:
                    res += str(len(ele)) + ele
            n += 1
        m += 1

    file.write(res)


def find_prefix(a_list):
    min_len = 100000
    for ele in a_list:
        if len(ele) < min_len:
            min_len = len(ele)

    prefix = ''
    for i in range(min_len):
        if len(a_list) == 1:
            prefix = a_list[0]
        if len(a_list) == 2:
            if a_list[0][i] == a_list[1][i]:
                prefix += a_list[0][i]
        if len(a_list) == 3:
            if a_list[0][i] == a_list[1][i] == a_list[2][i]:
                prefix += a_list[0][i]
        if len(a_list) == 4:
            if a_list[0][i] == a_list[1][i] == a_list[2][i] == a_list[3][i]:
                prefix += a_list[0][i]

    return prefix


def word_without_prefix(prefix, word):
    len_prefix = len(prefix)
    return word[len_prefix:]


def size_after_compress(path):
    return os.path.getsize(path)


def load_to_ram(path):
    start_loading_time = time.time()
    f = open(path, "r")
    docs = f.read()
    prefix = ''
    word = ''
    extract = []
    count = 0
    for i in range(len(docs)):
        if docs[i].isdigit() and docs[i+1] != '-': #handle a specific case that the digit is two number
            k = i+1
            m = i+1
            for j in range(int(docs[i])):
                if docs[k] != '*':
                    word += docs[k]
                k += 1
            for l in range(int(docs[i])):
                if docs[k] == '*':
                    break
                prefix += docs[k]
                m += 1
            extract.append(word)
            word = ''
            count += 1
        elif docs[i].isdigit() and docs[i+1] == '-':
            k = i+1
            word += prefix
            for j in range(int(docs[i])):
                if docs[k] != '-':
                    word += docs[k]
                    k += 1
                extract.append(word)
                word = ''
                count += 1
        if count % 4 == 0 and count != 0:
            prefix = ''
    end_loading_time = time.time()
    print(f"loading time: {end_loading_time - start_loading_time}")
    return extract


if __name__ == "__main__":
    # blocked_storage("resource/sample_text.txt")
    compress("./step1_blocked_storage.txt")
    extract = load_to_ram("./front_coding_res.txt")
    print(extract)