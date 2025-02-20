import sys
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
import random
from items import *
from map import *
from player import *
from game import *

# レイアウト設定用変数
sp_exp = Qw.QSizePolicy.Policy.Expanding


class MainWindow(Qw.QMainWindow):

    # コンストラクタ(初期化)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MainWindow')
        self.setGeometry(100, 50, 800, 600)

        # メインレイアウトの設定
        central_widget = Qw.QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = Qw.QVBoxLayout(central_widget)  # 垂直レイアウト

        # ボタン配置の水平レイアウトを作成します。
        self.button_layout = Qw.QHBoxLayout()  # ボタンレイアウト
        self.button_layout.setAlignment(Qc.Qt.AlignmentFlag.AlignLeft)  # 左寄せ
        main_layout.addLayout(self.button_layout)  # メインレイアウトにボタンレイアウトを追加

        self.ButtonInit()  # ボタンの初期化

        self.time = time
        self.TimeStatus = TimeStatus
        self.day = day

        # テキストボックス
        self.tb_log = Qw.QTextEdit('')
        self.tb_log.setMinimumSize(20, 100)
        self.tb_log.setSizePolicy(sp_exp, sp_exp)
        self.DrawItems()
        self.tb_log.setReadOnly(True)  # ログの読み取り専用設定
        main_layout.addWidget(self.tb_log)

        # ステータスバー
        self.sb_status = Qw.QStatusBar()
        self.setStatusBar(self.sb_status)
        self.sb_status.setSizeGripEnabled(False)
        self.sb_status.showMessage('プログラムを起動しました。')

        self.tb_log.setStyleSheet(
            "background-color: rgba(255, 255, 255, 150);")

        # からのボタン
        self.btn_forest = None
        self.btn_seaside = None

        # 確認ボタンのフラグ
        self.ClickedNext = False

    def DrawNextbutton(self):
        # 次に進むボタン
        self.btn_next = Qw.QPushButton('確認')
        self.btn_next.setMinimumSize(50, 30)
        self.btn_next.setMaximumSize(100, 30)
        self.btn_next.setSizePolicy(sp_exp, sp_exp)
        # ボタンクリックでメソッドを呼び出す
        self.btn_next.clicked.connect(self.ClickedNextButton)
        self.button_layout.addWidget(self.btn_next)

    def ClickedNextButton(self):
        self.ClickedNext = True

        # アイテム情報の表示

    def DrawItems(self):

        if self.time >= 24:
            self.time = self.time - 24
            self.day += 1
        if self.time >= 8 and self.time < 22:
            self.TimeStatus = '昼'
        else:
            self.TimeStatus = '夜'

        log = f'{self.day}日目\n\n'

        log += f'{self.time}：00\n'
        log += f'{self.TimeStatus}\n\n'
        if self.TimeStatus == '夜':
            log += '夜間は探索時により多くの正気度を失います\n\n'

        if player["正気度"] >= 100:
            player["正気度"] = 100
        if player["正気度"] <= 0:
            self.tb_log.clear()
            self.tb_log.append('正気度が0になりました。')
            self.tb_log.append('あなたは終わりのない無人島生活に耐えられなくなり、海に飛び込みました。')
            self.tb_log.append('ゲームオーバーです。')
            self.tb_log.append('確認ボタンをクリックするとゲームが終了します。')
            self.handle_next_button()
            sys.exit()
        if player["満腹度"] >= 100:
            player["満腹度"] = 100
        if player["満腹度"] <= 0:
            self.tb_log.clear()
            self.tb_log.append('満腹度が0になりました。')
            self.tb_log.append('あなたは空腹の余り自分の体を食べようとしました。')
            self.tb_log.append('ゲームオーバーです。')
            self.tb_log.append('確認ボタンをクリックするとゲームが終了します。')
            self.handle_next_button()
            sys.exit()
        if player["喉の潤い"] >= 100:
            player["喉の潤い"] = 100
        if player["喉の潤い"] <= 0:
            self.tb_log.clear()
            self.tb_log.append('喉の潤いが0になりました。')
            self.tb_log.append('あなたは喉の渇きに耐えられず、自分の血を飲もうとしました。')
            self.tb_log.append('ゲームオーバーです。')
            self.tb_log.append('確認ボタンをクリックするとゲームが終了します。')
            self.handle_next_button()
            sys.exit()
        log += 'ステータス\n\n'
        log += f'満腹度：{player["満腹度"]}\n喉の潤い：{player["喉の潤い"]}\n正気度：{player["正気度"]}\n\n'

        log += '素材\n\n'
        for item in items:
            if item['type'] == '素材' and item['amount'] > 0:
                log += f'{item["name"]}：{item["amount"]}\n'
        log += "\n消耗品\n\n"
        for item in items:
            if item['type'] == '消耗品' and item['amount'] > 0:
                log += f'{item["name"]}：{item["amount"]}\n'
        log += "\nアイテム\n\n"
        for item in items:
            if item['type'] == 'アイテム' and item['amount'] > 0:
                log += f'{item["name"]}：{item["amount"]}\n'
        self.tb_log.setText(log)

    def ButtonInit(self):
        # 「探索」ボタンの生成と設定
        self.btn_explore = Qw.QPushButton('探索')
        self.btn_explore.setMinimumSize(50, 30)
        self.btn_explore.setMaximumSize(100, 30)
        self.btn_explore.setSizePolicy(sp_exp, sp_exp)
        # 探索ボタンクリックでexploreメソッドを呼び出す
        self.btn_explore.clicked.connect(self.explore)
        self.button_layout.addWidget(self.btn_explore)
        self.btn_explore.installEventFilter(self)

        # 「クラフト」ボタンの生成と設定
        self.btn_craft = Qw.QPushButton('クラフト')
        self.btn_craft.setMinimumSize(50, 30)
        self.btn_craft.setMaximumSize(100, 30)
        self.btn_craft.setSizePolicy(sp_exp, sp_exp)
        self.btn_craft.clicked.connect(self.Craft)
        self.button_layout.addWidget(self.btn_craft)
        self.btn_craft.installEventFilter(self)

        # 「使用」ボタンの生成と設定
        self.btn_use = Qw.QPushButton('使用')
        self.btn_use.setMinimumSize(50, 30)
        self.btn_use.setMaximumSize(100, 30)
        self.btn_use.setSizePolicy(sp_exp, sp_exp)
        self.btn_use.clicked.connect(self.Use)
        self.button_layout.addWidget(self.btn_use)
        self.btn_use.installEventFilter(self)

        # すいみんボタンの生成と設定
        self.btn_sleep = Qw.QPushButton('睡眠')
        self.btn_sleep.setMinimumSize(50, 30)
        self.btn_sleep.setMaximumSize(100, 30)
        self.btn_sleep.setSizePolicy(sp_exp, sp_exp)
        self.btn_sleep.clicked.connect(self.Sleep)
        self.button_layout.addWidget(self.btn_sleep)
        self.btn_sleep.installEventFilter(self)

    def Sleep(self):
        self.tb_log.clear()
        self.DeleteButton()
        self.setStyleSheet(
            "QMainWindow {background-image: url('Assets/sleep.png'); background-size: cover;}")
        self.time += 7
        player["満腹度"] -= 10
        player["喉の潤い"] -= 10
        player["正気度"] += 50
        self.tb_log.append('zzz')
        self.handle_next_button()
        self.DeleteButton()
        self.ButtonInit()
        self.DrawItems()

    def DeleteButton(self):
        for i in reversed(range(self.button_layout.count())):
            widget = self.button_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

    def handle_next_button(self):
        self.DeleteButton()
        self.DrawNextbutton()
        loop = Qc.QEventLoop()
        self.btn_next.clicked.connect(loop.quit)
        loop.exec()
        self.ClickedNext = False

    # 探索ボタンがクリックされた時の処理
    def explore(self):
        self.tb_log.clear()  # ログをクリア
        # 現在のボタンをすべて削除
        self.DeleteButton()

        # 新たに「森」と「海辺」のボタンを追加
        if map_date[0]['unlock'] == True:
            self.btn_forest = Qw.QPushButton('森')
            self.btn_forest.setMinimumSize(50, 30)
            self.btn_forest.setMaximumSize(100, 30)
            self.btn_forest.setSizePolicy(sp_exp, sp_exp)
            self.btn_forest.installEventFilter(self)
            self.btn_forest.clicked.connect(lambda: self.on_explore_clicked(0))
            self.button_layout.addWidget(self.btn_forest)

        if map_date[1]['unlock'] == True:
            self.btn_seaside = Qw.QPushButton('海辺')
            self.btn_seaside.setMinimumSize(50, 30)
            self.btn_seaside.setMaximumSize(100, 30)
            self.btn_seaside.setSizePolicy(sp_exp, sp_exp)
            self.btn_seaside.installEventFilter(self)
            self.btn_seaside.clicked.connect(
                lambda: self.on_explore_clicked(1))
            self.button_layout.addWidget(self.btn_seaside)

        if map_date[2]['unlock'] == True:
            self.btn_deepforest = Qw.QPushButton('深い森')
            self.btn_deepforest.setMinimumSize(50, 30)
            self.btn_deepforest.setMaximumSize(100, 30)
            self.btn_deepforest.setSizePolicy(sp_exp, sp_exp)
            self.btn_deepforest.installEventFilter(self)
            self.btn_deepforest.clicked.connect(
                lambda: self.on_explore_clicked(2))
            self.button_layout.addWidget(self.btn_deepforest)

        if map_date[3]['unlock'] == True:
            self.btn_shipwreck = Qw.QPushButton('難破船')
            self.btn_shipwreck.setMinimumSize(50, 30)
            self.btn_shipwreck.setMaximumSize(100, 30)
            self.btn_shipwreck.setSizePolicy(sp_exp, sp_exp)
            self.btn_shipwreck.installEventFilter(self)
            self.btn_shipwreck.clicked.connect(
                lambda: self.on_explore_clicked(3))
            self.button_layout.addWidget(self.btn_shipwreck)

    def on_explore_clicked(self, index):
        self.tb_log.clear()
        player["満腹度"] -= map_date[index]['status'][0]
        player["喉の潤い"] -= map_date[index]['status'][1]
        player["正気度"] -= map_date[index]['status'][2]
        self.time += 2
        map_date[index]['count'] += 1
        if self.TimeStatus == '夜':
            player["正気度"] -= 10
        if (map_date[index]['name'] == "森" or map_date[index]['name'] == '深い森') and items[11]['amount'] > 0:
            items[0]['amount'] += 1
            self.tb_log.append('木材を入手しました。')
        if (map_date[index]['name'] == "森" or map_date[index]['name'] == '深い森') and items[12]['amount'] > 0:
            items[2]['amount'] += 1
            self.tb_log.append('生肉を入手しました。')
        if (map_date[index]['name'] == '海辺' or map_date[index] == 3) and items[13]['amount'] > 0:
            items[3]['amount'] += 1
            self.tb_log.append('石ころを入手しました。')

        # 背景画像の変更
        if map_date[index]['name'] == "森":
            self.setStyleSheet(
                "QMainWindow {background-image: url('Assets/forest.jpg'); background-size: cover;}")
        elif map_date[index]['name'] == "海辺":
            self.setStyleSheet(
                "QMainWindow {background-image: url('Assets/seaside.jpg'); background-size: cover;}")
        elif map_date[index]['name'] == "深い森":
            self.setStyleSheet(
                "QMainWindow {background-image: url('Assets/deepforest.jpg'); background-size: cover;}")
        elif map_date[index]['name'] == "難破船":
            self.setStyleSheet(
                "QMainWindow {background-image: url('Assets/shipwreck.jpg'); background-size: cover;}")
        for item in map_date[index]['items']:
            if item[3] == True and item[2] > random.random():
                self.tb_log.append(f'{item[0]}を入手しました。')
                for i in range(len(items)):
                    if items[i]['name'] == item[0]:
                        items[i]['amount'] += item[1]

        if map_date[0]['count'] == 5:
            map_date[2]['unlock'] = True
            self.tb_log.append('深い森が解放されました。')
        if map_date[1]['count'] == 5:
            map_date[3]['unlock'] = True
            self.tb_log.append('難破船が解放されました。')
        self.handle_next_button()
        self.DeleteButton()
        self.ButtonInit()
        self.DrawItems()

    # クラフトボタンがクリックされた時の処理
    def Craft(self):
        self.tb_log.clear()
        self.DeleteButton()
        self.DrawItems()
        self.time += 1
        # たき火ボタンの生成と設定
        self.btn_FireBench = Qw.QPushButton('たき火')
        self.btn_FireBench.setMinimumSize(50, 30)
        self.btn_FireBench.setMaximumSize(100, 30)
        self.btn_FireBench.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_FireBench)
        self.btn_FireBench.installEventFilter(self)
        self.btn_FireBench.clicked.connect(lambda: self.OnCraft('たき火'))
        # 焼き肉ボタンの生成と設定
        self.btn_FiredMeet = Qw.QPushButton('焼き肉')
        self.btn_FiredMeet.setMinimumSize(50, 30)
        self.btn_FiredMeet.setMaximumSize(100, 30)
        self.btn_FiredMeet.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_FiredMeet)
        self.btn_FiredMeet.installEventFilter(self)
        self.btn_FiredMeet.clicked.connect(lambda: self.OnCraft('焼き肉'))
        # 簡易浄水器ボタンの生成と設定
        self.btn_WaterPurifier = Qw.QPushButton('浄水器')
        self.btn_WaterPurifier.setMinimumSize(50, 30)
        self.btn_WaterPurifier.setMaximumSize(100, 30)
        self.btn_WaterPurifier.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_WaterPurifier)
        self.btn_WaterPurifier.installEventFilter(self)
        self.btn_WaterPurifier.clicked.connect(lambda: self.OnCraft('浄水器'))
        # 水ボタンの生成と設定
        self.btn_Water = Qw.QPushButton('水')
        self.btn_Water.setMinimumSize(50, 30)
        self.btn_Water.setMaximumSize(100, 30)
        self.btn_Water.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_Water)
        self.btn_Water.installEventFilter(self)
        self.btn_Water.clicked.connect(lambda: self.OnCraft('水'))
        # 石の斧ボタンの生成と設定
        self.btn_Axe = Qw.QPushButton('斧')
        self.btn_Axe.setMinimumSize(50, 30)
        self.btn_Axe.setMaximumSize(100, 30)
        self.btn_Axe.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_Axe)
        self.btn_Axe.installEventFilter(self)
        self.btn_Axe.clicked.connect(lambda: self.OnCraft('斧'))
        # 弓ボタンの生成と設定
        self.btn_Bow = Qw.QPushButton('弓')
        self.btn_Bow.setMinimumSize(50, 30)
        self.btn_Bow.setMaximumSize(100, 30)
        self.btn_Bow.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_Bow)
        self.btn_Bow.installEventFilter(self)
        self.btn_Bow.clicked.connect(lambda: self.OnCraft('弓'))
        # 石のつるはしボタンの生成と設定

        self.btn_Pickaxe = Qw.QPushButton('つるはし')
        self.btn_Pickaxe.setMinimumSize(50, 30)
        self.btn_Pickaxe.setMaximumSize(100, 30)
        self.btn_Pickaxe.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_Pickaxe)
        self.btn_Pickaxe.installEventFilter(self)
        self.btn_Pickaxe.clicked.connect(lambda: self.OnCraft('つるはし'))
        # 木材加工機ボタンの生成と設定
        self.btn_WoodMachine = Qw.QPushButton('木工機')
        self.btn_WoodMachine.setMinimumSize(50, 30)
        self.btn_WoodMachine.setMaximumSize(100, 30)
        self.btn_WoodMachine.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_WoodMachine)
        self.btn_WoodMachine.installEventFilter(self)
        self.btn_WoodMachine.clicked.connect(lambda: self.OnCraft('木工機'))
        # 石材加工機ボタンの生成と設定
        self.btn_StoneMachine = Qw.QPushButton('石工機')
        self.btn_StoneMachine.setMinimumSize(50, 30)
        self.btn_StoneMachine.setMaximumSize(100, 30)
        self.btn_StoneMachine.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_StoneMachine)
        self.btn_StoneMachine.installEventFilter(self)
        self.btn_StoneMachine.clicked.connect(lambda: self.OnCraft('石工機'))
        # 厚板ボタンの生成と設定
        self.btn_ThickPlate = Qw.QPushButton('厚板')
        self.btn_ThickPlate.setMinimumSize(50, 30)
        self.btn_ThickPlate.setMaximumSize(100, 30)
        self.btn_ThickPlate.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_ThickPlate)
        self.btn_ThickPlate.installEventFilter(self)
        self.btn_ThickPlate.clicked.connect(lambda: self.OnCraft('厚板'))
        # レンガボタンの生成と設定
        self.btn_Brick = Qw.QPushButton('レンガ')
        self.btn_Brick.setMinimumSize(50, 30)
        self.btn_Brick.setMaximumSize(100, 30)
        self.btn_Brick.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_Brick)
        self.btn_Brick.installEventFilter(self)
        self.btn_Brick.clicked.connect(lambda: self.OnCraft('レンガ'))
        # いかだボタンの生成と設定
        self.btn_Raft = Qw.QPushButton('いかだ')
        self.btn_Raft.setMinimumSize(50, 30)
        self.btn_Raft.setMaximumSize(100, 30)
        self.btn_Raft.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_Raft)
        self.btn_Raft.installEventFilter(self)
        self.btn_Raft.clicked.connect(lambda: self.OnCraft('いかだ'))

    def OnCraft(self, ItemName):
        if ItemName == 'たき火' and items[0]['amount'] >= 5:
            items[0]['amount'] -= 5
            items[4]['amount'] += 1
            self.tb_log.setText('たき火を作成しました。')
        elif ItemName == '焼き肉' and items[2]['amount'] >= 1 and items[4]['amount'] >= 1 and items[0]['amount'] >= 1:
            items[2]['amount'] -= 1
            items[0]['amount'] -= 1
            items[5]['amount'] += 1
            self.tb_log.setText('焼き肉を作成しました。')
        elif ItemName == '浄水器' and items[3]['amount'] >= 5:
            items[3]['amount'] -= 5
            items[10]['amount'] += 1
            self.tb_log.setText('浄水器を作成しました。')
        elif ItemName == '水' and items[7]['amount'] >= 1 and items[10]['amount'] >= 1:
            items[7]['amount'] -= 3
            items[8]['amount'] += 1
            self.tb_log.setText('水を作成しました')
        elif ItemName == '斧' and items[3]['amount'] >= 5 and items[0]['amount'] >= 3 and items[9]['amount'] >= 2:
            items[3]['amount'] -= 5
            items[0]['amount'] -= 3
            items[9]['amount'] -= 2
            items[11]['amount'] += 1
            self.tb_log.setText('斧を作成しました')
        elif ItemName == '弓' and items[0]['amount'] >= 5 and items[9]['amount'] >= 5:
            items[0]['amount'] -= 5
            items[9]['amount'] -= 5
            items[12]['amount'] += 1
            self.tb_log.setText('弓を作成しました')
        elif ItemName == 'つるはし' and items[3]['amount'] >= 5 and items[0]['amount'] >= 3 and items[9]['amount'] >= 2:
            items[3]['amount'] -= 5
            items[0]['amount'] -= 3
            items[9]['amount'] -= 2
            items[13]['amount'] += 1
            self.tb_log.setText('つるはしを作成しました')
        elif ItemName == '木工機' and items[0]['amount'] >= 5 and items[3]['amount'] >= 3 and items[14]['amount'] >= 3:
            items[0]['amount'] -= 5
            items[3]['amount'] -= 3
            items[14]['amount'] -= 3
            items[16]['amount'] += 1
            self.tb_log.setText('木工機を作成しました')
        elif ItemName == '石工機' and items[3]['amount'] >= 5 and items[0]['amount'] >= 3 and items[15]['amount'] >= 2:
            items[3]['amount'] -= 5
            items[0]['amount'] -= 3
            items[14]['amount'] -= 3
            items[17]['amount'] += 1
            self.tb_log.setText('石工機を作成しました')
        elif ItemName == '厚板' and items[0]['amount'] >= 0 and items[14]['amount'] >= 3 and items[16]['amount'] >= 1:
            items[0]['amount'] -= 3
            items[14]['amount'] -= 1
            items[15]['amount'] += 1
            self.tb_log.setText('厚板を作成しました')
        elif ItemName == 'レンガ' and items[3]['amount'] >= 5 and items[14]['amount'] >= 3 and items[18]['amount'] >= 1:
            items[3]['amount'] -= 3
            items[14]['amount'] -= 1
            items[17]['amount'] += 1
            self.tb_log.setText('レンガを作成しました')
        elif ItemName == 'いかだ' and items[16]['amount'] >= 3 and items[18]['amount'] >= 3 and items[9]['amount'] >= 10 and items[5]['amount'] >= 5 and items[8]['amount'] >= 5:
            items[16]['amount'] -= 3
            items[18]['amount'] -= 3
            items[9]['amount'] -= 10
            items[5]['amount'] -= 5
            items[8]['amount'] -= 5
            items[6]['amount'] += 1
            self.tb_log.setText('いかだを作成しました')

        self.handle_next_button()
        self.DeleteButton()
        self.ButtonInit()
        self.DrawItems()

    # 使用ボタンがクリックされた時の処理
    def Use(self):
        self.tb_log.clear()
        self.DeleteButton()
        self.DrawItems()
        # 生肉ボタンの生成と設定
        self.btn_Meat = Qw.QPushButton('生肉')
        self.btn_Meat.setMinimumSize(50, 30)
        self.btn_Meat.setMaximumSize(100, 30)
        self.btn_Meat.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_Meat)
        self.btn_Meat.installEventFilter(self)
        self.btn_Meat.clicked.connect(lambda: self.OnUse('生肉'))
        # 焼き肉ボタンの生成と設定
        self.btn_FiredMeet = Qw.QPushButton('焼き肉')
        self.btn_FiredMeet.setMinimumSize(50, 30)
        self.btn_FiredMeet.setMaximumSize(100, 30)
        self.btn_FiredMeet.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_FiredMeet)
        self.btn_FiredMeet.installEventFilter(self)
        self.btn_FiredMeet.clicked.connect(lambda: self.OnUse('焼き肉'))
        # 海水ボタンの生成と設定
        self.btn_SeaWater = Qw.QPushButton('海水')
        self.btn_SeaWater.setMinimumSize(50, 30)
        self.btn_SeaWater.setMaximumSize(100, 30)
        self.btn_SeaWater.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_SeaWater)
        self.btn_SeaWater.installEventFilter(self)
        self.btn_SeaWater.clicked.connect(lambda: self.OnUse('海水'))
        # 水ボタンの生成と設定
        self.btn_Water = Qw.QPushButton('水')
        self.btn_Water.setMinimumSize(50, 30)
        self.btn_Water.setMaximumSize(100, 30)
        self.btn_Water.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_Water)
        self.btn_Water.installEventFilter(self)
        self.btn_Water.clicked.connect(lambda: self.OnUse('水'))
        # いかだボタンの生成と設定
        self.btn_Raft = Qw.QPushButton('脱出')
        self.btn_Raft.setMinimumSize(50, 30)
        self.btn_Raft.setMaximumSize(100, 30)
        self.btn_Raft.setSizePolicy(sp_exp, sp_exp)
        self.button_layout.addWidget(self.btn_Raft)
        self.btn_Raft.installEventFilter(self)
        self.btn_Raft.clicked.connect(lambda: self.OnUse('脱出'))

    def OnUse(self, ItemName):
        if ItemName == '生肉' and items[2]['amount'] >= 1:
            items[2]['amount'] -= 1
            if player['満腹度'] < 100:
                player['満腹度'] += 10
                player["正気度"] -= 5
                if player['満腹度'] > 100:
                    player['満腹度'] = 100
            self.tb_log.setText('生肉を使用しました。')
        elif ItemName == '焼き肉' and items[5]['amount'] >= 1:
            items[5]['amount'] -= 1
            items[6]['amount'] += 1
            if player['満腹度'] < 100:
                player['満腹度'] += 20
                if player['満腹度'] > 100:
                    player['満腹度'] = 100
            self.tb_log.setText('焼き肉を使用しました。')
        elif ItemName == '海水' and items[7]['amount'] >= 1:
            items[7]['amount'] -= 1
            items[8]['amount'] += 1
            if player['喉の潤い'] < 100:
                player['喉の潤い'] += 10
                player["正気度"] -= 5
                if player['喉の潤い'] > 100:
                    player['喉の潤い'] = 100
            self.tb_log.setText('海水を使用しました。')
        elif ItemName == '水' and items[8]['amount'] >= 1:
            items[8]['amount'] -= 1
            if player['喉の潤い'] < 100:
                player['喉の潤い'] += 20
                if player['喉の潤い'] > 100:
                    player['喉の潤い'] = 100
            self.tb_log.setText('水を使用しました。')
        elif ItemName == '脱出' and items[6]['amount'] >= 1:
            items[6]['amount'] -= 1
            self.DeleteButton()
            self.tb_log.setText('無人島からの脱出に成功しました。')
            self.tb_log.append('おめでとうございます。')
            self.tb_log.append('脱出にかかった時間は')
            self.tb_log.append(f'{self.day}日と{self.time}時間でした。')
            self.tb_log.append('より良い記録を目指して是非再チャレンジしてください。')
            self.tb_log.append('確認ボタンをクリックするとゲームが終了します。')
            self.handle_next_button()
            sys.exit()

        self.handle_next_button()
        self.DeleteButton()
        self.ButtonInit()
        self.DrawItems()

    def eventFilter(self, obj, event):
        # 睡眠ボタン
        if obj == self.btn_sleep:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('7時間の睡眠をとります。')
                self.tb_log.append('満腹度、喉の潤いがそれぞれ10,10減少します。')
                self.tb_log.append('正気度が50回復します。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 探索ボタン
        if obj == self.btn_explore:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('島の探索を行い、素材を採集します。')
                self.tb_log.append('特定のエリアを一定回数探索すると、新たなエリアが解放されます。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 森ボタン

        elif obj == self.btn_forest:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('森を探索します。')
                self.tb_log.append('木材や動物の素材を入手できます。')
                self.tb_log.append('満腹度、喉の潤い、正気度がそれぞれ10,10,5減少します。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                if self.btn_forest.isVisible():
                    self.DrawItems()

        # 海辺ボタン
        elif obj == self.btn_seaside:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('海辺を探索します。')
                self.tb_log.append('石ころ、海水などの素材を入手できます。')
                self.tb_log.append('満腹度、喉の潤い、正気度がそれぞれ15,5,0減少します。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                if self.btn_seaside.isVisible():
                    self.DrawItems()

        # 深い森ボタン
        elif hasattr(self, 'btn_deepforest') and obj == self.btn_deepforest:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('深い森を探索します。')
                self.tb_log.append('木材や繊維、動物の素材を入手できます。')
                self.tb_log.append('満腹度、喉の潤い、正気度がそれぞれ20,10,10減少します。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                if self.btn_deepforest.isVisible():
                    self.DrawItems()

        # 難破船ボタン
        elif hasattr(self, 'btn_shipwreck') and obj == self.btn_shipwreck:
            if event.type() == Qc.QEvent.Enter:
                self.tb_log.setText('難破船を探索します。')
                self.tb_log.append('石ころや繊維などの素材を入手できます。')
                self.tb_log.append('満腹度、喉の潤い、正気度がそれぞれ20,10,5減少します。')
            elif event.type() == Qc.QEvent.Leave:
                if self.btn_shipwreck.isVisible():
                    self.DrawItems()

        # クラフトボタン
        elif obj == self.btn_craft:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('アイテムを作成します。')
                self.tb_log.append('素材を消費してアイテムを作成します。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 使用ボタン
        elif obj == self.btn_use:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('アイテムを使用します。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # たき火ボタン
        elif hasattr(self, 'btn_FireBench') and obj == self.btn_FireBench:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('木材5つで製作可能です。')
                self.tb_log.append('また、生肉を調理することができます。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 焼き肉ボタン
        elif hasattr(self, 'btn_FiredMeet') and obj == self.btn_FiredMeet:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('生肉1つ、木材1つで製作可能です。')
                self.tb_log.append('たき火が必要です。(消費はしない)')
                self.tb_log.append('消耗品として使用すると、満腹度を回復できます。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 生肉ボタン
        elif hasattr(self, 'btn_Meat') and obj == self.btn_Meat:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('生肉を使用します。')
                self.tb_log.append('消耗品として使用すると、満腹度を回復できるが、正気度が減少します。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 海水ボタン
        elif hasattr(self, 'btn_SeaWater') and obj == self.btn_SeaWater:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('海水を使用します。')
                self.tb_log.append('消耗品として使用すると、喉の潤いを回復できるが、正気度が減少します。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 水ボタン
        elif hasattr(self, 'btn_Water') and obj == self.btn_Water:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('海水を浄水器で浄水すると制作できます。')
                self.tb_log.append('消耗品として使用すると、喉の潤いを回復できる。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 簡易浄水器ボタン
        elif hasattr(self, 'btn_WaterPurifier') and obj == self.btn_WaterPurifier:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('石ころ5つで製作可能です。')
                self.tb_log.append('海水を水に浄水できます。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 石の斧ボタン
        elif hasattr(self, 'btn_Axe') and obj == self.btn_Axe:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('石ころ5つ、木材3つ、繊維2つで製作可能です。')
                self.tb_log.append('素材を採集する際に木材の取得量が増加する。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 弓ボタン
        elif hasattr(self, 'btn_Bow') and obj == self.btn_Bow:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('木材5つ、繊維5つで製作可能です。')
                self.tb_log.append('動物を狩る際に生肉の取得量が増加する。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 石のつるはしボタン
        elif hasattr(self, 'btn_Pickaxe') and obj == self.btn_Pickaxe:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('石ころ5つ、木材3つ、繊維2つで製作可能です。')
                self.tb_log.append('石ころの採集量が増加する。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 木材加工機ボタン
        elif hasattr(self, 'btn_WoodMachine') and obj == self.btn_WoodMachine:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('木材5つ、石ころ3つ、プラスチック3つで製作可能です。')
                self.tb_log.append('木材を加工して厚板を作成できるようになる。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 石材加工機ボタン
        elif hasattr(self, 'btn_StoneMachine') and obj == self.btn_StoneMachine:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('石ころ5つ、木材3つ、プラスチック3つで製作可能です。')
                self.tb_log.append('石ころを加工してレンガ を作成できるようになる。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 厚板ボタン
        elif hasattr(self, 'btn_ThickPlate') and obj == self.btn_ThickPlate:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('木材3つ、プラスチック1つで製作可能です。')
                self.tb_log.append('いかだの作成に使えます。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # レンガボタン
        elif hasattr(self, 'btn_Brick') and obj == self.btn_Brick:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('石ころ3つ、プラスチック1つで製作可能です。')
                self.tb_log.append('いかだの作成に使えます。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # いかだボタン
        elif hasattr(self, 'btn_Raft') and obj == self.btn_Raft:
            if event.type() == Qc.QEvent.Enter:  # マウスがボタンに入った時
                self.tb_log.setText('厚板3つ、レンガ3つ、繊維10つ、焼き肉5つ、水5つで製作可能です。')
                self.tb_log.append('長い船旅には食料と水分も欠かせない。')
                self.tb_log.append('なんでレンガなんて使うんだろう。')
                self.tb_log.append('無人島からの脱出に使えます。')
            elif event.type() == Qc.QEvent.Leave:  # マウスがボタンから離れた時
                self.DrawItems()

        # 他のイベントをそのまま伝播させる
        return super().eventFilter(obj, event)


# 本体
if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
