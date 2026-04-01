import getpass
import grp
import pwd


class UsersService:
    def status(self) -> dict:
        user = getpass.getuser()
        groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
        users = [u.pw_name for u in pwd.getpwall() if int(u.pw_uid) >= 1000][:50]
        return {
            "supported": True,
            "current_user": user,
            "group_count": len(groups),
            "groups": groups[:20],
            "local_users": users,
        }
