#!/usr/bin/env python3
import sys, os, logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("bootstrap")

MODEL_DIR = os.environ.get("MODEL_DIR", "/comfyui/models")

MODELS = [
    {
        "repo": "unsloth/Z-Image-Turbo-GGUF",
        "file": "z-image-turbo-Q4_K_M.gguf",
        "dest": os.path.join(MODEL_DIR, "unet"),
    },
    {
        "repo": "unsloth/Qwen3-4B-GGUF",
        "file": "Qwen3-4B-Q4_K_M.gguf",
        "dest": os.path.join(MODEL_DIR, "text_encoders"),
    },
    {
        "repo": "Comfy-Org/z_image_turbo",
        "file": "split_files/vae/ae.safetensors",
        "dest": os.path.join(MODEL_DIR, "vae"),
    },
    {
        "repo": "thutes-gbr25/NSFW-MASTER-Z-IMAGE-TURBO",
        "file": "NSFW_master_ZIT_000008766.safetensors",
        "dest": os.path.join(MODEL_DIR, "loras"),
    },
]

def main():
    from huggingface_hub import hf_hub_download

    for m in MODELS:
        filename = os.path.basename(m["file"])
        target = os.path.join(m["dest"], filename)
        if os.path.exists(target):
            logger.info(f"  SKIP (exists): {target}")
            continue
        os.makedirs(m["dest"], exist_ok=True)
        logger.info(f"  DOWNLOAD: {m['repo']}/{m['file']} -> {target}")
        try:
            hf_hub_download(m["repo"], m["file"], local_dir=m["dest"])
            logger.info(f"  DONE: {target}")
        except Exception as e:
            logger.error(f"  FAILED: {e}")

if __name__ == "__main__":
    main()
