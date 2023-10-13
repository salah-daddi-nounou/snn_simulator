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

