import shutil

from neonctl.backend.commands import CommandRunner


class PrivilegeManager:
    def __init__(self) -> None:
        self.runner = CommandRunner()

    def available_methods(self) -> list[str]:
        methods = []
        for item in ["pkexec", "sudo", "doas"]:
            if shutil.which(item):
                methods.append(item)
        return methods

    def preferred(self) -> str | None:
        methods = self.available_methods()
        return methods[0] if methods else None

    def wrap(self, cmd: list[str]) -> list[str]:
        method = self.preferred()
        if not method:
            return cmd
        if method == "sudo":
            return ["sudo", "-n", *cmd]
        return [method, *cmd]

    def test_elevation(self) -> bool:
        wrapped = self.wrap(["id", "-u"])
        result = self.runner.run(wrapped, timeout=10)
        return result.returncode == 0
