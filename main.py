import os
from moviepy.editor import VideoFileClip
from datetime import datetime

CLIPS_PATH = os.getenv('APPDATA') + '\\Medal\\store\\clips.json'
OUT_DIR = os.path.curdir + '\\' + 'Clips'+ '\\'
BUFFER = 5

class AutoClipper:
    def __init__(self, CLIPS_PATH):
        self.CLIPS_PATH = CLIPS_PATH
        self.processed = 0
        self.startTime = datetime.now()

    def run(self):
        self.loadJson()
        #self.processData()
        print('\nDone!\nProcessed Files: ' + str(self.processed))
        time_difference = datetime.now() - self.startTime

        # Calculate hours, minutes, and seconds
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_time_difference = "{}:{}:{}".format(hours, minutes, seconds)
        print(f"Duration: {formatted_time_difference}")
        
    def loadJson(self):
        # Python program to read json file
        import json

        # Opening JSON file
        f = open(self.CLIPS_PATH)

        # returns JSON object as a dictionary
        self.data = json.load(f)

        # Closing file
        f.close()

    def processData(self):
        # Iterating through the json list
        for clipId, clipData in self.data.items():
            if(clipData.get('bookmarks')):
                self.processClip(clipData)
                self.processed += 1
    
    def processClip(self, clipData):
        # Load Video Clip from clipData.FilePath
        filepath = clipData['FilePath']
        paths = filepath.split('\\')
        videoName = paths[len(paths) - 1]

        # Find clip range using clipData.bookmarks array
        start, end = float(clipData.get('bookmarks')[0].get('time')) - BUFFER, float(clipData.get('bookmarks')[len(clipData.get('bookmarks')) - 1].get('time')) + BUFFER
        if start < 0: start = 0
        if end > clipData.get('duration'): end = clipData.get('duration') 
        
        if os.path.exists(filepath):
            # Open and clip video
            video_clip = VideoFileClip(filepath)
            clipped_clip = video_clip.subclip(start, end)
            
            # Save video to /out
            clipped_clip.write_videofile(OUT_DIR + videoName.replace('.mp4', '_edit.mp4'), codec='libx264', audio_codec='aac')

            # Close the video clip
            video_clip.close()

if(__name__ == '__main__'):
    if not os.path.exists('Clips'):
        # If it doesn't exist, create the directory
        os.makedirs('Clips')
    app = AutoClipper(CLIPS_PATH)
    app.run()