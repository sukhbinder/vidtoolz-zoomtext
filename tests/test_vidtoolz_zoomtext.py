import pytest
import vidtoolz_zoomtext as w
import argparse
from types import SimpleNamespace
import os

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.fixture
def parser():
    subparsers = argparse.ArgumentParser().add_subparsers()
    return w.create_parser(subparsers)


def test_required_argument_main_video(parser):
    args = parser.parse_args(["some_video.mp4"])
    assert args.main_video == "some_video.mp4"
    assert args.text is None
    assert args.font == "Arial"
    assert args.output is None
    assert args.fontsize == 80
    assert args.padding == 80
    assert args.text_color == "white"


def test_all_arguments(parser):
    args = parser.parse_args(
        [
            "video.mp4",
            "-t",
            "Hello World",
            "-f",
            "Papyrus",
            "-o",
            "output.mp4",
            "-fs",
            "100",
            "-pad",
            "50",
            "-tc",
            "yellow",
        ]
    )
    assert args.main_video == "video.mp4"
    assert args.text == "Hello World"
    assert args.font == "Papyrus"
    assert args.output == "output.mp4"
    assert args.fontsize == 100
    assert args.padding == 50
    assert args.text_color == "yellow"


def test_missing_main_video_raises(parser):
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_plugin(capsys):
    w.zoomtext_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``vidtoolz`` plugin." in captured.out


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Test doesn't work in Github Actions.")
def test_run(tmpdir):
    outputfile = os.path.join(str(tmpdir), "temp.mp4")

    args = SimpleNamespace(
        main_video=os.path.join(os.path.dirname(__file__), "testvid.mp4"),
        text="Hello, world!",
        font="Arial",
        output=outputfile,
        fontsize=60,
        padding=80,
        text_color="white",
    )

    plugin = w.zoomtext_plugin
    plugin.run(args)
    assert os.path.exists(outputfile)
