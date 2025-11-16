from .base import BaseShCommand, find_path, ErrorReturnCode

defaut_config = dict()

class Command(BaseShCommand):
    def __init__(self, **kwds):
        '''
        Wrap yad
        '''
        super().__init__("yad")

    def dialog(self, text, title="", size=(1500,500), buttons={}):
        '''
        Run a dialog.

        buttons holds a dict from button labels to actions.  An action can be:
        - int :: an exit code to return if button is clicked.  Note, ESC is 252.
        - string :: a command line to run if clicked, does not exit the dialog
        - callable :: a Python callable to call if clicked, does not exit the dialog
        The return code is returned.
        '''
        def callback(line):
            line = line.strip()
            buttons[line](line)

        args = ['--text-info', '--always-print-result',
                '--width', str(size[0]), '--height', str(size[1])]
        if title:
            args += ['--title', title]

        for label, action in buttons.items():
            if isinstance(action, (int, str)):
                args += ['--button', f'{label}:{action}']
                continue
            args += ['--button', f'{label}:echo {label}']
        
        try:
            self._cmd(*args, _out=callback, _in=text)
        except ErrorReturnCode as err:
            return err.exit_code

        return 0

