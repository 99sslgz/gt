# gui.py (版本 2)

import tkinter as tk
from tkinter import font
from game_logic import GameLogic # 确保 game_logic.py 在同一目录下

class GameGUI(tk.Tk):
    def __init__(self, game_logic):
        super().__init__()
        self.game_logic = game_logic
        self.title("古代人生模拟器")
        self.geometry("1024x768")
        self.config(bg="#333333") # 将主窗口背景设为深灰色

        # 定义字体
        self.font_normal = font.Font(family="Microsoft YaHei", size=11)
        self.font_header = font.Font(family="Microsoft YaHei", size=12, weight="bold")
        self.font_button = font.Font(family="Microsoft YaHei", size=10)

        # 用于存放需要动态更新的按钮
        self.exit_buttons = []
        self.action_buttons = []

        # 创建UI元素
        self.create_widgets()
        
        # 初始更新界面
        self.update_display()
        self.update_message("你的人生，由此刻开启。")

    def create_widgets(self):
        # 使用 place 来进行更自由的布局

        # ---- 游戏信息 (左上角) ----
        # 使用一个无边框的Frame作为“半透明”背景
        info_bg = tk.Frame(self, bg="#1a1a1a") # 深一点的灰色，模拟透明感
        info_bg.place(x=10, y=10, width=220, height=60)
        
        self.time_label = tk.Label(self, text="", font=self.font_normal, bg=info_bg['bg'], fg="white", justify=tk.LEFT)
        self.time_label.place(x=20, y=20)
        self.location_label = tk.Label(self, text="", font=self.font_normal, bg=info_bg['bg'], fg="white", justify=tk.LEFT)
        self.location_label.place(x=20, y=45)

        # ---- 角色状态 (左侧) ----
        status_bg = tk.Frame(self, bg="#1a1a1a")
        status_bg.place(x=10, y=80, width=220, height=200)

        tk.Label(self, text="角色状态", font=self.font_header, bg=status_bg['bg'], fg="white").place(x=20, y=90)
        self.status_label = tk.Label(self, text="", font=self.font_normal, bg=status_bg['bg'], fg="white", justify=tk.LEFT, anchor="nw")
        self.status_label.place(x=20, y=115)

        # ---- 中央消息提示 ----
        self.message_label = tk.Label(self, text="", font=self.font_normal, bg="black", fg="white")
        self.message_label.place(x=0, y=738, relwidth=1.0, height=30)
    
    def get_compact_status_text(self):
        """生成紧凑版本的状态文本"""
        player = self.game_logic.player
        
        # 基础信息
        base_info = f"姓名: {player.name}\n年龄: {player.age // 12}岁 {player.age % 12}个月\n"
        
        # 并排展示能力值
        attrs = player.attributes
        attr_lines = []
        attr_keys = list(attrs.keys())
        for i in range(0, len(attr_keys), 2): # 每行显示两个
            line = f"{attr_keys[i]}: {attrs[attr_keys[i]]:<4}"
            if i + 1 < len(attr_keys):
                line += f"{attr_keys[i+1]}: {attrs[attr_keys[i+1]]}"
            attr_lines.append(line)
        
        # 其他状态
        other_info = f"\n体力: {player.energy}  心情: {player.mood}\n钱财: {player.money} 文"
        
        return base_info + "\n".join(attr_lines) + other_info

    def update_display(self):
        """刷新整个GUI以反映当前游戏状态"""
        player = self.game_logic.player
        current_location = player.location
        
        # 更新左上角信息
        self.time_label.config(text=f"时间: {self.game_logic.game_time.get_time_string()}")
        self.location_label.config(text=f"地点: {current_location.name}")
        
        # 更新紧凑的角色状态
        self.status_label.config(text=self.get_compact_status_text())

        # 清空并重建右侧的“移动”按钮
        for btn in self.exit_buttons:
            btn.destroy()
        self.exit_buttons.clear()
        
        for i, (direction, location) in enumerate(current_location.exits.items()):
            btn = tk.Button(self, text=f"{direction} ({location.name})",
                            font=self.font_button,
                            command=lambda loc=location: self.handle_move(loc))
            btn.place(x=900, y=20 + i * 40, width=110, height=30)
            self.exit_buttons.append(btn)

        # 清空并重建左下角的“操作”按钮 (Bug修复)
        for btn in self.action_buttons:
            btn.destroy()
        self.action_buttons.clear()

        for i, (action_name, (action_func, desc)) in enumerate(current_location.actions.items()):
            btn = tk.Button(self, text=action_name,
                            font=self.font_button,
                            command=lambda f=action_func, name=action_name: self.handle_action(f, name))
            btn.place(x=20 + i * 90, y=690, width=80, height=30)
            self.action_buttons.append(btn)

    def handle_move(self, location):
        """处理移动请求"""
        self.game_logic.move_player(location)
        self.update_message(f"你前往了 {location.name}。")
        self.update_display()

    def handle_action(self, action_function, action_name):
        """处理操作请求"""
        result_message = action_function()
        self.update_message(result_message)
        self.update_display()

    def update_message(self, text):
        """更新中央下方的消息标签"""
        self.message_label.config(text=text)

if __name__ == '__main__':
    game_logic = GameLogic()
    app = GameGUI(game_logic)
    app.mainloop()