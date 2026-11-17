# Production tools research, 17 Nov 2026

The owner called the Pompeii episode "really bad": not enough character, lighting, movement, voice. He asked for free or low-cost ways to reach the quality of his second reference video (a 14:30 flat-cartoon business story), because Higgsfield is too expensive. This is what was found. Nothing in the pipeline or in `CLAUDE.md` was changed: rule 1 (no image generators) and rule 6 (Sid's design) are his to change.

## What the reference is
- Flat 2D vector cartoon: bold outlines, flat colour with one layer of shading, detailed rooms with depth and light, round-headed characters with hair, glasses and clothes, handwritten captions, black title cards.
- Earlier measurement: 328 shots, median 2.5 s; 255 of 294 testable shots are a still drawing with a slow push-in of about 6%; narration about 152 words a minute with long pauses; music about 7 dB under the voice.
- So it is mostly illustrated stills with camera moves and small animations (mouths, blinks, an object moving, text writing on). It does not need a video generator.

## Our Pompeii episode against it (measured)
- 182 stills in 413 s: the cut rate is about the same as the reference.
- Narration 197 words a minute (Kokoro `am_michael` at speed 1.22), short gaps. The reference is 152 with long pauses.
- Music is a synthesised pad mixed 25 dB under the voice. The reference is about 7 dB under.
- The gap is the artwork, the voice pacing and the sound, not the number of shots.

## Images (the artwork)
| Option | Cost | Checked how | Notes |
| --- | --- | --- | --- |
| Cloudflare Workers AI, FLUX.2 klein 4B / FLUX.1 schnell | 10,000 neurons a day free, then $0.011 per 1,000 | Official pricing page | About 110 klein or 180 schnell images a day at 1280x720 by my arithmetic. klein takes up to 4 reference images (character consistency). Needs a free account and an API token. Not tested here: no token. |
| Google Gemini image models (Nano Banana family) | No free API tier. $0.034 to $0.039 an image | Official pricing page | About $5 to $6 for 150 images. Generally the strongest at keeping a character the same from a reference sheet. Not tested here: no key. |
| Hugging Face Spaces (FLUX.2, Z-Image, Qwen-Image) | Free account 5 GPU-minutes a day; PRO $9 a month gives 40 | Official ZeroGPU docs | A Hugging Face connector exists in Claude's directory (not connected). Anonymous use from this workspace failed: quota exhausted on the shared address. |
| Canva image generator | Inside the owner's Canva AI allowance (size unknown to me) | One test image generated today | Already connected. Output 2720x1536. Only a thumbnail comes back through the connector; full-size retrieval at volume is unproven. |
| Pollinations, no sign-up | Free, 1 image per 45 s | Two test images generated today | Not good enough: weak model, 1024x576, watermark, ignored the style and drew a modern kitchen. |
| vidIQ image tool | 22 credits an image | Tool description | 120 credits left this month; not viable for artwork. |

## Voice
- Free today: slow Kokoro down and use a deeper voice. Samples made: `am_onyx` and `am_fenrir` at 0.95 with pauses (about 175 words a minute), `bm_george` at 0.98 (152).
- Gemini 3.1 Flash TTS: the official pricing page lists a free tier (limits not published) and paid output at $20 per million audio tokens; a third-party calculation puts that near $0.03 a minute. Style can be directed in words. Output carries a SynthID watermark. Free-tier content may be used by Google to improve products.
- Open source: Chatterbox (MIT, voice cloning, built-in audio watermark), Qwen3-TTS (Apache-2.0, voice design from a description). One July 2026 test ran Qwen3-TTS 0.6B on 4 CPU cores at about a third of real time, so an episode would take roughly 40 minutes or more on our 2 cores. Not tested here. Both have public Hugging Face Spaces.
- ElevenLabs: free plan has no commercial licence and needs attribution, so not for a monetised channel. Starter is $6 a month for about 30 minutes.
- I cannot hear audio. Pace, pauses, loudness and transcripts can be measured; the owner has to pick the voice by ear.

## Video generators
- Official per-second API prices collected in Aug 2026: about $0.02 (Pruna) to $0.40 (Veo 3.1). Veo 3.1 Lite $0.05, Kling 3.0 Turbo about $0.11, MiniMax H3 $0.13.
- A 7-minute episode is 420 s: $8 to $55 for one pass at the cheap end, before retries. No free tier covers that; Gemini's API has no free Veo tier.
- Higgsfield: the owner is on the Ultra plan with 0.09 credits left. A Krea blog post (a competitor) says "unlimited" models cost nothing only on the Higgsfield website; through the connector every generation uses credits.
- Sensible use later: 4 or 5 hero shots an episode from a start frame, about 25 s in total.

## Motion from code (free)
- Push-in on every shot, parallax between background and character layers, blinks, mouth shapes from the narration (Rhubarb Lip Sync is a free command-line tool with Linux builds, JSON output, 6 to 9 mouth shapes; licence file not read), captions that write on, map routes that draw, split screens, black cards, light effects (vignette, glow, light shafts, colour grade per scene).
- Remotion is free for individuals and teams of up to three; not required, the Python engine can composite layers.

## Music
- YouTube Audio Library: free in monetised YouTube videos; some tracks need credit. No API: the owner would download a small set once from YouTube Studio. (Checked through a music seller's guide, not YouTube's own page.)
- vidIQ music: 25 credits a track.

## Keys
- Cloud environments have "network secrets": a key stored on the environment that sessions use without seeing it, applied by host. Scheduled runs use the same environment. Keys never go in this repository (it is public) or in chat.

## Recommendation given to the owner
1. Stop drawing scenes with code. Generate each scene as a flat-cartoon illustration from a fixed style and a character sheet, and keep code for assembly and motion.
2. Start on the free Cloudflare tier; pay Gemini a few dollars an episode only if the free model cannot keep characters consistent. Decide with a six-shot side-by-side.
3. Voice: pick by ear from samples; slow to about 150 to 160 words a minute with real pauses.
4. Real music mixed about 12 dB under the voice.
5. No video generator for now.
6. First step: a 30 to 45 second pilot of the Pompeii opening for his approval before the pipeline changes.

## Sources
- https://developers.cloudflare.com/workers-ai/platform/pricing/
- https://developers.cloudflare.com/changelog/post/2026-01-15-flux-2-klein-4b-workers-ai/
- https://blog.cloudflare.com/flux-2-workers-ai
- https://learnwithhasan.com/guide/free-ai-images-claude-code-cloudflare/
- https://ai.google.dev/gemini-api/docs/pricing
- https://blog.laozhang.ai/en/posts/gemini-image-generation-free-limit-2026
- https://huggingface.co/docs/hub/spaces-zerogpu.md
- https://huggingface.co/docs/hub/en/spaces-mcp-servers
- https://invideo.io/blog/ai-video-model-pricing
- https://magichour.ai/blog/kling-ai-pricing
- https://www.krea.ai/blog/higgsfield-pricing-explained-2026-unlimited-credits-and-real-monthly-costs
- https://dupple.com/learn/is-elevenlabs-free
- https://www.nemovideo.com/blog/gemini-3-1-flash-tts-pricing
- https://tts.ai/blog/open-source-text-to-speech-guide-2026/?lang=th
- https://ocdevel.com/blog/20260711-quantized-cpu-tts
- https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice/blob/main/README.md
- https://github.com/DanielSWolf/rhubarb-lip-sync
- https://www.remotion.dev/docs/license/faq
- https://oakgen.ai/youtube-summaries/how-to-create-stylized-stickman-animations-with-free-ai-tools-nv8Hv6BFAWM
- https://www.foximusic.com/blog/copyright-free-music-youtube-audio-library-guide/
- https://code.claude.com/docs/en/cloud-environments

## Addendum, same day: Hugging Face connector connected
- Account: free plan (not PRO), so 5 GPU-minutes a day.
- The connector lists the Spaces it can use: image generation (Qwen-Image, Qwen-Image-Fast, FLUX.1 schnell, FLUX.1 Krea), image editing from a reference picture (FLUX.1 Kontext, FLUX.2 klein edit, Qwen-Image-Edit), background removal, Chatterbox speech (300 characters a call, optional reference voice), Wan 2.2 image-to-video and first/last-frame video.
- Running a Space failed twice with: "The invoke operation is disabled because gradio=none is set." So through this connection I can browse and read parameters but not generate. No image, voice or clip was produced through it.
- Ways forward: the owner turns on "Dynamic Spaces" (and adds the Spaces) at huggingface.co/settings/mcp and reconnects, which may or may not lift the block; or a Hugging Face read token is stored on the cloud environment so the workspace calls the Spaces directly (the Spaces answered from this workspace earlier; only anonymous quota stopped them).
- Capacity: Hugging Face's docs say PRO's 40 minutes allow up to 600 FLUX.1 schnell images a day, which implies about 75 on the free 5 minutes. Slower, better models, speech and video all draw on the same minutes; their real cost per call is not measured yet.

## Addendum: what Hugging Face would cost for one episode a day
Nothing has been generated on Hugging Face yet, so these are estimates from published numbers, not measurements.
- Plans: free = 5 GPU-minutes a day; PRO = $9 a month, 40 minutes a day, then $1 per 10 minutes (official docs). PRO also includes $2 a month of Inference Providers credit.
- GPU time each Space reserves per call (read from each Space's `app.py`): FLUX.1 schnell 10 s; FLUX.1 Krea 25 s; FLUX.1 Kontext edit 25 s; Qwen-Image and Qwen-Image-Fast 40 s on the double-rate GPU (counts as 80 s); FLUX.2 klein (official Space) 85 s; Z-Image-Turbo and Chatterbox the 60 s default; Wan 2.2 image-to-video about 33 to 48 s for a 3.5 to 5 s clip.
- Whether quota is charged on the reserved time or the time actually used is not settled: a community answer (Apr 2026) says reserved; there is no staff statement.
- Assumed episode: 200 image generations including retries (140 scenes on Krea, 60 character-consistent edits on Kontext), 30 Chatterbox calls, 10 clip attempts.
  - Charged on reserved time: about 120 minutes a day. 80 over the allowance = $8 a day, about $250 a month with the subscription. With the voice made elsewhere: about 90 minutes, about $160 a month.
  - If only time actually used is charged the bill could be far lower; unknown until measured.
- Cheaper split for a daily episode: scene images on Cloudflare (200 a day at 1280x720 is about 18,200 neurons; 8,200 over the free 10,000 costs about $0.09 a day, roughly $3 a month), voice on the local model (free) or Gemini TTS (about $0.21 an episode), and Hugging Face PRO only for character edits and a few moving shots (about 32 reserved minutes a day, inside the 40). Roughly $12 to $20 a month.
- The free plan cannot make a daily episode: 5 minutes is about 12 Krea images.
