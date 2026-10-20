"""Kafu sprite built from the original character design (شخصية PopupPush — كفو)."""
import io, functools
import cairosvg
from PIL import Image

DEFS = '<defs><pattern id="sh" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#FFFFFF"/><path d="M7 1.5L12.5 7L7 12.5L1.5 7Z" fill="#E11D48"/><circle cx="7" cy="7" r="1.6" fill="#FFFFFF"/></pattern></defs>'
DRAPES = '<path d="M86 140 C62 190 52 250 58 318 L116 304 L118 150 Z" fill="url(#sh)" stroke="#E5E7EB" stroke-width="2"/><path d="M274 140 C298 190 308 250 302 318 L244 304 L242 150 Z" fill="url(#sh)" stroke="#E5E7EB" stroke-width="2"/>'
STAND = '<rect x="170" y="268" width="20" height="38" rx="4" fill="#2E375C"/><rect x="116" y="302" width="128" height="14" rx="7" fill="#2E375C"/>'
BODY = '<rect x="82" y="118" width="196" height="152" rx="30" fill="#141A2E" stroke="#4F46E5" stroke-width="7"/>'
HOOD = '<path d="M72 156 C70 98 118 64 180 64 C242 64 290 98 288 156 C246 136 114 136 72 156 Z" fill="url(#sh)" stroke="#E5E7EB" stroke-width="2"/><path d="M86 116 Q180 146 274 116" fill="none" stroke="#0A0E1A" stroke-width="11" stroke-linecap="round"/><path d="M92 101 Q180 129 268 101" fill="none" stroke="#0A0E1A" stroke-width="10" stroke-linecap="round"/>'
EYES = '<circle cx="146" cy="190" r="17" fill="#22D3EE"/><circle cx="214" cy="190" r="17" fill="#818CF8"/><circle cx="140" cy="184" r="5.5" fill="#FFFFFF"/><circle cx="208" cy="184" r="5.5" fill="#FFFFFF"/><ellipse cx="122" cy="220" rx="11" ry="6" fill="#F472B6" opacity="0.45"/><ellipse cx="238" cy="220" rx="11" ry="6" fill="#F472B6" opacity="0.45"/>'
BROWS = '<path d="M128 166 L160 158" stroke="#E0E7FF" stroke-width="6" stroke-linecap="round"/><path d="M232 166 L200 158" stroke="#E0E7FF" stroke-width="6" stroke-linecap="round"/>'
MOUTH = {
    "smile": '<path d="M154 222 Q180 246 206 222" fill="none" stroke="#22D3EE" stroke-width="7" stroke-linecap="round"/>',
    "open": '<path d="M152 220 Q180 262 208 220 Z" fill="#22D3EE"/><path d="M164 238 Q180 250 196 238" fill="none" stroke="#0A0E1A" stroke-width="3" stroke-linecap="round" opacity="0.35"/>',
    "worried": '<path d="M158 236 Q180 220 202 236" fill="none" stroke="#22D3EE" stroke-width="7" stroke-linecap="round"/>',
    "worried_open": '<ellipse cx="180" cy="232" rx="14" ry="11" fill="#22D3EE"/>',
}
HAND = lambda x, y: f'<circle cx="{x}" cy="{y}" r="14" fill="#E0E7FF" stroke="#4F46E5" stroke-width="5"/>'
ARM = lambda d: f'<path d="{d}" fill="none" stroke="#4F46E5" stroke-width="11" stroke-linecap="round"/>'
LEFT_DOWN = ARM("M82 226 Q54 246 56 280") + HAND(56, 290)
RIGHT_DOWN = ARM("M278 226 Q306 246 304 280") + HAND(304, 290)
ARMS = {
    "idle": LEFT_DOWN + RIGHT_DOWN,
    "wave1": ARM("M278 214 Q318 196 326 154") + HAND(328, 146) + LEFT_DOWN,
    "wave2": ARM("M278 214 Q326 206 342 170") + HAND(344, 162) + LEFT_DOWN,
    # phone held in the screen-left hand (as in the original "بضغطة من جوالي" pose)
    "phone": ARM("M82 226 Q52 252 74 280") + '<rect x="54" y="258" width="38" height="62" rx="8" fill="#0A0E1A" stroke="#E0E7FF" stroke-width="4"/><rect x="61" y="267" width="24" height="38" rx="3" fill="#22D3EE"/>' + HAND(73, 324) + RIGHT_DOWN,
    "cheer": ARM("M82 214 Q42 192 36 150") + HAND(34, 142) + ARM("M278 214 Q318 192 324 150") + HAND(326, 142),
    "worried": ARM("M82 226 Q60 214 92 196") + HAND(98, 192) + ARM("M278 226 Q300 214 268 196") + HAND(262, 192),
}

def svg(mouth="smile", arms="idle", brows=False):
    inner = DRAPES + STAND + BODY + ARMS[arms] + HOOD + EYES + (BROWS if brows else "") + MOUTH[mouth]
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 400" width="360" height="400">{DEFS}{inner}</svg>'

@functools.lru_cache(maxsize=256)
def sprite(mouth="smile", arms="idle", brows=False, width=600):
    png = cairosvg.svg2png(bytestring=svg(mouth, arms, brows).encode(), output_width=width)
    return Image.open(io.BytesIO(png)).convert("RGBA")

def paste_kafu(img, cx, cy, width, mood="happy", talking=0, arms="idle"):
    """cx, cy = centre of the sprite. Returns the sprite box (x0, y0, scale)."""
    worried = mood == "worried"
    if worried:
        mouth = "worried_open" if talking else "worried"
    else:
        mouth = "open" if talking else "smile"
    sp = sprite(mouth, arms, worried, int(width))
    x0, y0 = int(cx - sp.width / 2), int(cy - sp.height / 2)
    img.paste(sp, (x0, y0), sp)
    return x0, y0, sp.width / 360.0
