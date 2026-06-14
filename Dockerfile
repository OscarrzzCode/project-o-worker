FROM runpod/worker-comfyui:5.8.5-base

RUN pip install -q huggingface_hub gguf

RUN cd /comfyui/custom_nodes && \
    git clone https://github.com/city96/ComfyUI-GGUF && \
    cd ComfyUI-GGUF && pip install -q -r requirements.txt 2>/dev/null || true

COPY bootstrap_models.py /bootstrap_models.py
RUN chmod +x /bootstrap_models.py

RUN mv /start.sh /start_original.sh
RUN printf '#!/bin/bash\nset -e\necho "=== Bootstrap: downloading models ==="\npython3 /bootstrap_models.py\necho "=== Bootstrap complete, starting worker ==="\nexec /start_original.sh\n' > /start.sh && chmod +x /start.sh
