import string

from pattern.en import conjugate, PAST, PRESENT, SINGULAR, PLURAL
import spacy
from spacy.symbols import NOUN



SUBJ_DEPS = {'agent', 'csubj', 'csubjpass', 'expl', 'nsubj', 'nsubjpass'}

nlp = spacy.load('en_core_web_sm')


def _get_conjuncts(tok):
    """
    Return conjunct dependents of the leftmost conjunct in a coordinated phrase,
    e.g. "Burton, [Dan], and [Josh] ...".
    """
    return [right for right in tok.rights
            if right.dep_ == 'conj']


def is_plural_noun(token):
    """
    Returns True if token is a plural noun, False otherwise.

    Args:
        token (``spacy.Token``): parent document must have POS information

    Returns:
        bool
    """
    if token.doc.is_tagged is False:
        raise ValueError('token is not POS-tagged')
    return True if token.pos == NOUN and token.lemma != token.lower else False


def get_subjects_of_verb(verb):
    if verb.dep_ == "aux" and list(verb.ancestors):
        return get_subjects_of_verb(list(verb.ancestors)[0])
    """Return all subjects of a verb according to the dependency parse."""
    subjs = [tok for tok in verb.lefts
             if tok.dep_ in SUBJ_DEPS]
    # get additional conjunct subjects
    subjs.extend(tok for subj in subjs for tok in _get_conjuncts(subj))
    if not len(subjs):
        return get_subjects_of_verb(list(verb.ancestors)[0])
    return subjs


def is_plural_verb(token):
    if token.doc.is_tagged is False:
        raise ValueError('token is not POS-tagged')
    subjects = get_subjects_of_verb(token)
    if not len(subjects):
        return False
    plural_score = sum([is_plural_noun(x) for x in subjects])/len(subjects)

    return plural_score > .5


def change_tense(text, to_tense, nlp=nlp):
    """Change the tense of text.

    Args:
        text (str): text to change.
        to_tense (str): 'present','past', or 'future'
        npl (SpaCy model, optional):

    Returns:
        str: changed text.

    """
    tense_lookup = {'future': 'inf', 'present': PRESENT, 'past': PAST}
    tense = tense_lookup[to_tense]

    doc = nlp(text)

    out = list()
    out.append(doc[0].text)
    words = []
    for word in doc:
        words.append(word)
        if len(words) == 1:
            continue
        if (words[-2].text == 'will' and words[-2].tag_ == 'MD' and words[-1].tag_ == 'VB') or \
                        words[-1].tag_ in ('VBD', 'VBP', 'VBZ', 'VBN') or \
                (not words[-2].text in ('to', 'not') and words[-1].tag_ == 'VB'):

            if words[-2].text in ('were', 'am', 'is', 'are', 'was') or\
                    (words[-2].text == 'be' and len(words) > 2 and words[-3].text == 'will'):
                this_tense = tense_lookup['past']
            else:
                this_tense = tense

            subjects = [x.text for x in get_subjects_of_verb(words[-1])]
            if ('I' in subjects) or ('we' in subjects) or ('We' in subjects):
                person = 1
            elif ('you' in subjects) or ('You' in subjects):
                person = 2
            else:
                person = 3
            if is_plural_verb(words[-1]):
                number = PLURAL
            else:
                number = SINGULAR
            if (words[-2].text == 'will' and words[-2].tag_ == 'MD') or words[-2].text == 'had':
                out.pop(-1)
            if to_tense == 'future':
                if not (out[-1] == 'will' or out[-1] == 'be'):
                    out.append('will')
                # handle will as a noun in future tense
                if words[-2].text == 'will' and words[-2].tag_ == 'NN':
                    out.append('will')
            #if word_pair[0].dep_ == 'auxpass':
            out.append(conjugate(words[-1].text, tense=this_tense, person=person, number=number))
        else:
            out.append(words[-1].text)

        # negation
        if words[-2].text + words[-1].text in ('didnot', 'donot', 'willnot'):
            if tense == PAST:
                out[-2] = 'did'
            elif tense == PRESENT:
                out[-2] = 'do'
            else:
                out.pop(-2)

        # future perfect, and progressives, but ignore for "I will have cookies"
        if words[-1].text in ('have', 'has') and len(list(words[-1].ancestors)) and words[-1].dep_ == 'aux':
            out.pop(-1)

    text_out = ' '.join(out)

    for char in string.punctuation:
        if char in """(<['""":
            text_out = text_out.replace(char+' ', char)
        else:
            text_out = text_out.replace(' '+char, char)

    text_out = text_out.replace(" 's", "'s")  # fix posessive 's

    return text_out
