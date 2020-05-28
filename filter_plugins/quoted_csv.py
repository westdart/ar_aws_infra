def quoted_csv(the_array):
    '''
    Args:
        the_array: Array of strings
    Returns: String with each string double quoted and separated by commas
    '''
    result = ""
    for entry in the_array:
        result = (result + ',"' + entry + '"')
    return result[1:] if len(the_array) > 0 else result


class FilterModule(object):
    '''
    custom jinja2 filters for working with collections
    '''

    def filters(self):
        return {
            'quoted_csv': quoted_csv
        }


'''
Testing
'''
import unittest


class TestQuotedCsv(unittest.TestCase):

    def test_quoted_csv_empty(self):
        result = quoted_csv([])
        self.assertEqual("", result)

    def test_quoted_csv_single(self):
        result = quoted_csv(['this'])
        self.assertEqual('"this"', result)

    def test_quoted_csv_multiple(self):
        result = quoted_csv(['this', 'is', 'a', 'test'])
        self.assertEqual('"this","is","a","test"', result)


if __name__ == '__main__':
    unittest.main()
