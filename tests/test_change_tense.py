from tenseflow import change_tense as ct


def test_present2future():
    assert 'I will love you' == ct('I love you', 'future')


def test_first_person():
    assert ct('I loved you', 'present') == 'I love you'
    assert ct('I said no', 'present') == 'I say no'


def test_infinitive():
    assert ct('I love to love', 'future') == 'I will love to love'


def test_ambiguous_pos():
    assert ct('It was a thought', 'future') == 'It will be a thought'


def test_plural():
    assert ct('The rabbits ran', 'present') == 'The rabbits run'
    assert ct('The rabbit ran', 'present') == 'The rabbit runs'


def test_from_future():
    assert ct('It will work', 'present') == 'It works'


def test_will_as_noun():
    assert ct('The will says otherwise.', 'past') == 'The will said otherwise.'
    assert ct('The will says otherwise.', 'future') == 'The will will say otherwise.'


def test_from_pluperfect():
    assert ct('He had walked to the store.', 'present') == 'He walks to the store.'
    assert ct('I had walked to the store.', 'present') == 'I walk to the store.'
    assert ct('I had walked to the store.', 'future') == 'I will walk to the store.'


def test_from_present_progressive():
    assert ct('I was going to the store', 'present') == 'I am going to the store'


def test_from_future_progressive():
    assert ct('I will be going to the store', 'present') == 'I am going to the store'


def test_from_present_perfect_tense():
    assert ct('I have gone to the store.', 'present') == 'I go to the store.'
    assert ct('I win because I have five cookies', 'past') == 'I won because I had five cookies'


def test_negation():
    assert ct('I did not go', 'present') == 'I do not go'
    assert ct('I do not go', 'past') == 'I did not go'
    assert ct('I do not go', 'future') == 'I will not go'


def test_from_future_perfect():
    assert ct('I will have been alive', 'future') == 'I will be alive'
    assert ct('I will have been alive', 'present') == 'I am alive'
    assert ct('I will have been alive', 'past') == 'I was alive'
    assert ct('I will have five cookies', 'past') == 'I had five cookies'


def test_bug1():
    # in some cases, present tense verb is marked as VB
    assert ct('I sleep here and run there', 'past') == 'I slept here and ran there'


def test_passive():
    assert ct('The rooms were filled with cupboards and book-shelves.', 'future') ==\
           'The rooms will be filled with cupboards and book-shelves.'
    assert ct('I am filled.', 'future') == 'I will be filled.'
    assert ct('I will be filled.', 'future') == 'I will be filled.'

#def test_imperative():
#    assert ct('First, go to the store', 'future') == 'First, go to the store'
