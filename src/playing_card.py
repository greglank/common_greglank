class PlayingCard():
    """Represents a playing card.
    Originally designed to be completely agnostic to type of deck, with all
    relevant values set from Deck. However, added the lists of standard values
    so the class can be usable as a standalone playing card representation
    apart from Deck."""

    # Default values for a standard deck 
    # Long values in Title Case, short values in CAPS
    STD_VALUE_SHORT = [None, None, '2', '3', '4', '5', '6',
          '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    STD_VALUE_LONG = [None, None, 'Two', 'Three', 'Four', 'Five', 'Six',
          'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
    STD_VALUE_MINMAX = (2, 15)
    
    # Allow user to define sort for suits XXX
    # Long suits in Title Case, short suits in lowercase or symbol
    """
    # old representation
    STD_SUIT_LONG = [None, 'Hearts', 'Diamonds', 'Clubs', 'Spades']
    STD_SUIT_SHORT = [None, 'h', 'd', 'c', 's']
    STD_SUIT_SYMBOL = [None, '♥', '♦', '♣',  '♠']
    # STD_SUIT_SYMBOL = [None, '\u6526', '\u6626', '\u6326', '\u6026']
    """
    # new representation; ABC order
    STD_SUIT_LONG = [None, 'Clubs', 'Diamonds', 'Hearts', 'Spades']
    STD_SUIT_SHORT = [None, 'c', 'd', 'h', 's']
    STD_SUIT_SYMBOL = [None, '♣', '♦', '♥', '♠']
    # STD_SUIT_SYMBOL = [None, '\u6326', '\u6626', '\u6526', '\u6026']
    STD_SUIT_MINMAX = (1, 5)    

    printstyle_list = ['short', 'long', 'symbol']

    def __init__(self, value=0, suit=0, points=0, standard=True, printstyle='short'):
        """Typically constructed with suit and value (integers or strings).
        Can also call with a single nonzero integer ID if using a standard deck.
        If using a non-standard deck, be sure to call set_name and set_ID."""
        
        if standard:
            # if given single integer ID, convert to (value, suit)
            if isinstance(value, int) and isinstance(suit, int) and value > 0 and suit == 0:
                (value, suit) = PlayingCard.convert_ID(value)
            self.value = PlayingCard.convert_value(value)
            self.suit = PlayingCard.convert_suit(suit)
            self.set_name(PlayingCard.STD_VALUE_SHORT[self.value],
                          PlayingCard.STD_VALUE_LONG[self.value],
                          PlayingCard.STD_SUIT_SHORT[self.suit],
                          PlayingCard.STD_SUIT_LONG[self.suit],
                          PlayingCard.STD_SUIT_SYMBOL[self.suit])
            self.set_ID()
        else:
            self.value = value
            self.suit = suit
            self.name_value = str(value)
            self.name_value_long = str(value)
            self.name_suit = str(suit)
            self.name_suit_long = str(suit)
            self.name_symbol = str(suit)
            self.value_ID = 0  # integer ID, sorted by value
            self.suit_ID = 0  # integer ID, sorted by suit
        
        self.points = points    
        self.set_printstyle(printstyle)
        self.stored_hash = hash(self)  # what is this for?

    def __str__(self):
        '''Returns string format of card. Called by print() or str().'''
        if self.name_value is None or self.name_suit is None:
            return None
        elif self.printstyle_value == 2: #symbol
            return self.name_value + self.name_symbol
        elif self.printstyle_value == 1: #long
            return self.name_value_long + ' of ' + self.name_suit_long
        else:
            return self.name_value + self.name_suit

    def set_name(self, value_short, value_long, suit_short, suit_long, suit_symbol=None):
        """Set variations of the card's name"""

        if suit_symbol == None: suit_symbol = suit_short
        self.name_value = value_short
        self.name_value_long = value_long
        self.name_suit = suit_short
        self.name_suit_long = suit_long
        self.name_symbol = suit_symbol

    def set_ID(self, value_minmax=STD_VALUE_MINMAX, suit_minmax=STD_SUIT_MINMAX):
        """Set sorting ID based on range of cards in deck.
        Arguments are tuples in the form (inclusive, exclusive).
        Standard deck is (2, 15) and (1, 5)."""

        value_min, value_max = value_minmax
        suit_min, suit_max = suit_minmax

        # ordered by value, suit; standard deck is (value-2)*4 + suit
        self.value_ID = ((self.value - value_min) * (suit_max - suit_min)
            + (self.suit - suit_min + 1))

        # ordered by suit, value; standard deck is (suit-1)*13 + (value-1)
        self.suit_ID = ((self.suit - suit_min) * (value_max - value_min)
            + (self.value - value_min + 1))
        
    def set_printstyle(self, printstyle):
        """Select which variation of the printed name to use in print statements"""

        try:
            self.printstyle_value = PlayingCard.printstyle_list.index(printstyle)
        except:
            print('Bad printstyle: %s. Using short printstyle.' % printstyle)
            self.printstyle_value = 0    

    def is_value(self, target_value):
        """Check to see if card's value is equal to passed argument.
        Accepts strings or integers."""
        return self.value == target_value or self.name_value == target_value

    def is_suit(self, target_suit):
        """Check to see if card's suit is equal to passed argument.
        Accepts strings only."""
        return self.name_suit == target_suit

    def convert_ID(card_id, sort_by='value', value_minmax=STD_VALUE_MINMAX, suit_minmax=STD_SUIT_MINMAX):
        """Function: Converts an integer ID into a value and suit."""

        value_min, value_max = value_minmax
        suit_min, suit_max = suit_minmax
        
        if sort_by == 'suit':
            # ordered by suit, value
            val = (card_id - 1) % (value_max - value_min) + value_min
            suit = (card_id - 1) // (value_max - value_min) + suit_min
        else:
            # ordered by value, suit (default)
            if not sort_by == 'value':
                print('Bad sort type: %s. Sorting by value.' % sort_by)
            val = (card_id - 1) // (suit_max - suit_min) + value_min
            suit = (card_id - 1) % (suit_max - suit_min) + suit_min
        
        # print(f'Value: {val}, Suit: {suit}')
        return (val, suit)
            
    def convert_value(value, value_minmax=STD_VALUE_MINMAX,
                      short_list=STD_VALUE_SHORT, long_list=STD_VALUE_LONG):
        """Function: Converts an integer or string value
        to the appropriate integer value."""
        
        value_min, value_max = value_minmax
        if isinstance(value, int) and value >= value_min and value < value_max:
            return value
        elif isinstance(value, str):
            if value.isdigit():
                value = int(value)
                if value >= value_min and value < value_max:
                    return value
            elif value.upper() in short_list:
                return short_list.index(value.upper())
            elif value.title() in long_list:
                return long_list.index(value.title())
        return 0
    
    def convert_suit(suit, suit_minmax=STD_SUIT_MINMAX,
                     short_list=STD_SUIT_SHORT, long_list=STD_SUIT_LONG,
                     symbol_list=STD_SUIT_SYMBOL):
        """Function: Converts an integer or string suit
        to the appropriate integer suit."""
        
        suit_min, suit_max = suit_minmax
        if isinstance(suit, int) and suit >= suit_min and suit < suit_max:
            return suit
        elif isinstance(suit, str):
            if suit.isdigit():
                suit = int(suit)
                if suit >= suit_min and suit < suit_max:
                    return suit
            elif suit.upper() in short_list:
                return short_list.index(suit.upper())
            elif suit.title() in long_list:
                return long_list.index(suit.title())
            elif suit in symbol_list:
                return symbol_list.index(suit)
        return 0    

    def list_to_str(the_list):
        """Function: Return a list of PlayingCards as a string"""
        return '[%s]' % ', '.join(str(c) for c in the_list)

    def sort_list(the_list, desc=False, sort_by_suit=False):
        """Function: Sort a list of cards by value (default) or by suit.
        Sorts list in place (is that OK?), so no return value.
        Set desc=True to sort in descending order."""

        if sort_by_suit:
            sort_key = lambda card: card.suit_ID
        else:
            sort_key = lambda card: card.value_ID

        the_list.sort(key=sort_key, reverse=desc)

    def find_list(the_list, value=None, suit=None):
        """Function: Given a list of cards, return a list of cards that
        match given value and/or suit (None for value/suit means 'any')"""

        result_list = []
        for card in the_list:
            if (value == None or card.value == value) and (suit == None or card.suit == suit):
                result_list.append(card)

        return result_list

        #where the hell did this come from?!
        #if value == None and suit == None:
        #    return self.cards
        #elif suit == None:
        #    for card in self.cards:
        #        if card.value == value: result_list.append(card)
        #elif value == None:
        #    for card in self.cards:
        #        if card.suit == suit: result_list.append(card)
        #else:
        #    for card in self.cards:
        #        if card.value == value and card.suit == suit: result_list.append(card)




if __name__ == '__main__':
    for v in range(2, 15):
        for s in range (1, 5):
            c = PlayingCard(v, s, printstyle='long')
            print(c)
