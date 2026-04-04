"""
    encode num1 as function (symbolic lambda expression)
    encode num2 as function (symbolic lambda expression)
    build addition function (symbolic lambda expression)
    apply them
    reduce symbolic expression step-by-step
    decode the result and piece it back into an integer
"""
class FreshVar:
    # generate fresh variable names during alpha-renaming
    # => prevents variable capture during substitution
    def __init__(self):
        self.counter = 0

    def generate(self, base):
        # increment counter
        self.counter += 1

        # return fresh name
        return f"{base}_{self.counter}"

class Expr:
    # base class for all lambda calculus expressions
    def occurs_free(self, var):
        # check whether variable occurs free in expression
        raise NotImplementedError

    def substitute(self, var, value, fresh):
        # substitute all free occurrences of var with value
        raise NotImplementedError

    def beta_reduce(self, fresh):
        # perform one beta-reduction step
        raise NotImplementedError

    def reduce_normal_form(self):
        # repeatedly reduce until expression no longer changes
        current = self
        fresh = FreshVar()

        while True:
            next_expr = current.beta_reduce(fresh)

            if next_expr == current:
                return current

            current = next_expr

    def reduce_normal_form_print(self):
        # repeatedly reduce and print every intermediate step
        current = self
        fresh = FreshVar()
        step = 0

        while True:
            print(f"step {step} => {current.pretty()}")
            next_expr = current.beta_reduce(fresh)

            if next_expr == current:
                return current

            current = next_expr
            step += 1

    def pretty(self):
        # render expression in lambda-calculus syntax
        raise NotImplementedError

    def print_tree(self):
        # print AST in tree form
        self._print_tree_internal("", True)

    def _print_tree_internal(self, prefix, is_last):
        raise NotImplementedError

class Var(Expr):
    # variable node
    # example => x
    def __init__(self, name):
        self.name = name

    def occurs_free(self, var):
        # variable occurs free if names match
        return self.name == var

    def substitute(self, var, value, fresh):
        # replace variable if names match
        if self.name == var:
            return value

        # otherwise keep original variable
        return Var(self.name)

    def beta_reduce(self, fresh):
        # variable cannot be reduced further
        return Var(self.name)

    def pretty(self):
        return self.name

    def _print_tree_internal(self, prefix, is_last):
        connector = "└─" if is_last else "├─"
        print(f"{prefix}{connector}Var({self.name})")

    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name

    def __repr__(self):
        return f"Var({self.name!r})"

class Abs(Expr):
    # abstraction node
    # example => λx.body
    def __init__(self, param, body):
        self.param = param
        self.body = body

    def occurs_free(self, var):
        # free occurrence exists only if:
        # current binder is not same variable
        # and body contains free occurrence
        return self.param != var and self.body.occurs_free(var)

    def substitute(self, var, value, fresh):
        # if abstraction parameter is same as target variable
        # => stop substitution here
        if self.param == var:
            return Abs(self.param, self.body)

        # if replacement value contains current parameter as a free variable
        # => alpha-rename current parameter first
        if value.occurs_free(self.param):
            new_param = fresh.generate(self.param)

            # rename all bound uses of old parameter inside body
            renamed_body = self.body.substitute(self.param, Var(new_param), fresh)

            # continue substitution with renamed abstraction
            return Abs(new_param, renamed_body.substitute(var, value, fresh))

        # otherwise safely substitute inside body
        return Abs(self.param, self.body.substitute(var, value, fresh))

    def beta_reduce(self, fresh):
        # reduce inside abstraction body
        return Abs(self.param, self.body.beta_reduce(fresh))

    def pretty(self):
        return f"λ{self.param}.({self.body.pretty()})"

    def _print_tree_internal(self, prefix, is_last):
        connector = "└─" if is_last else "├─"
        print(f"{prefix}{connector}Abs {self.param}")

        new_prefix = prefix + ("  " if is_last else "│ ")
        self.body._print_tree_internal(new_prefix, True)

    def __eq__(self, other):
        return (
            isinstance(other, Abs)
            and self.param == other.param
            and self.body == other.body
        )

    def __repr__(self):
        return f"Abs({self.param!r}, {self.body!r})"

class App(Expr):
    # application node
    # example => (f x)
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def occurs_free(self, var):
        # free occurrence can appear in function or argument
        return self.func.occurs_free(var) or self.arg.occurs_free(var)

    def substitute(self, var, value, fresh):
        # substitute inside both function and argument
        return App(
            self.func.substitute(var, value, fresh),
            self.arg.substitute(var, value, fresh),
        )

    def beta_reduce(self, fresh):
        # if function position is an abstraction
        # => perform beta-reduction immediately
        if isinstance(self.func, Abs):
            return self.func.body.substitute(self.func.param, self.arg, fresh)

        # otherwise reduce function side first
        new_func = self.func.beta_reduce(fresh)

        if new_func != self.func:
            return App(new_func, self.arg)

        # if function side did not change
        # => reduce argument side
        return App(self.func, self.arg.beta_reduce(fresh))

    def pretty(self):
        return f"({self.func.pretty()} {self.arg.pretty()})"

    def _print_tree_internal(self, prefix, is_last):
        connector = "└─" if is_last else "├─"
        print(f"{prefix}{connector}App")

        new_prefix = prefix + ("  " if is_last else "│ ")
        self.func._print_tree_internal(new_prefix, False)
        self.arg._print_tree_internal(new_prefix, True)

    def __eq__(self, other):
        return (
            isinstance(other, App)
            and self.func == other.func
            and self.arg == other.arg
        )

    def __repr__(self):
        return f"App({self.func!r}, {self.arg!r})"

def var(name):
    # build variable node
    return Var(name)

def abs_expr(param, body):
    # build abstraction node
    return Abs(param, body)

def app(func, arg):
    # build application node
    return App(func, arg)

def church(n):
    """
        build Church numeral for non-negative integer n

        example =>
        church(3)
        =>
        λf.λx. f (f (f x))
    """
    body = "x"

    for _ in range(n):
        body = f"(f {body})"

    return parse(f"λf.λx.{body}")

def church_to_usize(expr):
    """
        convert Church numeral back into Python integer

        expected shape =>
        λf.λx. f (f (f x))
    """

    # must be first abstraction
    if not isinstance(expr, Abs):
        return None

    f_name = expr.param
    body1 = expr.body

    # must be second abstraction
    if not isinstance(body1, Abs):
        return None

    x_name = body1.param
    body2 = body1.body

    def count(e):
        # base case =>
        # reached x => zero applications
        if isinstance(e, Var) and e.name == x_name:
            return 0

        # recursive case =>
        # expression looks like (f something)
        if isinstance(e, App) and isinstance(e.func, Var) and e.func.name == f_name:
            inner = count(e.arg)

            if inner is not None:
                return inner + 1

        # anything else is not a Church numeral
        return None

    return count(body2)

class Token:
    # tokenizer symbols
    LAMBDA = "LAMBDA"
    DOT = "DOT"
    LP = "LP"
    RP = "RP"
    IDENT = "IDENT"
    NUMBER = "NUMBER"

def tokenize(text):
    """
        turn lambda-calculus string into tokens

        supports:
        - λ
        - /
        - \
        as lambda symbols
    """
    tokens = []
    i = 0

    while i < len(text):
        c = text[i]

        if c in ("λ", "/", "\\"):
            tokens.append((Token.LAMBDA, c))
            i += 1
        elif c == ".":
            tokens.append((Token.DOT, c))
            i += 1
        elif c == "(":
            tokens.append((Token.LP, c))
            i += 1
        elif c == ")":
            tokens.append((Token.RP, c))
            i += 1
        elif c.isspace():
            i += 1
        elif c.isalpha():
            ident = c
            i += 1

            while i < len(text) and text[i].isalnum():
                ident += text[i]
                i += 1

            tokens.append((Token.IDENT, ident))
        elif c.isdigit():
            num = c
            i += 1

            while i < len(text) and text[i].isdigit():
                num += text[i]
                i += 1

            tokens.append((Token.NUMBER, int(num)))
        else:
            raise ValueError(f"Unexpected character => {c}")

    return tokens

class Parser:
    # recursive-descent parser for lambda expressions
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        # look at current token without consuming
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def next(self):
        # consume current token
        token = self.peek()
        self.pos += 1
        return token

    def parse_expr(self):
        # parse full expression
        return self.parse_application()

    def parse_application(self):
        """
        parse left-associative applications

        example =>
        f x y
        =>
        ((f x) y)
        """
        expr = self.parse_atom()

        while self.peek() and self.peek()[0] in (
            Token.IDENT,
            Token.LP,
            Token.LAMBDA,
            Token.NUMBER,
        ):
            arg = self.parse_atom()
            expr = App(expr, arg)

        return expr

    def parse_atom(self):
        token = self.peek()

        if token is None:
            raise ValueError("Unexpected end of input")

        if token[0] == Token.LAMBDA:
            return self.parse_lambda()

        if token[0] == Token.LP:
            return self.parse_paren()

        if token[0] == Token.IDENT:
            return self.parse_var()

        if token[0] == Token.NUMBER:
            _, number = self.next()
            return church(number)

        raise ValueError(f"Unexpected token => {token}")

    def parse_var(self):
        token = self.next()

        if token[0] != Token.IDENT:
            raise ValueError("Expected identifier")

        return Var(token[1])

    def parse_paren(self):
        # consume '('
        self.next()

        expr = self.parse_expr()

        # expect ')'
        token = self.next()

        if token is None or token[0] != Token.RP:
            raise ValueError("Expected ')'")

        return expr

    def parse_lambda(self):
        # consume lambda symbol
        self.next()

        # read parameter name
        token = self.next()

        if token is None or token[0] != Token.IDENT:
            raise ValueError("Expected parameter after lambda")

        param = token[1]

        # expect dot
        token = self.next()

        if token is None or token[0] != Token.DOT:
            raise ValueError("Expected '.' after lambda parameter")

        # parse lambda body
        body = self.parse_expr()

        return Abs(param, body)

def parse(text):
    # tokenize source string
    tokens = tokenize(text)

    # parse into AST
    parser = Parser(tokens)
    return parser.parse_expr()

class LambdaIntMachine:
    """
        signed integer arithmetic machine powered by lambda calculus

        signed integer encoding =>
        integer n is represented as a pair:
        (positive_part, negative_part)

        examples =>
        5   => (5, 0)
        -3  => (0, 3)
        0   => (0, 0) or even (k, k), both decode to zero
    """

    def __init__(self):
        # Church pair constructor
        self.pair = parse("λx.λy.λf. f x y")

        # first selector
        self.first = parse("λp. p (λx.λy. x)")

        # second selector
        self.second = parse("λp. p (λx.λy. y)")

        # Church addition
        self.plus = parse("λm.λn.λf.λx. m f (n f x)")

        # pair-wise signed addition
        # addInt = λp.λq. pair (plus (first p) (first q)) (plus (second p) (second q))
        self.add_int = self._build_add_int()

    def _build_add_int(self):
        # build expression for adding signed pairs
        body = app(
            app(
                self.pair,
                app(
                    app(self.plus, app(self.first, var("p"))),
                    app(self.first, var("q"))
                )
            ),
            app(
                app(self.plus, app(self.second, var("p"))),
                app(self.second, var("q"))
            )
        )

        return abs_expr("p", abs_expr("q", body))

    def int_pair(self, n):
        """
            convert Python integer into signed Church pair

            n >= 0 =>
            (church(n), church(0))

            n < 0 =>
            (church(0), church(-n))
        """
        if n >= 0:
            return app(app(self.pair, church(n)), church(0))

        return app(app(self.pair, church(0)), church(-n))

    def extract_pair(self, expr):
        """
            extract both components of a Church pair and decode as Python ints
        """
        first_value = app(self.first, expr).reduce_normal_form()
        second_value = app(self.second, expr).reduce_normal_form()

        pos = church_to_usize(first_value)
        neg = church_to_usize(second_value)

        return (pos or 0, neg or 0)

    def decode_signed_pair(self, expr):
        """
            decode signed Church pair into actual Python integer
        """
        pos, neg = self.extract_pair(expr)
        return pos - neg

    def add(self, a, b, trace=False):
        """
            add two Python integers using lambda calculus reduction
        """
        # encode first integer
        p1 = self.int_pair(a)
        # encode second integer
        p2 = self.int_pair(b)

        # build application => ((addInt p1) p2)
        sum_expr = app(app(self.add_int, p1), p2)

        # optionally show full reduction
        if trace:
            print("encoded expression =>")
            print(sum_expr.pretty())
            print()
            reduced = sum_expr.reduce_normal_form_print()
        else:
            reduced = sum_expr.reduce_normal_form()

        # decode final reduced pair
        return self.decode_signed_pair(reduced)

    def inspect_add(self, a, b):
        """
        wildly verbose debug view for one addition
        """
        print("==========================================")
        print(f"input integers => a = {a}, b = {b}")
        print("==========================================")
        print()

        p1 = self.int_pair(a)
        p2 = self.int_pair(b)

        print("encoded pair for first integer =>")
        print(p1.pretty())
        print()

        print("encoded pair for second integer =>")
        print(p2.pretty())
        print()

        print("addInt expression =>")
        print(self.add_int.pretty())
        print()

        sum_expr = app(app(self.add_int, p1), p2)

        print("full application before reduction =>")
        print(sum_expr.pretty())
        print()

        print("reduction trace =>")
        reduced = sum_expr.reduce_normal_form_print()
        print()

        print("final reduced expression =>")
        print(reduced.pretty())
        print()

        pos, neg = self.extract_pair(reduced)

        print(f"decoded pair => (pos = {pos}, neg = {neg})")
        print(f"final integer => {pos} - {neg} = {pos - neg}")
        print()

        return pos - neg

class Solution:
    @staticmethod
    def sum(num1, num2):
        machine = LambdaIntMachine()
        return machine.add(num1, num2)
    
if __name__ == "__main__":
    machine = LambdaIntMachine()

    print(machine.add(3, 4))
    print(machine.add(5, -2))
    print(machine.add(-3, -6))
    print(machine.add(2, -2))
    print()

    machine.inspect_add(2, -1)