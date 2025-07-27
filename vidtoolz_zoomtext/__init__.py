import vidtoolz
import os
import sys
from moviepy import VideoFileClip, CompositeVideoClip, vfx
from vidtoolz_add_text.add_text import make_text_clip


def determine_output_path(input_file, output_file):
    input_dir, input_filename = os.path.split(input_file)
    name, _ = os.path.splitext(input_filename)

    if output_file:
        output_dir, output_filename = os.path.split(output_file)
        if not output_dir:  # If no directory is specified, use input file's directory
            return os.path.join(input_dir, output_filename)
        return output_file
    else:
        return os.path.join(input_dir, f"{name}_zoom.mp4")


def write_file(video_with_text, output_video_path, fps):
    try:
        # Write the result to a file
        video_with_text.write_videofile(
            output_video_path,
            codec="libx264",
            fps=fps,
            audio_codec="aac",
            temp_audiofile="temp_audio.m4a",
            remove_temp=True,
        )
    except Exception as e:
        sys.exit("Error writing video file: " + str(e))
    video_with_text.close()


def animate_video_with_text(
    input_path, bottom_text, font_size=50, font="Arial", text_color="white", padding=80
):
    # Load the original video
    clip = VideoFileClip(input_path)
    video_duration = clip.duration

    # Animate zoom from 100% to 80% over the first second
    def dynamic_resize(t):
        if t < 1:
            return 1 - 0.2 * (t / 1)  # Linear scale from 1.0 to 0.8 in 1 second
        elif t > video_duration - 1:
            return 0.8 + 0.2 * ((t - (video_duration - 1)) / 1)
        else:
            return 0.8

    # zoomed_clip = clip.fl_time(lambda t: t).resize(lambda t: dynamic_resize(t)).set_position("center")
    zoomed_clip = clip.with_effects(
        [vfx.Resize(lambda t: dynamic_resize(t))]
    ).with_position(("center", "top"))

    # Create a text clip that appears after 1 second and fades in
    start_time = 1
    duration = clip.duration - start_time
    txt_clip = make_text_clip(
        bottom_text,
        start_time,
        duration,
        fontsize=font_size,
        font=font,
        textcolor=text_color,
        pos_tuple=("center", "bottom"),
        padding=padding,
    )
    # Composite the zoomed video and text
    final_clip = CompositeVideoClip(
        [zoomed_clip, txt_clip], size=clip.size
    ).with_duration(clip.duration)

    # Write the result to a file
    return final_clip, clip.fps


def create_parser(subparser):
    parser = subparser.add_parser(
        "zoomtext", description="Zoom out the video and display text as caption."
    )
    parser.add_argument("main_video", help="Path to the main video file.")
    parser.add_argument("-t", "--text", help="Text to write")
    parser.add_argument(
        "-f",
        "--font",
        type=str,
        default="Arial",
        help="Font name to use. Ex Noteworthy, Melno, Papyrus, Zapfino (default: %(default)s)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output video file name (default: %(default)s)",
    )
    parser.add_argument(
        "-fs",
        "--fontsize",
        type=int,
        default=80,
        help="Fontsize (default: %(default)s)",
    )

    parser.add_argument(
        "-pad", "--padding", type=int, default=80, help="Padding (default: %(default)s)"
    )
    parser.add_argument(
        "-tc",
        "--text-color",
        type=str,
        default="white",
        help="Text color. (default: %(default)s)",
    )
    return parser


class ViztoolzPlugin:
    """Zoom out the video and display text as caption."""

    __name__ = "zoomtext"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        output = determine_output_path(args.main_video, args.output)
        clip, fps = animate_video_with_text(
            args.main_video,
            args.text,
            padding=args.padding,
            font=args.font,
            font_size=args.fontsize,
        )
        write_file(clip, output, fps)
        clip.close()

    def hello(self, args):
        # this routine will be called when "vidtoolz "zoomtext is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


zoomtext_plugin = ViztoolzPlugin()
