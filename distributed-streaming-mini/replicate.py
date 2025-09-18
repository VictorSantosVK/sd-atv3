
import sys, shutil, pathlib, json

cfg = json.load(open("nodes.json", "r", encoding="utf-8"))
dest_dirs = [pathlib.Path(n["root"]) for n in cfg["nodes"]]

def main():
    if len(sys.argv) < 2:
        print("Uso: python replicate.py CAMINHO_DO_ARQUIVO")
        sys.exit(1)
    src = pathlib.Path(sys.argv[1]).expanduser()
    if not src.exists():
        print(f"Arquivo não encontrado: {src}")
        sys.exit(1)

    for d in dest_dirs:
        d.mkdir(parents=True, exist_ok=True)
        dst = d / src.name
        shutil.copyfile(src, dst)
        print(f"[OK] Copiado para {dst}")
    print("Pronto! O arquivo está nos três nós. Abra com pick_node_and_open.py NOME_DO_ARQUIVO")

if __name__ == "__main__":
    main()
