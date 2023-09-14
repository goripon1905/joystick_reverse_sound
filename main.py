from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import json
import sys

pygame.init()
pygame.joystick.init()

print("-------------------------------")
print("リバース音ツール ver.1.0.0")
print("Created by goripon1905")
print("-------------------------------")

# JSONから設定の読み取り
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

# デバッグの設定を読み取り
debug_mode = config_data.get("debug", False)

# 指定したコントローラーとサウンドファイルのパスの読み取り
target_controller_name = config_data.get("target_controller_name", "")
print(f"指定コントローラ: {target_controller_name}")
sound_file_path = config_data.get("sound_file_path", "")
print(f"サウンドファイル: {sound_file_path}")

# 音量を0から100の範囲に制限
sound_volume = min(max(config_data.get("sound_volume", 50), 0), 100)
print(f"音量: {sound_volume}")

# ボタンのインデックスを読み取り
button_index = config_data.get("button_index","")
print(f"トリガーボタン: {button_index}")
print("===============================")

# コントローラーの数を取得
controller_count = pygame.joystick.get_count()
target_controller = None

# コントローラー指定
for i in range(controller_count):
    controller = pygame.joystick.Joystick(i)
    controller.init()
    if controller.get_name() == target_controller_name:
        target_controller = controller
        break

if target_controller is None:
    print(f"エラー：{target_controller_name} が見つかりません")
    print("解決法：接続されているデバイス名と指定したデバイス名が正しいか確認してください")
    input("何かキーを押して終了...")
    pygame.quit()
    exit()


pygame.mixer.init()

# サウンドファイルロード
sound = pygame.mixer.Sound(sound_file_path)

# 音量を設定
sound.set_volume(sound_volume / 100)

# JSONからデバッグの設定を読み込み
debug_mode = config_data.get("debug", "false").lower() == "true"

if debug_mode:
    print("★ デバッグモードが有効です")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"デバッグ: {event.button}押下")
                if event.button == button_index:
                    print("デバッグ：指定ボタン押下")
                    sound.play(-1)
                    print("デバッグ：リバース音_再生")

            elif event.type == pygame.JOYBUTTONUP:
                print(f"デバッグ: {event.button}離上")
                if event.button == button_index:
                    print("デバッグ：指定ボタン離上")
                    sound.stop()
                    print("デバッグ：リバース音_停止")
else:
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == button_index:
                        sound.play(-1)

                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == button_index:
                        sound.stop()
    except KeyboardInterrupt:
        pass

    finally:
        pygame.quit()
        sys.exit(0)