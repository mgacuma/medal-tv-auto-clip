import os
from datetime import datetime

CLIPS_PATH = os.getenv('APPDATA') if os.getenv('APPDATA') else '' + '\\Medal\\store\\clips.json'
OUT_DIR = os.path.curdir + '\\' + 'Clips'+ '\\'
BUFFER = 5

class AutoClipper:
    def __init__(self, CLIPS_PATH):
        self.CLIPS_PATH = CLIPS_PATH
        self.processed = 0
        self.startTime = datetime.now()

    def run(self):
        self.loadJson()
        self.processData()

        print('\nDone!\nProcessed Files: ' + str(self.processed))
        time_difference = datetime.now() - self.startTime
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_time_difference = "{}:{}:{}".format(hours, minutes, seconds)
        print(f"Duration: {formatted_time_difference}")
        
    def loadJson(self):
        import json
        f = open(self.CLIPS_PATH)
        self.data = json.load(f)
        f.close()

    def processData(self):
        for clipId, clipData in self.data.items():
            if(clipData.get('bookmarks')):
                self.processClip(clipData)
                self.processed += 1
    
    def processClip(self, clipData):
        videoPath = clipData['FilePath']
        paths = videoPath.split('\\')
        videoName = paths[len(paths) - 1]


        bookmarks = clipData['bookmarks']

        if len(bookmarks) < 1:
            raise Exception('Empty Bookmarks')
        
        start, end = float(bookmarks[0]['time']) - BUFFER, float(bookmarks[len(bookmarks) - 1]['time'] + BUFFER)
        if start < 0: start = 0
        if end > clipData['duration']: end = clipData['duration'] 
        
        if os.path.exists(videoPath):
            try:
                from moviepy.editor import VideoFileClip
                video_clip = VideoFileClip(videoPath)
                clipped_clip = video_clip.subclip(start, end)
                clipped_clip.write_videofile(OUT_DIR + videoName.replace('.mp4', '_edit.mp4'), codec='libx264', audio_codec='aac')
            
            except Exception as e:
                print('Error processing clip.', e)
            
            finally:
                video_clip.close()
        else: 
            print(videoPath, ' does not exist.')

if(__name__ == '__main__'):
    if not os.path.exists('Clips'):
        os.makedirs('Clips')
    app = AutoClipper(CLIPS_PATH)
    app.run()