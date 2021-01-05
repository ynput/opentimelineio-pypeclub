#
# Copyright Contributors to the OpenTimelineIO project
#
# Licensed under the Apache License, Version 2.0 (the "Apache License")
# with the following modification; you may not use this file except in
# compliance with the Apache License and the following modification to it:
# Section 6. Trademarks. is deleted and replaced with:
#
# 6. Trademarks. This License does not grant permission to use the trade
#    names, trademarks, service marks, or product names of the Licensor
#    and its affiliates, except as required to comply with Section 4(c) of
#    the License and to reproduce the content of the NOTICE file.
#
# You may obtain a copy of the Apache License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Apache License with the above modification is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the Apache License for the specific
# language governing permissions and limitations under the Apache License.
#
# TODO: move export function to adapter export.py
# TODO: pass property `includeTags` to export.py

import os
import hiero.core
from hiero.core import util

import opentimelineio as otio


class OTIOExportTask(hiero.core.TaskBase):

    def __init__(self, initDict):
        """Initialize"""
        hiero.core.TaskBase.__init__(self, initDict)
        self.otio_timeline = None

    def name(self):
        return str(type(self))

    def startTask(self):
        self.otio_timeline = otio.adapters.hiero.export.create_OTIO(
            self._sequence)

    def taskStep(self):
        return False

    def finishTask(self):
        try:
            exportPath = self.resolvedExportPath()

            # Check file extension
            if not exportPath.lower().endswith(".otio"):
                exportPath += ".otio"

            # check export root exists
            dirname = os.path.dirname(exportPath)
            util.filesystem.makeDirs(dirname)

            # write otio file
            otio.adapters.write_to_file(self.otio_timeline, exportPath)

        # Catch all exceptions and log error
        except Exception as e:
            self.setError("failed to write file {f}\n{e}".format(
                f=exportPath,
                e=e)
            )

        hiero.core.TaskBase.finishTask(self)

    def forcedAbort(self):
        pass


class OTIOExportPreset(hiero.core.TaskPresetBase):
    def __init__(self, name, properties):
        """Initialise presets to default values"""
        hiero.core.TaskPresetBase.__init__(self, OTIOExportTask, name)

        self.properties()["includeTags"] = True
        self.properties().update(properties)

    def supportedItems(self):
        return hiero.core.TaskPresetBase.kSequence

    def addCustomResolveEntries(self, resolver):
        resolver.addResolver(
            "{ext}",
            "Extension of the file to be output",
            lambda keyword, task: "otio"
        )

    def supportsAudio(self):
        return True


hiero.core.taskRegistry.registerTask(OTIOExportPreset, OTIOExportTask)
