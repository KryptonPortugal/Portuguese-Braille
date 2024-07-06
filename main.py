import re
import argparse

# Braille mappings from both files
braille_map = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵',
    'á': '⠷', 'é': '⠿', 'í': '⠌', 'ó': '⠬', 'ú': '⠾', 'ã': '', 'â': '⠡', 'ê': '⠣', 'ô': '⠹', 'à': '⠫', 'õ': '⠪', 'ç': '⠯',
    ' ': ' ', ',': '⠂', ';': '⠆', ':': '⠒', '.': '⠄', '’': '⠄', '?': '⠢', '!': '⠖', '...': '⠄⠄⠄', '-': '⠤⠤', '*': '⠔', '(': '⠣', ')': '⠜',
    '[': '⠷', ']': '⠾', '"': '⠦', '●': '⠪⠕', '■': '⠸⠽', '&': '⠯', '/': '⠠⠂', '|': '⠸', '×': '⠨⠦', '→': '⠒⠕', '←': '⠪⠒', '↔': '⠪⠒⠕',
    '#': '⠼⠅', '★': '⠨⠪', '†': '⠺⠂', '©': '⠣⠨⠉⠜', '®': '⠣⠨⠗⠜', '$': '⠰', '€': '⠈⠑', '£': '⠈⠇', '¥': '⠈⠽', '%': '⠸⠴', '‰': '⠸⠴⠴', '§': '⠎⠎', '+': '⠖', '-': '⠤',
    '÷': '⠲', '=': '⠶', '/': '⠲', '>': '⠕', '<': '⠪', '′′': '⠠⠦', '°': '⠴', '′': '⠳', '′′': '⠳⠳', '^': '⠡', '_' : '⠌',
    '‘':'⠠⠦', '’':'⠠⠦','«':'⠰⠦','»':'⠰⠦','‹':'⠰⠦','›':'⠰⠦','1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚', '@':'⠮'
}

braille_map_math = {
    'a': '⠐⠁', 'b': '⠐⠃', 'c': '⠐⠉', 'd': '⠐⠙', 'e': '⠐⠑', 'f': '⠐⠋', 'g': '⠐⠛', 'h': '⠐⠓', 'i': '⠐⠊', 'j': '⠐⠚',
    'k': '⠐⠅', 'l': '⠐⠇', 'm': '⠐⠍', 'n': '⠐⠝', 'o': '⠐⠕', 'p': '⠐⠏', 'q': '⠐⠟', 'r': '⠐⠗', 's': '⠐⠎', 't': '⠐⠞',
    'u': '⠐⠥', 'v': '⠐⠧', 'w': '⠐⠺', 'x': '⠐⠭', 'y': '⠐⠽', 'z': '⠐⠵',
    'á': '⠷', 'é': '⠿', 'í': '⠌', 'ó': '⠬', 'ú': '⠾', 'ã': '', 'â': '⠡', 'ê': '⠣', 'ô': '⠹', 'à': '⠫', 'õ': '⠪', 'ç': '⠯',
    ' ': ' ', ',': '⠂', ';': '⠆', ':': '⠒', '.': '⠄', '’': '⠄', '?': '⠢', '!': '⠖', '...': '⠄⠄⠄', '-': '⠤⠤', '*': '⠔', '(': '⠣', ')': '⠜',
    '[': '⠷', ']': '⠾', '"': '⠦', '●': '⠪⠕', '■': '⠸⠽', '&': '⠯', '/': '⠠⠂', '|': '⠸', '×': '⠨⠦', '→': '⠒⠕', '←': '⠪⠒', '↔': '⠪⠒⠕',
    '#': '⠼⠅', '★': '⠨⠪', '†': '⠺⠂', '©': '⠣⠨⠉⠜', '®': '⠣⠨⠗⠜', '$': '⠰', '€': '⠈⠑', '£': '⠈⠇', '¥': '⠈⠽', '%': '⠸⠴', '‰': '⠸⠴⠴', '§': '⠎⠎', '+': '⠖', '-': '⠤',
    '÷': '⠲', '=': '⠶', '/': '⠲', '>': '⠕', '<': '⠪', '′′': '⠠⠦', '°': '⠴', '′': '⠳', '′′': '⠳⠳', '^': '⠡', '_' : '⠌',
    '‘':'⠠⠦', '’':'⠠⠦','«':'⠰⠦','»':'⠰⠦','‹':'⠰⠦','›':'⠰⠦','1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑', '¤':'⠈',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚', '@':'⠮','{':'⠢','}':'⠔','´':'⠳','~':'⠐⠢','::':'⠰⠆'
}

# Special patterns for mathematical expressions
special_patterns = [
        (r'/alpha', '⠈⠁'), (r'/Alpha', '⠘⠁'), (r'/beta', '⠈⠃'), (r'/Beta', '⠘⠃'), (r'/gamma', '⠈⠛'), (r'/Gamma', '⠘⠛'), (r'/delta', '⠈⠙'), (r'/Delta', '⠘⠙'), (r'/eps', '⠈⠑'),
        (r'/Eps', '⠘⠑'), (r'/zeta', '⠈⠵'), (r'/Zeta', '⠘⠵'), (r'/eta', '⠈⠱'), (r'/Eta', '⠘⠱'), (r'/teta', '⠈⠹'), (r'/Teta', '⠘⠹'), (r'/iota', '⠈⠊'), (r'/Iota', '⠘⠊'),
        (r'/kappa', '⠈⠅'), (r'/Kappa', '⠘⠅'), (r'/lambda', '⠈⠇'), (r'/Lambda', '⠘⠇'), (r'/mu', '⠈⠍'),(r'/Mu', '⠘⠍'), (r'/nu', '⠈⠝'), (r'/Nu', '⠘⠝'), (r'/xi', '⠈⠭'),
        (r'/Xi', '⠘⠭'), (r'/omikron', '⠈⠕'), (r'/Omikron', '⠘⠕'), (r'/pi', '⠈⠏'), (r'/Pi', '⠘⠏'), (r'/ro', '⠈⠗'), (r'/Ro', '⠘⠗'), (r'/sigma', '⠈⠎'), (r'/Sigma', '⠘⠎'),
        (r'/Tau', '⠘⠞'), (r'/tau', '⠈⠞'), (r'/Upsi', '⠘⠥'), (r'/upsi', '⠈⠥'), (r'/Phi', '⠘⠋'), (r'/phi', '⠈⠋'), (r'/Chi', '⠘⠯'),
        (r'/chi', '⠈⠯'), (r'/Psi', '⠘⠽'),(r'/psi', '⠈⠽'), (r'/Omega', '⠘⠺'),(r'/omega', '⠈⠺'), (r'/{', '⠐⠇' ), (r'/}', '⠸⠂'), (r'/langle', '⠐⠅'), (r'rangle', '⠨⠂'),
        (r'/overline','⠈⠉'), (r'/underline','⠠⠤'), (r'/mathbbN','⠸⠝'), (r'/mathbbZ','⠸⠵'), (r'/mathbbQ','⠸⠟'), (r'/mathbbR','⠸⠗'),
        (r'/mathbbC','⠇⠉'), (r'/prod','⠦'), (r'/dot', '⠄'), (r'/plusminus','⠖⠒⠤'), (r'/div','⠲'), (r'/simeq', '⠐⠢⠄'), (r'/cong', '⠶⠶'),
        (r'/leq', '⠪⠶'), (r'/geq','⠕⠶'), (r'/neq','⠘⠶'), (r'/st','⠠⠂'), (r'/empty','⠇⠚'),
        (r'/univ','⠇⠥'), (r'/cup','⠇⠜'), (r'/cap','⠇⠱'), (r'\\', '⠐⠄' ), (r'/prodcart', '⠨⠦'),
        (r'/in','⠣⠂' ), (r'/sub','⠣⠆'), (r'/subeq', '⠣⠆'), (r'/notsub','⠘⠣⠆'), (r'/notin','⠘⠣⠂'),
        (r'/sim', '⠐⠢⠄'), (r'/quot','⠠⠂'), (r'/infty','⠼⠳'),
        (r'aleph', '⠠⠳'), (r'/forall', '⠨⠄'), (r'/exists','⠨⠢'), (r'/uexists','⠨⠆'), (r'/notforall','⠘⠨⠄'), (r'/notexists','⠘⠨⠢'),
        (r'/and','⠰⠂'), (r'/or','⠰⠄'), (r'/not','⠠⠄'), (r'/implies', '⠒⠕'), (r'/iff','⠪⠒⠕'), (r'/before','⠐⠪'), (r'/circ','⠠⠆'),
        (r'/lim','⠇⠌⠍⠄'), (r'/goesto','⠒⠂'), (r'/grows','⠸⠁'), (r'/decrease', '⠸⠄'), (r'/del','⠸⠙'), (r'/nabla','⠈⠻'),
        (r'/laplacian','⠸⠦'), (r'/int','⠯'), (r'/oint','⠯⠴⠱'), (r'/conv','⠐⠆'), (r'/log','⠇⠕⠛⠄'), (r'/ln','⠇⠭'),
        (r'/sin','⠎⠑⠝⠄'), (r'/cos','⠉⠕⠎⠄'), (r'/tan','⠞⠛⠄'), (r'/cotan','⠉⠕⠞⠛⠄'), (r'/sec','⠎⠑⠉⠄'), (r'/cosec','⠉⠕⠎⠎⠑⠉⠄'),
        (r'/arcsin','⠁⠗⠉⠄⠎⠑⠝⠄'), (r'/arccos','⠁⠗⠉⠄⠉⠕⠎⠄'), (r'/arctan','⠁⠗⠉⠄⠞⠛⠄'), (r'/arccottan','⠁⠗⠉⠄⠉⠕⠞⠛⠄'), (r'/arcsec','⠁⠗⠉⠄⠎⠑⠉⠄'), (r'/arccosec','⠁⠗⠉⠄⠉⠕⠎⠎⠑⠉⠄'),
        (r'/sinh','⠁⠗⠛⠄⠞⠓⠄'), (r'/cosh','⠁⠗⠛⠄⠉⠓⠄'), (r'/tanh','⠁⠗⠛⠄⠞⠓⠄'), (r'/coth','⠁⠗⠛⠄⠉⠞⠓⠄'), (r'/sech','⠁⠗⠛⠄⠎⠑⠉⠓⠄'), (r'/cosech','⠁⠗⠛⠄⠉⠕⠎⠎⠑⠉⠓'),
        (r'/line','⠐⠒⠂'), (r'/vector', '⠒⠂'), (r'/arc', '⠁⠒'), (r'/arco','⠢⠜'), (r'/ang','⠘⠒'),
        (r'/arang','⠘⠒⠢'), (r'/triang','⠠⠾'), (r'/quad','⠸⠽'), (r'/circle','⠪⠕'), (r'/rect', '⠯⠽'),
        (r'/curve','⠢⠔'), (r'/graus', '⠴'), (r'/rad','⠗⠁⠙⠄'), (r'/paralel', '⠸⠇'), (r'/perp', '⠼⠄'),
        (r'/pvec','⠲'), (r'/osum', '⠪⠖'), (r'/oprod', '⠪⠦')
    ] 

def convert_to_braille(text):
    # First, handle mathematical expressions
    pattern = r'\$(.+?)\$'
    text = re.sub(pattern, lambda m: convert_dollar_content_to_braille(m.group(1)), text)

    # Then, handle regular text
    braille_text = []
    i = 0
    was_digit = False

    while i < len(text):
        char = text[i]

        if char.isdigit():
            if not was_digit:
                braille_text.append('⠼')
                was_digit = True
            braille_text.append(braille_map[char])
        elif char.isalpha():
            if char.isupper():
                braille_text.append('⠨')
            braille_text.append(braille_map[char.lower()])
            was_digit = False
        else:
            was_digit = False
            braille_text.append(braille_map.get(char, char))

        i += 1

    return ''.join(braille_text)

def convert_dollar_content_to_braille(content):
    braille_text = ['']
    content = handle_complex_expressions(content)
    
    for char in content:
        if char.isdigit():
            braille_text.append('⠼' + braille_map_math.get(char, char))
        elif char.isalpha():
            if char.isupper():
                braille_text.append('⠨')
            braille_text.append(braille_map_math.get(char.lower(), char))
        else:
            braille_text.append(braille_map_math.get(char, char))
    return ''.join(braille_text)

def handle_complex_expressions(content):
    for pattern, replacement in special_patterns:
        content = re.sub(pattern, replacement, content)

    frac_pattern = r'/frac\{([^{}]*)\}\{([^{}]*)\}'
    content = re.sub(frac_pattern, handle_frac, content)
    
    return content

def handle_frac(match):
    numerator = match.group(1)
    denominator = match.group(2)
    numerator_braille = ''.join(braille_map_math.get(char, char) for char in numerator)
    denominator_braille = ''.join(braille_map_math.get(char, char) for char in denominator)
    return f'{numerator_braille}⠲{denominator_braille}'

def main(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        braille_text = convert_to_braille(text)

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(braille_text)

        print(f'Braille translation saved to {output_file}')
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except IOError as e:
        print(f"Error reading from or writing to file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert text file to Portuguese Braille, including mathematical expressions.')
    parser.add_argument('input_file', type=str, help='The input text file.')
    parser.add_argument('output_file', type=str, help='The output text file.')

    args = parser.parse_args()

    main(args.input_file, args.output_file)