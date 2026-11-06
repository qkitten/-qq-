"""诊断 listen_music 插件：搜索 -> 解析音频 -> 实际下载，统计耗时与错误。"""

import asyncio
import sys
import time

BASE = r"C:/Users/ZHANG789/Desktop/大肥鱼qq机器人项目/AstrBot"
sys.path.insert(0, BASE)
sys.path.insert(0, BASE + "/data/plugins")

import aiohttp  # noqa: E402
from astrbot_plugin_listen_music.core.bilibili import BilibiliClient  # noqa: E402


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        client = BilibiliClient(session, None)

        t0 = time.time()
        videos = await client.search_videos("周传雄 黄昏", limit=5)
        print(f"[search] {time.time()-t0:.2f}s, {len(videos)} hits")
        for v in videos:
            print("   ", v.bvid, v.title[:40])

        video = await client.get_video(videos[0].bvid)
        print("[video]", video.bvid, "pages:", len(video.pages), "cid:", video.pages[0].cid)

        t1 = time.time()
        audio = await client.resolve_audio(video.bvid, video.pages[0].cid)
        print(f"[resolve] {time.time()-t1:.2f}s url={audio.url[:90]}")
        print("   backups:", len(audio.backup_urls), "mime:", audio.mime_type,
              "need_remux:", audio.needs_remux, "duration_ms:", audio.duration_ms)

        t2 = time.time()
        async with session.get(audio.url, headers=dict(audio.headers)) as resp:
            print("[download] status:", resp.status, "len:", resp.headers.get("Content-Length"))
            total = 0
            async for chunk in resp.content.iter_chunked(128 * 1024):
                total += len(chunk)
                if time.time() - t2 > 120:
                    print("   ! 超过120秒，主动中断")
                    break
        print(f"[download] {time.time()-t2:.2f}s, {total/1024/1024:.2f} MB")


asyncio.run(main())
