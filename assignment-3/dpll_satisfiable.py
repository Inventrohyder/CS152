from typing import List, Set, Tuple, Dict

from literal import Literal


def simplify_clauses(
    clauses: List[Set[Literal]], 
    model: Dict[Literal, bool]
    ) -> List[Set[Literal]]:
    """Simplifies the KB based on the model provided"""
    
    def simplify_clause(
        clause: Set[Literal], 
        model: Dict[Literal, bool]
        ) -> Set[Literal]:
            """Simplifies a clause based on the model provided"""
            new_clause: Set[Literal] = set()
            for literal in clause:
                current_evaluation = model.get(literal, None)
                if current_evaluation and literal.sign or current_evaluation == False and literal.sign == False:
                    return None  # Returns nothing
                elif current_evaluation == None:
                    new_clause.add(literal)
            # Return the original clause if all the values are False
            if len(new_clause) == 0: return clause  
            return new_clause

    new_clauses: List[Set[Literal]] = []
    for clause in clauses:
        new_clause = simplify_clause(clause, model)
        if new_clause is not None:
            new_clauses.append(new_clause)
    return new_clauses


def get_symbols(clauses: List[Set[Literal]]) -> Set[str]:
    """Returns the symbols in the clauses"""
    symbols: Set[str] = set()
    for clause in clauses:
        for literal in clause:
            symbols.add(literal)
    return symbols


def evaluate_clauses(
    clauses: List[Set[Literal]], 
    model: Dict[Literal, bool]
    ) -> bool:
    """Checks if all the clauses evaluate to true, returning true, or if any
    evaluates to false, returning false, or if the status cannot be told, None"""
    
    current_clauses: List[Set[Literal]] = simplify_clauses(clauses, model)

    # When every clause in clauses is True in the model
    if len(current_clauses) == 0: return True

    for clause in current_clauses:
        # When all the literals in the clause are False, the clause is False
        all_false: bool  = True
        for literal in clause:
            if model.get(literal, None) is None:
                all_false = False
                break
        if all_false:
            return False
    return None

def most_common_symbol(
    symbols: Set[Literal], 
    clauses: List[Set[Literal]],
    model:Dict[Literal, bool]
    ) -> Tuple[Literal, Set[Literal]]:

    current_clauses: List[Set[Literal]] = simplify_clauses(clauses, model)

    def count_symbol(symbol: Literal) -> int:
        count = 0
        for clause in current_clauses:
            if symbol in clause:
                count += 1
        return count

    counts = {}
    highest: Literal = None
    for symbol in symbols:
        count: int = count_symbol(symbol)
        counts[symbol] = count
        if highest is None:
            highest = symbol
        else:
            if count > counts[highest]:
                highest = symbol
            elif count == counts[highest]:
                highest = symbol if symbol < highest else highest
            
    new_symbols = symbols.copy()
    new_symbols.remove(highest)
    return highest, new_symbols


def DPLL_Satisfiable(
    KB: List[Set[Literal]], 
    heuristic_level=0
    ) -> Tuple[bool, Dict[Literal, bool], List[Literal]]:
    ''' satisfiable, model = DPLLSatisfiable(KB)
        Takes in a KB and returns whether the KB is satisfiable, and the model that makes it so
        
        KB: A knowledge base of clauses (CNF) consisting of a list of sets of literals.  A KB might look like
            [{A,B},{-A,C,D}]
        heuristic_level: An integer that will be passed in to specify which heuristics to implement 
            (only for the extension activities).
        satisfiable: Returns True if the KB is satisfiable, or False otherwise
        Model: A dictionary that assigns a truth value to each literal for the model that satisfies KB.
            For example, a model might look like {A: True, B: False}
    '''
    def DPLL(
        clauses: List[Set[Literal]], 
        symbols: Set[Literal], 
        model:Dict[Literal, bool],
        heuristic_level: int = 0,
        symbol_list: List[Literal] = []
        ) -> Tuple[bool, Dict[Literal, bool], List[Literal]]:
        """
        Takes in a KB and recursively tries to figure out whether the KB is satisfiable, 
        and the model that makes it so.
            
        :param clauses: A knowledge base of clauses (CNF) consisting of a list of sets of literals.  A KB might look like
                [{A,B},{-A,C,D}]
        :param symbols: The symbols present in the KB
        :param model: The model to use during the search
        :param heuristic_level: An integer that will be passed in to specify which heuristics to implement 
                (only for the extension activities).
                0: No heuristic is used
                1: The degree heuristic
                2: Pure symbol and unit clause heuristics
                3: Most occuring pure symbol
        :param symbol_list: The currently chosen symbols. It should be initialized as empty
        :returns satisfiable: Returns True if the KB is satisfiable, or False otherwise
        :returns Model: A dictionary that assigns a truth value to each literal for the model that satisfies KB.
                For example, a model might look like {A: True, B: False}
        :returns symbol_list: symbols chosen for assignment
        """

        evaluation: bool = evaluate_clauses(clauses, model)

        if evaluation is not None:
            return evaluation, model, symbol_list

        if heuristic_level == 1:
            # Degree heuristic - Most common symbol first
            symbols_lst = list(symbols)
            P, rest = most_common_symbol(symbols, clauses, model) 
            symbol_list.append(P.pure())

            when_true = DPLL(clauses, rest, {**model, **{P.pure(): True}}, heuristic_level)
            if when_true[0]:
                return when_true

            when_false = DPLL(clauses, rest, {**model, **{P.pure(): False}}, heuristic_level)
            return when_false
        elif heuristic_level == 2:
            # Pure symbol heuristic
            P, value = find_pure_symbol(symbols, clauses, model)
            if P: 
                symbol_list.append(P.pure())
                new_symbols = symbols.copy()
                new_symbols.remove(P)
                return DPLL(clauses, new_symbols, {**model, **{P.pure(): value}}, heuristic_level)
            P, value = find_unit_clause(clauses, model)
            if P: 
                symbol_list.append(P.pure())
                new_symbols = symbols.copy()
                new_symbols.remove(P)
                return DPLL(clauses, new_symbols, {**model, **{P.pure(): value}}, heuristic_level)

            # Degree heuristic - Most common symbol first
            symbols_lst = list(symbols)
            P, rest = most_common_symbol(symbols, clauses, model) 
            symbol_list.append(P.pure())

            when_true = DPLL(clauses, rest, {**model, **{P.pure(): True}}, heuristic_level)
            if when_true[0]:
                return when_true

            when_false = DPLL(clauses, rest, {**model, **{P.pure(): False}}, heuristic_level)
            return when_false
        elif heuristic_level == 3:
            # Pure symbol heuristic
            P, value = find_pure_symbol(symbols, clauses, model, True)
            if P: 
                symbol_list.append(P.pure())
                new_symbols = symbols.copy()
                new_symbols.remove(P)
                return DPLL(clauses, new_symbols, {**model, **{P.pure(): value}}, heuristic_level)
            P, value = find_unit_clause(clauses, model, True)
            if P: 
                symbol_list.append(P.pure())
                new_symbols = symbols.copy()
                new_symbols.remove(P)
                return DPLL(clauses, new_symbols, {**model, **{P.pure(): value}}, heuristic_level)

            # Degree heuristic - Most common symbol first
            symbols_lst = list(symbols)

            P, rest = most_common_symbol(symbols, clauses, model) 
            symbol_list.append(P.pure())

            when_true = DPLL(clauses, rest, {**model, **{P.pure(): True}}, heuristic_level)
            if when_true[0]:
                return when_true

            when_false = DPLL(clauses, rest, {**model, **{P.pure(): False}}, heuristic_level)
            return when_false
        else:  # heuristic_level assumed to be 0
            symbols_lst = list(symbols)
            P, rest = symbols_lst[0], set(symbols_lst[1:])
            symbol_list.append(P.pure())

            when_true = DPLL(clauses, rest, {**model, **{P.pure(): True}}, heuristic_level)
            if when_true[0]:
                return when_true

            when_false = DPLL(clauses, rest, {**model, **{P.pure(): False}}, heuristic_level)
            return when_false
 
    clauses = KB
    symbols: List[str] = get_symbols(clauses)
    return DPLL(clauses, symbols, {}, heuristic_level)


def find_pure_symbol(
    symbols: Set[Literal], 
    clauses: List[Set[Literal]],
    model:Dict[Literal, bool],
    most_common: bool = False,
    ) -> Tuple[Literal, bool]:
    """
    Finds a pure symbol in the current state of the KB (clauses).
    """
    current_clauses: List[Set[Literal]] = simplify_clauses(clauses, model)

    pure_symbols: Set[Literal] = set()
    # Stores the sign a symbol should have to be pure 
    symbol_signs: Dict[Literal, bool] = {}
    symbols_lst = list(symbols) 
    for i in range(len(symbols)):
        symbol = symbols_lst[i]
        for clause in current_clauses:
            if symbol in clause:
                clause_lst = list(clause)
                literal = clause_lst[clause_lst.index(symbol)]
                if symbol in symbol_signs:
                    if literal.sign != symbol_signs[symbol]:
                        pure_symbols.remove(symbol)
                        i += 1
                        break
                else:
                    symbol_signs[symbol] = literal.sign
                    pure_symbols.add(symbol)

    if len(pure_symbols) == 0: 
        pure_symbol = None
    elif most_common:
        pure_symbol = most_common_symbol(pure_symbols, clauses, model)[0]
    else:
        pure_symbol =  sorted(list(pure_symbols))[0]

    if pure_symbol is None:
        return None, None

    return pure_symbol, symbol_signs[pure_symbol]
                

def find_unit_clause(
    clauses: List[Set[Literal]],
    model:Dict[Literal, bool],
    most_common: bool = False
) -> tuple:

    current_clauses: List[Set[Literal]] = simplify_clauses(clauses, model)

    unit_clauses: Set[Literal] = set()

    for clause in current_clauses:
        if len(clause) == 1:
            literal = clause.pop()
            unit_clauses.add(literal)
    
    if len(unit_clauses) == 0: 
        unit_clause = None
    elif most_common:
        unit_clause = most_common_symbol(unit_clauses, clauses, model)[0]
    else:
        unit_clause =  sorted(list(unit_clauses))[0]

    if unit_clause is None:
        return None, None
    
    return unit_clause, unit_clause.sign
