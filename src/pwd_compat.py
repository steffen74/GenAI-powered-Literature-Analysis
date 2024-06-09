import os
import platform

class pwd:
    @staticmethod
    def getpwuid(uid):
        if platform.system() == 'Windows':
            return pwd.struct_passwd(
                pw_name=os.getlogin(),
                pw_passwd=None,
                pw_uid=uid,
                pw_gid=None,
                pw_gecos=None,
                pw_dir=os.path.expanduser('~'),
                pw_shell=None
            )
        else:
            import pwd
            return pwd.getpwuid(uid)

    class struct_passwd:
        def __init__(self, pw_name, pw_passwd, pw_uid, pw_gid, pw_gecos, pw_dir, pw_shell):
            self.pw_name = pw_name
            self.pw_passwd = pw_passwd
            self.pw_uid = pw_uid
            self.pw_gid = pw_gid
            self.pw_gecos = pw_gecos
            self.pw_dir = pw_dir
            self.pw_shell = pw_shell
