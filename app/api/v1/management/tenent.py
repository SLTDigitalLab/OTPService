from db.psql_connector import DB, default_config
from type_def.tenent import Tenent, TenentRq
from type_def.auth import User
from type_def.common import Success, Error
from management.tenents import Tenents


class TenentAPI(Tenents):
    def __init__(self, user: User) -> None:
        super().__init__(user)

    def new(self, t: TenentRq) -> Tenent:
        tenent: Tenent | None = super().new(t)
        if tenent:
            return Success("Tenent created successfully", 200, tenent.__dict__)
        return Error("Failed to create tenent", 1000, 400)

    def get(self, id):
        tenent: Tenent | None = super().get(id)
        if tenent:
            return Success("Tenent found", 200, tenent.__dict__)
        return Error("Tenent not found", 1000, 400)

    def list(self):
        tenent_list: list[Tenent] | None = super().list()
        if tenent_list:
            return Success("Tenent found", 200, [_r.__dict__ for _r in tenent_list])
        return Error("Tenent not found", 1000, 400)

    def update():
        pass

    def delete():
        pass

    def rename(self, id: str, name: str):
        super().rename(id, name)
        # self.db.exec("UPDATE tenents SET name = %s, verified = %s WHERE tenent_id = %s and user_id = %s", (name, False, id, self.user.id))
        # c = self.db.commit()
        # print(c)

    # def verify(self, user):
    #     super().verify()
    #     self.db.exec("UPDATE tenents SET verified = %s WHERE tenent_id = %s ", (True, self.user.id))
    #     self.db.commit()

    # def disable(self):
    #     self.db.exec("UPDATE tenents SET disabled = %s WHERE user_id = %s", (True, self.user.id))
    #     self.db.commit()


class TenentAPIAdmin:
    def __init__(user: User) -> None:
        pass

    def verify():
        pass

    def disable():
        pass

    def delete():
        pass
