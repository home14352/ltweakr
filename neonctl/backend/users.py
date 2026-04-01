import getpass
import grp


class UsersService:
    def status(self) -> dict:
        user = getpass.getuser()
        groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
        return {
            "supported": True,
            "current_user": user,
            "group_count": len(groups),
            "groups": groups[:20],
        }
