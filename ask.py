
# pythonが動いている
import sys
from pathlib import Path

from openai_codex import Codex, Sandbox

## サンドボックスの設定
## 意味：外に被害がでないよに囲った安全な作業場所って意味
# None = codex コマンドと同じ設定。Sandbox.read_only なども入れられる
## read_only に設定するとサンドボックスが読み取り専用になる
## None に設定すると codex コマンドと同じ設定になる
## workspace_write に設定するとサンドボックスが書き込み可能になる（作業フォルダーの中なら書いてもいいってこと）
SANDBOX = Sandbox.read_only


# def = defineの略（定義するという意味）
def main():
    # ①sys.argv[1]：コマンドの1番目の引数を取り出す
    # ②Path()：文字列を「パス」として扱える形に変える。
    # ③.expanduser(): ~を自分のホームフォルダーに置き換える
    # ④.resolve() : 完全な絶対パスにする
    # ⑤str() : 普通の文字列に戻す＾
    folder = str(Path(sys.argv[1]).expanduser().resolve())
    print("folder:", folder)
    question = sys.argv[2]
    print("question:", question)# 質問内容を確認 今回だと"このフォルダのコードは何をしている？3行で"

    with Codex() as codex:
        print("codex:", codex)
        options = {
            # cwd = current working directory（作業フォルダ）を指定する
            "cwd": folder,

            # 開発者への指示（developer_instructions）を設定する部分
            "developer_instructions": (
                # fはフォーマット済み文字列（formatted string）の意味
                # 文字列の中に変数を埋め込むことができる
                # もしfがなかったらだたの{folder}という文字列になってしまう
                f"ユーザーが言う「このフォルダ」は作業フォルダ {folder} のことです。"
                "あなたはこのフォルダのファイルを読む権限を持っています。"
                "答える前に、必ずコマンドでファイル一覧と中身を確認してください。"
            ),
        }
        if SANDBOX is not None:
            options["sandbox"] = SANDBOX
        print("options[\"sandbox\"]:", options["sandbox"])
        print("options[\"cwd\"]:", options["cwd"])
        print("SANDBOX:", SANDBOX) # SANDBOXの設定を確認
        print("options:", options)
        thread = codex.thread_start(**options)
        print("thread started")
        print("thread:", thread)
        result = thread.run(question)
        print("result.final_response:", result.final_response)

        print("\n----- Codexがやったこと -----")
        for item in result.items:
            print(type(item.root).__name__)
        print("result.items:", result.items)


if __name__ == "__main__":
    main()

# .envの環境変数から読み込む場合は load_dotenv() を有効にする
# その場合は USE_API_KEY を True にする

# codexからログインする2つのパターンが存在する。
# 1つ目は .env の API キーを使う方法（USE_API_KEY を True にする）
# 2つ目は codex コマンドからログインしている状態を使う方法（現状はこちら）