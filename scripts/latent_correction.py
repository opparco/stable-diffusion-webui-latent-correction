import gradio as gr
from modules import scripts


class LatentCorrectionScript(scripts.Script):
    sorting_priority = 2

    def title(self):
        return "Latent Correction extension"

    def show(self, is_img2img):
        # make this extension visible in both txt2img and img2img tab.
        return scripts.AlwaysVisible

    def ui(self, *args, **kwargs):
        with gr.Accordion(open=False, label=self.title()):
            enabled = gr.Checkbox(label='Enabled', value=False)
            with gr.Row():
                ch1 = gr.Slider(label='ch1', minimum=-0.5, maximum=0.5, step=0.05, value=0)
                ch2 = gr.Slider(label='ch2', minimum=-0.5, maximum=0.5, step=0.05, value=0)
            with gr.Row():
                ch3 = gr.Slider(label='ch3', minimum=-0.5, maximum=0.5, step=0.05, value=0)
                ch4 = gr.Slider(label='ch4', minimum=-0.5, maximum=0.5, step=0.05, value=0)

        return enabled, ch1, ch2, ch3, ch4

    def post_sample(self, p, ps: scripts.PostSampleArgs, *script_args, **kwargs):
        enabled, *corrections = script_args

        if not enabled:
            return

        for i, correction in enumerate(corrections):
            if correction != 0:
                ps.samples[:, i, :, :] += correction
                p.extra_generation_params[f'Latent correction ch{i + 1}'] = correction
