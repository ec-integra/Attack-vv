from shell_commands_executor import ShellCommandsExecutor


class InvokerShellCommandService:
    def invoke_one_command(self, shell_command: str) -> str:
        result_command = ShellCommandsExecutor(shell_command).execute()
        return result_command

    def invoke_commands(self, shell_commands: list[str]) -> list[str]:
        result_shell_commands = []
        for commands in shell_commands:
            result_command = ShellCommandsExecutor(commands).execute()
            result_shell_commands.append(result_command)

        return result_shell_commands
