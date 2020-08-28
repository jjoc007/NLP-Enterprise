from mongo.saver import *
import pandas as pd
import texthero as hero


def consolidate():
    files_dictionary = get_all_file_dictionary()
    consolidate_list = {}
    for fd in files_dictionary:
        for word_fq in fd.get("word_frequency"):
            if consolidate_list.get(word_fq.get("word")) is None:
                consolidate_list[word_fq.get("word")] = {
                    "_id": word_fq.get("word"),
                    "freq": word_fq.get("frequency")
                }
            else:
                consolidate_list.get(word_fq.get("word"))["freq"] = consolidate_list.get(word_fq.get("word")).get("freq") + word_fq.get("frequency")

    list_words = []
    for key in consolidate_list.keys():
        list_words.append(consolidate_list.get(key))

    newlist = sorted(list_words, key=lambda k: k['freq'], reverse=True)

    #create bar consolidate
    words = []

    for word in newlist:
        words.append((word["_id"], word['freq']))

    #serieConsolidate = pd.DataFrame(words).set_index(0)[1]

    #n = serieConsolidate.head(40).plot.bar(rot=90, title="Top 40 words of all")
    #n.get_figure().savefig('consolidate_plot.jpg', format='jpg', bbox_inches="tight")

    save_company_dictionaries(newlist[0:100])
