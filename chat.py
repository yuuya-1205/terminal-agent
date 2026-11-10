import sys
from pathlib import Path

from openai_codex import Codex, Sandbox

SANDBOX = Sandbox.workspace_write

def main():
    # A if 条件 else B という形で三項演算子を使っている
    # ここでは、コマンドライン引数があればそれを使い、なければ"."カレントディレクトリを使うという意味になる
    folder = str(Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser().resolve())

    with Codex() as codex:
        thread = codex.thread_start(cwd=folder, sandbox=SANDBOX)
        print(f"{folder} について聞けます。終わるときは /quit")

        while True:
            question = input("> ").strip()
            if question in ("/quit", "/exit"):
                break
            if not question:
                continue
            result = thread.run(question)  # 同じ thread を使い回す＝前の話を覚えている
            print(result.final_response)

# このファイルを直接実行した時だけこのファイル(chat.py)を動かす
if __name__ == "__main__":
    main()