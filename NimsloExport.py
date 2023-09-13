import sys

def ExportTimeline(timeline, project, path):
    project.SetCurrentTimeline(timeline)
    #project.LoadRenderPreset(RenderPresetName)
    exportItemList = timeline.GetItemListInTrack("video", ExportTrackNumber)
    timelineName = timeline.GetName()

    i = 1
    print("")
    print(f"Creating Renders for {timelineName}")
    print(f"{len(exportItemList)} exports in timeline")
    for item in exportItemList:
        exportTimings = {
            "MarkIn" : item.GetStart(),
            "MarkOut" : item.GetEnd() - 1,
            "CustomName" : f"{timelineName} {i}",
            "TargetDir" : path
        }
        i = i + 1
        print(f"Adding render for: {timelineName} {i}")
        project.SetRenderSettings(exportTimings)
        project.AddRenderJob()

def GetResolve():
    try:
    # The PYTHONPATH needs to be set correctly for this import statement to work.
    # An alternative is to import the DaVinciResolveScript by specifying absolute path (see ExceptionHandler logic)
        import DaVinciResolveScript as bmd
    except ImportError:
        if sys.platform.startswith("darwin"):
            expectedPath="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
        elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            import os
            expectedPath=os.getenv('PROGRAMDATA') + "\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\"
        elif sys.platform.startswith("linux"):
            expectedPath="/opt/resolve/libs/Fusion/Modules/"

        # check if the default path has it...
        try:
            import imp
            bmd = imp.load_source('DaVinciResolveScript', expectedPath+"DaVinciResolveScript.py")
        except ImportError:
            # No fallbacks ... report error:
            print("Unable to find module DaVinciResolveScript - please ensure that the module DaVinciResolveScript is discoverable by python")
            print("For a default DaVinci Resolve installation, the module is expected to be located in: "+expectedPath)
            sys.exit()

    return bmd.scriptapp("Resolve")

resolve = GetResolve()
path = resolve.Fusion().RequestDir()
project = resolve.GetProjectManager().GetCurrentProject()
TimelineCount = project.GetTimelineCount()
ExportTrackNumber = 2
RenderPresetName = "H.264 Master"
NameExcludes = ["Timeline 1"]


project.DeleteAllRenderJobs()
for i in range(1, TimelineCount + 1):
    timeline = project.GetTimelineByIndex(i)
    print(f"found timeline: {timeline.GetName()}")
    if(timeline.GetName() not in NameExcludes):
        ExportTimeline(timeline, project, path)



