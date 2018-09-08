from server import app
import unittest


class TestCase(unittest.TestCase):
  def setUp(self):
    app.config['TESTING'] = True
    self.app = app.test_client()
  
  def test_get_mimic(self):
    rv = self.app.get('/getmimic/1')
    self.assertEqual(rv.mimetype, 'image/jpg')

    rv = self.app.get('/getmimic/90000')
    self.assertEqual(rv.status_code, 404)

  def test_compare(self):
    rv = self.app.post('/compare', json={
      'id': 90000,
      'img': 'lolwhat'
    })
    
    self.assertEqual(rv.status_code, 404)

    rv = self.app.post('/compare', json={
      'id': 1
    })

    self.assertEqual(rv.status_code, 400)

    rv = self.app.post('/compare', json={
      'id': 1,
      'img': """data:image/jpeg;base64,-->/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nI
                CIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIy
                MjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF
                9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3
                R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHw
                EAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVY
                nLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqs
                rO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigD//2Q=="""
    })

    self.assertEqual(rv.status_code, 200)

if __name__ == '__main__':
  unittest.main()