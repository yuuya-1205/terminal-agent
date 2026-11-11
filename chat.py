import sys
from pathlib import Path
import subprocess
from openai_codex import Codex, Sandbox

SANDBOX = Sandbox.workspace_write

def main():
    # A if 条件 else B という形で三項演算子を使っている
    # ここでは、コマンドライン引数があればそれを使い、なければ"."カレントディレクトリを使うという意味になる
    folder = str(Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser().resolve())

    with Codex() as codex:
        thread = codex.thread_start(cwd=folder, sandbox=SANDBOX)
        print(f"{folder} について聞けます。/diff で変更を見る、/undo で元に戻す、/quit で終了")

        while True:
            # これについて調べる
            question = input("> ").strip()
            if question in ("/quit", "/exit"):
                break
            if question == "/diff":
                print("subprocess.run:", subprocess.run(["git", "-C", folder, "diff"], capture_output=True, text=True).stdout or "変更はありません")
                continue
            if question == "/undo":
                subprocess.run(["git", "-C", folder, "checkout", "."])
                print("最後のコミットの状態に戻しました")
                continue
            if not question:
                continue
            result = thread.run(question)  # 同じ thread を使い回す＝前の話を覚えている
            print(result.final_response)
           
            # 何が変わったかを見せる
            stat = subprocess.run(["git", "-C", folder, "diff", "--stat"], capture_output=True, text=True).stdout
            if stat.strip():
                print("\n変わったファイル（/diff で中身、/undo で元に戻す）:")
                print(stat)

# このファイルを直接実行した時だけこのファイル(chat.py)を動かす
if __name__ == "__main__":
    main()