print("starting")
import torch
import os
import shortuuid

from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import create_pan_cameras, decode_latent_images, gif_widget, decode_latent_mesh

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print("running on: ", device)
print("loading models...")

xm = load_model('transmitter', device=device)
model = load_model('text300M', device=device)
diffusion = diffusion_from_config(load_config('diffusion'))

print("models loaded")

render_mode = 'stf'

path = os.path.join(os.path.dirname(__file__), 'output')
print(path)
if not os.path.exists(path):
    os.makedirs(path)



def createModel():
    prompt = input("Enter a prompt: ")
    batch_size = int(input("Batch size (1): ") or 1)
    guidance_scale = float(input("Guidance scale (15.0): ") or 15.0)
    # guidance_scale = 30.0
    size = 64

    latents = sample_latents(
        batch_size=batch_size,
        model=model,
        diffusion=diffusion,
        guidance_scale=guidance_scale,
        model_kwargs=dict(texts=[prompt] * batch_size),
        progress=True,
        clip_denoised=True,
        use_fp16=True,
        use_karras=True,
        karras_steps=64,
        sigma_min=1e-3,
        sigma_max=160,
        s_churn=0,
    )

    # cameras = create_pan_cameras(size, device)
    # for i, latent in enumerate(latents):
    #     images = decode_latent_images(xm, latent, cameras, rendering_mode=render_mode)
    #     display(gif_widget(images))

    uuid = shortuuid.uuid()

    for i, latent in enumerate(latents):
        t = decode_latent_mesh(xm, latent).tri_mesh()
        filenamePLY = f'{path}/{prompt.replace(" ", "_")}_GS{guidance_scale}_{uuid}_{i}.ply'
        filenameOBJ = f'{path}/{prompt.replace(" ", "_")}_GS{guidance_scale}_{uuid}_{i}.obj'
        with open(filenamePLY, 'wb') as f:
            t.write_ply(f)
        with open(filenameOBJ, 'w') as f:
            t.write_obj(f)
        print(f'Saved {filenamePLY}')
    
    print("")
    print("====================================")
    print("")


while True:
    createModel()