import importlib.util
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SESSION_FILE = BASE_DIR / ".collector_session.json"
COLLECTOR_SCRIPT = BASE_DIR / "scripts" / "01_collect_data.py"


def load_member_hashes() -> dict:
    spec = importlib.util.spec_from_file_location("collect_data", str(COLLECTOR_SCRIPT))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {COLLECTOR_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "MEMBER_HASHES", {})


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(BASE_DIR),
        text=True,
        capture_output=True,
        check=check,
    )


def main() -> None:
    if not SESSION_FILE.exists():
        print("❌ No active session found. Run 'python scripts/01_collect_data.py' and log in first.")
        sys.exit(1)

    session = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
    key_hash = session.get("key_hash", "").strip()

    member_hashes = load_member_hashes()
    member = member_hashes.get(key_hash)

    if not member:
        print("❌ Session key not recognized. Please re-run 'python scripts/01_collect_data.py' and log in.")
        sys.exit(1)

    slug = member["slug"].strip()
    name = member.get("name", slug)

    csv_rel_path = f"data/raw/landmarks_{slug}.csv"
    csv_full_path = BASE_DIR / csv_rel_path

    if not csv_full_path.exists():
        print(f"❌ Dataset file not found: {csv_rel_path}")
        print("   Record your signs with 'python scripts/01_collect_data.py' first.")
        sys.exit(1)

    branch_name = f"data/{slug}"

    try:
        current_branch = run_git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        if current_branch != branch_name:
            exists = run_git("rev-parse", "--verify", branch_name, check=False).returncode == 0
            if exists:
                run_git("checkout", branch_name)
            else:
                run_git("checkout", "-b", branch_name)
            print(f"✅ Switched to branch: {branch_name}")

        # Stage ONLY this teammate's CSV file
        run_git("add", csv_rel_path)

        # Check if there are actual changes to commit
        diff = run_git("diff", "--cached", "--quiet", check=False)
        if diff.returncode == 0:
            print(f"ℹ️  No new changes in {csv_rel_path} to commit.")
            return

        run_git("commit", "-m", f"data({slug}): submit sign samples from {name}")
        print(f"✅ Committed {csv_rel_path}")

        print(f"🚀 Pushing to origin/{branch_name}...")
        run_git("push", "-u", "origin", branch_name)

        print("\n🎉 Done! Now open GitHub in your browser and click 'Compare & pull request':")
        print("   https://github.com/MinKhant30/msl-prototype")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Git error:\n{e.stderr or e.stdout}")
        sys.exit(1)


if __name__ == "__main__":
    main()