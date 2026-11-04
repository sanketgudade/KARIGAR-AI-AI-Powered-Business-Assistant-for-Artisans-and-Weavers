import re
import html.parser

with open('frontend/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the script content inside <script type="text/babel">
babel_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
if babel_match:
    babel_code = babel_match.group(1)
    print("Found Babel script block. Character length:", len(babel_code))
    
    # Check brace matching in the script
    stack = []
    lines = babel_code.split('\n')
    for line_no, line in enumerate(lines, 1):
        for ch in line:
            if ch in '({[':
                stack.append((ch, line_no))
            elif ch in ')}]':
                if not stack:
                    print(f"Error: unmatched closing '{ch}' at line {line_no}")
                else:
                    top, top_line = stack.pop()
                    if (top == '(' and ch != ')') or (top == '{' and ch != '}') or (top == '[' and ch != ']'):
                        print(f"Mismatched '{top}' (from line {top_line}) and '{ch}' at line {line_no}")

    if stack:
        print(f"Warning: {len(stack)} unclosed brackets/braces! First unclosed: {stack[0]}")
    else:
        print("Babel script bracket/brace matching PASSED 100%!")
else:
    print("Error: Could not find Babel script block!")
