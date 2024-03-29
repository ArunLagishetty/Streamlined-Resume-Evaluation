import spacy
import Distill

try:
    nlp = spacy.load('en_core_web_sm')

except ImportError:
    print("Spacy's English Language Modules aren't present \n Install them by doing \n python -m spacy download en_core_web_sm")


def _base_clean(text):
    """
    This function takes in text and performs various cleaning operations on it using the Distill
    library.
    
    :param text: The input text that needs to be cleaned
    :return: the cleaned text after performing tokenization, removal of stopwords, removal of tags, and
    lemmatization.
    """
    """
    Takes in text read by the parser file and then does the text cleaning.
    """
    text = Distill.tokenize(text)
    text = Distill.remove_stopwords(text)
    text = Distill.remove_tags(text)
    text = Distill.lemmatize(text)
    return text


def _reduce_redundancy(text):
    """
    Takes in text that has been cleaned by the _base_clean and uses set to reduce the repeating words
    giving only a single word that is needed.
    """
    return list(set(text))


def _get_target_words(text):
    """
    Takes in text and uses Spacy Tags on it, to extract the relevant Noun, Proper Noun words that contain words related to tech and JD. 

    """
    target = []
    sent = " ".join(text)
    doc = nlp(sent)
    for token in doc:
        if token.tag_ in ['NN', 'NNP']:
            target.append(token.text)
    return target



    """
    The function "Cleaner" takes in a text input, cleans it by removing redundancies and targeting
    specific words, and returns a list of the cleaned sentences.
    
    :param text: The input text that needs to be cleaned and processed. It is passed as an argument to
    the Cleaner function
    :return: The function `Cleaner` returns a list containing three elements: the original input text
    after being cleaned, the text with redundancy reduced, and the text with target words extracted.
    """
def Cleaner(text):
    sentence = []
    sentence_cleaned = _base_clean(text)
    sentence.append(sentence_cleaned)
    sentence_reduced = _reduce_redundancy(sentence_cleaned)
    sentence.append(sentence_reduced)
    sentence_targetted = _get_target_words(sentence_reduced)
    sentence.append(sentence_targetted)
    return sentence
