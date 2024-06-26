"""
This module provides utility functions for substituting values into templates
and executing shell commands. It is designed to facilitate the automation
of script generation and execution processes.
The substitution method used here is inspired by the approach in the monaco project by @servinagrero:
https://github.com/servinagrero/monaco/tree/develop

Functions:
    substitute_templ: Reads a template from a file, substitutes values from
    provided dictionaries, and writes the result to an output file.
    exec_cmd: Executes a given shell command, optionally displaying the output.

Example Usage:
```python
substitute_templ('input_template.txt', 'output_file.txt', {'key1': 'value1'}, {'key2': 'value2'})
exec_cmd('ls -la', verbose=True)
```
"""

from string import Template
from subprocess import run, DEVNULL
from typing import Dict

def substitute_templ(template_file: str, output_file: str, *substitution_dicts: Dict[str, str]):
    """Substitute values into a template read from a file.
    
    Args:
      template_file: Path to the input file containing the template.
      output_file: Path to the output file to write the substituted content.
      *substitution_dicts: Dictionaries containing values to substitute into the template.
    """
    with open(template_file, 'r') as tmpl_file:
        tmpl = Template(tmpl_file.read())
        substitutions = {k: v for d in substitution_dicts for k, v in d.items()}
        substituted_content = tmpl.safe_substitute(substitutions)
        
        with open(output_file, 'w+') as result_file:
            result_file.write(substituted_content)


def exec_cmd(command: str, *, verbose: bool = False) -> None:
    """Execute a given shell command using subprocess.run.
    
    Args:
      command: Shell command to execute.
      verbose: Whether to display the output of the command.
    """
    run_args = {
        'args': command,  # Corrected this line
        'shell': True,
        'check': True
    }
    
    if not verbose:
        run_args['stdout'] = DEVNULL
        run_args['stderr'] = DEVNULL

    run(**run_args)

