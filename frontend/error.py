from typing import Optional

def format_error(
    error_type: str,
    message: str,
    filename: str,
    source: str,
    line: int,
    column: int,
    token_length: int = 1
) -> str:
    """
    Formats a minimalistic error message with UTF-8 vertical lines, underlining, and arrows.
    
    Args:
        error_type: Type of error (e.g., "SyntaxError").
        message: Error message (e.g., "Expected SEMICOLON, got EOF").
        filename: Path to the source file.
        source: Full source code of the file.
        line: Line number where the error occurred (1-based).
        column: Column number where the error occurred (1-based).
        token_length: Length of the token causing the error (default: 1).
    
    Returns:
        A formatted string with a single, concise error output.
    """
    # Split source into lines
    lines = source.splitlines()
    num_lines = len(lines)
    
    # Validate line
    if not (1 <= line <= num_lines):
        return (
            f"{error_type}: {message}\n"
            f"File: {filename}, Line: <unknown>, Column: <unknown>\n"
            f"  | <no source available>"
        )
    
    # Get context lines (2 before, 2 after)
    context_before = 2
    context_after = 2
    start_line = max(1, line - context_before)
    end_line = min(num_lines, line + context_after)
    
    # Prepare code snippet
    max_line_num_width = len(str(end_line))
    code_snippet = []
    max_line_length = 80  # Truncate long lines
    
    for i in range(start_line - 1, end_line):
        line_num = i + 1
        code = lines[i].rstrip()[:max_line_length]
        if len(lines[i]) > max_line_length:
            code += "..."
        
        # Format line number
        line_num_str = str(line_num).rjust(max_line_num_width)
        prefix = f"  {line_num_str} | "
        
        code_snippet.append(f"{prefix}{code}")
        if line_num == line:
            # Underline error
            indent = " " * (column - 1)
            underline = "~" * token_length
            code_snippet.append(f"{' ' * (max_line_num_width + 4)} | {indent}{underline}")
            
            # Add arrow for missing elements
            if "expected" in message.lower():
                arrow_pos = column + token_length - 1
                arrow_indent = " " * arrow_pos
                expected_item = message.split("Expected ")[1].split(",")[0].lower()
                code_snippet.append(f"{' ' * (max_line_num_width + 4)} | {arrow_indent}→ Expected {expected_item}")
    
    # Generate hint
    hint = ""
    if "empty input" in message.lower():
        hint = "Hint: Enter a non-empty value."
    elif "expected" in message.lower():
        expected_item = message.split("Expected ")[1].split(",")[0].lower()
        hint = f"Hint: Add a {expected_item} after the statement."
    elif "undefined variable" in message.lower():
        hint = "Hint: Declare the variable before use."
    elif "type error" in message.lower():
        hint = "Hint: Check type compatibility."
    
    # Build final output
    error_header = f"{error_type}: {message}"
    file_info = f"File: {filename}, Line: {line}, Column: {column}"
    
    return (
        f"{error_header}\n"
        f"{file_info}\n"
        f"\n".join(code_snippet) + 
        (f"\n{hint}" if hint else "")
    )