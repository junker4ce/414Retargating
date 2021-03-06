from pyfbsdk import *

from pyfbsdk_additions import *
import os

def GetMotionBuilderInstallationDirectory() :
    applicationPath = FBSystem().ApplicationPath
    return applicationPath[0:applicationPath.index('bin')]

def previewSnake(control, event):
    # load fbx and bvh files
    loadSnakeFiles()
    #find right foot, left arm and right arm in bvh refernce
    rightUpLeg = FBFindModelByLabelName("BVH:RightUpLeg")
    leftArm = FBFindModelByLabelName("BVH:LeftArm")
    rightArm = FBFindModelByLabelName("BVH:RightArm")
    #unparent the above limbs, to remove their animation
    rightUpLeg.Parent = None
    rightArm.Parent = None
    leftArm.Parent = None

def addJointToCharacter (characterObject, slot, jointName):
    myJoint = FBFindModelByLabelName(jointName)
    if myJoint:
        proplist = characterObject.PropertyList.Find(slot + "Link")
        proplist.append(myJoint)

def removeJointFromCharacter(characterObject, slot, jointName):
    myJoint = FBFindModelByLabelName(jointName)
    if myJoint:
        proplist = characterObject.PropertyList.Find(slot + "Link")
        proplist.remove(myJoint)

def CleanModel(objects_to_clean, node):
    objects_to_clean.append(node)
    for child in node.Children:
        CleanModel(objects_to_clean, child)

def ValueChange(control,event):
    scenePlayer.Goto(FBTime(0, 0, 0, int(control.Value), 0))

def Transaction(control,event):
    if(event.IsBeginTransaction==False):
        scenePlayer.Goto(FBTime(0, 0, 0, int(control.Value), 0))

def playScene(control, event):
    scenePlayer.Play()

wagcnt = False
tailadded = False

def moveLeg(control, event):
   # leg= FBFindModelByLabelName("BVH:LeftLeg").LongName
   #print leg
    global bvhList
    global wagcnt
    for comp in FBSystem().Scene.Components:
        #print comp.LongName
        if (comp.LongName == "BVH:Tail"):
            comp.Selected = True
            comp.Rotation.SetAnimated(True)
            print wagcnt
            if ( wagcnt == False):
                comp.Rotation = FBVector3d(30, 0, 0)
                wagcnt = True
                
            elif( wagcnt==True):
                comp.Rotation = FBVector3d(-30,0,0)
                wagcnt = False
            
       
        else:
            comp.Selected = False

def restartResponse(control, event):
    scenePlayer.GotoStart()

def loadAllScene(control,event):
    global FBXFilenames
    FBXFilenames = []
    loadFiles()

def nextFrameRespone(control,event):
    scenePlayer.StepForward()

def prevFrameRespone(control,event):
    scenePlayer.StepBackward()

def createButton(text, color):
    newButton = FBButton()
    newButton.Caption = text
    newButton.Style = FBButtonStyle.kFBPushButton
    newButton.Justify = FBTextJustify.kFBTextJustifyCenter
    newButton.Look = FBButtonLook.kFBLookColorChange
    if color != None:
        newButton.SetStateColor(FBButtonState.kFBButtonState0, color)
    return newButton

def renameClick(control, event):
    global modelList
    modelList[0][boneIndex].Name = textEnter.Text
    populateList(modelList[0])

def stopScene(control, event):
    scenePlayer.Stop()

def addModel(control, event):
    global app, bvhCharacter, scenePlayer
    #prompt to choose new fbx file
    fbxName = fbxPopup()
    #load the character into the scene
    app.FileMerge(fbxName, False)
    # get the last loaded character
    fbxCharacter = FBSystem().Scene.Characters[len(FBSystem().Scene.Characters) - 1]

    print 'Number of characters in scene = ', (len(FBSystem().Scene.Characters))
    #retarget the actual motion to the new character
    fbxCharacter.InputCharacter = bvhCharacter
    fbxCharacter.InputType = FBCharacterInputType.kFBCharacterInputCharacter
    fbxCharacter.ActiveInput = True
    #scenePlayer.LoopStop = sceneLength
    scenePlayer.SetTransportFps(FPS)
    print "The scene length will be set to " + str(sceneLength)
    FBSystem().CurrentTake.LocalTimeSpan = FBTimeSpan(
    FBTime(0, 0, 0, 0, 0),
    FBTime(0, 0, 0, sceneLength, 0)
    )

def populateList(skeleton):
    global bvhList
    bvhList.Items.removeAll()
    for node in skeleton:
        bvhList.Items.append(node.Name)
    bvhList.Selected(boneIndex, True)
    
def addTailResponse(control, event):
    global tailadded
    if(tailadded==False):
        hipRef = FBFindModelByLabelName('BVH:Hips')
        tail = FBModelSkeleton('BVH:Tail')
        tail.Parent = hipRef
        tail.Show = True
        tail.Translation = FBVector3d(0, 0, -5)
        tail.Scaling = FBVector3d(0.5,0.5,0.5)
        hipRef2 = FBFindModelByLabelName('BVH:Tail')
        tail2 = FBModelSkeleton('BVH:Tail2')
        tail2.Parent = hipRef2
        tail2.Translation = FBVector3d(0, 1, -7)
        tailadded=True
    
def saveResponse(control, event):
    # Save the file using a dialog box.
    saveDialog = FBFilePopup()
    saveDialog.Style = FBFilePopupStyle.kFBFilePopupSave
    saveDialog.Filter = '*'

    saveDialog.Caption = 'Save the Current FBX'
    # Set the path to the current user's My Documents.
    saveDialog.Path = os.path.expanduser('~') + '\Documents'
    saveDialog.FileName = 'Retarget.fbx'

    if saveDialog.Execute():
        app.FileSave(saveDialog.FullFilename)

boneIndex = 0
scenePlayer = FBPlayerControl()
FBXFilenames = []
sceneLength = 0
bvhCharacter = None
app = None
FPS = FBTimeMode

lBipedMap = (('Reference', 'BVH:reference'),
        ('Hips','BVH:Hips'),
        ('Tail', 'BVH:Tail'),
        ( 'LeftUpLeg', 'BVH:LeftUpLeg' ),
        ( 'LeftLeg', 'BVH:LeftLeg' ),
        ( 'LeftFoot', 'BVH:LeftFoot'),
        ( 'RightUpLeg', 'BVH:RightUpLeg'),
        ( 'RightLeg', 'BVH:RightLeg'),
        ( 'RightFoot', 'BVH:RightFoot'),
        ( 'Spine', 'BVH:Spine'),
        ( 'LeftArm', 'BVH:LeftArm'),
        ( 'LeftForeArm', 'BVH:LeftForeArm'),
        ( 'LeftHand', 'BVH:LeftHand'),
        ( 'RightArm', 'BVH:RightArm'),
        ( 'RightForeArm', 'BVH:RightForeArm'),
        ( 'RightHand', 'BVH:RightHand'),
        ( 'Head', 'BVH:Head'),
        ( 'Neck', 'BVH:Neck'))

lSnakeRemover = ( ( 'RightUpLeg', 'BVH:RightUpLeg'),
        ( 'RightLeg', 'BVH:RightLeg'),
        ( 'RightFoot', 'BVH:RightFoot'),
        ( 'LeftArm', 'BVH:LeftArm'),
        ( 'LeftForeArm', 'BVH:LeftForeArm'),
        ( 'LeftHand', 'BVH:LeftHand'),
        ( 'RightArm', 'BVH:RightArm'),
        ( 'RightForeArm', 'BVH:RightForeArm'),
        ( 'RightHand', 'BVH:RightHand'))


def fbxPopup():
    from pyfbsdk import FBFilePopup, FBFilePopupStyle, FBMessageBox

    lFp2 = FBFilePopup()
    fbxName = None
    lFp2.Caption = "Select an FBX File for the Retargeting"
    lFp2.Style = FBFilePopupStyle.kFBFilePopupOpen

    lFp2.Filter = "*"

    # Set the default path.
    lFp2.Path = GetMotionBuilderInstallationDirectory()+"Tutorials"
    # Get the GUI to show.
    lRes = lFp2.Execute()
    # If we select files, show them, otherwise indicate that the selection was canceled
    if lRes:
        fbxName = lFp2.Path + "/" + lFp2.FileName
    else:
        FBMessageBox( "Invalid selection", "Selection canceled", "OK", None, None )
    # Cleanup.
    del( lFp2, lRes, FBFilePopup, FBFilePopupStyle, FBMessageBox )
    return fbxName

def loadBVH():
    lFp = FBFilePopup()
    lFp.Caption = "Select a BVH File to be Retargeted"
    lFp.Style = FBFilePopupStyle.kFBFilePopupOpen

    lFp.Filter = "*"

    # Set the default path.
    lFp.Path = r"C:\Users"
    # Get the GUI to show.
    lRes = lFp.Execute()
    # If we select files, show them, otherwise indicate that the selection was canceled
    if lRes:
        return lFp.Path + "/" + lFp.FileName
    else:
        FBMessageBox( "Invalid selection", "Selection canceled", "OK", None, None )


def loadFiles():
    from pyfbsdk import FBFilePopup, FBFilePopupStyle, FBMessageBox

    global FBXFilenames, bvhCharacter, app, BVHFilename

    app = FBApplication()
    app.FileNew()

    system = FBSystem()
    scene = system.Scene
    #POP UP FOR BVH FILE

    if (FBXFilenames == []):
        BVHFilename = loadBVH()
    #POP UP FOR FBX FILE(automatic redirect to tutorial folder)
    fbxName = fbxPopup()

    app.FileOpen(fbxName, False)

    fbxCharacter = app.CurrentCharacter
    print fbxCharacter
    print 'Number of characters in scene = ', (len(FBSystem().Scene.Characters))

    app.FileImport(BVHFilename, False)
    bvhCharacter = FBCharacter("MJ")

    for ( pslot, pjointname ) in lBipedMap:
        addJointToCharacter(bvhCharacter, pslot, pjointname)
    bvhCharacter.SetCharacterizeOn(True)
    bvhCharacter.CreateControlRig(True)
    
    controlRefName = FBFindModelByLabelName('BVH:reference')
    controlRefName.Translation = FBVector3d(0.0, 0.0, 0.0) 
    controlRefName.Scaling = FBVector3d(6.5, 6.5, 6.5) 
    
    fbxCharacter.InputCharacter = bvhCharacter
    fbxCharacter.InputType = FBCharacterInputType.kFBCharacterInputCharacter
    fbxCharacter.ActiveInput = True

def loadSnakeFiles(control, event):
    from pyfbsdk import FBFilePopup, FBFilePopupStyle, FBMessageBox

    global FBXFilenames, bvhCharacter, app, BVHFilename

    app = FBApplication()
    app.FileNew()

    system = FBSystem()
    scene = system.Scene
    #POP UP FOR BVH FILE

    if (FBXFilenames == []):
        BVHFilename = loadBVH()
    #POP UP FOR FBX FILE(automatic redirect to tutorial folder)
    fbxName = fbxPopup()

    app.FileOpen(fbxName, False)

    fbxCharacter = app.CurrentCharacter
    print fbxCharacter
    print 'Number of characters in scene = ', (len(FBSystem().Scene.Characters))

    app.FileImport(BVHFilename, False)
    bvhCharacter = FBCharacter("MJ")

    for ( pslot, pjointname ) in lBipedMap:
        addJointToCharacter(bvhCharacter, pslot, pjointname)
    bvhCharacter.SetCharacterizeOn(True)
    bvhCharacter.CreateControlRig(True)

    controlRefName = FBFindModelByLabelName('BVH:reference')
    controlRefName.Translation = FBVector3d(0.0, 0.0, 0.0) 
    controlRefName.Scaling = FBVector3d(6.5, 6.5, 6.5) 

    for ( pslot, pjointname ) in lSnakeRemover:
        removeJointFromCharacter(bvhCharacter, pslot, pjointname)

    fbxCharacter.InputCharacter = bvhCharacter
    fbxCharacter.InputType = FBCharacterInputType.kFBCharacterInputCharacter
    fbxCharacter.ActiveInput = True


loadFiles()
global sceneLength
FPS = FBPlayerControl().GetTransportFps()
#scenePlayer.SetTransportFps(FBTimeMode.kFBTimeMode60Frames)

#UI WINDOW CREATION
tool = FBCreateUniqueTool("Retargeter")
tool.StartSizeX = 600
tool.StartSizeY = 200

x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
h = FBAddRegionParam(0,FBAttachType.kFBAttachBottom,"")
tool.AddRegion("main","main", x, y, w, h)

red = FBColor(0.8, 0.0, 0.1)
green = FBColor(0.1, 0.8, 0.0)

PlayButton = createButton("Play Scene", green)
PlayButton.OnClick.Add(playScene)

StopButton = createButton("Stop Scene", red)
StopButton.OnClick.Add(stopScene)

loadAll = createButton("Choose New Files", None)
loadAll.OnClick.Add(loadAllScene)

snakeButton = createButton ("Snake", None)
snakeButton.OnClick.Add(loadSnakeFiles)

MoveLef = createButton("Wag Tail", None)
MoveLef.OnClick.Add(moveLeg)

nextFrame = createButton("Next Frame", None)
nextFrame.OnClick.Add(nextFrameRespone)

prevFrame = createButton("Prev Frame", None)
prevFrame.OnClick.Add(prevFrameRespone)

restartScene = createButton("Restart Scene", None)
restartScene.OnClick.Add(restartResponse)

addFBX = createButton("Add Model", None)
addFBX.OnClick.Add(addModel)

addTail = createButton("Add Tail", None)
addTail.OnClick.Add(addTailResponse)

saveScene = createButton("Save Scene", None)
saveScene.OnClick.Add(saveResponse)

hs = FBSlider()
hs.Orientation = FBOrientation.kFBHorizontal
hs.Caption ="frame slider"
hs.Min = scenePlayer.LoopStart.GetFrame()
hs.Max = scenePlayer.LoopStop.GetFrame()
sceneLength = scenePlayer.LoopStop.GetFrame()

hs.OnChange.Add(ValueChange)
hs.OnTransaction.Add(Transaction)
hs.Value = 0

#Assembling the UI
hbox1 = FBHBoxLayout( FBAttachType.kFBAttachLeft )
hbox1.AddRelative(prevFrame, 1.0)
hbox1.AddRelative(PlayButton, 1.0)
hbox1.AddRelative(StopButton, 1.0)
hbox1.AddRelative(nextFrame, 1.0)
hbox1.AddRelative(MoveLef,1.0)

hbox3 = FBHBoxLayout( FBAttachType.kFBAttachLeft )
hbox3.AddRelative(addFBX, 2.0)
hbox3.AddRelative(snakeButton, 1.0)
hbox3.AddRelative(addTail,1.0)

hbox4 = FBHBoxLayout( FBAttachType.kFBAttachLeft)
hbox4.AddRelative(loadAll, 1.0)
hbox4.AddRelative(saveScene, 1.0)

window = FBVBoxLayout(FBAttachType.kFBAttachTop)
tool.SetControl("main", window)

window.AddRelative(hs, 1.0)
window.AddRelative(hbox1, 1.0)
window.AddRelative(hbox3, 1.0)
window.AddRelative(hbox4, 1.0)

ShowTool(tool)