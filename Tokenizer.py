from re import match

class Token():
    def __init__(self, token_name: str, value: str, Ln: int) -> None:
        self.token_name = token_name
        self.value = value
        self.Ln = Ln

    def __str__(self) -> str:
        return self.value
        # return f"{self.value}\t{self.token_name}\t{self.Ln}"

    @staticmethod
    def Tokenize(code_line: str, Ln: int) -> list:
        tokens = []
        codes = code_line.split()
        for code in codes:
            while code:
                for i in range(-1, 7):
                    result = Token.tokenMatch(code, i)
                    if result and result.span()[0] == 0:
                        if i == -1: return tokens
                        matched = code[result.span()[0]:result.span()[1]]
                        tokens.append(Token.createToken(i, matched, Ln))
                        code = code[result.span()[1]:]
                        break
        return tokens

    @staticmethod
    def createToken(t: int, word: str, Ln: int):
        if t == 0: return Token('keyword', word, Ln)
        if t == 1: return Token('Number', word, Ln)
        if t == 2: return Token('iden', word, Ln)
        if t == 3: return Token('Symbol', word, Ln)
        if t == 4: return Token('Comparison Operator', word, Ln)
        if t == 5: return Token('Operator', word, Ln)
        if t == 6: return Token('Logical Operator', word, Ln)      
    
    @staticmethod
    def tokenMatch(word, ktype):
        if ktype == -1: return match(r"(\/\/).*", word) # comment
        if ktype == 0: return match(r"if|for|while|function|of|let|return|Number|List|Null", word)
        if ktype == 1: return match(r"^-[0-9]+|[0-9]+", word)
        if ktype == 2: return match(r"^[a-zA-Z_][a-zA-Z_0-9]*", word)
        if ktype == 3: return match(r"[{}();:.,!]|=>|\]|\[", word) # { } ( ) ; : . , ! ] | =>
        if ktype == 4: return match(r"==|!=|<=|>=|>|<", word) # == != <= >= > | <
        if ktype == 5: return match(r"\+|\-|=|\*\*|\*|\/|%", word) # + - = ** * \
        if ktype == 6: return match(r"and|or", word)

match_list = []
pointer = 0
with open('src.txt', 'r') as src_file:
    Ln = 1
    for line in src_file:
        match_list += Token.Tokenize(line, Ln)
        Ln += 1