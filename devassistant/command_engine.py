
from devassistant.command_runners import CommandRunners, LoadCmdCommandRunner

class CommandEngine(object):

    def __init__(self, kwargs=None):
        self.command_runners = CommandRunners()
        self.logger = None
        self.kwargs = kwargs


    def run(self, command):
        '''Run a lang.Command instance'''
        for runner_prefix, runners in self.command_runners.items():
            if runner_prefix == command.prefix:
                try:
                    # The last CommandRunner loaded is used so that the
                    # user-provided runners have precedence
                    runner = [r for r in runners if r.matches(command)][-1]
                    logical_result, result = runner(command).run()

                    # Special case for loading CommandRunners
                    if runner is LoadCmdCommandRunner:
                        self._register_command_runners(result)

                    return logical_result, result
                except IndexError:
                    msg = 'No command runner for type "{t}" found!'.format(t=command.comm_type)
                    raise Exception(msg)

    def _register_command_runners(self, runners_dict):
        '''Register command runners'''
        for prefix, runners in runners_dict.items():
            for runner in runners:
                self.command_runners.register(runner, prefix)
