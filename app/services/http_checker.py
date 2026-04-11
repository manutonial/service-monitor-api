import time
import httpx

class HttpChecker:
    
    async def check(self, url: str):
        start = time.perf_counter()

        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                response = await client.get(url)
            time_elapsed = int((time.perf_counter() - start) * 1000) # pyright: ignore[reportInvalidTypeForm]

            return {
                "status": response.status_code,
                "response_time_ms": time_elapsed,
                "error_message": None
            }
        
        except Exception as e:
            time_elapsed = int((time.perf_counter() - start) * 1000) # pyright: ignore[reportInvalidTypeForm]
            
            return {
                "status": None,
                "response_time_ms": time_elapsed,
                "error_message": str(e)
            }