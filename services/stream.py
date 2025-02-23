from services.camera import Camera
from services.encoder import HLSEncoder, HLSPresets

def produce_stream():
    camera = Camera()
    enc = HLSEncoder(
        "video/out.m3u8",
        shape=camera.get_resolution(),
        input_fps=30,
        use_wallclock_pts=True,
        preset=HLSPresets.DEFAULT_CPU,
    )
    
    with enc:
        while True:
            frame = camera.get_frame()
            enc(frame)

if __name__ == '__main__':
    produce_stream()