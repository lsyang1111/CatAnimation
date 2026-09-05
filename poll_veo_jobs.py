"""
poll_veo_jobs.py
================
Reads operation names from veo_ops.txt, polls until done, downloads videos.
"""
import os, sys, time, requests

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not set", flush=True)
    sys.exit(1)

out_dir = os.path.dirname(os.path.abspath(__file__))
ops_file = os.path.join(out_dir, "veo_ops.txt")

if not os.path.exists(ops_file):
    print(f"ERROR: {ops_file} not found. Run submit_veo_jobs.py first.", flush=True)
    sys.exit(1)

operations = []
with open(ops_file) as f:
    for line in f:
        line = line.strip()
        if "|" in line:
            name, op_name = line.split("|", 1)
            operations.append((name, op_name))

print(f"Loaded {len(operations)} operations:", flush=True)
for name, op in operations:
    print(f"  {name} -> {op}", flush=True)

print("\nPolling for completion...", flush=True)
completed = set()
start_time = time.time()

while len(completed) < len(operations):
    for filename, op_name in operations:
        if filename in completed:
            continue
        url = f"https://generativelanguage.googleapis.com/v1beta/{op_name}?key={API_KEY}"
        try:
            res = requests.get(url).json()
            if res.get("done"):
                if "response" in res and "generateVideoResponse" in res["response"]:
                    samples = res["response"]["generateVideoResponse"].get("generatedSamples", [])
                    if samples:
                        video_uri = samples[0]["video"]["uri"]
                        video_res = requests.get(f"{video_uri}&key={API_KEY}")
                        save_path = os.path.join(out_dir, filename)
                        with open(save_path, "wb") as vf:
                            vf.write(video_res.content)
                        size_mb = len(video_res.content) / 1024 / 1024
                        print(f"  [SAVED] {filename} ({size_mb:.1f} MB)", flush=True)
                        completed.add(filename)
                    else:
                        print(f"  [ERROR] {filename}: no samples in response", flush=True)
                        completed.add(filename)
                elif "error" in res:
                    print(f"  [ERROR] {filename}: {res['error']}", flush=True)
                    completed.add(filename)
                else:
                    print(f"  [DONE but no video?] {filename}: {res}", flush=True)
                    completed.add(filename)
            else:
                elapsed = int(time.time() - start_time)
                print(f"  [WAITING] {filename} ... ({elapsed}s)", flush=True)
        except Exception as e:
            print(f"  [WARN] {filename}: {e}", flush=True)

    if len(completed) < len(operations):
        time.sleep(20)

print("\n=== All downloads complete! ===", flush=True)
print("Now run: python concat_videos.py", flush=True)
