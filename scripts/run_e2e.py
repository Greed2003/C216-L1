from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
COMPOSE_FILE = ROOT / "compose.e2e.yaml"
COMPOSE_PROJECT = "c216-l1-e2e"

COMPOSE_COMMAND = [
    "docker",
    "compose",
    "-p",
    COMPOSE_PROJECT,
    "-f",
    str(COMPOSE_FILE),
]


def run(
    command: Sequence[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    print(f"\n> {shlex.join(command)}", flush=True)

    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=check,
        text=True,
    )


def remove_stack() -> None:
    run(
        [
            *COMPOSE_COMMAND,
            "down",
            "-v",
            "--remove-orphans",
        ],
        check=False,
    )


def main() -> int:
    npm = "npm.cmd" if os.name == "nt" else "npm"

    remove_stack()

    try:
        run(
            [
                *COMPOSE_COMMAND,
                "up",
                "-d",
                "--build",
                "--wait",
                "--wait-timeout",
                "120",
            ]
        )

        run(
            [
                *COMPOSE_COMMAND,
                "exec",
                "-T",
                "api",
                "poetry",
                "run",
                "alembic",
                "upgrade",
                "head",
            ]
        )

        run([*COMPOSE_COMMAND, "ps"])

        environment = os.environ.copy()
        environment["E2E_BASE_URL"] = "http://127.0.0.1:5174"

        run(
            [npm, "run", "test:e2e"],
            cwd=ROOT / "frontend",
            env=environment,
        )

        return 0
    finally:
        remove_stack()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode) from error
    except KeyboardInterrupt:
        raise SystemExit(130)
