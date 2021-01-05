
""" compatibility OpenTimelineIO 0.12.0 and older
"""

import json
import DaVinciResolveScript
import opentimelineio as otio


class _Bmdr(object):
    pass


# build modul class
_bmdr = _Bmdr()

_bmdr.resolve = DaVinciResolveScript.scriptapp('Resolve')
_bmdr.fusion = DaVinciResolveScript.scriptapp('Fusion')
_bmdr.project_manager = _bmdr.resolve.GetProjectManager()
_bmdr.current_project = _bmdr.project_manager.GetCurrentProject()
_bmdr.media_pool = _bmdr.current_project.GetMediaPool()
_bmdr.track_types = {
    "video": otio.schema.TrackKind.Video,
    "audio": otio.schema.TrackKind.Audio
}
_bmdr.project_fps = None


def build_timeline(otio_timeline):
    # TODO: build timeline in mediapool `otioImport` folder
    # TODO: loop otio tracks and build them in the new timeline
    for clip in otio_timeline.each_clip():
        # TODO: create track item
        print(clip.name)
        print(clip.parent().name)
        print(clip.range_in_parent())


def _build_track(otio_track):
    # TODO: _build_track
    pass


def _build_media_pool_item(otio_media_reference):
    # TODO: _build_media_pool_item
    pass


def _build_track_item(otio_clip):
    # TODO: _build_track_item
    pass


def _build_gap(otio_clip):
    # TODO: _build_gap
    pass


def _build_marker(track_item, otio_marker):
    frame_start = otio_marker.marked_range.start_time.value
    frame_duration = otio_marker.marked_range.duration.value

    # marker attributes
    frameId = (frame_start / 10) * 10
    color = otio_marker.color
    name = otio_marker.name
    note = otio_marker.metadata.get("note") or json.dumps(otio_marker.metadata)
    duration = (frame_duration / 10) * 10

    track_item.AddMarker(
        frameId,
        color,
        name,
        note,
        duration
    )


def _build_media_pool_folder(name):
    """
    Returns folder with input name and sets it as current folder.

    It will create new media bin if none is found in root media bin

    Args:
        name (str): name of bin

    Returns:
        resolve.api.MediaPool.Folder: description

    """

    root_folder = _bmdr.media_pool.GetRootFolder()
    sub_folders = root_folder.GetSubFolderList()
    testing_names = list()

    for subfolder in sub_folders:
        subf_name = subfolder.GetName()
        if name in subf_name:
            testing_names.append(subfolder)
        else:
            testing_names.append(False)

    matching = next((f for f in testing_names if f is not False), None)

    if not matching:
        new_folder = _bmdr.media_pool.AddSubFolder(root_folder, name)
        _bmdr.media_pool.SetCurrentFolder(new_folder)
    else:
        _bmdr.media_pool.SetCurrentFolder(matching)

    return _bmdr.media_pool.GetCurrentFolder()


def read_from_file(otio_file):
    otio_timeline = otio.adapters.read_from_file(otio_file)
    build_timeline(otio_timeline)
