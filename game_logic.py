# game_logic.py

class Player:
    """玩家角色类"""
    def __init__(self, name):
        self.name = name
        self.age = 12 * 15  # 15岁
        self.attributes = {
            "文学": 10, "艺术": 10, "武术": 10, "智力": 10,
            "道德": 10, "魅力": 10, "野心": 10,
        }
        self.money = 100  # 初始资金
        self.energy = 100  # 体力
        self.mood = "平静" # 心情
        self.location = None

    def get_status_text(self):
        """返回格式化的玩家状态文本"""
        status = f"姓名: {self.name}\n"
        status += f"年龄: {self.age // 12}岁 {self.age % 12}个月\n\n"
        for attr, value in self.attributes.items():
            status += f"{attr}: {value}\n"
        status += f"\n体力: {self.energy}\n"
        status += f"钱财: {self.money} 文\n"
        status += f"心情: {self.mood}"
        return status

class GameTime:
    """游戏时间类"""
    def __init__(self, start_year=713):
        self.year = start_year
        self.month = 1

    def advance_time(self, months=1):
        self.month += months
        while self.month > 12:
            self.month -= 12
            self.year += 1
        return f"时光飞逝... {months}个月过去了。"

    def get_time_string(self):
        return f"开元{self.year - 712}年 {self.month}月"

class Location:
    """地点类"""
    def __init__(self, name, description, background_image=None):
        self.name = name
        self.description = description
        self.exits = {}
        self.actions = {}
        self.background_image = background_image # 为以后加图片做准备

    def add_exit(self, direction, location):
        self.exits[direction] = location

    def add_action(self, action_name, action_function, description):
        self.actions[action_name] = (action_function, description)

class GameLogic:
    """游戏主逻辑类"""
    def __init__(self):
        self.player = Player("无名氏")
        self.game_time = GameTime()
        self._setup_locations()
        self.player.location = self.locations["自宅"]

    def _setup_locations(self):
        self.locations = {
            "京师": Location("京师", "繁华的京师，天子脚下，龙蟠虎踞之地。"),
            "自宅": Location("自宅", "你在京师的家。虽是陋室，却也温馨。"),
            "卧室": Location("卧室", "你的卧室，陈设简单，只有一床一桌。"),
            "书房": Location("书房", "你的书房，书架上零散地放着几本书。"),
        }
        self.locations["自宅"].add_exit("出门", self.locations["京师"])
        self.locations["自宅"].add_exit("进入卧室", self.locations["卧室"])
        self.locations["自宅"].add_exit("进入书房", self.locations["书房"])
        self.locations["卧室"].add_exit("回到大厅", self.locations["自宅"])
        self.locations["书房"].add_exit("回到大厅", self.locations["自宅"])
        self.locations["京师"].add_exit("回家", self.locations["自宅"])
        
        self.locations["书房"].add_action("读书", self.study, "静下心来，阅读一本书。")
        self.locations["卧室"].add_action("休息", self.rest, "在床上小憩片刻，恢复精力。")

    def study(self):
        time_passed_msg = self.game_time.advance_time(1)
        self.player.age += 1
        self.player.attributes["文学"] += 2
        self.player.attributes["智力"] += 1
        self.player.energy -= 10
        return f"{time_passed_msg}\n你认真研读，感觉学识有所长进，但有些疲惫。"

    def rest(self):
        time_passed_msg = self.game_time.advance_time(1)
        self.player.age += 1
        self.player.energy = 100
        return f"{time_passed_msg}\n你在卧室里休息，养精蓄锐，体力完全恢复了。"

    def move_player(self, new_location):
        self.player.location = new_location