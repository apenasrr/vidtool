from __future__ import annotations

import logging
import os
from pathlib import Path

from .. import tools, utils
from ..mediainfo import ffprobe


def get_video_codec(stream_video):

    video_codec = stream_video["codec_name"]
    return video_codec


def get_video_profile(stream_video):

    video_profile = stream_video["profile"]
    return video_profile


def get_video_resolution_height(stream_video):

    video_resolution_height = stream_video["height"]
    return video_resolution_height


def get_video_resolution_width(stream_video):

    video_resolution_width = stream_video["width"]
    return video_resolution_width


def get_video_bitrate(dict_inf, stream_video):
    """Bitrate search. It may be in one of the 2 possible places.

    Args:
        dict_inf (dict): video metadata
        stream_video (dict): video stream data

    Raises:
        NameError: If Bitrate is not found in any of the possible places

    Returns:
        int: video bitrate
    """

    try:
        video_bitrate = stream_video["bit_rate"]
    except Exception as e:
        try:
            video_bitrate = dict_inf["format"]["bit_rate"]
        except Exception as e:
            print(f"{e}\n{dict_inf}")
            file = dict_inf["format"]["filename"]
            msg_err = (
                "File bellow don't have 'bit_rate' in "
                + f"detail file:\n{file}"
            )
            logging.error(msg_err)
            raise NameError(msg_err)

    return int(video_bitrate)


def get_is_avc(stream_video):

    try:
        is_avc_str = stream_video["is_avc"]
        if is_avc_str == "true":
            is_avc = 1
        else:
            is_avc = 0
    except:
        is_avc = 0
    return is_avc


def get_audio_codec(stream_audio):

    audio_codec = stream_audio["codec_name"]
    return audio_codec


def get_list_path_video(
    folder_path: Path, video_extensions: list[str]
) -> list[str]:

    # To input more file video extension:
    #  https://dotwhat.net/type/video-movie-files

    tuple_video_extension_raw = tuple(video_extensions)
    tuple_video_extension = tuple(
        "." + ext for ext in tuple_video_extension_raw
    )
    str_tuple_video_extension = ", ".join(tuple_video_extension)
    logging.info(f"Find for video with extension: {str_tuple_video_extension}")

    # get_all_file_path
    dict_all_file_result = utils.get_all_file_path(folder_path)

    # In case of error by max_path, interrupts execution
    if len(dict_all_file_result["errors"]) != 0:
        list_file_path_too_long = [
            str(x) for x in dict_all_file_result["errors"]
        ]
        for file_path_too_long in list_file_path_too_long:
            logging.error(f"File path too long: %s", file_path_too_long)
        raise ValueError("file_path_too_long")

    # Select desired videos by extension
    list_file_selected = []
    list_file_path = dict_all_file_result["content"].copy()
    for file_path in list_file_path:
        if file_path.name.lower().endswith(tuple_video_extension):
            logging.info("Selected file: %s", file_path.name)
            list_file_selected.append(file_path)
        else:
            logging.info("___Unselected: %s", file_path.name)

    return list_file_selected


def get_list_dict_inf_ffprobe(list_path_file: list[str]):
    """Returns metadata from a video file lists

    Args:
        list_path_file (list): Video file lists

    Returns:
        list[dict]: Video Metadata
    """

    list_dict = []
    for file_selected in list_path_file:
        d = {}
        d["path_file"] = str(file_selected)
        # generate raw metadata
        logging.info("Catching video metadata: %s", file_selected)
        dict_inf_ffprobe = ffprobe(file_selected).get_output_as_dict()
        d["metadata"] = dict_inf_ffprobe
        list_dict.append(d)
    return list_dict


def generate(list_dict_inf_ffprobe):

    list_dict = []
    for dict_file in list_dict_inf_ffprobe:

        path_file = dict_file["path_file"]
        print(f"parsing: {path_file}")
        # path_file = dict_inf_ffprobe['format']['filename']
        dict_inf_ffprobe = dict_file["metadata"]
        # parse data
        duration_dict = tools.get_duration_ffprobe(dict_inf=dict_inf_ffprobe)
        if duration_dict is False:
            print("!File seems corrupt.\n")
            continue
        duration = duration_dict["duration_str"]
        duration_seconds = duration_dict["duration_seconds"]
        total_bitrate = int(dict_inf_ffprobe["format"]["bit_rate"])
        format_name = dict_inf_ffprobe["format"]["format_name"]

        is_video = False
        for stream in dict_inf_ffprobe["streams"]:
            if stream["codec_type"] == "video":
                stream_video = stream
                is_video = True
                break

        if is_video:

            video_codec = get_video_codec(stream_video)
            video_profile = get_video_profile(stream_video)
            video_resolution_height = get_video_resolution_height(stream_video)
            video_resolution_width = get_video_resolution_width(stream_video)
            video_bitrate = get_video_bitrate(dict_inf_ffprobe, stream_video)
            is_avc = get_is_avc(stream_video)
        else:
            logging.error(
                "File above don't have tag 'video' in "
                + f"detail file:\n{path_file}"
            )
            continue

        has_audio = False
        for stream in dict_inf_ffprobe["streams"]:
            if stream["codec_type"] == "audio":
                stream_audio = stream
                has_audio = True
                break

        if has_audio is False:
            logging.info(
                "File above don't have tag 'audio' in "
                + f"detail file:\n{path_file}"
            )
            has_audio = False

        if has_audio:
            audio_codec = get_audio_codec(stream_audio)
        else:
            audio_codec = ""

        # generate dict
        d = {}
        d["duration"] = duration
        d["duration_seconds"] = duration_seconds
        d["file_size"] = os.path.getsize(path_file)
        d["format_name"] = format_name
        d["total_bitrate"] = total_bitrate
        d["video_bitrate"] = video_bitrate
        d["video_codec"] = video_codec
        d["audio_codec"] = audio_codec
        d["is_avc"] = is_avc
        d["video_profile"] = video_profile
        d["video_resolution_height"] = video_resolution_height
        d["video_resolution_width"] = video_resolution_width
        d["path_file"] = path_file
        d["file_path_folder"] = os.path.dirname(path_file)
        d["file_name"] = os.path.split(path_file)[1]
        list_dict.append(d)

    return list_dict
