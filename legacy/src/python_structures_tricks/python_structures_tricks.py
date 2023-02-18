
def unpacking_a_sequence_into_variables():
    """
    Any sequence (or iterable) can be unpacked into variables
    using a simple assignment operation. The only requirement
    is that the number of the variables and structures match
    the sequence.

    Example:
        >>> p = (5, 6)
        >>> x, y = p
        >>> x
        5
        >>> y
        6

    Also works with structures.

    Example:
        >>> data = [ 'ACME', 50, 91.1, (2012, 12, 21)]
        >>> name, shares, price, date = data
        >>> name
        'ACME'
        >>> shares
        50
        >>> price
        91.1
        >>> date
        (2012, 12, 21)
    """
    pass

def unpacking_elements_from_iterables_of_arbitrary_length():
    """
    You can use Python star expression.

    >>> record = ('John', 'john@doe.com', '555-343-7272', '555-553-1212', 'blue')
    >>> name, email, *phones, eyes = record
    >>> name
    'John'
    >>> email
    'john@doe.com'
    >>> phones
    ('555-343-7272', '555-553-1212')
    >>> eyes
    'blue'
    """
    pass

if __name__ == '__main__':
    import doctest
    doctest.testmod( verbose=True)
