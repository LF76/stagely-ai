# Technical Architecture & Runware Integration Spec

## 1. System Overview

Stagely AI couples a lightweight client studio with an ultra-low-latency edge diffusion pipeline powered by Runware. The goal is to deliver photorealistic commercial lifestyle assets in under 2 seconds while preserving 100% of the original product's typography, branding, and color fidelity.

```
+-------------------------------------------------------------+
|                      Client Frontend                        |
|  - Next.js / Tailwind Studio Workspace                     |
|  - Live Before/After Interactive Comparison Canvas          |
|  - Preset Environment Manager & Custom Prompt Engine        |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                    Stagely Orchestration                     |
|  - Image Alpha Matting Validation                           |
|  - Depth Map & Contact Shadow Geometry Estimation           |
|  - Async Batch Queue Management                             |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                   Runware Edge Inference                    |
|  1. POST /imageBackgroundRemoval (Alpha isolation)          |
|  2. POST /imageInference (Flux Latent Inpainting + Depth)   |
|  3. POST /imageUpscale (RealESRGAN 4x print resolution)     |
+-------------------------------------------------------------+
```

---

## 2. Runware API Integration Code

### Python SDK Implementation Example

```python
import asyncio
from runware import Runware, IImageInference, IImageBackgroundRemoval, IImageUpscale

async def generate_product_staging(
    api_key: str,
    product_image_url: str,
    scene_prompt: str
):
    """
    Executes a 3-stage Runware pipeline:
    1. Cutout product
    2. Inpaint environmental context
    3. 4x Upscale
    """
    runware = Runware(api_key=api_key)
    await runware.connect()

    # Step 1: Remove background
    cutout_results = await runware.imageBackgroundRemoval(
        inputImage=product_image_url,
        outputFormat="PNG",
        rgba=[255, 255, 255, 0]
    )
    isolated_product_url = cutout_results[0].imageURL

    # Step 2: Depth-guided background synthesis
    inpaint_results = await runware.imageInference(
        positivePrompt=f"{scene_prompt}, commercial studio photography, dramatic lighting, sharp focus, 8k",
        negativePrompt="blurry, distorted product, low resolution, warped text, deformed geometry",
        model="runware:100@1",  # Flux Schnell / SDXL Inpainting checkpoint
        maskImage=isolated_product_url,
        numberResults=1,
        height=1024,
        width=1024,
        steps=4,
        CFGScale=2.5
    )
    staged_image_url = inpaint_results[0].imageURL

    # Step 3: 4x Super-resolution Upscaling
    upscaled_results = await runware.imageUpscale(
        inputImage=staged_image_url,
        upscaleFactor=4,
        outputFormat="JPG"
    )
    final_4k_url = upscaled_results[0].imageURL

    await runware.disconnect()
    return final_4k_url
```

---

## 3. Latency & Unit Economics

### Latency Budget (Target: < 2.0s)
* **Alpha Cutout**: ~0.25s
* **Flux Latent Inpaint**: ~0.85s
* **RealESRGAN 4x Upscale**: ~0.24s
* **Network & Overhead**: ~0.15s
* **Total Pipeline Latency**: **~1.49s**

### Cost per Generation vs. Traditional Photography
* **Runware Compute Cost**:
  * Background Removal: \$0.0008
  * Inpainting Inference: \$0.0012
  * 4x Upscale: \$0.0004
  * **Total Runware Cost**: **\$0.0024 per asset**
* **Traditional Studio Shot Cost**: **\$120.00 per asset**
* **Gross Margin**: **> 95%** at \$0.15/render retail pricing.
