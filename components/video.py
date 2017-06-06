from PIL import Image, ImageDraw
from PyQt4 import uic, QtGui, QtCore
import os, subprocess, threading
from queue import PriorityQueue
from . import __base__

class Video:
    '''Video Component Frame-Fetcher'''
    def __init__(self, ffmpeg, videoPath, width, height, frameRate, chunkSize, parent, loopVideo):
        self.parent = parent
        self.chunkSize = chunkSize
        self.size = (width, height)
        self.frameNo = -1
        self.currentFrame = 'None'
        if loopVideo:
            self.loopValue = '-1'
        else:
            self.loopValue = '0'
        self.command = [
            ffmpeg,
            '-thread_queue_size', '512',
            '-r', frameRate,
            '-stream_loop', self.loopValue,
            '-i', videoPath,
            '-f', 'image2pipe',
            '-pix_fmt', 'rgba',
            '-filter:v', 'scale='+str(width)+':'+str(height),
            '-vcodec', 'rawvideo', '-',
        ]
        
        self.frameBuffer = PriorityQueue()
        self.frameBuffer.maxsize = int(frameRate)
        self.finishedFrames = {}
        
        self.thread = threading.Thread(target=self.fillBuffer, name=self.__doc__)
        self.thread.daemon = True
        self.thread.start()
        
    def frame(self, num):
        while True:
            if num in self.finishedFrames:
                image = self.finishedFrames.pop(num)
                return Image.frombytes('RGBA', self.size, image)
            i, image = self.frameBuffer.get()
            self.finishedFrames[i] = image
            self.frameBuffer.task_done()
    
    def fillBuffer(self):        
        self.pipe = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)
        while True:
            if self.parent.canceled:
                break
            self.frameNo += 1

            # If we run out of frames, use the last good frame and loop.
            if len(self.currentFrame) == 0:
                self.frameBuffer.put((self.frameNo-1, self.lastFrame))
                continue

            self.currentFrame = self.pipe.stdout.read(self.chunkSize)
            #print('creating frame #%s' % str(self.frameNo))
            if len(self.currentFrame) != 0:
                self.frameBuffer.put((self.frameNo, self.currentFrame))
                self.lastFrame = self.currentFrame

class Component(__base__.Component):
    '''Video'''
    def widget(self, parent):
        self.parent = parent
        self.settings = parent.settings
        page = uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'video.ui'))
        self.videoPath = ''
        self.x = 0
        self.y = 0
        self.loopVideo = False
        
        page.lineEdit_video.textChanged.connect(self.update)
        page.pushButton_video.clicked.connect(self.pickVideo)
        page.checkBox_loop.stateChanged.connect(self.update)
        
        self.page = page
        return page

    def update(self):
        self.videoPath = self.page.lineEdit_video.text()
        self.loopVideo = self.page.checkBox_loop.isChecked()
        self.parent.drawPreview()
        
    def previewRender(self, previewWorker):
        width = int(previewWorker.core.settings.value('outputWidth'))
        height = int(previewWorker.core.settings.value('outputHeight'))
        self.chunkSize = 4*width*height
        frame = self.getPreviewFrame(width, height)
        if not frame:
            return Image.new("RGBA", (width, height),(0,0,0,0))
        else:
            return frame
    
    def preFrameRender(self, **kwargs):
        super().preFrameRender(**kwargs)
        width = int(self.worker.core.settings.value('outputWidth'))
        height = int(self.worker.core.settings.value('outputHeight'))
        self.chunkSize = 4*width*height
        self.video = Video(self.parent.core.FFMPEG_BIN, self.videoPath,
            width, height, self.settings.value("outputFrameRate"),
            self.chunkSize, self.parent, self.loopVideo)
        
    def frameRender(self, moduleNo, arrayNo, frameNo):
        return self.video.frame(frameNo)

    def loadPreset(self, pr):
        self.page.lineEdit_video.setText(pr['video'])
        
    def savePreset(self):
        return {
            'video' : self.videoPath,
        }
        
    def pickVideo(self):
        imgDir = self.settings.value("backgroundDir", os.path.expanduser("~"))
        filename = QtGui.QFileDialog.getOpenFileName(self.page,
            "Choose Video", imgDir, "Video Files (*.mp4 *.mov)")
        if filename: 
            self.settings.setValue("backgroundDir", os.path.dirname(filename))
            self.page.lineEdit_video.setText(filename)
            self.update()
    
    def getPreviewFrame(self, width, height):
        if not self.videoPath or not os.path.exists(self.videoPath):
            return
        command = [
            self.parent.core.FFMPEG_BIN,
            '-thread_queue_size', '512',
            '-i', self.videoPath,
            '-f', 'image2pipe',
            '-pix_fmt', 'rgba',
            '-filter:v', 'scale='+str(width)+':'+str(height),
            '-vcodec', 'rawvideo', '-',
            '-ss', '90',
            '-vframes', '1',
        ]
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)
        byteFrame = pipe.stdout.read(self.chunkSize)
        image = Image.frombytes('RGBA', (width, height), byteFrame)
        pipe.stdout.close()
        pipe.kill()
        return image