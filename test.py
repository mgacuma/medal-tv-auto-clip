import unittest
from unittest.mock import patch
from datetime import datetime
from main import AutoClipper

class TestAutoClipper(unittest.TestCase):

    def setUp(self):
        self.valid_json_path = 'path/to/valid/clips.json'
        self.invalid_json_path = 'path/to/invalid/clips.json'
        self.nonexistent_video_path = 'path/to/nonexistent/video.mp4'
        self.buffered_clip_data = {
            'item1': {
                'FilePath': 'path/to/video1.mp4',
                'duration': 10,
                'bookmarks': [{'time': 2}, {'time': 7}]
            },
            'item2': {
                'FilePath': 'path/to/video2.mp4',
                'duration': 25,
                'bookmarks': [{'time': 3}, {'time': 4}]
            }
        }
    
    @patch('main.AutoClipper.loadJson', return_value = None)
    @patch('main.AutoClipper.processData', return_value = None)
    def test_run(self, loadJson, processData):
        app = AutoClipper(self.valid_json_path)
        app.run()

        loadJson.assert_called_once_with()
        processData.assert_called_once_with()

    @patch('builtins.open')
    @patch('json.load', return_value = None)
    def test_load_json(self, mock_load, mock_open):
        app = AutoClipper(self.valid_json_path)
        app.loadJson()

        mock_open.assert_called_once_with(self.valid_json_path)
        mock_load.assert_called_once_with(mock_open.return_value)

    @patch('main.AutoClipper.processClip')
    def test_process_data(self, mock_processClip):
        app = AutoClipper(self.valid_json_path)
        app.data = self.buffered_clip_data
        app.processData()

        mock_processClip.assert_called()
        mock_processClip.assert_called_with(self.buffered_clip_data['item2'])

    # @patch('moviepy.editor.VideoFileClip')
    @patch('main.os.path.exists', return_value = True)
    def test_process_clip(self, mock_exists, mock_video_file_clip):
        print('ASDASD')
        mock_clip_instance = mock_video_file_clip.return_value
        mock_clip_instance.subclip.return_value = mock_clip_instance

        app = AutoClipper(self.valid_json_path)
        app.processClip(self.buffered_clip_data.item1)

        mock_video_file_clip.assert_called_once(self.buffered_clip_data.item1.FilePath)
        mock_exists.assert_called_once_with(self.buffered_clip_data.item1.FilePath)
        mock_clip_instance.subclip.assert_called_once_with(0, 10)
        mock_clip_instance.write_videofile.assert_called_once_with('/output/directory/video_edit.mp4', codec='libx264', audio_codec='aac')

    
    # def test_run_with_valid_input(self, mock_makedirs, mock_exists, mock_clip):
    #     app = AutoClipper(self.valid_json_path)
    #     app.run()
    #     # Add assertions for the expected behavior

    # def test_run_with_empty_bookmarks(self):
    #     app = AutoClipper(self.valid_json_path)
    #     with self.assertRaises(Exception) as context:
    #         app.processClip({'bookmarks': []})
    #     self.assertEqual(str(context.exception), 'Empty Bookmarks')

    # @patch('os.path.exists', return_value=False)
    # def test_run_with_nonexistent_video_file(self, mock_exists):
    #     app = AutoClipper(self.invalid_json_path)
    #     app.processClip(self.buffered_clip_data)
    #     # Add assertions for the expected behavior

    # def test_process_clip_with_negative_buffer(self):
    #     app = AutoClipper(self.valid_json_path)
    #     app.processClip(self.buffered_clip_data)
    #     # Add assertions for the expected behavior

    # def test_process_clip_with_large_buffer(self):
    #     app = AutoClipper(self.valid_json_path)
    #     app.processClip(self.buffered_clip_data)
    #     # Add assertions for the expected behavior

    # @patch('os.makedirs')
    # def test_run_creates_clips_directory(self, mock_makedirs):
    #     app = AutoClipper(self.valid_json_path)
    #     app.run()
    #     # Add assertions for the expected behavior

if __name__ == '__main__':
    unittest.main()