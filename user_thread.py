import sys
import asyncio


class User_Thread:
    def __aiter__(self):
        self.loop = asyncio.get_event_loop()
        return self

    async def __anext__(self) -> str:
        cmd = await self.loop.run_in_executor(None, sys.stdin.readline)
        return cmd.strip()
