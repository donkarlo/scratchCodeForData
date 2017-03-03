'''
But it’s probably less error-prone to do the parsing on the way in, which we can do by
creating a function that wraps csv.reader. We’ll give it a list of parsers, each specify‐
ing how to parse one of the columns. And we’ll use None to represent “don’t do any‐
thing to this column”:
'''
def parse_row_dont_use(input_row, parsers):
    """given a list of parsers (some of which may be None)
    apply the appropriate one to each element of the input_row"""
    return [parser(value) if parser is not None else value
        for value, parser in zip(input_row, parsers)]
            
'''
What if there’s bad data? A “float” value that doesn’t actually represent a number?
We’d usually rather get a None than crash our program. We can do this with a helper
function:
'''
def try_or_none(f):
    """wraps f to return None if f raises an exception
    assumes f takes only one input"""
    def f_or_none(x):
        try: 
            return f(x)
        except: 
            return None
    return f_or_none
    
'''use this one'''
def parse_row(input_row, parsers):
    return [try_or_none(parser)(value) if parser is not None else value
        for value, parser in zip(input_row, parsers)]


def parse_rows_with(reader, parsers):
    """wrap a reader to apply the parsers to each of its rows"""
    for row in reader:
        yield parse_row(row, parsers)
        
'''EXAMPLE
for data
6/20/2014,AAPL,90.91
6/20/2014,MSFT,41.68
6/20/3014,FB,64.5
6/19/2014,AAPL,91.86
6/19/2014,MSFT,n/a
6/19/2014,FB,64.34
'''
import dateutil.parser
import csv
data = []
with open("comma_delimited_stock_prices.csv", "rb") as f:
    reader = csv.reader(f)
    for line in parse_rows_with(reader, [dateutil.parser.parse, None, float]):
        data.append(line)

'''after which we just need to check for None rows:
'''
for row in data:
    if any(x is None for x in row):
        print row
        
def try_parse_field(field_name, value, parser_dict):
    """try to parse value using the appropriate function from parser_dict"""
    parser = parser_dict.get(field_name)
     # None if no such entry
    if parser is not None:
        return try_or_none(parser)(value)
    else:
        return value

def parse_dict(input_dict, parser_dict):
    return { field_name : try_parse_field(field_name, value, parser_dict)
        for field_name, value in input_dict.iteritems() }


