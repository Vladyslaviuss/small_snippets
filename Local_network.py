class Router:
    def __init__(self):
        self.buffer = []
        self.servers = {}

    def link(self, server):
        # Подключили сервер к роутеру (Добавляем обьект класса Server в словарь)
        self.servers[server.ip] = server
        # Дали знать серверу, что он подключен к роутеру (Меняем флаг в его локальном свойстве)
        server.router = self

    def unlink(self, server):
        # Удаляем сервер из словаря (отвязываем)
        s = self.servers.pop(server.ip, False)
        if s:
            #Сообщаем серверу, что теперь он не подключен никуда
            s.router = None

    def send_data(self):
        # d - обьекты класса Data (пакеты данных)
        for d in self.buffer:
            # c помощью цикла передаем все данные нужному серверу по IP
            if d.ip in self.servers:
                # Заполняем буффер нужного сервера пакетами данных
                self.servers[d.ip].buffer.append(d)
        # Очищаем буффер роутера
        self.buffer.clear()


class Server:
    server_ip = 1

    def __init__(self):
        self.buffer = []
        self.ip = Server.server_ip
        Server.server_ip += 1
        self.router = None

    def send_data(self, data):
        # data - обьект класса Data
        # Проверяем, или сервер не связан ни с каким роутером
        if self.router: #is not None
            self.router.buffer.append(data)

    def get_data(self):
        # создать копию пакетов данных
        b = self.buffer.copy()
        # очистить буффер от пакетов данных
        self.buffer.clear()
        return b

    def get_ip(self):
        return self.ip


class Data:
    def __init__(self, msg, ip):
        self.data = msg
        self.ip = ip


router = Router()
sv_from = Server()
sv_from2 = Server()
router.link(sv_from)
router.link(sv_from2)
router.link(Server())
router.link(Server())
sv_to = Server()
router.link(sv_to)
sv_from.send_data(Data("Hello", sv_to.get_ip()))
sv_from2.send_data(Data("Hello", sv_to.get_ip()))
sv_to.send_data(Data("Hi", sv_from.get_ip()))
router.send_data()
msg_lst_from = sv_from.get_data()
msg_lst_to = sv_to.get_data()