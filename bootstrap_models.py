#!/usr/bin/env python3
import sys, os, logging, shutil
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("bootstrap")

MODEL_DIR = os.environ.get("MODEL_DIR", "/comfyui/models")

MODELS = [
    {
        "repo": "unsloth/Z-Image-Turbo-GGUF",
        "file": "z-image-turbo-Q4_K_M.gguf",
        "dest_dir": os.path.join(MODEL_DIR, "unet"),
    },
    {
        "repo": "unsloth/Qwen3-4B-GGUF",
        "file": "Qwen3-4B-Q4_K_M.gguf",
        "dest_dir": os.path.join(MODEL_DIR, "text_encoders"),
    },
    {
        "repo": "thutes-gbr25/NSFW-MASTER-Z-IMAGE-TURBO",
        "file": "NSFW_master_ZIT_000008766.safetensors",
        "dest_dir": os.path.join(MODEL_DIR, "loras"),
    },
]

def download_flat(repo, file, dest_dir):
    from huggingface_hub import hf_hub_download
    os.makedirs(dest_dir, exist_ok=True)
    tmp = hf_hub_download(repo, file)
    target = os.path.join(dest_dir, os.path.basename(file))
    if not os.path.exists(target):
        shutil.copy2(tmp, target)
    return target

def download_vae():
    from huggingface_hub import hf_hub_download
    dest = os.path.join(MODEL_DIR, "vae")
    os.makedirs(dest, exist_ok=True)
    target = os.path.join(dest, "ae.safetensors")
    if os.path.exists(target):
        return target
    tmp = hf_hub_download("Comfy-Org/z_image_turbo", "split_files/vae/ae.safetensors")
    shutil.copy2(tmp, target)
    return target

def main():
    for m in MODELS:
        target = os.path.join(m["dest_dir"], os.path.basename(m["file"]))
        if os.path.exists(target):
            logger.info(f"  SKIP: {target}")
            continue
        logger.info(f"  DOWNLOAD: {m['repo']}/{m['file']} -> {target}")
        try:
            download_flat(m["repo"], m["file"], m["dest_dir"])
            logger.info(f"  DONE: {target}")
        except Exception as e:
            logger.error(f"  FAILED: {e}")

    vae_target = os.path.join(MODEL_DIR, "vae", "ae.safetensors")
    if not os.path.exists(vae_target):
        logger.info(f"  DOWNLOAD VAE: -> {vae_target}")
        try:
            download_vae()
            logger.info(f"  DONE: {vae_target}")
        except Exception as e:
            logger.error(f"  FAILED: {e}")

if __name__ == "__main__":
    main()
