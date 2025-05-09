import asyncio
import threading
import time
import os
import socket

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI()


def cpu_intensive_task():
    while True:
        pass  # Infinite loop to keep the CPU busy


@app.get("/")
def read_root():
    return {"msg": "python-fastapi"}


@app.get("/api/exit")
def exit_application():
    print("An application error occurred - exiting with exit code 1")
    os._exit(1)
    return {"msg": "An application error occurred"}


@app.get("/api/sleep")
async def sleep():
    await asyncio.sleep(120)
    print("Slept for 120 seconds")
    return {"msg": "Sleep for 120 seconds"}


@app.get("/api/cpu")
def cpu():
    # Create multiple threads to increase CPU usage
    threads = []
    for i in range(4):  # Adjust the number of threads as needed
        thread = threading.Thread(target=cpu_intensive_task)
        thread.start()
        threads.append(thread)

    # Run the CPU-intensive task for a limited time
    time.sleep(100)  # Adjust the duration as needed

    # Stop the threads after the duration
    for thread in threads:
        thread.join(timeout=1)

    return {"msg": "CPU-intensive task completed"}


async def fake_video_streamer():
    for i in range(10000):
        yield b"some fake video bytes \n"
        # Wait 1 second in between each iteration to clearly show that this is being streamed in comparison to a typical response
        await asyncio.sleep(1)


@app.get("/api/memory/{memory_size}")
def memory(memory_size: int):
    memory_arr = []
    for _ in range(memory_size):
        memory_arr.append([0] * memory_size)

    return {"msg": "Memory allocated"}


@app.get("/api/stream")
def stream():
    return StreamingResponse(
        fake_video_streamer(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )


@app.get("/api/notstream")
async def notstream():
    arr = []
    for i in range(10000):
        await asyncio.sleep(1)
        arr.append(f"some fake video bytes {i}")

    return JSONResponse(content=arr)


@app.get("/api/dnsfailure")
def dnsfailure():
    # Simulate a DNS failure by trying to resolve a non-existent domain
    try:
        socket.gethostbyname("othernonexistent.domain")
    except socket.gaierror as e:
        return JSONResponse(content={"msg": str(e)}, status_code=500)

    return JSONResponse(content={"msg": "DNS resolution succeeded"})


@app.get("/api/dnssuccess")
def dnsfailure():
    # Simulate a DNS failure by trying to resolve a non-existent domain
    try:
        socket.gethostbyname("google.com")
    except socket.gaierror as e:
        return JSONResponse(content={"msg": str(e)}, status_code=500)

    return JSONResponse(content={"msg": "DNS resolution succeeded"})
