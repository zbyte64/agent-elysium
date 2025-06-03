import asyncio
import sys


async def ainput(string: str) -> str:
    sys.stdout.write(string)
    return await asyncio.to_thread(sys.stdin.readline)


def interaction_params(**kwargs):
    return {
        "print_f": print,
        "input_f": ainput,
    }
